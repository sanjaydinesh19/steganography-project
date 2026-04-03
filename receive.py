import socket

from crypto.aes_gcm import decrypt_data
from utils.helpers import unpack_payload
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

            # Receive key first
            key_len = int.from_bytes(receive_all(conn, 2), 'big')
            key = receive_all(conn, key_len)

            print("Received key")

            # Receive image
            img_len = int.from_bytes(receive_all(conn, 4), 'big')
            print("Receiving image of size:", img_len)

            data = receive_all(conn, img_len)

            with open("received.png", "wb") as f:
                f.write(data)

    print("Image received")

    payload = extract_payload("received.png")
    n, t, c = unpack_payload(payload)

    recovered = decrypt_data(n, c, t, key)

    print("Recovered message:", recovered)


if __name__ == "__main__":
    main()