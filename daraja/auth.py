import requests
import base64
from datetime import datetime


class MpesaAuth:
    SANDBOX_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    PRODUCTION_URL = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    def __init__(self, consumer_key: str, consumer_secret: str, environment: str = "sandbox"):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.base_url = self.SANDBOX_URL if environment == "sandbox" else self.PRODUCTION_URL

    def get_access_token(self) -> str:
        credentials = base64.b64encode(f"{self.consumer_key}:{self.consumer_secret}".encode()).decode()
        response = requests.get(
            self.base_url,
            headers={"Authorization": f"Basic {credentials}"}
        )
        response.raise_for_status()
        return response.json()["access_token"]

    @staticmethod
    def generate_password(shortcode: str, passkey: str) -> tuple:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        raw = f"{shortcode}{passkey}{timestamp}"
        password = base64.b64encode(raw.encode()).decode()
        return password, timestamp
