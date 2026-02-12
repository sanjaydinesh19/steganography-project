def build_payload(nonce: bytes, auth_tag: bytes, ciphertext: bytes) -> bytes:
    return nonce + auth_tag + ciphertext


def unpack_payload(payload: bytes):
    nonce = payload[:12]
    auth_tag = payload[12:28]
    ciphertext = payload[28:]
    return nonce, auth_tag, ciphertext
