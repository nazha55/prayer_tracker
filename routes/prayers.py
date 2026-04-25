from fastapi import APIRouter, Depends
from schemas.prayer import UpdatePrayerRequest
from services.prayer_service import get_today_prayers, update_prayer
from utils.dependencies import get_current_user

router = APIRouter()


@router.get("/today")
def get_today(user_id: int = Depends(get_current_user)):
    return get_today_prayers(user_id)


@router.put("/update")
def update(data: UpdatePrayerRequest, user_id: int = Depends(get_current_user)):
    return update_prayer(user_id, data.prayer, data.status)