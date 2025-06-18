import time

from fastapi import FastAPI, Request

from app.api.main import api_router
from app.core.config import settings
from app.core.logging_config import access_logger, error_logger


app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=f'{settings.API_VERSION_STR}/docs',
    openapi_url=f'{settings.API_VERSION_STR}/openapi.json',
)

app.include_router(router=api_router, prefix=settings.API_VERSION_STR)

# --- Request/Response Logging Middleware ---
@app.middleware('http')
async def log_requests(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        access_logger.info(
            f'Request: {request.method} {request.url.path} - '
            f'Status: {response.status_code} - '
            f'Process Time: {process_time:.4f}s'
        )
        return response
    except Exception as e:
        process_time = time.time() - start_time
        error_logger.exception(
            f'Error during request: {request.method} {request.url.path} - '
            f'Process Time: {process_time:.4f}s - '
            f'Exception: {e}'
        )
        raise # Re-raise the exception after logging it
