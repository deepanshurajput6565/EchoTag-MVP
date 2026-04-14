"""
decode.py — LSB Steganography Decoder
======================================
Extracts a hidden text message from a watermarked PNG image by reading the
Least Significant Bit (LSB) of each pixel channel value and reconstructing
the original binary payload until the stop delimiter is found.

This is the exact inverse of encode.py.  Both scripts share the same
STOP_DELIMITER constant — they must match or decoding will fail.

Author: Digital Asset Protection MVP
"""

import cv2
import numpy as np
import sys

# ─────────────────────────────────────────────────────────────
#  CONSTANTS  (must match encode.py exactly)
# ─────────────────────────────────────────────────────────────

STOP_DELIMITER = "1111111111111110"


# ─────────────────────────────────────────────────────────────
#  HELPER: binary string  →  text
# ─────────────────────────────────────────────────────────────

def binary_to_text(binary_str: str) -> str:
    """
    Convert a binary string (multiple of 8 bits) back to a UTF-8 string.

    Example:
        '0100100001101001' → chr(0b01001000)=72='H'  chr(0b01101001)=105='i'
        Result: 'Hi'
    """
    chars = []
    # Slice the binary string into 8-bit chunks
    for i in range(0, len(binary_str), 8):
        byte = binary_str[i:i + 8]
        if len(byte) < 8:
            break   # ignore any incomplete trailing byte
        chars.append(chr(int(byte, 2)))   # int(x, 2) = parse binary string
    return "".join(chars)


# ─────────────────────────────────────────────────────────────
#  MAIN DECODER
# ─────────────────────────────────────────────────────────────

def decode(image_path: str) -> str:
    """
    Extract and return the hidden message from the watermarked image
    at *image_path*.

    Steps:
      1. Load image
      2. Flatten pixel array and harvest LSBs one by one
      3. Stop as soon as the STOP_DELIMITER is found in the bit stream
      4. Convert the harvested bits (minus the delimiter) back to text
    """

    # ── 1. Load the watermarked image ───────────────────────
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not open image: '{image_path}'")

    # ── 2. Flatten and extract LSBs ─────────────────────────
    flat = image.flatten()   # 1-D array: [B0, G0, R0, B1, G1, R1, …]

    bits_collected: list[str] = []
    delimiter_len = len(STOP_DELIMITER)

    for pixel_val in flat:
        # ┌─────────────────────────────────────────────────────────────┐
        # │  READING THE LSB — explained for judges:                    │
        # │                                                             │
        # │  pixel_val & 1                                              │
        # │    1  in binary = 0b00000001  (only the LSB is set)        │
        # │    AND-ing isolates the LSB; all other bits become 0       │
        # │                                                             │
        # │  Example: pixel = 217  (0b11011001)                        │
        # │    0b11011001 & 0b00000001 = 0b00000001  =  1              │
        # │  Example: pixel = 216  (0b11011000)                        │
        # │    0b11011000 & 0b00000001 = 0b00000000  =  0              │
        # └─────────────────────────────────────────────────────────────┘
        lsb = str(pixel_val & 1)   # extract LSB → '0' or '1'
        bits_collected.append(lsb)

        # ── 3. Check for stop delimiter ─────────────────────
        # Only start checking once we have accumulated enough bits
        if len(bits_collected) >= delimiter_len:
            # Look at the tail of the collected bits
            tail = "".join(bits_collected[-delimiter_len:])
            if tail == STOP_DELIMITER:
                # Trim the delimiter from the payload before decoding
                payload_bits = "".join(bits_collected[:-delimiter_len])
                print(f"[decode] Stop delimiter found after {len(bits_collected)} bits.")
                break
    else:
        # Loop completed without finding the delimiter
        raise ValueError(
            "Stop delimiter not found. The image may not contain a hidden "
            "message, or it was encoded with a different delimiter/tool."
        )

    # ── 4. Convert bits → text ──────────────────────────────
    secret_text = binary_to_text(payload_bits)
    return secret_text


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT — edit path below to test immediately
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # ── Dummy test value (must match the output from encode.py) ─
    WATERMARKED_IMAGE = "watermarked.png"

    try:
        message = decode(WATERMARKED_IMAGE)
        print(f"\n[decode] ✅ Hidden message found:\n\n  {message}\n")
    except (FileNotFoundError, ValueError) as e:
        print(f"[decode] ❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
