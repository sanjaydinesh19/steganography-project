import os
from crypto.aes_gcm import encrypt_data, decrypt_data
from utils.helpers import build_payload, unpack_payload
from stego.dct_embed import embed_payload
from stego.dct_extract import extract_payload


def main():

    key = os.urandom(32)
    msg = b"""
        Steganography is the practice of concealing information within another medium
        so that the presence of the hidden data is not obvious.
        """


    nonce, ct, tag = encrypt_data(msg, key)
    payload = build_payload(nonce, tag, ct)

    print("Payload length:", len(payload))

    embed_payload("input(512x512).jpg", "stego.jpg", payload)

    recovered_payload = extract_payload("stego.jpg")
    n, t, c = unpack_payload(recovered_payload)

    recovered = decrypt_data(n, c, t, key)

    print("Recovered:", recovered)


if __name__ == "__main__":
    main()
