from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class Page(BaseModel, Generic[T]):
    """Pagination result data structure."""

    elements: list[T]  # Data
    page_number: int  # Page number
    page_size: int  # Number of records per page
    total_records: int  # Total number of records
