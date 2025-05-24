import paystackapi

class PaystackClient:
    def __init__(self):
        self.secret_key = "sk_test_20019f453606ecf4a2c90bb9b75548e087e714c5"
        self.api = paystackapi.Paystack(secret_key=self.secret_key)