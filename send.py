import socket
from Crypto.Random import get_random_bytes

from crypto.aes_gcm import encrypt_data, decrypt_data
from utils.helpers import build_payload, unpack_payload
from stego.dct_embed import embed_payload
from stego.dct_extract import extract_payload


HOST = "10.143.57.197"
PORT = 5000


def receive_all(sock, length):
    data = b''
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            raise ConnectionError("Connection lost")
        data += packet
    return data


def main():
    key = get_random_bytes(32)

    # 🔹 Send message
    user_input = input("Enter message to send: ")
    msg = user_input.encode()

    nonce, ct, tag = encrypt_data(msg, key)
    payload = build_payload(nonce, tag, ct)

    embed_payload("input(2048x2048).png", "stego.png", payload)

    with open("stego.png", "rb") as f:
        img_data = f.read()

    print("Connecting to receiver...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        s.sendall(len(key).to_bytes(2, 'big') + key)
        s.sendall(len(img_data).to_bytes(4, 'big') + img_data)

        print("Sent image + key")

        print("Waiting for reply...")

        # Receive key
        key_len = int.from_bytes(receive_all(s, 2), 'big')
        recv_key = receive_all(s, key_len)

        # Receive image
        img_len = int.from_bytes(receive_all(s, 4), 'big')
        img_data = receive_all(s, img_len)

        with open("reply.png", "wb") as f:
            f.write(img_data)

        print("Reply image received")

    payload = extract_payload("reply.png")
    n, t, c = unpack_payload(payload)

    recovered = decrypt_data(n, c, t, recv_key)

    print("Reply message:", recovered.decode())


if __name__ == "__main__":
    main()
