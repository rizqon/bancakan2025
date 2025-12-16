from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.services.auth import register_user, authenticate_user, update_user_wallet
from app.services.lago import create_customer, create_wallet, create_subscription

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register",
    summary="Register a new user",
    response_description="Registration status"
)
def register(payload: dict, db: Session = Depends(get_db)):
    """
    Register a new user.

    ### Request Body
    - **email**: str - Email address of the user.
    - **password**: str - Password for the account.

    ### Responses
    - **200**: User registered successfully.
    - **400**: If request is invalid or user already exists or registration components fail.

    ### Process
    1. Registers the user in the database.
    2. Creates payment customer via Lago.
    3. Creates a wallet for the user in Lago.
    4. Creates a subscription in Lago.
    5. Updates user's wallet info in database.

    Returns a success message if everything succeeded.
    """
    email = payload.get("email")
    password = payload.get("password")

    if not email or not password:
        raise HTTPException(400, "email & password required")

    # REGISTER USER
    user = register_user(db, email, password)
    if not user:
        raise HTTPException(400, "user already exists")

    # CREATE CUSTOMER
    customer = create_customer(user.id, user.email, "IDR")
    if not customer:
        raise HTTPException(400, "failed to create customer")

    # CREATE WALLET
    wallet = create_wallet(user.id)
    if not wallet:
        raise HTTPException(400, "failed to create wallet")

    # CREATE SUBSCRIPTION
    subscription = create_subscription(user.id, user.subscription_id)
    if not subscription:
        raise HTTPException(400, "failed to create subscription")

    # UPDATE USER
    user = update_user_wallet(db, user.id, wallet.lago_id)
    if not user:
        raise HTTPException(400, "failed to update user")

    return {
        "message": "registered",
    }

@router.post(
    "/login",
    summary="Login and obtain an API key",
    response_description="Login status and api_key"
)
def login(payload: dict, db: Session = Depends(get_db)):
    """
    Authenticate a user and retrieve API key.

    ### Request Body
    - **email**: str - User's email.
    - **password**: str - User's password.

    ### Responses
    - **200**: Success, returns API key for authentication.
    - **401**: Invalid credentials.
    """
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
