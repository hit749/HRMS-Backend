from fastapi import APIRouter
from src.endpoints import tax

router = APIRouter()
router.include_router(tax.router)
