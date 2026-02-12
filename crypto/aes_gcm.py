from Crypto.Cipher import AES
import os

def encrypt_data(plaintext: bytes, key: bytes):
    nonce = os.urandom(12)  # FORCE 96-bit nonce
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ciphertext, auth_tag = cipher.encrypt_and_digest(plaintext)
    return nonce, ciphertext, auth_tag


def decrypt_data(nonce: bytes, ciphertext: bytes, auth_tag: bytes, key: bytes):
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, auth_tag)
