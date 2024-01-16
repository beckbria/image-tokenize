import debugging
import imageio.v3 as iio
from imagemap import *
from imagesplit import *
import numpy as np
from PIL import Image

# TODO: Take these constants as command line arguments
filename = "mit_2024_i_write_these_words.png"
bg_color = np.array([255, 255, 255])
min_height = 40

# Debug output
debug_write_image_files = False
debug_trim = False
debug_hash = True

im_numpy = iio.imread(filename)

# Remove the alpha channel
im_numpy = im_numpy[:, :, :3]

image_rows_numpy = horizontalSegments(im_numpy, bg_color, min_height)

image_chars_numpy = list(map(lambda r: verticalSegments(r, bg_color), image_rows_numpy))

image_chars_pil = list(
    map(lambda r: list(map(lambda c: Image.fromarray(c), r)), image_chars_numpy)
)

if debug_write_image_files:
    debugging.writeFilesBySize(image_chars_numpy)

if debug_trim:
    debugging.printSizes(image_chars_numpy)

if debug_hash:
    debugging.verifyEqualGlyphs(image_chars_pil)

char_map = ImageToLetterMap()

# The hash function can be slow, so gather the letters as we initially insert them

image_chars = []
for row in image_chars_pil:
    charRow = []
    for char in row:
        charRow.append(char_map.ensureExists(char))
    image_chars.append(charRow)
print(image_chars)
