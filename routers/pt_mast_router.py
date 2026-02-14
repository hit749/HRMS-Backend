from fastapi import APIRouter
from src.endpoints import pt_mast

router = APIRouter()
router.include_router(pt_mast.router)
