from http.client import HTTPException
from typing import Union, Any, Dict, List
from uuid import UUID

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import http_404, http_409
from app.db.tables.enum import SearchFields
from app.db.tables.library import Book
from app.schemas.books import BookCreate, BookRead, BookPatch


class BookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_instance(self, book_id: Union[str, UUID]) -> Union[Any, HTTPException]:
        try:
            book_id = UUID(str(book_id))
            stmt = (
                select(Book)
                .where(Book.id == book_id)
            )
        except ValueError:
            raise http_404(msg="Book not found")

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def _extract_changes(book_patch: BookPatch) -> Dict[str, Any]:
        if isinstance(book_patch, dict):
            return book_patch
        return book_patch.model_dump(exclude_unset=True)

    async def get_book(self, book: Union[str, UUID]) -> Union[BookRead, HTTPException]:
        db_book = await self._get_instance(book_id=book)
        if db_book is None:
            return http_404(msg="Book not found")

        return BookRead(**db_book.__dict__)

    async def get_books(self, limit: int = 10, offset: int=0) -> Dict[str, Union[List[BookRead], Any]]:
        stmt = (
            select(Book)
            .offset(offset)
            .limit(limit)
        )
        try:
            result = await self.session.execute(stmt)
            result_list = result.fetchall()

            for row in result_list:
                row.Book.__dict__.pop('_sa_instance_state', None)

            result = [BookRead(**row.Book.__dict__) for row in result_list]
            return {
                "result": result,
                "no_of_books": len(result),
            }
        except Exception as e:
            raise http_404(msg=f"Books does not exists.") from e

    async def add_book(self, book: BookCreate) -> Union[BookRead, HTTPException]:

        if not isinstance(book, dict):
            db_book = Book(**book.model_dump())
        else:
            db_book = Book(**book)

        try:
            self.session.add(db_book)
            await self.session.commit()
            await self.session.refresh(db_book)
        except IntegrityError as e:
            raise http_404(msg=f"Book with details: {db_book} already exists") from e

        return BookRead(**db_book.__dict__)

    async def patch_book(self, book_id: Union[str, UUID],  book: BookPatch) -> Union[BookRead, HTTPException]:
        db_book = (await self._get_instance(book_id=book_id)).__dict__
        changes = await self._extract_changes(book_patch=book)

        stmt = (
            update(Book)
            .where(Book.id == db_book.get('id'))
            .values(changes)
        )
        book_name = db_book.get('name')

        try:
            await self.session.execute(stmt)
        except Exception as e:
            raise http_409(msg=f"Error while updating book: {book_name}") from e

        db_book = (await self._get_instance(book_id=book_id)).__dict__
        return BookRead(**db_book)

    async def delete_book(self, book_id: Union[str, UUID]) -> None:
        db_book = (await self._get_instance(book_id=book_id)).__dict__

        stmt = (
            delete(Book)
            .where(Book.id == db_book.get('id'))
        )

        try:
            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as e:
            raise http_409(msg=f"Error while deleting book: {book_id}") from e

    async def search_books(
            self,
            field: SearchFields,
            query_input: str,
            limit: int = 10,
            offset: int = 0
    ) -> Dict[str, Union[List[BookRead], Any]]:
        stmt = select(Book)

        match field:
            case SearchFields.title:
                stmt = stmt.where(Book.title.ilike(f"%{query_input}%"))
            case SearchFields.author:
                stmt = stmt.where(Book.authors.ilike(f"%{query_input}%"))
            case SearchFields.isbn:
                stmt = stmt.where(Book.isbn.ilike(f"%{query_input}%"))
            case _:
                raise ValueError(f"Invalid search field: {field}")

        stmt = stmt.offset(offset).limit(limit)

        result = await self.session.execute(stmt)
        books = result.scalars().unique().all()

        book_reads = [BookRead.from_orm(book) for book in books]

        return {
            "result": book_reads,
            "query": query_input,
            "field": field.value,
            "no_of_books": len(book_reads),
        }
