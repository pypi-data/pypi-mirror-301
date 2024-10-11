from datetime import datetime

from attrs import frozen


@frozen
class JobRun:
    start_time: datetime
    end_time: datetime


@frozen
class LogFileEP:
    job_name: str
    file_name: str
    load_dttm: datetime
    runs: list[JobRun]


@frozen
class LogDirectory:
    path: str
    logs: list[LogFileEP]
    min_load_dttm: datetime
