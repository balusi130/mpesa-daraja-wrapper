import os
from dotenv import load_dotenv
from daraja import MpesaClient

load_dotenv()

client = MpesaClient(
    consumer_key=os.getenv("MPESA_CONSUMER_KEY"),
    consumer_secret=os.getenv("MPESA_CONSUMER_SECRET"),
    environment=os.getenv("MPESA_ENV", "sandbox"),
    shortcode=os.getenv("MPESA_SHORTCODE"),
    passkey=os.getenv("MPESA_PASSKEY")
)

# Trigger STK Push
response = client.stk_push(
    phone_number="254712345678",
    amount=1,
    account_reference="TestOrder001",
    description="Test payment via daraja wrapper",
    callback_url="https://yourapp.com/mpesa/callback"
)

print("STK Push response:", response)

checkout_id = response.get("CheckoutRequestID")
if checkout_id:
    status = client.stk_query(checkout_id)
    print("Payment status:", status)
