#!/usr/bin/env python3

import sys
from PIL import Image

TARGET_W = 128
TARGET_H = 64
THRESHOLD = 128   # 0–255 (più basso = più nero)


def main():
    if len(sys.argv) != 3:
        print("Uso: python3 to_128x64_bw.py input.png output.png")
        sys.exit(1)

    in_path  = sys.argv[1]
    out_path = sys.argv[2]

    # Apri immagine e converti in scala di grigi
    im = Image.open(in_path).convert("L")

    # Ridimensiona (senza antialias per preservare i bordi)
    im = im.resize((TARGET_W, TARGET_H), Image.NEAREST)

    # Threshold → bianco / nero
    im = im.point(lambda p: 255 if p > THRESHOLD else 0, mode="1")

    # Salva risultato
    im.save(out_path)

    print(f"Creato: {out_path} ({TARGET_W}x{TARGET_H}, B/N)")


if __name__ == "__main__":
    main()
