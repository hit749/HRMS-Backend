from fastapi import APIRouter
from src.endpoints import location

router = APIRouter()
router.include_router(location.router)
