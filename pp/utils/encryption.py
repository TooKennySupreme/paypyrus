from Crypto.Cipher import AES
from Crypto import Random
import string, random
from .. import config

def encrypt_aes(msg):
    iv = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(AES.block_size))
    key = config.crypto_key
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted = iv + cipher.encrypt(msg)
    return encrypted.encode("base64")

def decrypt_aes(msg):
    msg = msg.decode("base64")
    iv = msg[:AES.block_size]
    key = config.crypto_key
    cipher = AES.new(key, AES.MODE_CFB, iv)
    msg = msg[AES.block_size:]
    decrypted = cipher.decrypt(msg)
    return decrypted
