#!/usr/bin/env python3
from PIL import Image
im = Image.open("pu_up.png")
print(im.size)
w = im.size[0]
h = im.size[1]
print(w)
print(h)
print(w/128)
print(h/64)
divw = w/64
divh = w/128

print(im.getpixel((10,10)))

a = ""
for i in range(0,int(h/divw)):
	for j in range(0,int(w/divh)):
		if(im.getpixel((j*divh+1,i*divw+1)) == (0, 0, 0)):
			print("1", end="")
			a+= "1"
		else:
			print("0", end="")
			a+="0"
	print("")

bytes_per_row = w // 8          # 16
total_bytes = len(a) // 8       # 768

for i in range(total_bytes):
	byte = a[i*8:(i*8+8)]
	print("B" + byte, end=", ")
	if (i + 1) % bytes_per_row == 0:
		print()

exit()
print(len(a))
div = 8
print(div)
righe = 0
for i in range(0, int(len(a)/div)):
	strg = a[(i*8):(i*8+8)]
	print("B"+strg, end= ", ")
	if(i%div == div-1):
		righe += 1
		print("")
print("righe: ", righe)
for i in range(0, int(len(a)/div)):
	strg = a[(i*8):(i*8+8)]
	print(hex(int(strg, 2)), end= ", ")
	if(i%(div*2) == (div*2)-1):
		print("")
