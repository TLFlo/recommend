from bson import ObjectId
from datetime import datetime, timezone

from fastapi import HTTPException, status

from app.repositories import provider_repo
from app.schemas.provider_schema import ProviderCreate
from app.repositories.category_repo import get_categories_by_ids


async def create_provider(
    provider: ProviderCreate,
    owner_id: str,
) -> dict:
    # --------------------------------
    # 1. Convertir les IDs
    # --------------------------------

    try:
        category_object_ids = [
            ObjectId(category_id) for category_id in provider.category_ids
        ]

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more category IDs are invalid.",
        ) from exc

    # --------------------------------
    # 2. Chercher les catégories
    # --------------------------------

    categories = await get_categories_by_ids(category_object_ids)

    # --------------------------------
    # 3. Vérifier qu'elles existent
    # --------------------------------

    if len(categories) != len(category_object_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more categories were not found.",
        )
    now = datetime.now(timezone.utc)
    # --------------------------------
    # 4. Préparer le document
    # --------------------------------

    provider_data = provider.model_dump()

    provider_data.pop("category_ids")

    provider_data["categories"] = [
        {
            "id": category["_id"],
            "name": category["name"],
            "slug": category["slug"],
        }
        for category in categories
    ]

    provider_data["owner_id"] = ObjectId(owner_id)

    provider_data["status"] = "active"

    provider_data["rating"] = {
        "average": 0.0,
        "count": 0,
    }

    provider_data["images"] = []

    provider_data["created_at"] = now
    provider_data["updated_at"] = now

    for service in provider_data["services"]:
        service["id"] = ObjectId()

        service["rating"] = {
            "average": 0.0,
            "count": 0,
            "sum": 0
        }
    
    return await provider_repo.create_provider(provider_data)
