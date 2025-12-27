#!/usr/bin/env python3

import sys
from PIL import Image


def image_to_bits_native(im):
    width, height = im.size

    if height % 8 != 0:
        raise ValueError(
            f"L'altezza dell'immagine ({height}) deve essere multipla di 8"
        )

    pixels = im.load()
    bits = [0] * (width * height)

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            bits[y * width + x] = 1 if (r + g + b) < (128 * 3) else 0

    return bits, width, height


def bits_to_pages(bits, width, height):
    framebuffer = []

    pages = height // 8
    for page in range(pages):
        for x in range(width):
            byte = 0
            for bit in range(8):
                y = page * 8 + bit
                if bits[y * width + x]:
                    byte |= (1 << bit)
            framebuffer.append(byte)

    return framebuffer


def print_cpp_array(data, name, width, height):
    print("#include <avr/pgmspace.h>\n")

    print(f"// Risoluzione: {width}x{height}")
    print(f"// Byte totali: {len(data)}\n")

    print(f"const uint8_t {name}[{len(data)}] PROGMEM = {{")

    for i, b in enumerate(data):
        print(f" 0x{b:02X},", end="")
        if (i + 1) % 16 == 0:
            print()
    print("};")


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 convert_native.py image.png", file=sys.stderr)
        sys.exit(1)

    image_path = sys.argv[1]
    var_name = image_path.rsplit(".", 1)[0]

    im = Image.open(image_path).convert("RGB")

    bits, width, height = image_to_bits_native(im)
    framebuffer = bits_to_pages(bits, width, height)

    print_cpp_array(framebuffer, var_name, width, height)


if __name__ == "__main__":
    main()
