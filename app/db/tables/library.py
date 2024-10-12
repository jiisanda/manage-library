from datetime import timezone, datetime
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import Column, String, Integer, Text, ForeignKey, DateTime, text, Enum
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import Mapped, relationship

from app.db.models import Base
from app.db.tables.enum import TransactionStatus


class Book(Base):
    __tablename__ = 'book'

    id: UUID = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True, nullable=False)
    title: str = Column(String)
    authors: List[str] = Column(ARRAY(String))
    isbn: str = Column(String)
    publisher: Optional[str] = Column(String)
    stock: int = Column(Integer, default=0)

    transactions = relationship("Transactions", backref="book", lazy=True)



class Members(Base):
    __tablename__ = 'members'

    id: UUID = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True, nullable=False)
    name: str = Column(String)
    email: str = Column(String, unique=True)
    address: Optional[str] = Column(Text)
    debt: int = Column(Integer, default=0)

    transactions = relationship("Transactions", backref="members", lazy=True)


class Transactions(Base):
    __tablename__ = 'transactions'

    id: UUID = Column(UUID(as_uuid=True), default=uuid4, primary_key=True, index=True, nullable=False)
    book_id: Mapped[UUID] = Column(UUID(as_uuid=True), ForeignKey('book.id'), nullable=False)
    member_id: Mapped[UUID] = Column(UUID(as_uuid=True), ForeignKey('members.id'), nullable=False)
    status: Enum = Column(Enum(TransactionStatus), default=TransactionStatus.issued)
    issue_date = Column(
        DateTime(timezone=True),
        default=datetime.now(timezone.utc),
        nullable=False,
        server_default=text("NOW()")
    )
    return_date = Column(DateTime(timezone=True), nullable=True)
    late_fee: Optional[float] = Column(Integer, default=0.0)
