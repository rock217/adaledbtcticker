import atexit
import math
import os
import time

import Image
import ImageDraw
import ImageFont

from rgbmatrix import Adafruit_RGBmatrix

# Configuration
fps            = 2
width          = 64  # Matrix size (pixels) -- change for different matrix
height         = 32  # types (incl. tiling).  Other code may need tweaks.
matrix         = Adafruit_RGBmatrix(32, 2) # rows, chain length

green          = (0, 132, 69)
red            = (225, 39, 38)
orange         = (232, 116, 36)
blue           = (15, 75, 145)
silver         = (125, 134,140)
plum           = (194, 147, 181)
aqua           = (216, 240, 252)
white          = (255, 255, 255)
black          = (0, 0, 0)

font           = ImageFont.load(os.path.dirname(os.path.realpath(__file__)) + '/helvR08.pil')

# Main application -----------------------------------------------------------

# Drawing takes place in offscreen buffer to prevent flicker
image       = Image.new('RGB', (width, height))
draw        = ImageDraw.Draw(image)

# Clear matrix on exit.  Otherwise it's annoying if you need to break and
# fiddle with some code while LEDs are blinding you.
def clearOnExit():
	matrix.Clear()
atexit.register(clearOnExit)


def drawBox():
	draw.line((0, 0, width, 0), fill=aqua)  # top
	draw.line((0, height - 1, width, height - 1), fill=aqua)  # bottom
	draw.line((0, 0, 0, height), fill=aqua)  # left
	draw.line((width - 1, 0, width - 1, height), fill=aqua)  # right


# Splash Screen'
draw.text((1, 0), "BTCTickr v0.1", font=font, fill=white)
draw.text((1, 10), "Made by Rock!", font=font, fill=white)
draw.text((1, 20), "Loading Data...", font=font, fill=green)
matrix.SetImage(image.im.id, 0, 0)

time.sleep(5)

currentTime     = 0.0
prevTime        = 0.0
error           = None
errlen          = 0
# Event loop

while True:
	# Draw Stuff
	draw.rectangle((0, 0, width, height), fill=black)
	drawBox()
	separator = ":" if int(time.time()) % 2 == 0 else " "
	time_label = time.strftime("%b %d %H"+separator+"%M")
	draw.text((5, 20), time_label, font=font, fill=green)

	# Timing
	currentTime = time.time()
	timeDelta = (1.0 / fps) - (currentTime - prevTime)
	if (timeDelta > 0.0):
		time.sleep(timeDelta)
	prevTime = currentTime

	# Offscreen buffer is copied to screen
	matrix.SetImage(image.im.id, 0, 0)


