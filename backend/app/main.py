from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database.indexes import create_indexes

app = FastAPI(
    title="Tadiavo-eo",
    description="Local service discovery and recommendation API",
    version="1.0.0"
)

@asynccontextmanager
async def lifespan(app: FastAPI):

    await create_indexes()

    yield

@app.get("/")
async def root():
    return {
        "message": "Tadiavo-eo API is running"
    }
