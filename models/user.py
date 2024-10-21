from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(60), unique=True, index=True)
    user_password = Column(String(255))

class UserCreate(BaseModel):
    user_name: str
    user_password: str

class TokenData(BaseModel):
    user_id: str
    club_id: int
