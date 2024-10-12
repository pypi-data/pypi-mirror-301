from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Any, Type, List

from pydantic import BaseModel
from sqlalchemy import func
from sqlmodel import select, desc, asc
from sqlmodel.ext.asyncio.session import AsyncSession

from vovo.persistence.models import Page
from vovo.persistence.utils import set_timestamps
from vovo.utils.orm import get_primary_keys

T = TypeVar("T", bound=BaseModel)


class GenericRepository(Generic[T], ABC):
    """Generic base repository."""

    @abstractmethod
    async def get(self, *args: Any, **kwargs: Any) -> T | None:
        """Get a single record by either positional or keyword arguments (or both).

        Args:
            *args (Any): Positional arguments representing values for filtering.
                         The order of arguments should match the expected field order.
            **kwargs (Any): Keyword arguments representing field names and their corresponding values
                            for filtering (e.g., id=1, name="John").

        Returns:
            Optional[T]: Record or None if not found.
        """
        raise NotImplementedError()

    @abstractmethod
    async def list(self, limit: int = 100, **filters) -> list[T]:
        """Gets a list of records

        Args:
            limit (int): The maximum number of records to return. Default is 100.
            **filters: Filter conditions, several criteria are linked with a logical 'and'.

         Raises:
            ValueError: Invalid filter condition.

        Returns:
            List[T]: List of records.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_page_list(self, page_number: int, page_size: int, order_by: str | List[str] | None = None,
                            **filters: Any) -> Page[T]:
        """Get a paginated list of records."""
        raise NotImplementedError()

    @abstractmethod
    async def get_count(self, **filters: Any) -> int:
        """Get the count query with filters"""
        raise NotImplementedError()

    @abstractmethod
    async def add(self, record: T) -> T:
        """Creates a new record.

        Args:
            record (T): The record to be created.

        Returns:
            T: The created record.
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(self, record: T) -> T:
        """Updates an existing record.

        Args:
            record (T): The record to be updated incl. record id.

        Returns:
            T: The updated record.
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, *args: Any, **kwargs: Any) -> None:
        """Deletes a record by either positional or keyword arguments.

        Args:
            *args (Any): Positional arguments representing values for filtering.
            **kwargs (Any): Keyword arguments representing field names and their corresponding values for filtering.
        """
        raise NotImplementedError()


class GenericSqlRepository(GenericRepository[T], ABC):

    def __init__(self, session: AsyncSession, model: Type[T]) -> None:
        """Creates a new repository instance.

        Args:
            session (AsyncSession): SQLModel async session.
            model (Type[T]): SQLModel class type.
        """
        self.session = session
        self.model = model

    async def get(self, *args: Any, **kwargs: Any) -> T | None:

        query = self._build_query(*args, **kwargs).limit(1)
        res = await self.session.exec(query)
        return res.first()

    async def list(self, limit: int = 100, **filters) -> list[T]:
        """Gets a list of records from the database."""
        query = select(self.model)
        # Apply filters dynamically
        if filters:
            try:
                query = query.filter_by(**filters)
            except AttributeError as e:
                raise ValueError(f"Invalid filter condition: {e}")

            # Apply limit
        query = query.limit(limit)
        res = await self.session.exec(query)

        return list(res.all())

    async def get_page_list(self, page_number: int = 1, page_size: int = 10, order_by: str | List[str] | None = None,
                            **filters: Any) -> Page[T]:
        """Get a paginated list of records with optional ordering."""
        # Calculate the total number of records
        total_records = await self.get_count(**filters)

        # Apply limit, offset, and ordering for pagination
        query = select(self.model).filter_by(**filters).limit(page_size).offset((page_number - 1) * page_size)

        # Apply ordering if specified
        if order_by:
            if isinstance(order_by, str):
                order_by = [order_by]
            order_criteria = []
            for order in order_by:
                if order.startswith('-'):
                    # Descending order
                    field_name = order[1:]
                    order_criteria.append(desc(getattr(self.model, field_name)))
                else:
                    # Ascending order
                    order_criteria.append(asc(getattr(self.model, order)))
            query = query.order_by(*order_criteria)

        res = await self.session.exec(query)
        elements = list(res.all())

        return Page(elements=elements, page_number=page_number, page_size=page_size, total_records=total_records)

    async def get_count(self, **filters: Any) -> int:
        """Gets the count of records with optional filters."""
        query = select(func.count()).select_from(self.model)
        if filters:
            try:
                query = query.filter_by(**filters)
            except AttributeError as e:
                raise ValueError(f"Invalid filter condition: {e}")
        res = await self.session.exec(query)
        return res.one()

    async def add(self, record: T) -> T:
        """Adds a new record to the database."""
        set_timestamps(record, is_new=True)
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def update(self, record: T) -> T:
        set_timestamps(record)
        """Updates an existing record in the     database."""
        self.session.add(record)
        await self.session.commit()
        await self.session.refresh(record)
        return record

    async def delete(self, *args: Any, **kwargs: Any) -> None:
        """Deletes a record from the database using its key."""
        record = await self.get(*args, **kwargs)
        if record:
            await self.session.delete(record)
            await self.session.commit()

    def _build_query(self, *args: Any, **kwargs: Any):
        """Helper function to build query based on primary keys or filters."""
        if args:
            primary_keys = get_primary_keys(self.model)
            if len(args) != len(primary_keys):
                raise ValueError(f"Expected {len(primary_keys)} primary key values, got {len(args)}.")
            pk_filter = dict(zip(primary_keys, args))
            return select(self.model).filter_by(**pk_filter)
        elif kwargs:
            return select(self.model).filter_by(**kwargs)
        else:
            raise ValueError(
                "Either primary key arguments (*args) or filtering conditions (**kwargs) must be provided.")
