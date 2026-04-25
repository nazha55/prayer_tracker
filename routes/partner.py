from fastapi import APIRouter, Depends
from schemas.user import PartnerLinkInput
from utils.dependencies import get_current_user
from services.partner_service import link_partner, get_partner_dashboard

router = APIRouter()


@router.post("/link")
def link(data: PartnerLinkInput, user_id: int = Depends(get_current_user)):
    return link_partner(user_id, data.email)


@router.get("/dashboard")
def dashboard(user_id: int = Depends(get_current_user)):
    return get_partner_dashboard(user_id)