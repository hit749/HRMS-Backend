from fastapi import APIRouter
from src.endpoints import ctc

router = APIRouter()
router.include_router(ctc.router)
