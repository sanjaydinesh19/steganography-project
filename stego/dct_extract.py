from PIL import Image


def bits_to_bytes(bits):
    data = bytearray()
    for i in range(0, len(bits), 8):
        byte = 0
        for bit in bits[i:i+8]:
            byte = (byte << 1) | bit
        data.append(byte)
    return bytes(data)


def extract_payload(stego_path: str):
    img = Image.open(stego_path).convert("RGB")
    pixels = list(img.getdata())

    bits = []

    for pixel in pixels:
        r, g, b = pixel
        bits.append(r & 1)
        bits.append(g & 1)
        bits.append(b & 1)

    # First 32 bits = length
    length_bits = bits[:32]
    length_bytes = bits_to_bytes(length_bits)
    payload_length = int.from_bytes(length_bytes, 'big')

    total_bits = payload_length * 8

    if len(bits) < 32 + total_bits:
        raise ValueError("Corrupted or incomplete payload")

    payload_bits = bits[32:32 + total_bits]

    return bits_to_bytes(payload_bits)