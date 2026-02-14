from fastapi import APIRouter
from src.endpoints import employMaster

router = APIRouter()
router.include_router(employMaster.router)
