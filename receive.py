import socket

from crypto.aes_gcm import decrypt_data
from utils.helpers import unpack_payload
from stego.dct_extract import extract_payload  # LSB version


HOST = "0.0.0.0"   # listen on all interfaces
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
    key = b'0123456789abcdef0123456789abcdef'

    print("Waiting for connection...")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)

        conn, addr = s.accept()
        with conn:
            print("Connected by", addr)

            # Read length
            length_bytes = receive_all(conn, 4)
            length = int.from_bytes(length_bytes, 'big')

            print("Receiving image of size:", length)

            # Read full image
            data = receive_all(conn, length)

            with open("received.png", "wb") as f:
                f.write(data)

    print("Image received and saved as received.png")

    # Extract + decrypt
    payload = extract_payload("received.png")
    n, t, c = unpack_payload(payload)

    recovered = decrypt_data(n, c, t, key)

    print("Recovered message:", recovered)


if __name__ == "__main__":
    main()