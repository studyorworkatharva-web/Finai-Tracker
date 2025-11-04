from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserCreate, UserPublic
from app.schemas.token import Token
from app.crud import user as crud_user
from app.core.security import create_access_token, create_refresh_token, verify_password, decode_token
from app.api.deps import get_current_user
from app.db.models.user import User

router = APIRouter()

@router.post("/signup", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return crud_user.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token_data = {"sub": str(user.id)}
    access_token = create_access_token(data=token_data)
    refresh_token = create_refresh_token(data=token_data)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    token_data = decode_token(refresh_token)
    if not token_data or not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user = crud_user.get_user(db, user_id=token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
        
    new_token_data = {"sub": str(user.id)}
    new_access_token = create_access_token(data=new_token_data)
    new_refresh_token = create_refresh_token(data=new_token_data)
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }