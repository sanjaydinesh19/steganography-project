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
  - pyserial (for Pi to Laptop communication)

---

## System Architecture

### Nodes
- User A (Raspberry Pi 4) – Edge device
- User B (Laptop) – Processing node

---

## Communication Flow

### Phase 1: Pi to Laptop
1. Plaintext message is encrypted using AES-GCM
2. Ciphertext is sent via serial communication
3. Laptop receives and decrypts the message

---

### Phase 2: Laptop to Pi
1. Laptop encrypts its own message using AES-GCM
2. Ciphertext is embedded inside an image using steganography
3. Stego image is sent to Raspberry Pi
4. Raspberry Pi extracts hidden data
5. Raspberry Pi decrypts ciphertext to recover plaintext

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
- Typically uses PNG images (lossless format)

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

---

## Future Improvements

- Key-based random embedding (PRNG)
- Error correction codes
- Hybrid DCT + LSB system
- Wireless communication (WiFi instead of serial)

---

## Conclusion

This project demonstrates a practical secure communication system by combining:
- Strong encryption (AES-GCM)
- Covert data hiding (Steganography)

The transition from JPEG (DCT) to LSB ensures:
- Real-world deployability
- Compatibility with embedded systems
- Reliable bidirectional communication

---

## Author
Sanjay Dinesh