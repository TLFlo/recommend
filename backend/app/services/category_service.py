from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.repositories.category_repo import (
    create_category,
)
from app.schemas.category_schema import CategoryCreate


async def create_category_service(
    category: CategoryCreate,
) -> dict:
    category_data = category.model_dump()

    # Vérification du nom
    category_data["name"] = category_data["name"].strip()

    if not category_data["name"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category name cannot be empty.",
        )

    try:
        return await create_category(category_data)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create category.",
        ) from exc
