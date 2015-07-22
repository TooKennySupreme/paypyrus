import os

secret_key = "ige3*ZWJ9fCBw@89ige3*ZWJ9fCBw@89"

# database
host = "127.0.0.1"
dbuser = "root"
dbpassword = "root"
dbname = "paypyrus"

current_host = "http://localhost:5000"

# venmo API key
venmo_client_id = "2778"
venmo_client_secret = "xZ9gBxxrXRXMsMmX8EayEvms3HSskTGC"

venmo_redirect_uri = ""
venmo_endpoint = "https://api.venmo.com/v1/"
venmo_auth_scope = "make_payments access_profile access_email"

token_length = 20

# This key must be 16, 24, or 32 bytes long
crypto_key = os.environ.get("ENCRYPTION_KEY", '^CEqNJ0ce4*8Hh6IsQ15AHC3pVXdCkGK')
