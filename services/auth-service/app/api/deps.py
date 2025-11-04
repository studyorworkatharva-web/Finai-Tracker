from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import oauth2_scheme, decode_token
from app.crud.user import get_user
from app.schemas.token import TokenData
from app.db.models.user import User

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = decode_token(token)
    if token_data is None or token_data.user_id is None:
        raise credentials_exception
        
    user = get_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return user