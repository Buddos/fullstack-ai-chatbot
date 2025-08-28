from datetime import datetime, timedelta
from uuid import uuid4
from fastapi import Query, HTTPException, status

# ✅ In-memory token storage
tokens = {}

def create_token(expiration_minutes: int = 5) -> str:
    """
    Create a new token with expiration time.
    """
    token = str(uuid4())
    expire_time = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    tokens[token] = expire_time
    return token

def verify_token(token: str) -> bool:
    """
    Verify if token exists and has not expired.
    """
    if token not in tokens:
        return False
    if datetime.utcnow() > tokens[token]:
        # remove expired token
        del tokens[token]
        return False
    return True

def get_token(token: str = Query(...)) -> str:
    """
    FastAPI dependency that validates tokens automatically.
    """
    if not verify_token(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return token

