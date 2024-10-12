from datetime import datetime, timezone
from typing import TypeVar

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def set_timestamps(record: T, is_new: bool = False):
    """Sets the created_at, updated_at fields for a record.

    Args:
        record (T): The record to update timestamps for.
        is_new (bool, optional): Whether the record is new. Defaults to False.
    """

    # Check if the record has a created_at attribute and set it if needed
    current_time = datetime.now(timezone.utc)

    if is_new and hasattr(record, "created_at"):
        if getattr(record, "created_at") is None:
            setattr(record, "created_at", current_time)

    # Always update the updated_at field, either on creation, update, or delete
    if hasattr(record, "updated_at"):
        setattr(record, "updated_at", current_time)