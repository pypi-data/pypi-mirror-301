from datetime import datetime, timezone
from typing import Optional, TypeVar, Generic

from pydantic import Field, BaseModel

T = TypeVar("T", bound=BaseModel)


class TimestampMixin:
    """创建时间&更新时间定义"""
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None


class Page(BaseModel, Generic[T]):
    """Pagination result data structure."""

    elements: list[T]  # Data
    page_number: int  # Page number
    page_size: int  # Number of records per page
    total_records: int  # Total number of records
