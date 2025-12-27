#!/usr/bin/env python3

import sys
from PIL import Image

TARGET_W = 128
TARGET_H = 64


def image_to_bits(im, target_w=TARGET_W, target_h=TARGET_H):
    width, height = im.size
    step_x = width / target_w
    step_y = height / target_h

    pixels = im.load()
    bits = [0] * (target_w * target_h)

    for y in range(target_h):
        py = int(y * step_y)
        for x in range(target_w):
            px = int(x * step_x)
            r, g, b = pixels[px, py]
            bits[y * target_w + x] = 1 if (r + g + b) < 128 * 3 else 0

    return bits


def bits_to_sh1106(bits, width=TARGET_W, height=TARGET_H):
    framebuffer = []

    for page in range(height // 8):
        for x in range(width):
            byte = 0
            for bit in range(8):
                y = page * 8 + bit
                if bits[y * width + x]:
                    byte |= (1 << bit)
            framebuffer.append(byte)

    return framebuffer


def print_arrays_hex(data, name):
    print("#include <avr/pgmspace.h>\n")

    # ---------- HEX ----------
    print(f"")
    print(f"")
    print(f"const uint8_t {name}[{len(data)}] PROGMEM = {{")

    for i, b in enumerate(data):
        print(f"0x{b:02X},", end="")
        if (i + 1) % 16 == 0:
            print()
    print("};\n")

def print_arrays_bin(data, name):
    print("#include <avr/pgmspace.h>\n")

    # ---------- BIN ----------
    print(f"// === BIN ===")
    print(f"const uint8_t {name}_bin[{len(data)}] PROGMEM = {{")

    for i, b in enumerate(data):
        print(f" 0b{b:08b},", end="")
        if (i + 1) % 8 == 0:
            print()
    print("};")


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 convert_4_arduino.py image.png", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]
    var_name = image_path.rsplit(".", 1)[0]

    im = Image.open(image_path).convert("RGB")
    bits = image_to_bits(im)
    framebuffer = bits_to_sh1106(bits)

    print_arrays_hex(framebuffer, var_name)


if __name__ == "__main__":
    main()
