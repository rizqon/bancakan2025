import secrets
import bcrypt
import uuid
from sqlalchemy.orm import Session
from app.models.user import User

def hash_password(password: str) -> str:
    # Encode password ke bytes dan hash
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

def generate_api_key() -> str:
    return secrets.token_hex(24)

def register_user(db: Session, email: str, password: str):
    if db.query(User).filter(User.email == email).first():
        return None

    user = User(
        id=str(uuid.uuid4()),
        email=email,
        password=hash_password(password),
        api_key=generate_api_key(),
        subscription_id=str(uuid.uuid4())
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def update_user_wallet(db: Session, user_id: str, wallet_id: str):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    user.wallet_id = wallet_id

    db.commit()
    db.refresh(user)

    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if not verify_password(password, user.password):
        return None

    return user.api_key
