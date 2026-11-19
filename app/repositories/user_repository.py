from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_users(self):
        result = await self.db.execute(
            select(User).order_by(User.created_at.desc())
        )

        return result.scalars().all()

    async def get_user_by_id(self, user_id):
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def update_user_status(self,user: User,is_active: bool):
        user.is_active = is_active
        await self.db.commit()
        await self.db.refresh(user)
        return user
    