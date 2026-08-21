from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ReviewCreate(BaseModel):
    provider_id: str
    rating: float | None = Field(
        default=None,
        ge=1,
        le=5,
    )
    comment: str | None = None