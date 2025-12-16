from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Customer
from fastapi import HTTPException

client = Client(
    api_url="http://lago-api:3000",
    api_key="8ab36d9b-a2c7-44e5-9abd-44211e9886d1"
)

def create_customer(id: int, email: str, currency: str = "IDR"):

    customer = Customer(
        external_id=str(id),
        name=email,
        email=email,
        currency=currency,
        timezone="Asia/Jakarta"
    )

    try:
        return client.customers.create(customer)
    except LagoApiError as e:
        # Log error untuk debugging
        print(f"Lago API Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))