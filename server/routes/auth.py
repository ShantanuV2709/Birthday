import os
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from auth_utils import create_access_token, verify_password, get_password_hash
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    # Check against hardcoded credentials in .env
    admin_1 = os.getenv("ADMIN_USER_1")
    pass_1 = os.getenv("ADMIN_PASS_1")
    admin_2 = os.getenv("ADMIN_USER_2")
    pass_2 = os.getenv("ADMIN_PASS_2")
    
    # Simple check for demo purposes. 
    # In production, password hashes would be compared using auth_utils.verify_password
    if (request.username == admin_1 and request.password == pass_1) or \
       (request.username == admin_2 and request.password == pass_2):
        access_token = create_access_token(data={"sub": request.username})
        return {"access_token": access_token, "token_type": "bearer"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
