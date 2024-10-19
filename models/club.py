from pydantic import BaseModel

class Club(BaseModel):
    id: int
    name: str