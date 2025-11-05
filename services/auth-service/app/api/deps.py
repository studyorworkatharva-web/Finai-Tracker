"""
Dependencies for authentication and database session management.
Ensures that only authenticated users can access protected routes.
"""

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import oauth2_scheme, decode_token
from app.crud.user import get_user
from app.db.models.user import User


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    Validates the provided JWT access token and returns the associated user.
    If the token is invalid or expired, raises a 401 Unauthorized error.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Decode the JWT and extract user ID
    token_data = decode_token(token)
    if not token_data or not getattr(token_data, "user_id", None):
        raise credentials_exception

    # Fetch the user from the database
    user = get_user(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception

    return user
