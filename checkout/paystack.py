import paystackapi

class PaystackClient:
    def __init__(self):
        self.secret_key = "sk_test_b437a50bcfe02ae4d9b33baac55f90bae488b92b"
        self.api = paystackapi.Paystack(secret_key=self.secret_key)