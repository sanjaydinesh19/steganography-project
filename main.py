import os
from crypto.aes_gcm import encrypt_data, decrypt_data
from utils.helpers import build_payload, unpack_payload

def main():
    key = os.urandom(32)
    msg = b"Step 2 payload test"

    nonce, ct, tag = encrypt_data(msg, key)

    print("Nonce length:", len(nonce))
    print("Auth tag length:", len(tag))
    print("Ciphertext length:", len(ct))

    payload = build_payload(nonce, tag, ct)
    print("Payload length:", len(payload))

    n, t, c = unpack_payload(payload)
    recovered = decrypt_data(n, c, t, key)

    print("Recovered:", recovered)

if __name__ == "__main__":
    main()
