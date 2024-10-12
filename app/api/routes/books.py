from typing import List, Union, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query, HTTPException
from starlette import status

from app.api.dependencies.repositories import get_repository
from app.db.repository.book import BookRepository
from app.schemas.library import BookRead, BookCreate, BookPatch

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
