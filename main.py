import numpy as np
import pyperclip
from PIL import Image, ImageGrab

maximum = 32
img = ImageGrab.grabclipboard().convert("RGB")
if (sz := max(img.size[0] / 2, img.size[1])) > maximum:

	def apply(x):
		return int(x * maximum / sz)

	print(sz)
	print(img.size)
	img = img.resize((apply(img.size[0]), apply(img.size[1])))
img_arr = np.array(img)
codes = [
	(30, 0x4E, 0x50, 0x58),
	(31, 0xDC, 0x32, 0x2F),
	(32, 0x85, 0x99, 0x00),
	(33, 0xB5, 0x89, 0x00),
	(34, 0x26, 0x8B, 0xD2),
	(35, 0xD3, 0x36, 0x82),
	(36, 0x2A, 0xA1, 0x98),
	(37, 0xFF, 0xFF, 0xFF),
	(40, 0x00, 0x2B, 0x36),
	(41, 0xCB, 0x4B, 0x16),
	(42, 0x58, 0x6E, 0x75),
	(43, 0x65, 0x7B, 0x83),
	(44, 0x83, 0x94, 0x96),
	(45, 0x6C, 0x71, 0xC4),
	(46, 0x93, 0xA1, 0xA1),
	(47, 0xFD, 0xF6, 0xE3),
]

msg = "```ansi\n"
prev = 0
ansi = "\u001b"
for y in range(img_arr.shape[0]):
	for x in range(img_arr.shape[1]):
		px = img_arr[y][x][:]
		correct = min(
			[
				(col[0], sum([(float(x) - float(y)) ** 2 for x, y in zip(px, col[1:])]))
				for col in codes
			],
			key=lambda x: x[1],
		)[0]
		msg += f"{f"{ansi}[0;{correct}m" if prev != correct else ""}{" " if correct > 39 else "█"}"
		prev = correct
	msg += "\n"
msg += "\n```"
print(msg)
# pyperclip.copy(msg)
