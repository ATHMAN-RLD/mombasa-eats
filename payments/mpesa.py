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