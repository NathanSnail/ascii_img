import numpy as np
import pyperclip
from PIL import ImageGrab

charmax = 2000


img = ImageGrab.grabclipboard().convert("RGB")

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
ansi = "\u001b"


def compute(maximum, img):
	if (sz := max(img.size[0], img.size[1])) > maximum:

		def apply(x):
			return int(x * maximum / sz)

		img = img.resize((apply(img.size[0] * 2), apply(img.size[1])))
	img_arr = np.array(img, dtype=np.float32)

	msg = "```ansi\n"
	prev_fg = 0
	prev_bg = 0
	for y in range(img_arr.shape[0]):
		for x in range(img_arr.shape[1]):
			px = img_arr[y][x][:]
			correct = min(
				[
					(
						col[0],
						sum(
							[
								(x - y) ** 2 * w
								for x, y, w in zip(px, col[1:], [0.299, 0.587, 0.114])
							]
						),
					)
					for col in codes
				],
				key=lambda x: x[1],
			)[0]
			if correct > 39:
				msg += f"{f"{ansi}[{correct}m " if prev_bg != correct else " "}"
				prev_bg = correct
			else:
				msg += f"{f"{ansi}[{correct}m█" if prev_fg != correct else "█"}"
				prev_fg = correct
		msg += "\n"
	msg += "```"
	return msg


low = 10  # it just looks awful if this small
high = 100  # don't waste time searching unrealistic images
while True:
	search = (
		low * 2 + high
	) // 3  # bigger images take longer to search so not doing binary search is faster
	msg = compute(search, img)
	if (low * 2 + high) // 3 == low:
		break
	if len(msg) > charmax:
		high = search - 1
	else:
		low = search

print(msg)
pyperclip.copy(msg)
