from fastapi import FastAPI

from app.api.router import router
from app.core.config import settings
from app.db.models import check_tables

app = FastAPI(
    title=settings.title,
    version=settings.version,
    description=settings.description,
    docs_url=settings.docs_url,
    openapi_url=settings.openapi_url,
)

app.include_router(router=router, prefix=settings.api_prefix)


@app.get("/", tags=["Default"])
async def root():
    return {"jiisanda": "Library Management API Assignment for Frappe"}


@app.on_event("startup")
async def app_startup() -> None:
    return await check_tables()
