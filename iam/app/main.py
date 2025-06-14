from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f'{settings.API_VERSION_STR}/docs',
    openapi_url=f'{settings.API_VERSION_STR}/openapi.json',
)

app.include_router(router=api_router, prefix=settings.API_VERSION_STR)
