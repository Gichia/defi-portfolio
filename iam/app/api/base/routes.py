from fastapi import APIRouter

router = APIRouter(prefix='', tags=['Home'])


@router.get('/')
async def home() -> dict:
    return {'detail': 'Welcome'}


@router.get('/health-check')
async def health_check() -> bool:
    return True
