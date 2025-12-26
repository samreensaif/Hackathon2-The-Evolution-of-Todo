from datetime import timedelta
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from passlib.context import CryptContext
from sqlmodel import Session, select

from todo.auth import create_access_token
from todo.db import engine
from todo.models import User

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(user_in: dict) -> Any:
    email = user_in.get("email")
    password = user_in.get("password")
    name = user_in.get("name")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    with Session(engine) as session:
        # Check if user already exists
        statement = select(User).where(User.email == email)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise HTTPException(status_code=409, detail="User already exists")

        user = User(
            email=email,
            password_hash=get_password_hash(password),
            name=name
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"id": user.id, "email": user.email, "name": user.name}

@router.post("/auth/login")
def login(credentials: dict) -> Any:
    email = credentials.get("email")
    password = credentials.get("password")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if not user or not user.password_hash or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = create_access_token(data={"sub": str(user.id), "email": user.email})
        return {
            "accessToken": access_token,
            "tokenType": "bearer",
            "user": {"id": user.id, "email": user.email, "name": user.name}
        }
