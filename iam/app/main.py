from fastapi import FastAPI
from contextlib import asynccontextmanager

from app import prestart
from app.api.main import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    prestart.main()
    yield


app = FastAPI(
    lifespan=lifespan,
    title=settings.PROJECT_NAME,
    docs_url=f'{settings.API_VERSION_STR}/docs',
    openapi_url=f'{settings.API_VERSION_STR}/openapi.json',
)

app.include_router(router=api_router, prefix=settings.API_VERSION_STR)
