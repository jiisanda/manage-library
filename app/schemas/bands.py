from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.db.tables.enum import TransactionStatus


class BookBase(BaseModel):
    _id: UUID
    title: str
    authors: List[str]
    isbn: str
    publisher: Optional[str]
    stock: int = 0


class MemberBase(BaseModel):
    _id: UUID
    name: str
    email: EmailStr
    address: Optional[str]
    debt: int = 0


class TransactionBase(BaseModel):
    _id: UUID
    book_id: UUID
    member_id: UUID
    status: TransactionStatus
    issue_date: datetime
    return_date: Optional[datetime] = None
    late_fee: Optional[float] = 0.0
