import datetime
from ulid import ULID


def id_generator() -> ULID:
    """ULID ID generator."""
    return ULID()


def id_generator_with_timestamp(timestamp: int | float) -> ULID:
    return ULID.from_timestamp(timestamp)


def id_generator_with_datetime(dt: datetime.datetime) -> ULID:
    return ULID.from_datetime(dt)


def id_generator_string() -> str:
    return str(id_generator())


def id_generator_int() -> int:
    return int(id_generator())


def id_generator_hex() -> str:
    return id_generator().hex


def id_generator_timestamp() -> float:
    return id_generator().timestamp


def id_generator_datetime() -> datetime:
    return id_generator().datetime


def id_generator_uuid() -> str:
    return str(id_generator().to_uuid())
