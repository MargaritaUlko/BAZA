from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, exceptions, models, schemas
from passlib.context import CryptContext

from database import User, get_user_db

crypt_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    return crypt_context.hash(password)

def verify_password(password_to_check: str, stored_hash: str) -> bool:
    try:
        print(password_to_check)
        print(stored_hash)

        if crypt_context.verify(password_to_check, stored_hash):
            print('BEBRA!!!')
        return crypt_context.verify(password_to_check, stored_hash)

    except Exception as e:
        print(f"Error verifying password: {e}")
        return False

class UserManager(BaseUserManager[User, int]):
    async def authenticate(self, email: str, password: str) -> Optional[User]:
        user = await self.get_by_email(email)
        if user is None:
            return None
        # if crypt_context.verify(password, user.hashed_password):
        if verify_password(password, user.hashed_password):
            print(password)
            print(user.hashed_password)
            return user

        return None

    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = hash_password(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)
        await self.on_after_register(created_user, request)

        return created_user

def get_user_manager(user_db=Depends(get_user_db)):
    return UserManager(user_db)
