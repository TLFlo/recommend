from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.indexes import create_indexes
from app.routes.providers_route import router as provider_router
from app.routes.category_route import router as category_router

app = FastAPI(
    title="Tadiavo-eo",
    description="Local service discovery and recommendation API",
    version="1.0.0",
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_indexes()

    yield


app.include_router(provider_router)
app.include_router(category_router)
