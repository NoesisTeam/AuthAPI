from fastapi import Depends, HTTPException, status
from models.user import User, TokenData, UserCreate
from typing import Optional
from repositories.user_repository import UserRepository
from core.security import hash_password, verify_password
from datetime import datetime, timedelta, timezone
from core import app_settings
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer

settings = app_settings.get_settings()

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="access_token")

def create_club_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

class AuthenticationService:
    def __init__(self):
        self.user_repository = UserRepository()

    def authenticate_user(self, user_name: str, password: str) -> Optional[User]:
        user = self.user_repository.find_by_user_name(user_name)
        if user and verify_password(password, user.user_password):
            return user
        return None

    def register_user(self, user: UserCreate) -> UserCreate:
        user.user_password = hash_password(user.user_password)
        return self.user_repository.create_user(user)

    def get_role_id_in_club_by_user_name(self, user_name: str, club_id: int):
        user = self.user_repository.find_by_user_name(user_name)
        return self.user_repository.get_role_id_in_club(user.id, club_id)

    def get_role_name_in_club_by_id(self, id_user: int, club_id: int):
        return self.user_repository.get_role_name_in_club(id_user, club_id)

    def find_by_user_name(self, user_name):
        return self.user_repository.find_by_user_name(user_name)



