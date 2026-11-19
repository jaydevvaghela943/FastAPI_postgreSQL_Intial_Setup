from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.database.connection import engine
from app.database.base import Base
from app.models import User, Document
from app.routers.health_router import router as health_router

from app.routers.auth_router import router as auth_router
from app.routers.user_router import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables during local development
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    # Close database connections
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="Role-Based RAG Knowledge Base API",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(health_router)
app.include_router(auth_router)
app.include_router(user_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to RAG Knowledge Base API",
        "status": "running",
        "version": "1.0.0"
    }
