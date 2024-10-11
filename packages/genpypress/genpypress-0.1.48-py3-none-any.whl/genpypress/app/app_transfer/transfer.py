import json
import re
from pathlib import Path
from textwrap import dedent

import cattrs
import teradatasql as td
from attrs import define, field, frozen
from loguru import logger

from genpypress.tera import get_session, show_stats, show_table, show_view

UTF8 = "utf-8"
TABLES = ["T"]
VIEWS = ["V"]


@define
class TransferObject:
    source_db: str
    source_name: str
    table_kind: str
    source_ddl: str
    source_stats: str
    deployed: bool = field(default=False)


@define
class TransferDatabase:
    db_from: str
    db_to: str
    objects: list[TransferObject] = field(factory=list)


@frozen
class _Rule:
    find: re.Pattern
    replace: str


@frozen
class _Statement:
    sql: str
    errors_ok: list[int] = field(factory=list)


def _transfer_objects(
    sess: td.TeradataConnection,
    batch: TransferDatabase,
    *,
    store_to: str | Path | None = None,
    rules: list[_Rule],
    filter: list[re.Pattern],
):
    if store_to:
        _store_to = Path(store_to)

    # change default db
    with sess.cursor() as cur:
        sql = f"database {batch.db_to};"
        logger.info(sql)
        cur.execute(sql)

    for obj in batch.objects:
        skip = obj.deployed
        if filter and not skip:
            for f in filter:
                if not f.search(obj.source_name):
                    logger.debug(f"filter: {obj.source_name}")
                    skip = True
                    break

        if skip:
            logger.debug(f"skip: {obj.source_name}")
            continue

        # pokus se objekt založit, ale při první chybě to vzdej (nezkoušej další statements)
        for stmt in get_deploy_statements(obj, rules=rules):
            logger.info(stmt.sql)
            with sess.cursor() as cur:
                try:
                    cur.execute(stmt.sql, ignoreErrors=stmt.errors_ok)
                except td.Error as err:
                    msg = str(err).splitlines()[0]
                    logger.error(msg)
                    break
        if store_to:
            obj.deployed = True
            save_transfer_objects(_store_to, batch)


def transfer_objects(
    batch: TransferDatabase,
    *,
    rewrites: None | list[str],
    store_to: str | Path | None = None,
    filter: None | list[str],
    iterations: int = 3,
):
    _filter: list[re.Pattern] = []
    if filter:
        logger.debug("compiling filters")
        _filter = [re.compile(f, re.I) for f in filter]
        logger.debug(f"{_filter}")

    logger.debug("compiling rewrite rules")
    rules = _compile_rules(rewrites)
    logger.debug(f"{rules=}")

    # deployment zkusíme provést ve třech iteracích, protože nám nemusí v první iteraci projít nějaká views
    with get_session() as sess:
        for _ in range(iterations):
            _transfer_objects(
                sess,
                batch,
                rules=rules,
                filter=_filter,
                store_to=store_to,
            )

    # na závěr to chce nějaký report...


def _compile_rules(rewrites: None | list[str]) -> list[_Rule]:
    _rewrites = [] if not rewrites else rewrites
    rules: list[_Rule] = []
    for rew in _rewrites:
        try:
            r_from, r_to, *r_flags = rew.split("/")
            flags = 0

            if r_flags:
                if r_flags == ["i"]:
                    flags = re.I
                else:
                    raise ValueError(f"unsupported flags: {r_flags}")
            rule = _Rule(find=re.compile(r_from, flags=flags), replace=r_to)
            logger.debug(rule)
            rules.append(rule)
        except ValueError:
            logger.error(f"--rewrites={rew}: failed to split, include / in rule")
            raise
    return rules


def get_transfer_objects(
    db_from: str,
    db_to: str,
    *,
    store_to: str | Path | None = None,
    filter: str | None = None,
) -> TransferDatabase:
    """
    Funkce se připojí do Teradaty, a získá seznam objektů pro přenos do cílové databáze.

    Args:
        db_from (str): z jaké zdrojové databáze
        db_to (str): do jaké cílové databáze
        store_to (str | Path | None, optional): kam odkládat mezivýsledky

    Returns:
        TransferDatabase: definice přenosové dávky
    """
    with get_session() as sess:
        return _get_transfer_objects(
            sess,
            db_from=db_from,
            db_to=db_to,
            store_to=store_to,
            filter=filter,
        )


