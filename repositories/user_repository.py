from fastapi import HTTPException
from typing import Optional
from sqlalchemy.orm import Session
from models.user import User, UserCreate
from core.app_settings import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from core.database import get_engine

settings = get_settings()
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class UserRepository:
    def __init__(self):
        self.session = SessionLocal()

    def close(self):
        self.session.close()

    def find_by_user_name(self, user_name: str) -> Optional[User]:
        query = text('SELECT id_user, user_name, user_password FROM users WHERE user_name = :user_name')
        cursor = self.session.execute(query, {"user_name": user_name})
        row = cursor.fetchone()
        if row:
            return User(id=row[0], user_name= row[1], user_password=row[2])
        return None

    def create_user(self, user: UserCreate) -> UserCreate:
        query = text('INSERT INTO users (user_name, user_password) VALUES (:user_name, :user_password)')
        try:
            self.session.execute(query, {"user_name": user.user_name, "user_password": user.user_password})
            self.session.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal error in db")
        return user

    def get_role_in_club(self, user_id: int, club_id: int):
        query = text('SELECT id_role FROM participant_role_club WHERE id_user = :user_id AND id_club = :club_id')
        cursor = self.session.execute(query, {"user_id": user_id, "club_id": club_id})
        row = cursor.fetchone()
        return row[0] if row else None
