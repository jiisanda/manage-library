from datetime import datetime
from typing import Optional
from uuid import UUID

from app.db.tables.enum import TransactionStatus
from app.schemas.bands import TransactionBase


class TransactionCreate(TransactionBase):
    ...


class TransactionRead(TransactionBase):
    ...


class TransactionPatch(TransactionBase):
    book_id: UUID = None
    member_id: UUID = None
    status: TransactionStatus = None
    issue_date: datetime = None
    return_date: datetime = None
    late_fee: Optional[float] = None
