from fastapi import APIRouter

from app.core.config import settings

from app.api.base import routes as base_routes
from app.api.users import routes as user_routes

api_router = APIRouter()

# Import all module routes here
api_router.include_router(base_routes.router)
api_router.include_router(user_routes.router)
