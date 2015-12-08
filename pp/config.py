import os

secret_key = "GENERATE_A_RANDOM_SECRET_KEY_HERE"

# Database information
host = "127.0.0.1"
dbuser = "root"
dbpassword = "root"
dbname = "paypyrus"

# Remote host of Paypyrus server
current_host = "http://localhost:5000"

# Venmo API information
venmo_client_id = "1234"
venmo_client_secret = "CLIENT_SECRET_GOES_HERE"

venmo_redirect_uri = ""
venmo_endpoint = "https://api.venmo.com/v1/"
venmo_auth_scope = "make_payments access_profile access_email"

# length of Paypyrus tokens
token_length = 20

# This key must be 16, 24, or 32 bytes long
# used to encrypt token information

# Please set the encryption key in the ENCRYPTION_KEY environmental variable
# if used in production
crypto_key = os.environ.get("ENCRYPTION_KEY", 'DEVELOPMENT_CRYPTO_KEY')
in_production = bool(os.environ.get("IN_PRODUCTION", False))
