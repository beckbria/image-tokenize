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
debug_trim = True

# https://imageio.readthedocs.io/
im_numpy = iio.imread(filename)

# Remove the alpha channel
im_numpy = im_numpy[:, :, :3]

image_rows_numpy_raw = horizontalSegments(im_numpy, bg_color, min_height)

image_rows_numpy = list(
    map(lambda r: verticalSegments(r, bg_color), image_rows_numpy_raw)
)

image_rows_pil = list(
    map(lambda r: list(map(lambda c: Image.fromarray(c), r)), image_rows_numpy)
)

if debug_write_image_files:
    debugging.writeFilesBySize(image_rows_numpy)

if debug_trim:
    debugging.printSizes(image_rows_numpy)
    debugging.verifyEqualGlyphs(image_rows_pil)

char_map = ImageToLetterMap(image_rows_pil)

image_chars = []
for row in image_rows_numpy:
    charRow = []
    for char in row:
        charRow.append(char_map.get(char))
    image_chars.append(charRow)
print(image_chars)
