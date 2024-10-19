from typing import Optional

from pydantic import BaseModel

class User(BaseModel):
    user_name: str
    password: str

class TokenData(BaseModel):
    user_name: Optional[str] = None
    role_id: Optional[str] = None
    club_id: Optional[str] = None
