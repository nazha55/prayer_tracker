from fastapi import APIRouter, Depends
from schemas.routine import CreateRoutineRequest, ToggleRoutineRequest
from services.routine_service import create_routine, get_routines, toggle_routine
from utils.dependencies import get_current_user

router = APIRouter()


@router.post("/")
def create(data: CreateRoutineRequest, user_id: int = Depends(get_current_user)):
    return create_routine(user_id, data.title)


@router.get("/")
def list_routines(user_id: int = Depends(get_current_user)):
    return get_routines(user_id)


@router.put("/toggle")
def toggle(data: ToggleRoutineRequest, user_id: int = Depends(get_current_user)):
    return toggle_routine(user_id, data.routine_id)