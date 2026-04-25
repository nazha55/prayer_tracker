from fastapi import APIRouter, Depends
from utils.dependencies import get_current_user
from services.history_service import get_prayer_history

router = APIRouter()


@router.get("/prayers")
def history(days: int = 30, user_id: int = Depends(get_current_user)):
    return get_prayer_history(user_id, days)