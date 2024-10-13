from typing import List, Union, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query, HTTPException
from starlette import status

from app.api.dependencies.repositories import get_repository
from app.db.repository.book import BookRepository
from app.db.tables.enum import SearchFields
from app.schemas.books import BookRead, BookCreate, BookPatch

router = APIRouter(tags=["Books"])


@router.post(
    "",
    response_model=BookRead,
    status_code=status.HTTP_201_CREATED,
    name="add_book",
)
async def add_book(
        book: BookCreate = Body(...),
        repository: BookRepository = Depends(get_repository(BookRepository)),
) -> BookRead:

    return await repository.add_book(book)


@router.get(
    "/{book}/detail",
    response_model=None,
    status_code=status.HTTP_200_OK,
    name="get_book",
)
async def get_book(
        book: Union[str, UUID],
        repository: BookRepository = Depends(get_repository(BookRepository)),
) -> Union[BookRead, HTTPException]:

    return await repository.get_book(book=book)


@router.get(
    "",
    response_model=Dict[str, Union[List[BookRead], Any]],
    status_code=status.HTTP_200_OK,
    name="get_books",
)
async def get_books(
        limit: int = Query(default=10, lt=100),
        offset: int = Query(default=0),
        repository: BookRepository = Depends(get_repository(BookRepository)),
) -> Dict[str, Union[List[BookRead], Any]]:

    return await repository.get_books(limit=limit, offset=offset)


@router.put(
    "/{book}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    name="update_book",
)
async def update_book(
        book: Union[str, UUID],
        book_patch: BookPatch = Body(...),
        repository: BookRepository = Depends(get_repository(BookRepository)),
) -> Union[BookRead, HTTPException]:

    await repository.get_book(book=book)

    return await repository.patch_book(
        book_id=book,
        book=book_patch,
    )


@router.delete(
    "/{book}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_book",
)
async def delete_book(
        book: Union[str, UUID],
        repository: BookRepository = Depends(get_repository(BookRepository)),
) -> None:

    await repository.delete_book(book_id=book)

@router.get(
    "/search",
    response_model=None,
    status_code=status.HTTP_200_OK,
    name="search_books",
)
async def search_books(
        field: SearchFields = Query(..., description="Field to search in (name, author, or isbn)"),
        query: str = Query(..., description="Search query"),
        limit: int = Query(default=10, lt=100),
        offset: int = Query(default=0),
        repository: BookRepository = Depends(get_repository(BookRepository)),
) -> Dict[str, Union[List[BookRead], Any]]:

    return await repository.search_books(field=field, query_input=query, limit=limit, offset=offset)


@router.post(
    "/import",
    status_code=status.HTTP_201_CREATED,
    name="import_books"
)
async def import_books(
        title: str = Query(None),
        authors: str = Query(None),
        isbn: str = Query(None),
        publisher: str = Query(None),
        pages: int = Query(20, description="Number of books to import"),
        repository: BookRepository = Depends(get_repository(BookRepository)),
) -> Dict[str, Union[List[BookRead], Any]]:

    return await repository.import_books(
        title=title,
        authors=authors,
        isbn=isbn,
        publisher=publisher,
        pages=pages,
    )
