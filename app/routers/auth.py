from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.dependencies import DbSession
from app.models import User
from app.schemas import (
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse,
)
from app.security import (
    hash_password,
    verify_password,
    create_access_token,
)

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(data: RegisterRequest, db: DbSession):
    email = str(data.email).lower()

    existing = db.scalar(
        select(User).where(User.email == email)
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        name=data.name,
        email=email,
        hashed_password=hash_password(data.password),
        role=data.role,
        is_active=True,
    )

    db.add(user)

    try:
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(data: LoginRequest, db: DbSession):
    email = str(data.email).lower()

    user = db.scalar(
        select(User).where(User.email == email)
    )

    if (
        not user
        or not verify_password(data.password, user.hashed_password)
        or not user.is_active
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
    }