import socket
from Crypto.Random import get_random_bytes

from crypto.aes_gcm import encrypt_data, decrypt_data
from utils.helpers import build_payload, unpack_payload
from stego.dct_embed import embed_payload
from stego.dct_extract import extract_payload


HOST = "0.0.0.0"
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
    print("Waiting for connection...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)

        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)

            key_len = int.from_bytes(receive_all(conn, 2), 'big')
            key = receive_all(conn, key_len)

            img_len = int.from_bytes(receive_all(conn, 4), 'big')
            data = receive_all(conn, img_len)

            with open("received.png", "wb") as f:
                f.write(data)

            print("Image received")

            payload = extract_payload("received.png")
            n, t, c = unpack_payload(payload)

            recovered = decrypt_data(n, c, t, key)
            print("Message from sender:", recovered.decode())

            reply_key = get_random_bytes(32)

            reply_msg = input("Enter reply message: ").encode()

            nonce, ct, tag = encrypt_data(reply_msg, reply_key)
            payload = build_payload(nonce, tag, ct)

            embed_payload("input(2048x2048).png", "reply_stego.png", payload)

            with open("reply_stego.png", "rb") as f:
                img_data = f.read()

            # Send back
            conn.sendall(len(reply_key).to_bytes(2, 'big') + reply_key)
            conn.sendall(len(img_data).to_bytes(4, 'big') + img_data)

            print("Reply sent")


if __name__ == "__main__":
    main()
