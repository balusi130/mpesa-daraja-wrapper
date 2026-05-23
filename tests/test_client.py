import pytest
from unittest.mock import patch, MagicMock
from daraja.client import MpesaClient
from daraja.auth import MpesaAuth


def test_generate_password_returns_tuple():
    password, timestamp = MpesaAuth.generate_password("174379", "test_passkey")
    assert isinstance(password, str)
    assert isinstance(timestamp, str)
    assert len(timestamp) == 14  # YYYYMMDDHHmmss


def test_generate_password_is_base64():
    import base64
    password, timestamp = MpesaAuth.generate_password("174379", "test_passkey")
    # Should decode without error
    decoded = base64.b64decode(password).decode()
    assert "174379" in decoded


@patch("daraja.auth.requests.get")
def test_get_access_token(mock_get):
    mock_get.return_value.json.return_value = {"access_token": "test_token_123"}
    auth = MpesaAuth("key", "secret", "sandbox")
    token = auth.get_access_token()
    assert token == "test_token_123"


@patch("daraja.client.requests.post")
def test_stk_push_calls_correct_endpoint(mock_post):
    mock_post.return_value.json.return_value = {"ResponseCode": "0"}
    mock_post.return_value.raise_for_status = MagicMock()

    with patch.object(MpesaAuth, "get_access_token", return_value="fake_token"):
        client = MpesaClient("key", "secret", "sandbox", shortcode="174379", passkey="passkey")
        response = client.stk_push(
            phone_number="254712345678",
            amount=100,
            account_reference="Test",
            description="Test payment",
            callback_url="https://example.com/callback"
        )

    assert mock_post.called
    assert "stkpush" in mock_post.call_args[0][0]
