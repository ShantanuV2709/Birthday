from fastapi import Request, HTTPException, status
from jose import JWTError, jwt
import os

SECRET_KEY = os.getenv("JWT_SECRET", "secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

async def auth_middleware(request: Request, call_next):
    # Only protect /api/guests (GET) and /api/expenditure
    # Allow /api/guests (POST) and /api/auth/login
    
    path = request.url.path
    method = request.method
    
    protected_routes = [
        ("/api/guests", "GET"),
        ("/api/expenditure", "GET")
    ]
    
    is_protected = False
    for route_path, route_method in protected_routes:
        if path.startswith(route_path) and method == route_method:
            is_protected = True
            break
            
    if is_protected:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            
    response = await call_next(request)
    return response
