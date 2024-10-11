import os
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import teradatasql as td
from attrs import asdict, field, frozen
from loguru import logger

UTF8 = "utf-8"


@frozen
class ConnParams:
    user: str
    password: str
    logmech: str = field(default="LDAP")
    tmode: str = field(default="TERA")
    host: str = field(default="edwprod.cz.o2")


@contextmanager
def get_session() -> Generator[td.TeradataConnection, None, None]:
    """
    Pokusí se provést logon do Teradaty, a vrátit session.
    Parametry se odvozují následujícím způsobem:
    - user:
        proměnná TO2_DOMAIN_USER,
        soubor ~/Vaults/o2/o2_username.txt
    - password:
        proměnná TO2_DOMAIN_PASSWORD,
        soubor ~/Vaults/o2/o2_password.txt
    - logmech:

    Yields:
        Generator[td.TeradataConnection, None, None]: _description_
    """
    cf = get_conn_params()
    try:
        logger.debug(f"connect {cf.host}/{cf.user}: {cf.logmech}, {cf.tmode}")
        sess = td.connect(**asdict(cf))
        yield sess
    finally:
        if sess:
            logger.debug(f"disconnect {cf.host}/{cf.user}: {cf.logmech}, {cf.tmode}")
            sess.close()


@contextmanager
def get_cursor(
    sess: td.TeradataConnection | None = None,
) -> Generator[td.TeradataCursor, None, None]:
    """
    Vrací kurzor. Pokud je k dispozici session, použije se,
    jinak se vytvoří nová session.

    Args:
        sess (td.TeradataConnection | None): session - nepovinný argument

    Yields:
        Generator[td.TeradataCursor, None, None]: kurzor
    """
    if isinstance(sess, td.TeradataConnection):
        with sess.cursor() as cur:
            yield cur
    else:
        with get_session() as sess:
            with sess.cursor() as cur:
                yield cur


def get_conn_params() -> ConnParams:
    if c := __params_environ():
        return c
    if c := __params_secrets():
        return c
    raise ValueError("failed to get connection parameters")


def __params_environ() -> ConnParams | None:
    """
    Pokusí se zjistit parametry pro connect string z proměnných prostředí.

    Returns:
        ConnParams | None: _description_
    """
    try:
        TD_USERNAME = os.environ["TO2_DOMAIN_USER"]
        TD_PASSWORD = os.environ["TO2_DOMAIN_PASSWORD"]
    except KeyError:
        return None
    return ConnParams(user=TD_USERNAME, password=TD_PASSWORD)


def __params_secrets(
    *,
    secrets_subdir: str = "Vaults/o2",
    username_file: str = "o2_username.txt",
    password_file: str = "o2_password.txt",
) -> ConnParams | None:
    try:
        dr = Path().home() / secrets_subdir
        uname = (dr / username_file).read_text(encoding=UTF8).strip()
        upass = (dr / password_file).read_text(encoding=UTF8).strip()
        return ConnParams(user=uname, password=upass)
    except Exception:
        return None


def show_stats(sess: td.TeradataConnection, db: str, name: str) -> str:
    return _show(sess, f"""show stats on "{db}"."{name}";""", ignoreErrors=[3624])


def show_table(sess: td.TeradataConnection, db: str, name: str) -> str:
    return _show(sess, f"""show table "{db}"."{name}";""")


def show_view(sess: td.TeradataConnection, db: str, name: str) -> str:
    return _show(sess, f"""show view "{db}"."{name}";""")


def _show(
    sess: td.TeradataConnection,
    sql: str,
    *,
    ignoreErrors: list[int] | int | None = None,
):
    with get_cursor(sess) as cur:
        logger.debug(sql)
        rows = [
            r[0].replace("\r", "\n")
            for r in cur.execute(sql, ignoreErrors=ignoreErrors)
        ]
        return "\n".join(rows)
