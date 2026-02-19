import jpegio as jio


def bits_to_bytes(bits):
    data = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i:i+8]:
            byte = (byte << 1) | bit
        data.append(byte)
    return bytes(data)


def extract_payload(stego_path: str):

    jpeg = jio.read(stego_path)
    coef = jpeg.coef_arrays[0]

    h, w = coef.shape
    bits = []

    for i in range(h):
        for j in range(w):

            if i % 8 == 0 and j % 8 == 0:
                continue

            if coef[i, j] == 0:
                continue

            bits.append(coef[i, j] & 1)

    # First 32 bits → length
    length_bits = bits[:32]
    length_bytes = bits_to_bytes(length_bits)
    payload_length = int.from_bytes(length_bytes, 'big')

    total_bits = payload_length * 8
    payload_bits = bits[32:32 + total_bits]

    return bits_to_bytes(payload_bits)
