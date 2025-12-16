from sqlalchemy import Column, Integer, String
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    api_key = Column(String, unique=True, index=True, nullable=False)
    subscription_id = Column(String, unique=True, index=True, nullable=False)
    wallet_id = Column(String, unique=True, index=True, nullable=True)
