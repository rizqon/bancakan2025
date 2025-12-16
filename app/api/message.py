from fastapi import APIRouter, Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.models.user import User
from app.services.whatsapp import send_whatsapp_message
from app.services.lago import send_event, check_credits

router = APIRouter()

def get_user_by_api_key(db: Session, api_key: str):
    """
    Mengambil user dari database berdasarkan API key.

    Args:
        db (Session): Session database.
        api_key (str): API key milik user.

    Returns:
        User: Instance user jika ditemukan, None jika tidak ditemukan.
    """
    return db.query(User).filter(User.api_key == api_key).first()

@router.post(
    "/message",
    summary="Kirim pesan WhatsApp",
    response_description="Hasil pengiriman pesan"
)
def message_api(
    payload: dict, 
    x_api_key: str = Header(..., description="API Key untuk autentikasi"), 
    db: Session = Depends(get_db)
):
    """
    Mengirim pesan WhatsApp ke nomor tertentu.

    ## Body Request
    - **phone_number**: str - Nomor tujuan.
    - **message**: str - Pesan yang ingin dikirim.

    ## Header
    - **x-api-key**: str - API Key user untuk autentikasi.

    ## Response
    - **200**: Pesan berhasil dikirim.
    - **401**: API key tidak valid.
    - **400**: Request tidak valid atau kredit tidak cukup.

    ## Alur Proses
    1. Memvalidasi API key dan input.
    2. Mengecek saldo kredit pengguna.
    3. Mengirim pesan WhatsApp.
    4. Mengirim event ke subscription.

    Returns:
        dict: Hasil kirim pesan.
    """
    user = get_user_by_api_key(db, x_api_key)
    if not user:
        raise HTTPException(401, "invalid API key")

    phone_number = payload.get("phone_number")
    message = payload.get("message")
    if not phone_number or not message:
        raise HTTPException(400, "phone_number & message are required")

    # Mengecek apakah user memiliki kredit cukup
    credits = check_credits(user.wallet_id)
    if not credits:
        raise HTTPException(400, "no credits available")

    if float(credits.credits_balance) < 100:
        raise HTTPException(400, "insufficient credits, please top up your credits")

    # Kirim pesan WhatsApp
    result = send_whatsapp_message(phone_number, message)

    # Kirim event ke subscription
    send_event(user.subscription_id)

    return result

@router.get(
    "/check-credits",
    summary="Cek jumlah kredit",
    response_description="Jumlah kredit yang tersedia"
)
def check_credits_api(
    x_api_key: str = Header(..., description="API Key untuk autentikasi"), 
    db: Session = Depends(get_db)
):
    """
    Mengecek jumlah kredit yang dimiliki user.

    ## Header
    - **x-api-key**: str - API Key user untuk autentikasi.

    ## Response
    - **200**: Berhasil, mengembalikan jumlah kredit.
    - **401**: API key tidak valid.
    - **400**: Kredit tidak tersedia.

    Returns:
        dict: Informasi kredit.
    """
    user = get_user_by_api_key(db, x_api_key)
    if not user:
        raise HTTPException(401, "invalid API key")

    credits = check_credits(user.wallet_id)
    if not credits:
        raise HTTPException(400, "no credits available")

    return {
        "message": "credits checked",
        "credits": float(credits.credits_balance)
    }