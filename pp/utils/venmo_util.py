import requests, urllib
from .. import config

class VenmoAPI:
    def __init__(self):
        self.venmo_endpoint = config.venmo_endpoint
        self.client_id = config.venmo_client_id
        self.client_secret = config.venmo_client_secret
        self.auth_scope = config.venmo_auth_scope

    def get_request_url(self, request_endpoint, request_args=None):
        if request_args != None:
            args_encoded = "?" + urllib.urlencode(request_args)
        else:
            args_encoded = ""

        request_endpoint = "{}{}{}".format(self.venmo_endpoint, request_endpoint, args_encoded)
        return request_endpoint

    def make_api_request(self, code, args={}):
        args_default = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code
        }
        request_endpoint = self.get_request_url("oauth/access_token")
        args_default.update(args)
        print args_default
        response = requests.post(request_endpoint, data=args_default)
        resjson = response.json()
        try:
            print resjson["error"]["message"]
            raise ValueError(resjson["error"]["message"])
        except KeyError:
            return resjson

    def make_transaction(self, isPhone, phone_email, access_token, amount):
        parameters = {
            "access_token": access_token,
            "note": "My $" + str(amount) + " paypyrus has been redeemed! Send your own paypyrus at ______.com",
            "amount": amount
        }
        identifier = 'phone' if isPhone else 'email'
        parameters[identifier] = phone_email
        request_endpoint = self.get_request_url("payments")
        response = requests.post(request_endpoint, data=parameters)
        resjson = response.json()
        try:
            print resjson["error"]["message"]
            raise ValueError(resjson["error"]["message"])
        except KeyError:
            return resjson

    def get_user_data(self, code):
        return self.make_api_request(code)

    def authorize(self):
        auth_args = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.auth_scope,
            "response_type": "code"
        }
        venmo_auth_endpoint = self.get_request_url("oauth/authorize", request_args=auth_args)
        return venmo_auth_endpoint
