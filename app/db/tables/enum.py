from enum import Enum


class TransactionStatus(Enum):
    issued = "issued"
    returned = "returned"


class SearchFields(Enum):
    title = "title"
    author = "author"
    isbn = "isbn"
