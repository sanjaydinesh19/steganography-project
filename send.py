import socket
import os

from crypto.aes_gcm import encrypt_data
from utils.helpers import build_payload
from stego.dct_embed import embed_payload  # LSB version


HOST = "192.168.0.195"
PORT = 5000


def main():
    key = b'0123456789abcdef0123456789abcdef'

    msg = b"Hello from Raspberry Pi via Steganography!"

    nonce, ct, tag = encrypt_data(msg, key)
    payload = build_payload(nonce, tag, ct)

    print("Payload length:", len(payload))

    embed_payload("input(512x512).png", "stego.png", payload)

    # Read image as bytes
    with open("stego.png", "rb") as f:
        data = f.read()

    print("Connecting to receiver...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        length = len(data).to_bytes(4, 'big')

        print("Sending image of size:", len(data))
        s.sendall(length + data)

    print("Image sent successfully.")


if __name__ == "__main__":
    main()