from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.services.auth import register_user, authenticate_user
from app.services.lago import create_customer

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
def register(payload: dict, db: Session = Depends(get_db)):
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        raise HTTPException(400, "email & password required")

    user = register_user(db, email, password)
    if not user:
        raise HTTPException(400, "user already exists")

    customer = create_customer(user.id, user.email, "IDR")
    if not customer:
        raise HTTPException(400, "failed to create customer")

    return {
        "message": "registered",
    }

@router.post("/login")
def login(payload: dict, db: Session = Depends(get_db)):
    api_key = authenticate_user(
        db,
        payload.get("email"),
        payload.get("password")
    )

    if not api_key:
        raise HTTPException(401, "invalid credentials")

    return {
        "message": "logged in",
        "api_key": api_key
    }
