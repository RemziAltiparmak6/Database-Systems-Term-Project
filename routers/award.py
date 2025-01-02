from fastapi import APIRouter, Depends, HTTPException
from services.award import create_award_service, update_award_service, delete_award_service, get_all_awards_service
from models.award import AwardCreate, AwardResponse, AwardUpdate
from helper import get_current_user, admin_required
router = APIRouter(prefix="/awards", tags=["Awards"])


@router.post("/", response_model=AwardResponse)
def create_award(award: AwardCreate,current_user: dict = Depends(admin_required)):
    return create_award_service(award)

@router.put("/{award_id}/", response_model=dict)
def update_award(award_id: int, award_update: AwardUpdate,current_user: dict = Depends(admin_required)):
    return update_award_service(award_id, award_update)

@router.delete("/{award_id}/", response_model=dict)
def delete_award(award_id: int,current_user: dict = Depends(admin_required)):
    return delete_award_service(award_id)

@router.get("/", response_model=list[AwardResponse])
def get_all_awards(current_user: dict = Depends(get_current_user)):
    return get_all_awards_service()
