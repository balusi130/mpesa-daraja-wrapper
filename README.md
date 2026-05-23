# mpesa-daraja-wrapper

A Python wrapper for the Safaricom Daraja API that makes M-Pesa integration straightforward. The official Daraja docs are decent but there is a lot of boilerplate involved in every call — token generation, base64 encoding, timestamp formatting, callback handling. This package takes care of all of that so you can focus on the actual logic.

Built this while working on fintech systems at Safaricom. The STK Push flow in particular has a lot of moving parts that are easy to get wrong the first time, so having a tested wrapper saves a lot of debugging.

---

## Supported endpoints

- **STK Push (Lipa na M-Pesa Online)** — trigger a payment prompt on a customer's phone
- **STK Push Query** — check the status of an STK Push request
- **B2C (Business to Customer)** — send money from a business shortcode to a phone number
- **C2B Register URLs** — register your confirmation and validation callback URLs
- **Transaction Status** — query the status of any M-Pesa transaction
- **Account Balance** — check your shortcode balance

---

## Installation

```bash
pip install mpesa-daraja-wrapper
```

Or from source:

```bash
git clone https://github.com/balusi130/mpesa-daraja-wrapper.git
cd mpesa-daraja-wrapper
pip install -e .
```

---

## Quick start

```python
from daraja import MpesaClient

client = MpesaClient(
    consumer_key="your_consumer_key",
    consumer_secret="your_consumer_secret",
    environment="sandbox"  # or "production"
)

# Trigger STK Push
response = client.stk_push(
    phone_number="254712345678",
    amount=100,
    account_reference="Order001",
    description="Payment for order 001",
    callback_url="https://yourapp.com/mpesa/callback"
)

print(response)
# {'MerchantRequestID': '...', 'CheckoutRequestID': '...', 'ResponseCode': '0', ...}
```

---

## B2C example

```python
response = client.b2c(
    phone_number="254712345678",
    amount=500,
    command_id="BusinessPayment",
    remarks="Salary payment",
    queue_timeout_url="https://yourapp.com/mpesa/timeout",
    result_url="https://yourapp.com/mpesa/result"
)
```

---

## Configuration

| Parameter | Description |
|-----------|-------------|
| `consumer_key` | From your Daraja app |
| `consumer_secret` | From your Daraja app |
| `environment` | `"sandbox"` or `"production"` |
| `shortcode` | Your business shortcode (optional, can pass per-call) |
| `passkey` | Your Lipa na M-Pesa passkey (required for STK Push) |

---

## Project structure

```
mpesa-daraja-wrapper/
├── daraja/
│   ├── __init__.py
│   ├── client.py         # Main MpesaClient class
│   ├── auth.py           # Token generation
│   ├── stk_push.py
│   ├── b2c.py
│   ├── c2b.py
│   └── transaction_status.py
├── tests/
│   └── test_client.py
├── examples/
│   └── stk_push_example.py
├── requirements.txt
├── setup.py
└── README.md
```

---

## Running tests

```bash
pytest tests/ -v
```

Tests use the sandbox environment. Set `MPESA_CONSUMER_KEY` and `MPESA_CONSUMER_SECRET` as environment variables before running.

---

## Notes

- All phone numbers should be in the format `254XXXXXXXXX` (no `+`, no leading `0`)
- The sandbox environment uses test credentials from the Daraja developer portal
- Callback URLs must be publicly accessible HTTPS endpoints (use ngrok for local development)

---

MIT License