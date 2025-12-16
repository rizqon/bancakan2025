from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.message import router as message_router
from app.core.init_db import init_db

app = FastAPI(title="API Billing Demo")

init_db()

@app.get("/")
def read_root():
    return {"message": "Hello, World"}

app.include_router(auth_router)
app.include_router(message_router, prefix="/v1")
