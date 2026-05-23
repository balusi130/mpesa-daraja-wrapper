import requests
from daraja.auth import MpesaAuth


class MpesaClient:
    SANDBOX_BASE = "https://sandbox.safaricom.co.ke"
    PRODUCTION_BASE = "https://api.safaricom.co.ke"

    def __init__(self, consumer_key: str, consumer_secret: str, environment: str = "sandbox",
                 shortcode: str = None, passkey: str = None):
        self.auth = MpesaAuth(consumer_key, consumer_secret, environment)
        self.base_url = self.SANDBOX_BASE if environment == "sandbox" else self.PRODUCTION_BASE
        self.shortcode = shortcode
        self.passkey = passkey

    def _headers(self):
        token = self.auth.get_access_token()
        return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    def stk_push(self, phone_number: str, amount: int, account_reference: str,
                 description: str, callback_url: str, shortcode: str = None, passkey: str = None) -> dict:
        sc = shortcode or self.shortcode
        pk = passkey or self.passkey
        password, timestamp = MpesaAuth.generate_password(sc, pk)

        payload = {
            "BusinessShortCode": sc,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": sc,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": account_reference,
            "TransactionDesc": description
        }

        response = requests.post(
            f"{self.base_url}/mpesa/stkpush/v1/processrequest",
            json=payload, headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def stk_query(self, checkout_request_id: str, shortcode: str = None, passkey: str = None) -> dict:
        """Check the status of an STK Push request."""
        sc = shortcode or self.shortcode
        pk = passkey or self.passkey
        password, timestamp = MpesaAuth.generate_password(sc, pk)

        payload = {
            "BusinessShortCode": sc,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }

        response = requests.post(
            f"{self.base_url}/mpesa/stkpushquery/v1/query",
            json=payload, headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def b2c(self, phone_number: str, amount: int, command_id: str,
            remarks: str, queue_timeout_url: str, result_url: str,
            shortcode: str = None) -> dict:
        payload = {
            "InitiatorName": "apiop2",
            "SecurityCredential": "",
            "CommandID": command_id,
            "Amount": amount,
            "PartyA": shortcode or self.shortcode,
            "PartyB": phone_number,
            "Remarks": remarks,
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url,
            "Occasion": ""
        }

        response = requests.post(
            f"{self.base_url}/mpesa/b2c/v1/paymentrequest",
            json=payload, headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def transaction_status(self, transaction_id: str, shortcode: str = None) -> dict:
        payload = {
            "Initiator": "apiop2",
            "SecurityCredential": "",
            "CommandID": "TransactionStatusQuery",
            "TransactionID": transaction_id,
            "PartyA": shortcode or self.shortcode,
            "IdentifierType": "4",
            "ResultURL": "",
            "QueueTimeOutURL": "",
            "Remarks": "status check",
            "Occasion": ""
        }

        response = requests.post(
            f"{self.base_url}/mpesa/transactionstatus/v1/query",
            json=payload, headers=self._headers()
        )
        response.raise_for_status()
        return response.json()

    def account_balance(self, queue_timeout_url: str, result_url: str, shortcode: str = None) -> dict:
        """Query the balance of a shortcode."""
        payload = {
            "Initiator": "apiop2",
            "SecurityCredential": "",
            "CommandID": "AccountBalance",
            "PartyA": shortcode or self.shortcode,
            "IdentifierType": "4",
            "Remarks": "balance check",
            "QueueTimeOutURL": queue_timeout_url,
            "ResultURL": result_url
        }

        response = requests.post(
            f"{self.base_url}/mpesa/accountbalance/v1/query",
            json=payload, headers=self._headers()
        )
        response.raise_for_status()
        return response.json()
