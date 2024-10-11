import os
import pathlib
import re
import shutil
from textwrap import dedent

from attrs import define
from loguru import logger

DEPLOYDIR = "_deployment"
UTF8 = "utf-8"
HOME_DIR = pathlib.Path.home()
RUN = "run"
COMPILE = "compile"

BTEQ_HEADER = f"""
-----------------------------------------------------------
.SET SESSION CHARSET 'UTF8'
.SET WIDTH 65531
.SET ERRORLEVEL UNKNOWN SEVERITY 8;
.SET ERROROUT STDOUT;
.SET MAXERROR 1
-----------------------------------------------------------
.RUN FILE='{str(HOME_DIR)}/Vaults/o2/logon_prod.sql'
--.SET ERRORLEVEL 3803 SEVERITY 0;          -- create table
--.SET ERRORLEVEL 3807 SEVERITY 0;          -- drop table

"""


def _get_bash_cmd(p: pathlib.Path) -> str:
    rv = dedent(
        f"""
    echo "running {p.stem}"
    bteq < {p.name}.bteq &>>../../log/{p.stem}.log
    retval=$?
    if [ $retval -ne 0 ]; then
        echo "===============ERROR================="
        echo "====================================="
        exit $retval
    fi
    """
    )
    return rv


def _make_executable(path: pathlib.Path):
    mode = os.stat(path).st_mode
    mode |= (mode & 0o444) >> 2  # copy R bits to X
    os.chmod(path, mode)


def _attempts(name: str) -> list[str]:
    return [name.upper(), name.lower(), name.title()]


def _get_dir(path: pathlib.Path) -> pathlib.Path:
    parent = path.parent
    name = path.name
    for attempt in _attempts(name):
        d = parent / attempt
        if d.is_dir():
            return d
    raise ValueError(f"dir does not exist: {path}")


def compile_rewrites(rules: list[str] | None) -> dict[str, str]:
    replacements = {}
    if not rules:
        return replacements
    for rule in rules:
        logger.debug(f"{rule=}")
        rule_from, rule_to = rule.split("/")
        replacements[rule_from] = rule_to
    return replacements


def scandir(
    p: pathlib.Path,
    *,
    rewrites: list[str] | None,
):
    pack_dir = _get_dir(p / "db")
    tera_dir = _get_dir(pack_dir / "teradata")
    logger.info(f"{pack_dir=}")
    logger.info(f"{tera_dir=}")

    deploy_dir = pack_dir / DEPLOYDIR
    log_dir = p / "log"
    step_directories = [
        i for i in tera_dir.iterdir() if i.is_dir() and i.name != DEPLOYDIR
    ]
    step_directories = sorted(step_directories, key=lambda x: x.name)

    logger.info(f"mkdir: {deploy_dir}")
    deploy_dir.mkdir(parents=True, exist_ok=True)
    logger.info(f"shutil.rmtree: {log_dir}")
    shutil.rmtree(log_dir, ignore_errors=True)
    logger.info(f"mkdir: {log_dir}")
    log_dir.mkdir(parents=True, exist_ok=True)

    # produkce nebo dev?
    replacements = compile_rewrites(rewrites)
    logger.info(replacements)
    commands = []
    for step in step_directories:
        logger.info(f"step={step.name}")
        _make_step(pack_dir, step, tera_dir.name, replacements)
        commands.append(_get_bash_cmd(step))

    shc = "#!/bin/bash\n" + "\n\n".join(commands)
    sh = deploy_dir / "runme.sh"
    sh.write_text(shc, encoding="utf-8")
    _make_executable(sh)


@define
class _Content:
    encoding: str
    content: str


def _read_file(f: pathlib.Path) -> _Content:
    for enc in (UTF8, "windows-1250", "utf-16-le", "utf-16-be"):
        try:
            c = _Content(content=f.read_text(encoding=enc), encoding=enc)
            return c
        except UnicodeError:
            pass
    raise ValueError(f"can not read: {f}")


def _run_or_compile(script: str, f: pathlib.Path) -> str:
    if re.search(r"(REPLACE|CREATE)\s+PROCEDURE", script, re.I):
        logger.warning(f"compile: {f}")
        return COMPILE
    return RUN


def _make_step(
    pack_dir: pathlib.Path,
    step_dir: pathlib.Path,
    tera_dir_name: str,
    replacements: dict[str, str],
):
    """
    _make_step: vrací seznam BTEQ příkazů, které spustí nasazení.
    Mimo jiné řeší problematiku převodu prod databází na dev databáze,
    podle konfigurace.
    """
    logger.info(f"{step_dir=}")

    def replace_database(d: str) -> str:
        for k, v in replacements.items():
            d = re.sub(k, v, d, flags=re.IGNORECASE)
        return d

    databases = [d.name for d in step_dir.iterdir() if d.is_dir()]
    databases = sorted(databases)

    commands = []

    files = sorted(
        [
            f for f in step_dir.glob("*.*") if f.suffix.lower() in (".sql", ".bteq")
        ]  # noqa: E501
    )
    for f in files:
        rp = f.relative_to(step_dir)

        # normalizuj kódování
        content = _read_file(f)
        if content.encoding != UTF8:
            logger.warning(f"rewrite to {UTF8}: {f}")
            f.write_text(content.content, encoding=UTF8)

        # sestav bteq call
        run_cmd = _run_or_compile(content.content, f)
        commands.append(f".{run_cmd} file='../{step_dir.name}/{str(rp)}'")

    for db in databases:
        dbdir = step_dir / db
        commands.append("")

        commands.append(f"database {replace_database(db)};")
        files = [
            f for f in dbdir.rglob("*.*") if f.suffix.lower() in (".sql", ".bteq")
        ]  # noqa: E501
        for f in files:
            # normalizuj kódování
            content = _read_file(f)
            if content.encoding != UTF8:
                logger.warning(f"rewrite to {UTF8}: {f}")
                f.write_text(content.content, encoding=UTF8)

            # sestav bteq call
            rp = f.relative_to(step_dir)
            run_cmd = _run_or_compile(content.content, f)
            commands.append(f".{run_cmd} file='../{step_dir.name}/{str(rp)}'")

            rp = f.relative_to(step_dir)
            commands.append(
                f".{run_cmd} file='../{tera_dir_name}/{step_dir.name}/{str(rp)}'"
            )  # noqa: E501

    commands.insert(0, BTEQ_HEADER)
    bteq_content = "\n".join(commands)

    fbtq = pack_dir / DEPLOYDIR / f"{step_dir.name}.bteq"
    fbtq.write_text(bteq_content, encoding="utf-8")
