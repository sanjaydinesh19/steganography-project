import jpegio as jio


def bytes_to_bits(data: bytes):
    bits = []
    for byte in data:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits


def set_lsb(value, bit):
    """Set LSB of value to bit, never returning 0."""
    if value % 2 != bit % 2:
        delta = 1 if value > 0 else -1
        new_val = value + delta
        if new_val == 0:
            new_val = value - delta
        return new_val
    return value


def count_usable_coefficients(coef):
    """Count non-zero, non-DC coefficients available for embedding."""
    h, w = coef.shape
    count = 0
    for i in range(h):
        for j in range(w):
            if i % 8 == 0 and j % 8 == 0:
                continue
            if coef[i, j] != 0:
                count += 1
    return count


def embed_payload(input_path: str, output_path: str, payload: bytes):
    # Add 4-byte length prefix
    length_prefix = len(payload).to_bytes(4, 'big')
    full_data = length_prefix + payload
    bits = bytes_to_bits(full_data)

    jpeg = jio.read(input_path)
    coef = jpeg.coef_arrays[0]  # Y channel

    # --- Capacity reporting ---
    usable_coeffs = count_usable_coefficients(coef)
    max_payload_bytes = (usable_coeffs // 8) - 4  # subtract 4-byte length prefix
    used_coeffs = len(bits)
    usage_pct = (used_coeffs / usable_coeffs) * 100 if usable_coeffs > 0 else 0

    print(f"[Capacity]  Usable DCT coefficients : {usable_coeffs}")
    print(f"[Capacity]  Max payload size         : {max_payload_bytes} bytes")
    print(f"[Capacity]  Payload being embedded   : {len(payload)} bytes")
    print(f"[Capacity]  Image capacity used       : {usage_pct:.2f}%")
    print(f"[Capacity]  Image capacity remaining  : {100 - usage_pct:.2f}%")
    # --------------------------

    h, w = coef.shape
    bit_index = 0
    for i in range(h):
        for j in range(w):
            if i % 8 == 0 and j % 8 == 0:
                continue
            if bit_index >= len(bits):
                break
            if coef[i, j] == 0:
                continue

            coef[i, j] = set_lsb(int(coef[i, j]), bits[bit_index])
            bit_index += 1

        if bit_index >= len(bits):
            break

    if bit_index < len(bits):
        raise ValueError(
            f"Image too small for payload. "
            f"Need {len(bits)} bits but only {usable_coeffs} usable coefficients available."
        )

    jpeg.coef_arrays[0] = coef
    jio.write(jpeg, output_path)
    print("Embedding complete.")
