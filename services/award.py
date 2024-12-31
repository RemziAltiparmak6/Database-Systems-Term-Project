from crud.award import add_award, update_award, delete_award, get_all_awards
from models.award import AwardCreate, AwardResponse, AwardUpdate
from fastapi import HTTPException, status

def create_award_service(award: AwardCreate) -> AwardResponse:
    """
    Creates a new award.
    """
    try:
        award_id = add_award(award)
        return AwardResponse(award_id=award_id, name=award.name, year=award.year)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the award: {str(e)}"
        )

def update_award_service(award_id: int, award_update: AwardUpdate) -> AwardResponse:
    """
    Updates an award's details.
    """
    try:
        updated_award_id = update_award(award_id, award_update.dict(exclude_unset=True))
        return {"award_id": updated_award_id,"name":award_update.name , "year":award_update.year}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the award: {str(e)}"
        )

def delete_award_service(award_id: int):
    """
    Deletes an award.
    """
    try:
        delete_award(award_id)
        return {"message": f"Award with ID {award_id} deleted successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the award: {str(e)}"
        )

def get_all_awards_service():
    """
    Retrieves all awards.
    """
    try:
        awards = get_all_awards()
        return awards
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching awards: {str(e)}"
        )
