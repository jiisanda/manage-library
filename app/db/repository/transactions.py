from datetime import datetime, timezone
from http.client import HTTPException
from typing import Union, Any, Dict, List
from uuid import UUID

from sqlalchemy import select, delete, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import http_404, http_409
from app.db.tables.enum import TransactionStatus
from app.db.tables.library import Transactions
from app.schemas.transactions import TransactionRead, TransactionCreate, TransactionPatch


class TransactionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _get_instance(self, transaction_id: UUID) -> Union[Any, HTTPException]:
        try:
            transaction_id = UUID(str(transaction_id))
            stmt = (
                select(Transactions)
                .where(Transactions.id == transaction_id)
            )

            result = await self.session.execute(stmt)
            return result.scalar_one_or_none()
        except ValueError as e:
            raise http_404(msg=f"Transaction does not exists.") from e

    @staticmethod
    async def _extract_changes(transaction_patch: TransactionPatch) -> Dict[str, Any]:
        if isinstance(transaction_patch, dict):
            return transaction_patch
        return transaction_patch.model_dump(exclude_unset=True)

    @staticmethod
    def _return_book(transaction: dict, return_date: datetime) -> float:
        issue_date = transaction.get('issue_date')

        days_rented = (return_date-issue_date).days
        rent_fee_per_day = 10
        rent_fee = days_rented * rent_fee_per_day

        return rent_fee

    async def get_transaction(self, transaction_id: UUID) -> Union[TransactionRead, HTTPException]:
        db_transaction = await self._get_instance(transaction_id=transaction_id)
        if db_transaction is None:
            return http_404(msg=f"Transaction does not exists.")

        return TransactionRead(**db_transaction.__dict__)

    async def get_transactions(self, limit: int = 10, offset: int=0) -> Dict[str, Union[List[TransactionRead], Any]]:
        stmt = (
            select(Transactions)
            .offset(offset)
            .limit(limit)
        )
        try:
            result = await self.session.execute(stmt)
            result_list = result.fetchall()

            for row in result_list:
                row.Transactions.__dict__.pop('_sa_instance_state', None)

            result = [TransactionRead(**row.Transactions.__dict__) for row in result_list]
            return {
                "result": result,
                "no_of_transactions": len(result),
            }
        except Exception as e:
            raise http_404(msg=f"Transactions does not exists.") from e

    async def add_transaction(self, transaction: TransactionCreate) -> Union[TransactionRead, HTTPException]:
        if not isinstance(transaction, dict):
            db_transaction = Transactions(**transaction.model_dump())
        else:
            db_transaction = Transactions(**transaction)

        try:
            self.session.add(db_transaction)
            await self.session.commit()
            await self.session.refresh(db_transaction)
        except IntegrityError as e:
            raise http_404(msg=f"Transaction: {db_transaction} already exists.") from e

        return TransactionRead(**db_transaction.__dict__)

    async def patch_transaction(self, transaction_id: Union[str, UUID], transaction: TransactionPatch) -> Union[TransactionRead, HTTPException]:
        db_transaction = (await self._get_instance(transaction_id)).__dict__
        changes = await self._extract_changes(transaction_patch=transaction)

        # rent fee calculation
        if transaction.status == TransactionStatus.returned or transaction.return_date:
            return_date = (transaction.return_date if transaction.return_date else datetime.now(timezone.utc))
            rent_fee = self._return_book(transaction=db_transaction, return_date=return_date)
            changes["return_date"] = return_date
            changes["late_fee"] = rent_fee

        stmt = (
            update(Transactions)
            .where(Transactions.id == db_transaction.get('id'))
            .values(changes)
        )

        try:
            await self.session.execute(stmt)
        except Exception as e:
            raise http_409(msg=f"Transaction could not be added.") from e

        db_transaction = (await self._get_instance(transaction_id)).__dict__
        return TransactionRead(**db_transaction)

    async def delete_transaction(self, transaction_id: UUID) -> None:
        db_transaction = (await self._get_instance(transaction_id=transaction_id)).__dict__

        try:
            stmt = (
                delete(Transactions)
                .where(Transactions.id == db_transaction.get('id'))
            )

            await self.session.execute(stmt)
            await self.session.commit()
        except Exception as e:
            raise http_409(msg=f"Error while deleting transaction: {transaction_id}") from e
