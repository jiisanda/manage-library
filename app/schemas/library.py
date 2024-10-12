from app.schemas.bands import BookBase


class BookCreate(BookBase):
    ...

class BookRead(BookBase):
    ...

class BookPatch(BookBase):
    title: str = None
    authors: str = None
    stock: int = None
