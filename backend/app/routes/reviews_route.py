from fastapi import APIRouter

from app.schemas.review_schema import ReviewCreate
from app.services.review_service import create_review


router = APIRouter(
    prefix="/reviews",
    tags=["Reviews"],
)


@router.post("")
async def create_review_route(
    review: ReviewCreate,
    user_id: str,
):

    return await create_review(
        review=review,
        user_id=user_id,
    )