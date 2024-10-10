from jose import jwt
from fastapi import HTTPException, status, Cookie
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")  # Secret key để verify token

# Hàm verify token
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Hàm protect để kiểm tra token trong headers hoặc cookies
async def protect(jwt_cookie: Optional[str] = Cookie(None), authorization: Optional[str] = None):
    token = None

    if jwt_cookie:
        token = jwt_cookie
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verify token
    return verify_token(token)
