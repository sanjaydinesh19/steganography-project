# Secure Steganographic Communication System (AES-GCM + Image Steganography)

## Overview
This project implements a secure communication system that combines:
- Cryptography using AES-GCM
- Steganography using image-based data hiding

The goal is to ensure that:
1. The message is encrypted (confidentiality + integrity)
2. The encrypted data is hidden inside an image (covert communication)

---

## Technologies Used

- AES-GCM (Authenticated Encryption)
  - Provides confidentiality and integrity
  - Detects tampering using authentication tag

- Steganography
  - Initially implemented using DCT-based embedding (JPEG domain)
  - Migrated to LSB-based embedding (Spatial domain)

- Python Libraries
  - jpegio (initial approach)
  - Pillow / OpenCV (final approach for LSB)
  - pyserial (initial communication approach)
  - socket (final communication over TCP)

---

## System Architecture

### Nodes
- User A (Raspberry Pi 4) – Edge device
- User B (Laptop) – Processing node

---

## Communication Flow

### Phase 1: Pi to Laptop
1. Plaintext message is encrypted using AES-GCM
2. Ciphertext is embedded into an image using LSB steganography
3. Stego image is transmitted over TCP
4. Laptop receives the image
5. Hidden payload is extracted
6. Ciphertext is decrypted to recover plaintext

---

## Initial Approach: JPEG (DCT-Based Steganography)

### Method
- Used jpegio to modify DCT coefficients
- Embedded data in:
  - Non-zero coefficients
  - Skipping DC components

### Advantages
- High resistance to statistical detection
- Robust against compression

### Limitations
- jpegio requires native compilation (C extensions)
- Difficult to install on ARM-based systems (Raspberry Pi)
- Build failures during pip installation
- Not suitable for embedded environments

---

## Migration to LSB (Spatial Domain)

### Reason for Switching

The project was redesigned to ensure:
- Platform compatibility (Raspberry Pi support)
- Bidirectional communication
- Ease of deployment and reliability

---

### LSB Method

- Data is embedded in the Least Significant Bits of pixel values
- Works directly on image pixels (RGB channels)
- Uses PNG images (lossless format)

---

## Capacity Comparison

| Method | 512x512 Image | 1024x1024 Image |
|--------|--------------|----------------|
| DCT (JPEGIO) | ~494 bytes | ~14 KB |
| LSB (RGB) | ~96 KB | ~384 KB |

LSB provides significantly higher capacity.

---

## Trade-offs

### DCT (JPEG Domain)
- More secure against detection  
- Compression resistant  
- Difficult to deploy on Raspberry Pi  

### LSB (Spatial Domain)
- Easy to implement  
- Works on Raspberry Pi  
- High capacity  
- Less resistant to statistical analysis  
- Not robust to image compression  

---

## Security Considerations

Even though LSB is less stealthy:
- AES-GCM encryption ensures data confidentiality
- Extracted data remains unreadable without the key
- Authentication tag prevents tampering

---

## Design Decision

To balance:
- Security
- Performance
- Hardware compatibility

The system uses:

AES-GCM (security) + LSB steganography (compatibility)

---

## Features

- End-to-end encrypted communication
- Image-based hidden data transmission
- Cross-device communication (Pi and Laptop)
- Modular design (crypto and stego separated)
- TCP-based communication between nodes

---

## How to Run (TCP Pipeline Test)

### Prerequisites (Both Pi and Laptop)

```bash
cd steganography-project
source venv/bin/activate
pip install -r requirements.txt
```

Ensure:
- Both devices are connected to the same network
- PNG input images are present (e.g., `input_512.png`, `input_1024.png`)

---

### Step 1: Start Receiver (Laptop)

```bash
python3 receive.py
```

Expected output:
```
Waiting for connection...
```

---

### Step 2: Run Sender (Raspberry Pi)

```bash
python3 send.py
```

Expected output:
```
Payload length: XXX
Sending image of size: XXXXX
Image sent successfully.
```

---

### Step 3: Verify Output (Laptop)

After receiving:

```
Connected by (...)
Receiving image of size: XXXXX
Image received and saved as received.png
Recovered message: b'...'
```

---

## Verification Checklist

- No errors during execution
- Image (`received.png`) is generated
- Extracted message matches original plaintext
- Same encryption key used on both devices

---

## Future Improvements

- Key-based random embedding (PRNG)
- Error correction codes
- Hybrid DCT + LSB system
- Hardware-backed key storage (ATECC)
- Bidirectional communication

---

## Conclusion

This project demonstrates a practical secure communication system by combining:
- Strong encryption (AES-GCM)
- Covert data hiding (Steganography)
- Network-based communication (TCP sockets)

The transition from JPEG (DCT) to LSB ensures:
- Real-world deployability
- Compatibility with embedded systems
- Reliable cross-device communication

---

## Author
Sanjay Dinesh