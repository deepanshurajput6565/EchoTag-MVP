"""
encode.py — LSB Steganography Encoder
======================================
Hides a secret text message inside an image by replacing the Least Significant
Bit (LSB) of each pixel channel value with one bit of the secret payload.

How LSB works (the core idea):
  A pixel value like 217 in binary is  →  1 1 0 1 1 0 0 1
                                                           ↑
                              Least Significant Bit ───────┘
  Flipping this bit changes 217 → 216, a difference invisible to the human eye.
  We exploit this to smuggle data: one bit per pixel channel, zero visual impact.

Author: Digital Asset Protection MVP
"""

import cv2
import numpy as np
import sys

# ─────────────────────────────────────────────────────────────
#  CONSTANTS  (must match decode.py exactly)
# ─────────────────────────────────────────────────────────────

# 16-bit stop delimiter that signals end-of-message to the decoder.
# Chosen to be distinctive: 15 ones followed by a zero.
# The probability of this pattern appearing randomly in real text is tiny.
STOP_DELIMITER = "1111111111111110"


# ─────────────────────────────────────────────────────────────
#  HELPER: text  →  binary string
# ─────────────────────────────────────────────────────────────

def text_to_binary(text: str) -> str:
    """
    Convert each character of *text* to its 8-bit binary representation.

    Example:
        'Hi' → ord('H')=72 → '01001000'
                ord('i')=105 → '01101001'
        Result: '0100100001101001'
    """
    binary_chars = []
    for char in text:
        # format(n, '08b') → zero-padded 8-bit binary string
        binary_chars.append(format(ord(char), "08b"))
    return "".join(binary_chars)


# ─────────────────────────────────────────────────────────────
#  MAIN ENCODER
# ─────────────────────────────────────────────────────────────

def encode(image_path: str, secret_text: str, output_path: str) -> None:
    """
    Embed *secret_text* into the image at *image_path* and write the
    watermarked image to *output_path* (must be a .png path).

    Steps:
      1. Load image
      2. Build binary payload  =  secret_bits + STOP_DELIMITER
      3. Validate capacity
      4. Flatten pixel array and embed payload bit-by-bit
      5. Reshape and save as lossless PNG
    """

    # ── 1. Load the cover image ──────────────────────────────
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not open image: '{image_path}'")

    # ── 2. Build the binary payload ──────────────────────────
    secret_binary = text_to_binary(secret_text)
    payload = secret_binary + STOP_DELIMITER   # append stop sentinel
    payload_len = len(payload)

    print(f"[encode] Secret text   : {secret_text!r}")
    print(f"[encode] Binary length : {payload_len} bits  ({payload_len // 8} bytes + delimiter)")

    # ── 3. Capacity check ────────────────────────────────────
    # Each pixel has 3 channels (B, G, R); each channel holds 1 bit.
    total_bits_available = image.size  # height × width × channels
    if payload_len > total_bits_available:
        raise ValueError(
            f"Image too small!  Payload needs {payload_len} bits "
            f"but image only holds {total_bits_available} bits.\n"
            f"Use a larger image or a shorter message."
        )

    # ── 4. Embed payload into the flattened pixel array ──────
    # Flatten to a 1-D array of uint8 values: [B0, G0, R0, B1, G1, R1, …]
    flat = image.flatten()

    for i, bit_char in enumerate(payload):
        bit = int(bit_char)   # '0' or '1'  →  0 or 1

        # ┌─────────────────────────────────────────────────────────────┐
        # │  THE CORE BITWISE OPERATION  — explained for judges:        │
        # │                                                             │
        # │  flat[i] & ~1                                               │
        # │    ~1  in 8-bit = 0b11111110  (all ones except LSB)        │
        # │    AND-ing clears the LSB of the pixel → "make room"       │
        # │                                                             │
        # │  ... | bit                                                  │
        # │    OR-ing with our target bit writes it into the LSB       │
        # │                                                             │
        # │  Combined: (pixel & ~1) | bit                              │
        # │    If pixel = 217  (0b11011001)  and  bit = 0:             │
        # │      0b11011001 & 0b11111110 = 0b11011000  =  216  ✓       │
        # │    If pixel = 216  (0b11011000)  and  bit = 1:             │
        # │      0b11011000 & 0b11111110 = 0b11011000                  │
        # │      0b11011000 | 0b00000001 = 0b11011001  =  217  ✓       │
        # └─────────────────────────────────────────────────────────────┘
        flat[i] = (flat[i] & ~1) | bit

    # ── 5. Reshape and save ──────────────────────────────────
    watermarked = flat.reshape(image.shape)

    # CRITICAL: must save as PNG (lossless).
    # JPEG recompresses pixel values → destroys LSB payload irreversibly.
    if not output_path.lower().endswith(".png"):
        output_path = output_path.rsplit(".", 1)[0] + ".png"
        print(f"[encode] Output path corrected to: {output_path}")

    success = cv2.imwrite(output_path, watermarked)
    if not success:
        raise IOError(f"Failed to write output image to '{output_path}'")

    print(f"[encode] ✅ Watermarked image saved → {output_path}")


# ─────────────────────────────────────────────────────────────
#  ENTRY POINT — edit paths below to test immediately
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # ── Dummy test values (change these) ────────────────────
    INPUT_IMAGE  = "cover.png"          # any PNG/JPG/BMP cover image
    OUTPUT_IMAGE = "watermarked.png"    # output MUST be PNG
    SECRET       = "Copyright © 2026 MyBrand | Asset ID: XJ-00421"

    try:
        encode(INPUT_IMAGE, SECRET, OUTPUT_IMAGE)
    except (FileNotFoundError, ValueError, IOError) as e:
        print(f"[encode] ❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
