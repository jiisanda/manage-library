from fastapi import APIRouter

from app.api.routes.books import router as books_router
from app.api.routes.members import router as member_router
from app.api.routes.transactions import router as transaction_router

router = APIRouter()

router.include_router(books_router, prefix="/books")
router.include_router(member_router, prefix="/members")
router.include_router(transaction_router, prefix="/transactions")
