from PIL import Image
import sys

def image_to_bitmap(im, target_w=128, target_h=64):
    width, height = im.size
    step_x = width / target_w
    step_y = height / target_h

    pixels = im.load()
    bits = []
    rows = []

    for y in range(target_h):
        row_bits = []
        py = int(y * step_y)

        for x in range(target_w):
            px = int(x * step_x)
            r, g, b = pixels[px, py]
            bit = "1" if (r + g + b) < 128 * 3 else "0"
            row_bits.append(bit)
            bits.append(bit)

        rows.append("".join(row_bits))

    return rows, bits


def bits_to_bytes(bits, bytes_per_row):
    binary_bytes = []
    hex_bytes = []

    for i in range(0, len(bits), 8):
        byte_bits = "".join(bits[i:i+8])
        binary_bytes.append("B" + byte_bits)
        hex_bytes.append(f"0x{int(byte_bits, 2):02X}")

    return binary_bytes, hex_bytes


# =======================
# MAIN
# =======================

name = sys.argv[1]
var_name = name.rsplit(".", 1)[0]
im = Image.open(name).convert("RGB")

rows, bits = image_to_bitmap(im)

for row in rows:
    print(row)

bytes_per_row = 128 // 8
binary_bytes, hex_bytes = bits_to_bytes(bits, bytes_per_row)


print("\nBINARIO:")
print()
print(f"const uint8_t {var_name}[] PROGMEM = {{")
for i, b in enumerate(binary_bytes, 1):
    print(b, end=", ")
    if i % bytes_per_row == 0:
        print()

print("};")
print()

print("\nHEX:")
print()
print(f"const uint8_t {var_name}[] PROGMEM = {{")
for i, h in enumerate(hex_bytes, 1):
    print(h, end=", ")
    if i % bytes_per_row == 0:
        print()
print("};")
