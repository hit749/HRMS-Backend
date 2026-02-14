from fastapi import APIRouter
from src.endpoints import bank

router = APIRouter()
router.include_router(bank.router)
