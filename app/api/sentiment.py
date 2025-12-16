from fastapi import APIRouter, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.user import User
from app.services.sentiment import analyze_sentiment
# from app.services.billing import track_usage

router = APIRouter()

def get_user_by_api_key(db: Session, api_key: str):
    return db.query(User).filter(User.api_key == api_key).first()

@router.post("/sentiment")
def sentiment_api(
    payload: dict,
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    user = get_user_by_api_key(db, x_api_key)
    if not user:
        raise HTTPException(401, "invalid API key")

    text = payload.get("text")
    if not text:
        raise HTTPException(400, "text is required")

    result = analyze_sentiment(text)

    # track_usage(
    #     api_key=x_api_key,
    #     event_name="sentiment_call",
    #     quantity=1
    # )

    return result
