import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings

MPESA_AUTH_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"


def get_access_token():
    response = requests.get(
        MPESA_AUTH_URL,
        auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET),
    )
    response.raise_for_status()
    data = response.json()
    return data["access_token"]  

import base64
from datetime import datetime

MPESA_STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"


def generate_password(timestamp):
    raw = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
    return base64.b64encode(raw.encode()).decode()


def initiate_stk_push(phone_number, amount, account_reference, callback_url):
    access_token = get_access_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = generate_password(timestamp)

    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": account_reference,
        "TransactionDesc": "Mombasa Eats order payment",
    }

    response = requests.post(MPESA_STK_PUSH_URL, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()  