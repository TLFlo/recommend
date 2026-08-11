from pydantic import BaseModel

from backend.app.schemas.service import ServiceCreate


class Location(BaseModel):
    type: str = "Point"
    coordinates: list[float]


class Address(BaseModel):
    city: str
    district: str | None = None
    description: str | None = None


class ProviderCreate(BaseModel):

    name: str

    category_id: str

    description: str | None = None

    services: list[ServiceCreate]

    location: Location

    address: Address

    phone: str | None = None