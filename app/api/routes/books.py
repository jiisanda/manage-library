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
    """
    Add a new book to the repository.

    This function processes a request to create a new book entry by accepting the necessary book data and storing it in the repository. 
    Upon successful addition, it returns the details of the newly created book.

    Args:
        book (BookCreate): The data for the book to be created.
        repository (BookRepository): The repository instance used for adding the book.

    Returns:
        BookRead: The details of the created book.

    Raises:
        HTTPException: If an error occurs during the book addition process.
    """


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
    """
    Retrieve the details of a specific book from the repository.

    This function handles requests to fetch the details of a book identified by its unique identifier. 
    It returns the book's information if found, or raises an exception if the book does not exist.

    Args:
        book (Union[str, UUID]): The identifier of the book to retrieve.
        repository (BookRepository): The repository instance used to access book data.

    Returns:
        Union[BookRead, HTTPException]: The details of the requested book or an HTTP exception if not found.

    Raises:
        HTTPException: If the book cannot be found in the repository.
    """

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
    """
    Retrieve a list of books from the repository with optional pagination.

    This function allows clients to fetch a collection of books, supporting pagination through limit and offset parameters. 
    It returns a dictionary containing the list of books and any additional information as needed.

    Args:
        limit (int): The maximum number of books to return (default is 10, must be less than 100).
        offset (int): The number of books to skip before starting to collect the result set (default is 0).
        repository (BookRepository): The repository instance used to access book data.

    Returns:
        Dict[str, Union[List[BookRead], Any]]: A dictionary containing a list of books and any additional information.

    Raises:
        HTTPException: If there is an error retrieving the books from the repository.
    """

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
    """
    Update the details of an existing book in the repository.

    This function processes a request to modify the information of a specific book identified by its unique identifier. 
    It applies the provided changes and returns the updated book details upon successful modification.

    Args:
        book (Union[str, UUID]): The identifier of the book to update.
        book_patch (BookPatch): The data containing the updates to be applied to the book.
        repository (BookRepository): The repository instance used to access and modify book data.

    Returns:
        Union[BookRead, HTTPException]: The updated details of the book or an HTTP exception if the book cannot be found.

    Raises:
        HTTPException: If the book does not exist or if there is an error during the update process.
    """

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
    """
    Delete a specific book from the repository.

    This function handles requests to remove a book identified by its unique identifier from the repository. 
    Upon successful deletion, it returns no content, indicating that the operation was completed.

    Args:
        book (Union[str, UUID]): The identifier of the book to be deleted.
        repository (BookRepository): The repository instance used to access and modify book data.

    Returns:
        None

    Raises:
        HTTPException: If the book cannot be found or if there is an error during the deletion process.
    """

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
    """
    Search for books in the repository based on specified criteria.

    This function allows clients to perform a search for books using a specified field and query string. 
    It supports pagination through limit and offset parameters, returning a list of matching books.

    Args:
        field (SearchFields): The field to search in (e.g., name, author, or isbn).
        query (str): The search query string used to find matching books.
        limit (int): The maximum number of books to return (default is 10, must be less than 100).
        offset (int): The number of books to skip before starting to collect the result set (default is 0).
        repository (BookRepository): The repository instance used to access book data.

    Returns:
        Dict[str, Union[List[BookRead], Any]]: A dictionary containing a list of books that match the search criteria and any additional information.

    Raises:
        HTTPException: If there is an error during the search process.
    """


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
    """
    Import books into the repository based on specified criteria.

    This function facilitates the import of books by accepting various parameters such as title, authors, ISBN, and publisher. It allows for the specification of the number of books to import and returns a list of the imported books.

    Args:
        title (str): The title of the book(s) to import.
        authors (str): The authors of the book(s) to import.
        isbn (str): The ISBN of the book(s) to import.
        publisher (str): The publisher of the book(s) to import.
        pages (int): The number of books to import (default is 20).
        repository (BookRepository): The repository instance used to access and modify book data.

    Returns:
        Dict[str, Union[List[BookRead], Any]]: A dictionary containing a list of the imported books and any additional information.

    Raises:
        HTTPException: If there is an error during the import process.
    """

    return await repository.import_books(
        title=title,
        authors=authors,
        isbn=isbn,
        publisher=publisher,
        pages=pages,
    )
