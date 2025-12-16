import os
import uuid
from datetime import datetime
from lago_python_client.client import Client
from lago_python_client.exceptions import LagoApiError
from lago_python_client.models import Customer, Wallet, Subscription, Event
from fastapi import HTTPException

client = Client(
    api_url=os.getenv("LAGO_BACKEND_URL"),
    api_key=os.getenv("LAGO_API_KEY")
)

PLAN_CODE = os.getenv("LAGO_PLAN_CODE")
BILLABLE_METRIC_CODE = os.getenv("LAGO_BILLABLE_METRIC_CODE")

def create_customer(id: str, email: str, currency: str = "IDR"):

    print(os.getenv("LAGO_API_URL"))
    customer = Customer(
        external_id=id,
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

def create_subscription(customer_id: str, subscription_id: str):
    subscription = Subscription(
        external_customer_id=customer_id,
        plan_code=PLAN_CODE,
        external_id=subscription_id,
    )
    
    try:
        return client.subscriptions.create(subscription)
    except LagoApiError as e:
        # Log error untuk debugging
        print(f"Lago API Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def create_wallet(customer_id: str):
    wallet = Wallet(
        name='API Credits',
        rate_amount='1',
        currency='IDR',
        external_customer_id=customer_id
    )
    try:
        return client.wallets.create(wallet)
    except LagoApiError as e:
        # Log error untuk debugging
        print(f"Lago API Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def send_event(subscription_id: str):


    print(subscription_id)
    print(BILLABLE_METRIC_CODE)
    print(int(datetime.now().timestamp()))
    event = Event(
        transaction_id=str(uuid.uuid4()),
        external_subscription_id=subscription_id,
        code=BILLABLE_METRIC_CODE,
        timestamp=int(datetime.now().timestamp()),
    )
    
    try:
        return client.events.create(event)
    except LagoApiError as e:
        # Log error untuk debugging
        print(f"Lago API Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

def check_credits(subscription_id: str):
    wallet = client.wallets.find(subscription_id)
    return wallet