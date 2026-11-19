from fastapi import HTTPException, status
from app.models.user import User
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from app.repositories.auth_repository import AuthRepository
from app.core.config import settings


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    async def register(self, data):
        existing_user = await self.repository.get_user_by_email(
            str(data.email)
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        user = User(
            full_name=data.full_name,
            email=str(data.email).lower(),
            password_hash=hash_password(data.password),
            role="user",
            is_active=True
        )

        return await self.repository.create_user(user)

    async def login(self, data):
        user = await self.repository.get_user_by_email(
            str(data.email)
        )

        if not user or not verify_password(data.password,user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
                headers={"WWW-Authenticate": "Bearer"}
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your account is inactive"
            )

        token = create_access_token(user.id)

        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_in": (
                settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
        }

    async def get_profile(self, user):
        return user