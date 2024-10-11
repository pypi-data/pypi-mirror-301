import json
from datetime import datetime
from pathlib import Path
from typing import Any

import cattrs
from cattrs import Converter
from loguru import logger

from genpypress.app.app_logparser import model

converter = Converter()


# serialize and deserialize pendulum.DateTime
converter.register_unstructure_hook(datetime, lambda dt: dt.isoformat())
converter.register_structure_hook(datetime, lambda ts, _: datetime.fromisoformat(ts))


UTF8 = "utf-8"
ENCODINGS = [UTF8, "windows-1250"]
_START_PFX = "Log started: "
_FAIL_PFX = "FAIL: @ "
_END_PFX = "Log finished: "
_JOB_NAME_PFX = "Job name is"
_LOAD_DTTM_PFX = "Using load_dttm"


def parse_dir(path: Path, *, filter: str = "") -> model.LogDirectory:
    skip_parents = ["binlogs", "etllogs", "cmdlogs"]
    logs: list[model.LogFileEP] = []
    for f in path.rglob("*.log"):
        if filter not in f.name.upper():
            continue
        if f.parent.name.lower() in skip_parents:
            continue
        log = parse_ep_log(f)
        if log:
            logs.append(log)
    min_load_dttm = min([lg.load_dttm for lg in logs])
    return model.LogDirectory(
        path=path.as_posix(),
        logs=logs,
        min_load_dttm=min_load_dttm,
    )


def to_json(metadata: model.LogDirectory) -> str:
    data = converter.unstructure(metadata)
    return json.dumps(data, indent=4)


def from_json(data: str) -> model.LogDirectory:
    datadict = json.loads(data)
    return converter.structure(datadict, model.LogDirectory)


def parse_ep_log(file: Path) -> model.LogFileEP | None:
    """Pokusí se provést parsing log souboru.

    Args:
        file (Path): cesta k souboru

    Raises:
        ValueError: _description_

    Returns:
        model.LogFileEP: _description_
    """
    content = read_file(file)
    load_dttm, job_name, start_time, end_time = None, None, None, None
    runs = []
    for line in content.splitlines():
        line = line.strip()

        if line.startswith(_START_PFX):
            _dttm = line.removeprefix(_START_PFX).strip()
            start_time = datetime.strptime(_dttm, "%Y-%m-%d %H:%M:%S")
            start_time = start_time.replace(tzinfo=None)
        elif line.startswith(_FAIL_PFX):
            _dttm = line.removeprefix(_FAIL_PFX).strip()
            end_time = datetime.strptime(_dttm, "%Y-%m-%d %H:%M:%S")
            end_time = end_time.replace(tzinfo=None)
        elif line.startswith(_END_PFX):
            _dttm = line.removeprefix(_END_PFX).strip()
            end_time = datetime.strptime(_dttm, "%Y-%m-%d %H:%M:%S")
            end_time = end_time.replace(tzinfo=None)
        elif line.startswith(_JOB_NAME_PFX):
            job_name = line.removeprefix(_JOB_NAME_PFX).split(":")[1].strip()
        elif line.startswith(_LOAD_DTTM_PFX):
            _dttm = line.removeprefix(_LOAD_DTTM_PFX).partition(":")[2].strip()
            load_dttm = datetime.strptime(_dttm, "%Y-%m-%d %H:%M:%S")
            load_dttm = load_dttm.replace(tzinfo=None)

        if start_time and end_time and load_dttm:
            runs.append(model.JobRun(start_time, end_time))
            start_time, end_time = None, None

    if job_name and runs:
        return model.LogFileEP(
            job_name=job_name,
            runs=runs,
            file_name=file.as_posix(),
            load_dttm=load_dttm,
        )
    return None


def how_long(log: model.LogFileEP, *, which: str = "last") -> float:
    """Vrací celkovou dobu běhu daného jobu v sekundách.

    Args:
        log (model.LogFileEP): log soubor
        which (str, optional):
            last=doba běhu v poslední iteraci, pokud bylo běhů několik (restarty, apod)
            total=celková doba běhu

    Raises:
        ValueError: _description_

    Returns:
        float: _description_
    """
    _expected_which = ["total", "last"]
    if which not in _expected_which:
        raise ValueError(f"which: není jedna z hodnot {_expected_which}")

    last = log.runs[-1].end_time
    if which == "total":
        first = log.runs[0].start_time
    else:
        first = log.runs[-1].start_time

    duration = last - first
    return duration.total_seconds()


def read_file(f: Path) -> str:
    """Pokusí se načíst soubor s tím, že dopředu není známé jeho kódování.
    Postupně se vyzkouší utf-8 a windows-1250, a pokud oboje selže,
    předpokládá se UTF-8, ale s errors="replace".

    Args:
        f (Path): soubor

    Returns:
        str: _description_
    """
    logger.debug(f)
    for e in ENCODINGS:
        try:
            return f.read_text(encoding=e, errors="strict")
        except UnicodeError:
            pass
    return f.read_text(encoding=UTF8, error="replace")


d = model.LogDirectory