def load_transfer_objects(p: Path) -> TransferDatabase:
    raw_data = p.read_text(encoding=UTF8)
    data = json.loads(raw_data)
    return cattrs.structure(data, TransferDatabase)


def save_transfer_objects(p: Path, batch: TransferDatabase):
    data = cattrs.unstructure(batch)
    raw_data = json.dumps(data, indent=4)
    p.write_text(raw_data, encoding=UTF8)


def _get_transfer_objects(
    sess: td.TeradataConnection,
    db_from: str,
    db_to: str,
    *,
    store_to: str | Path | None = None,
    filter: str | None = None,
) -> TransferDatabase:
    if store_to and not isinstance(store_to, Path):
        store_to = Path(store_to)

    db_from, db_to = db_from.upper(), db_to.upper()
    _fltr = f" and {filter}" if filter else ""

    _result = None
    if store_to:
        try:
            _result = load_transfer_objects(store_to)
        except Exception as err:
            logger.warning(err)
    result = _result if _result else TransferDatabase(db_from=db_from, db_to=db_to)

    # pokud ještě nemáš seznam objektů, získej ho
    if not result.objects:
        sql = dedent(
            f"""
            select trim(tableName), trim(tableKind)
            from dbc.tablesV
            where databaseName = '{db_from}'
            and substring(tableName from 1 for 1) <> '_'
            and tableKind in ('V','T') {_fltr}
            order by tableKind, tableName
            """
        )
        # první průchod: získej seznam objektů pro přenos
        with sess.cursor() as cur:
            logger.debug(sql)
            try:
                result.objects = [
                    TransferObject(
                        source_db=db_from,
                        source_name=r[0].strip().upper(),
                        table_kind=r[1].strip().upper(),
                        source_ddl="",
                        source_stats="",
                    )
                    for r in cur.execute(sql)
                ]
            except Exception as err:
                logger.error(err)
                raise

        if store_to:
            save_transfer_objects(store_to, result)

    # druhý průchod: doplň ddl skripty
    for obj in result.objects:
        # pokud již máš DDL, například protože jsi ho předtím načetl ze souboru,
        # nepokoušej se ho získat z TD
        if obj.source_ddl:
            continue
        obj.source_ddl = _ddl(sess, obj)
        obj.source_stats = _stats(sess, obj)
        if store_to:
            save_transfer_objects(store_to, result)


def _ddl(sess: td.TeradataConnection, obj: TransferObject) -> str:
    if obj.table_kind in TABLES:
        return show_table(sess, db=obj.source_db, name=obj.source_name)
    if obj.table_kind in VIEWS:
        return show_view(sess, db=obj.source_db, name=obj.source_name)


def _stats(sess: td.TeradataConnection, obj: TransferObject) -> str:
    if obj.table_kind not in TABLES:
        return ""
    return show_stats(sess, db=obj.source_db, name=obj.source_name)


def get_deploy_statements(
    obj: TransferObject,
    *,
    strip_source_db: bool = True,
    rules: list[_Rule],
) -> list[_Statement]:
    """
    Funkce připraví DDL daného objektu pro nasazení v cílové databázi.

    Args:
        pbj (TransferObject): _description_
    """

    RE_STRIP = re.compile(f"{obj.source_db}[.]", re.I)

    # funkce která provádí strip databáze, do které objekt zakládáme
    def _strip(t: str) -> str:
        if not strip_source_db:
            return t
        return RE_STRIP.sub("", t)

    # připrav DDL skripty pro přenos objektu
    statements: list[_Statement] = []
    # tabulky nejdřív zkusíme dropnout
    if obj.table_kind in TABLES:
        statements.append(
            _Statement(
                sql=f"drop table {obj.source_name};",
                errors_ok=[3807],
            )
        )
    # pro DDL se pokusíme provést přepis podle pravidel,
    source_ddl = _strip(obj.source_ddl)  # zruš info o databázi
    for rule in rules:  # rewrite podle pravidel (views)
        source_ddl = rule.find.sub(rule.replace, source_ddl)
    statements.append(_Statement(sql=source_ddl))

    # statistiky
    for stats in obj.source_stats.split(";"):
        statements.append(_Statement(sql=(_strip(stats) + ";")))
    return statements
