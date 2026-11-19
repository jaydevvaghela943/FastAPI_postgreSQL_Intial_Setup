import asyncio
import getpass

from sqlalchemy import select

from app.database.connection import (
    engine,
    AsyncSessionLocal
)

from app.database.base import Base
from app.models import User

from app.core.security import hash_password


async def create_admin():

    print("\nCreate Initial Admin Account\n")

    full_name = input("Full Name: ").strip()
    email = input("Email: ").strip().lower()

    password = getpass.getpass("Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")

    if not full_name or not email:
        print("Name and email are required.")
        return

    if len(password) < 8:
        print("Password must have at least 8 characters.")
        return

    if password != confirm_password:
        print("Passwords do not match.")
        return

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.email == email)
        )

        existing_user = result.scalar_one_or_none()
        if existing_user:

            print("This email already exists.")
            return

        admin = User(
            full_name=full_name,
            email=email,
            password_hash=hash_password(password),
            role="admin",
            is_active=True
        )

        db.add(admin)
        await db.commit()
        print("\nAdmin account created successfully!")

    await engine.dispose()

async def main():

    try:
        await create_admin()
    finally:
        await engine.dispose()

if __name__ == "__main__":
     asyncio.run(main())