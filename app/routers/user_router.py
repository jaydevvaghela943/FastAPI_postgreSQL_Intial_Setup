import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.connection import get_db

from app.schemas.auth_schema import UserResponse
from app.schemas.user_schema import (
    AdminCreateUserRequest,
    UserStatusUpdate
)

from app.repositories.user_repository import UserRepository
from app.repositories.auth_repository import AuthRepository

from app.services.user_service import UserService
from app.dependencies.auth_dependencies import get_current_admin

router = APIRouter(prefix="/api/v1/users",tags=["User Management"])

def get_user_service(db: AsyncSession):
    user_repository = UserRepository(db)
    auth_repository = AuthRepository(db)

    return UserService(user_repository,auth_repository)

@router.get("/", response_model=list[UserResponse])
async def get_users(db: AsyncSession = Depends(get_db),admin=Depends(get_current_admin)):
    service = get_user_service(db)
    return await service.get_all_users()


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(data: AdminCreateUserRequest,db: AsyncSession = Depends(get_db),admin=Depends(get_current_admin)):
    service = get_user_service(db)
    user = await service.create_user(data)

    return {
        "id": str(user.id),
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }


@router.patch("/{user_id}/status", response_model=UserResponse)
async def update_user_status(user_id: uuid.UUID,data: UserStatusUpdate,db: AsyncSession = Depends(get_db),admin=Depends(get_current_admin)):
    service = get_user_service(db)
    user = await service.update_user_status(
        user_id,
        data.is_active,
        admin
    )

    return {
        "id": str(user.id),
        "full_name": user.full_name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }