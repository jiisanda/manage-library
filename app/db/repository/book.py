from http.client import HTTPException
from typing import Union, Any, Dict, List
from uuid import UUID

import httpx
from sqlalchemy import select, update, delete, func
from sqlalchemy.exc import IntegrityError, MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import http_404, http_409, http_400
from app.db.tables.enum import SearchFields
from app.db.tables.library import Book
from app.schemas.books import BookCreate, BookRead, BookPatch


class BookRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_instance(self, book_id: Union[str, UUID]) -> Union[Any, HTTPException]:
        try:
            book_id = UUID(str(book_id))
        except ValueError:
            raise http_404(msg="Book not found")

        stmt = (
            select(Book)
            .where(Book.id == book_id)
        )

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def _extract_changes(book_patch: BookPatch) -> Dict[str, Any]:
        if isinstance(book_patch, dict):
            return book_patch
        return book_patch.model_dump(exclude_unset=True)

    async def _get_book_bi_isbn(self, isbn: str) -> Union[Any, HTTPException]:
        stmt = select(Book).where(Book.isbn == isbn)

        result = await self.session.execute(stmt)
        # Handle multiple results explicitly
        try:
            book = result.scalar_one_or_none()
        except MultipleResultsFound:
            raise http_400(msg=f"Multiple books found with ISBN {isbn}")

        return book

    async def get_book(self, book: Union[str, UUID]) -> Union[BookRead, HTTPException]:
        db_book = await self._get_instance(book_id=book)
        if db_book is None:
            return http_404(msg="Book not found")

        return BookRead(**db_book.__dict__)

    async def get_books(self, limit: int = 10, offset: int=0) -> Dict[str, Union[List[BookRead], Any]]:

        # Query to get the total count of books
        total_count_stmt = select(func.count()).select_from(Book)
        total_count_result = await self.session.execute(total_count_stmt)
        total_books = total_count_result.scalar()  # Get the total number of books

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
                "no_of_books": total_books
            }
        except Exception as e:
            raise http_404(msg=f"Books does not exists.") from e

    async def add_book(self, book: BookCreate) -> Union[BookRead, HTTPException] | None:

        if not isinstance(book, dict):
            db_book = Book(**book.model_dump())
        else:
            db_book = Book(**book)

        # checking if book already exists
        existing_book = await self._get_book_bi_isbn(isbn=db_book.isbn)
        if existing_book:
            return None

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

    async def import_books(
            self,
            title: str,
            authors: str,
            isbn: str,
            publisher: str,
            pages: int,
    ) -> Dict[str, Union[List[BookRead], Any]]:
        books_imported = []
        page = 1

        while len(books_imported) < pages:
            try:
                # Call the Frappe API with the current page and parameters
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        "https://frappe.io/api/method/frappe-library",
                        params={
                            "page": page,
                            "title": title,
                            "authors": authors,
                            "isbn": isbn,
                            "publisher": publisher,
                        },
                    )
                    data = response.json()

                # Check if the API returned books
                if not data.get("message"):
                    raise http_404(msg="Books not found")

                # Add books to the repository
                for book_data in data["message"]:
                    if len(books_imported) >= pages:
                        break

                    book = BookCreate(
                        title=book_data["title"],
                        authors=book_data["authors"],
                        isbn=book_data["isbn"],
                        publisher=book_data["publisher"],
                        stock=5,
                    )
                    if await self.add_book(book):
                        books_imported.append(book)

                page += 1

            except Exception as e:
                raise http_400(msg=f"Error while importing books.") from e

        return {
            "books": books_imported,
            "books_imported": len(books_imported)
        }
