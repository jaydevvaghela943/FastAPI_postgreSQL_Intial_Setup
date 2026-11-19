from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db

from app.schemas.auth_schema import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    UserResponse
)

from app.repositories.auth_repository import AuthRepository
from app.services.auth_service import AuthService
from app.dependencies.auth_dependencies import get_current_user


router = APIRouter(prefix="/api/v1/auth",tags=["Authentication"])

def get_auth_service(db: AsyncSession):
    repository = AuthRepository(db)
    return AuthService(repository)


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(data: RegisterRequest,db: AsyncSession = Depends(get_db)):
    service = get_auth_service(db)
    user = await service.register(data)
    return {
        "id": str(user.id),
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest,db: AsyncSession = Depends(get_db)):
    service = get_auth_service(db)
    return await service.login(data)

@router.get("/me", response_model=UserResponse)
async def get_my_profile(current_user=Depends(get_current_user)):
    return {
        "id": str(current_user.id),
        "full_name": current_user.full_name,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active
    }