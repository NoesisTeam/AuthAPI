from typing import Optional

from pydantic import BaseModel

class User(BaseModel):
    user_name: str
    password: str

class TokenData(BaseModel):
    user_id: str
    club_id: int
