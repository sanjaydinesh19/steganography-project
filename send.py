import socket
from Crypto.Random import get_random_bytes

from crypto.aes_gcm import encrypt_data
from utils.helpers import build_payload
from stego.dct_embed import embed_payload


HOST = "192.168.0.195"
PORT = 5000


def main():
    key = get_random_bytes(32)

    # 🔹 Take message input from user
    user_input = input("Enter message to send: ")
    msg = user_input.encode()

    nonce, ct, tag = encrypt_data(msg, key)
    payload = build_payload(nonce, tag, ct)

    print("Payload length:", len(payload))

    embed_payload("input(512x512).png", "stego.png", payload)

    with open("stego.png", "rb") as f:
        img_data = f.read()

    print("Connecting to receiver...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        # Send key
        s.sendall(len(key).to_bytes(2, 'big') + key)

        # Send image
        s.sendall(len(img_data).to_bytes(4, 'big') + img_data)

    print("Image + key sent successfully.")


if __name__ == "__main__":
    main()