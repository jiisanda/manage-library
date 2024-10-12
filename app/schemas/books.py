from app.schemas.bands import BookBase


class BookCreate(BookBase):
    ...

class BookRead(BookBase):
    ...

class BookPatch(BookBase):
    isbn: str = None
    publisher: str = None
    title: str = None
    authors: str = None
    stock: int = None
