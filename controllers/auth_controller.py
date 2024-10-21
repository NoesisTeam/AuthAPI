from fastapi import APIRouter, HTTPException

from models.user import UserCreate, TokenData
from services.auth_service import AuthenticationService, create_club_token

router = APIRouter()

auth_service = AuthenticationService()


@router.post("/register")
async def register_user(user: UserCreate):
    return auth_service.register_user(user)


@router.get("/hola")
async def hello():
    return "Hola!"


@router.post("/login")
async def login(credentials: UserCreate):
    user = auth_service.authenticate_user(credentials.user_name, credentials.user_password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "user": user}


@router.post("/token_club")
async def token_club(token_data: TokenData):
    role_id = auth_service.get_role_in_club(token_data.user_id, token_data.club_id)
    participant_data = {"user": token_data.user_id,
                        "role": role_id,
                        "club": token_data.club_id}
    access_token = create_club_token(data=participant_data)
    return {"access_token": access_token, "token_type": "bearer"}
