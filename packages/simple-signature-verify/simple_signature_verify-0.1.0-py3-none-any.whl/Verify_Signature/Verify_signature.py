import base64
import hashlib
import hmac

class PaymentSDK:
    def __init__(self, client_id, client_secret, merchant_id):
        if not all(isinstance(i, str) for i in [client_id, client_secret, merchant_id]):
            raise TypeError("client_id, client_secret, and merchant_id must all be strings.")
        self.client_id = client_id
        self.client_secret = client_secret
        self.merchant_id = merchant_id

    def generate_hmac_sha256(self, message, secret):
        secret_bytes = secret.encode('utf-8')
        message_bytes = message.encode('utf-8')
        hmac_instance = hmac.new(secret_bytes, message_bytes, hashlib.sha256)
        signature = base64.b64encode(hmac_instance.digest()).decode('utf-8')
        return signature

    def verify_signature(self, body, secret, signature):
        if not all(isinstance(i, str) for i in [body, secret, signature]):
            raise TypeError("body, secret, and signature must all be strings.")
        if secret != self.client_secret:
            raise ValueError("Provided secret does not match the initialized client secret.")
        expected_signature = self.generate_hmac_sha256(body, secret)
        return "Yes" if hmac.compare_digest(signature, expected_signature) else "No"
