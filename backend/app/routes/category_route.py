from fastapi import APIRouter, status

from app.schemas.category_schema import CategoryCreate
from app.services.category_service import create_category_service


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    category: CategoryCreate,
):
    return await create_category_service(category)
