from fastapi import APIRouter, status

from app.schemas.provider_schema import ProviderCreate
from app.services import provider_service


router = APIRouter(
    prefix="/prestataires",
    tags=["Pretataires"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_provider(
    provider: ProviderCreate,
    owner_id: str,
):
    return await provider_service.create_provider(
        provider,
        owner_id,
    )
