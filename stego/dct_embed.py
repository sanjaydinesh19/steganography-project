from PIL import Image


def bytes_to_bits(data: bytes):
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def embed_payload(input_path: str, output_path: str, payload: bytes):
    # Add 4-byte length prefix
    length_prefix = len(payload).to_bytes(4, 'big')
    full_data = length_prefix + payload
    bits = bytes_to_bits(full_data)

    img = Image.open(input_path).convert("RGB")
    pixels = list(img.getdata())

    max_capacity = len(pixels) * 3  # 3 channels per pixel

    if len(bits) > max_capacity:
        raise ValueError("Payload too large for image")

    print(f"[Capacity] Max bits: {max_capacity}")
    print(f"[Capacity] Bits used: {len(bits)}")

    new_pixels = []
    bit_idx = 0

    for pixel in pixels:
        r, g, b = pixel

        if bit_idx < len(bits):
            r = (r & ~1) | bits[bit_idx]
            bit_idx += 1
        if bit_idx < len(bits):
            g = (g & ~1) | bits[bit_idx]
            bit_idx += 1
        if bit_idx < len(bits):
            b = (b & ~1) | bits[bit_idx]
            bit_idx += 1

        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(output_path, "PNG") 

    print("Embedding complete.")