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

    await repository.delete_transaction(transaction_id=transaction)
