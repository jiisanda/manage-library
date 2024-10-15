from typing import List, Union, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Query, HTTPException
from starlette import status

from app.api.dependencies.repositories import get_repository
from app.db.repository.book import BookRepository
from app.db.repository.members import MemberRepository
from app.db.repository.transactions import TransactionRepository
from app.schemas.transactions import TransactionRead, TransactionCreate, TransactionPatch

router = APIRouter(tags=["Transactions"])


@router.post(
    "",
    response_model=TransactionRead,
    status_code=status.HTTP_201_CREATED,
    name="add_transaction",
)
async def add_transaction(
        transaction: TransactionCreate = Body(...),
        repository: TransactionRepository = Depends(get_repository(TransactionRepository)),
        member_repository: MemberRepository = Depends(get_repository(MemberRepository)),
        book_repository: BookRepository = Depends(get_repository(BookRepository)),
) -> TransactionRead:
    """
    Add a new transaction to the repository.

    This function handles the creation of a new transaction by accepting the necessary transaction data and storing it in the repository. 
    Upon successful addition, it returns the details of the newly created transaction.

    Args:
        transaction (TransactionCreate): The data for the transaction to be added.
        repository (TransactionRepository): The repository instance used to interact with transaction data.
        member_repository (MemberRepository): The repository instance used to access member data.
        book_repository (BookRepository): The repository instance used to access book data.

    Returns:
        TransactionRead: The details of the newly created transaction.

    Raises:
        HTTPException: If there is an error during the transaction addition process.
    """

    return await repository.add_transaction(
        transaction=transaction,
        member=member_repository,
        book=book_repository,
    )


@router.get(
    "/{transaction}/detail",
    response_model=None,
    status_code=status.HTTP_200_OK,
    name="get_transaction_detail",
)
async def get_transaction_detail(
        transaction: Union[str, UUID],
        repository: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> Union[TransactionRead, HTTPException]:
    """
    Retrieve the details of a specific transaction from the repository.

    This function processes requests to fetch the details of a transaction identified by its unique identifier. 
    It returns the transaction's information if found, or raises an exception if the transaction does not exist.

    Args:
        transaction (Union[str, UUID]): The identifier of the transaction to retrieve.
        repository (TransactionRepository): The repository instance used to access transaction data.

    Returns:
        Union[TransactionRead, HTTPException]: The details of the requested transaction or an HTTP exception if not found.

    Raises:
        HTTPException: If the transaction cannot be found in the repository.
    """

    return await repository.get_transaction(transaction_id=transaction)


@router.get(
    "",
    response_model=Dict[str, Union[List[TransactionRead], Any]],
    status_code=status.HTTP_200_OK,
    name="get_transactions",
)
async def get_members(
        limit: int = Query(default=10, lt=100),
        offset: int = Query(default=0),
        repository: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> Dict[str, Union[List[TransactionRead], Any]]:
    """
    Retrieve a list of transactions from the repository with optional pagination.

    This function allows clients to fetch a collection of transactions, supporting pagination through limit and offset parameters. 
    It returns a dictionary containing the list of transactions and any additional information as needed.

    Args:
        limit (int): The maximum number of transactions to return (default is 10, must be less than 100).
        offset (int): The number of transactions to skip before starting to collect the result set (default is 0).
        repository (TransactionRepository): The repository instance used to access transaction data.

    Returns:
        Dict[str, Union[List[TransactionRead], Any]]: A dictionary containing a list of transactions and any additional information.

    Raises:
        HTTPException: If there is an error retrieving the transactions from the repository.
    """

    return await repository.get_transactions(limit=limit, offset=offset)


@router.put(
    "/{transaction}",
    response_model=None,
    status_code=status.HTTP_200_OK,
    name="update_transaction",
)
async def update_transaction(
        transaction: Union[str, UUID],
        transaction_patch: TransactionPatch = Body(...),
        repository: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> Union[TransactionRead, HTTPException]:
    """
    Update the details of an existing transaction in the repository.

    This function processes a request to modify the information of a specific transaction identified by its unique identifier. 
    It applies the provided changes and returns the updated transaction details upon successful modification.

    Args:
        transaction (Union[str, UUID]): The identifier of the transaction to update.
        transaction_patch (TransactionPatch): The data containing the updates to be applied to the transaction.
        repository (TransactionRepository): The repository instance used to access and modify transaction data.

    Returns:
        Union[TransactionRead, HTTPException]: The updated details of the transaction or an HTTP exception if the transaction cannot be found.

    Raises:
        HTTPException: If the transaction does not exist or if there is an error during the update process.
    """

    await repository.get_transaction(transaction_id=transaction)

    return await repository.patch_transaction(
        transaction_id=transaction,
        transaction=transaction_patch,
    )


@router.delete(
    "/{transaction}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="delete_transaction",
)
async def delete_transaction(
        transaction: Union[str, UUID],
        repository: TransactionRepository = Depends(get_repository(TransactionRepository)),
) -> None:
    """
    Delete a specific transaction from the repository.

    This function handles requests to remove a transaction identified by its unique identifier from the repository. Upon successful deletion, it returns no content, indicating that the operation was completed.

    Args:
        transaction (Union[str, UUID]): The identifier of the transaction to be deleted.
        repository (TransactionRepository): The repository instance used to access and modify transaction data.

    Returns:
        None

    Raises:
        HTTPException: If the transaction cannot be found or if there is an error during the deletion process.
    """

    await repository.delete_transaction(transaction_id=transaction)
