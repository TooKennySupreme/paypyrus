import requests, urllib
import config

class VenmoAPI:
    def __init__(self, auth_code=None):
        self.venmo_endpoint = config.venmo_endpoint
        self.client_id = config.venmo_client_id
        self.client_secret = config.venmo_client_secret
        self.auth_scope = config.venmo_auth_scope

        self.auth_code = auth_code

    def get_request_url(self, request_endpoint, request_args=None):
        if request_args not None:
            args_encoded = urllib.urlencode(request_args)
        else:
            args_encoded = ""

        request_endpoint = "{}{}{}".format(self.venmo_endpoint, request_endpoint, args_encoded)


    def authorize(self):
        auth_args = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": self.auth_scope
        }
        venmo_auth_endpoint = get_request_url("oauth/authorize", request_args=auth_args)
