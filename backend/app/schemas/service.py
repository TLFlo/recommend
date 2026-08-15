from pydantic import BaseModel, Field


class Price(BaseModel):
    avg: float = Field(gt=0)
    currency: str = "MGA"


class Rating(BaseModel):
    average: float = Field(default=0, ge=0, le=5)
    count: int = 0


class ServiceCreate(BaseModel):
    name: str
    description: str | None = None
    price: Price


class ServiceResponse(ServiceCreate):
    id: str
    rating: Rating
