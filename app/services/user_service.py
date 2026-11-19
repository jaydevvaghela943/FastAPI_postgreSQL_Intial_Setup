from fastapi import HTTPException, status

from app.models.user import User

from app.core.security import hash_password

from app.repositories.user_repository import UserRepository
from app.repositories.auth_repository import AuthRepository

class UserService:
    def __init__(
        self,
        user_repository: UserRepository,
        auth_repository: AuthRepository
    ):

        self.user_repository = user_repository
        self.auth_repository = auth_repository

    async def create_user(self, data):
        existing = await self.auth_repository.get_user_by_email(str(data.email))
        if existing:
            raise HTTPException(status_code=409,detail="Email already registered")

        user = User(
            full_name=data.full_name,
            email=str(data.email).lower(),
            password_hash=hash_password(data.password),
            role=data.role,
            is_active=True
        )

        return await self.auth_repository.create_user(user)

    async def get_all_users(self):
        return await self.user_repository.get_all_users()

    async def update_user_status(self,user_id,is_active: bool,current_user):
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404,detail="User not found")

        if user.id == current_user.id and not is_active:
            raise HTTPException(status_code=400,detail="You cannot deactivate your own account")

        return await self.user_repository.update_user_status(user,is_active)