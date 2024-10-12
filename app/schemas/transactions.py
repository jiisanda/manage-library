from datetime import datetime
from typing import Optional

from app.db.tables.enum import TransactionStatus
from app.schemas.bands import TransactionBase


class TransactionCreate(TransactionBase):
    ...


class TransactionRead(TransactionBase):
    ...


class TransactionPatch(TransactionBase):
    status: TransactionStatus = None
    return_date: datetime = None
    late_fee: Optional[float] = None
