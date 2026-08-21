from fastapi import APIRouter, Depends

from app.services.recommend_service import (
    get_personalized_recommendations,
)

router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)


@router.get("/for_me")
async def get_my_recommendations(
    user_id: str,
):
    return await get_personalized_recommendations(
        user_id
    )