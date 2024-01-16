from imagemap import *
import imageio.v3 as iio
import numpy as np
import os

# TODO: Take these constants as command line arguments
filename = "mit_2024_i_write_these_words.png"
bg_color = np.array([255, 255, 255])
min_height = 40
ignore_alpha = True

# Debug output
debug_find_rows = False
debug_find_chars = False
debug_write_image_files = False
debug_trim = True
debug_char_map = False


# trimImage removed empty rows and columns from the border of an image
# Input:
#     Type <pixel> is an np.ndarray corresponding to the number of bytes in a pixel of the image
#     image: np.ndarray[rows, cols]<pixel> - an image containing a series of characters on a
#            constant background color. Rows of characters are separated by
#            at least one line of solid bgcolor pixels
#     background: pixel (np.ndarray)
# Return:
#     image np.ndarray<pixel>
def trimImage(image, background):
    row_count, col_count, _ = image.shape
    first_row = -1
    last_row = -1
    first_col = -1
    last_col = -1
    for idx, row in enumerate(image):
        blank = (row == background).all()
        if not blank:
            last_row = idx
            if first_row < 0:
                first_row = idx
    for idx in range(col_count):
        column = image[:, idx, :]
        blank = (column == background).all()
        if not blank:
            last_col = idx
            if first_col < 0:
                first_col = idx
    return image[first_row : last_row + 1, first_col : last_col + 1]


# horizontalSegments finds rows of characters in the source image and returns
# then as an array.
# Input:
#     Type <pixel> is an np.ndarray corresponding to the number of bytes in a pixel of the image
#     image: np.ndarray[rows, cols]<pixel> - an image containing a series of characters on a
#            constant background color. Rows of characters are separated by
#            at least one line of solid bgcolor pixels
#     background: pixel (np.ndarray)
#     minimum_height: minimum row height. If a segment is detected with fewer than this number of pixels,
#            the row will continue until that many are found. Defaults to 1.
# Return:
#     List of image np.ndarray<pixel>
def horizontalSegments(image, background, minimum_height=1):
    image_rows = []
    found_char = False
    start = -1
    for idx, row in enumerate(image):
        blank = (row == background).all()
        if blank and found_char:
            height = (idx - start) + 1
            if height < minimum_height:
                continue
            # We have reached the end of a row of characters
            image_rows.append(image[start:idx])
            if debug_find_rows:
                print("Found chars from row ", start, " to row ", idx)
            found_char = False
        elif not blank and not found_char:
            # We have found the start of a row of characters
            found_char = True
            start = idx
    # See if we ended in a row
    if found_char:
        if debug_find_rows:
            print("Found chars from row ", start, " to end")
        image_rows.append(image[start:])
    return image_rows


# verticalSegments finds rows of characters in the source image and returns
# then as an array.
# Input:
#     Type <pixel> is an np.ndarray corresponding to the number of bytes in a pixel of the image
#     image: np.ndarray[rows, cols]<pixel> - an image containing a series of characters on a
#            constant background color. Rows of characters are separated by
#            at least one line of solid bgcolor pixels
#     background: pixel (np.ndarray)
#     trim: Should empty rows/columns be removed from images after tokenizing? Defaults to True.
#     minimum_width: minimum character width. If a segment is detected with fewer than this number
#            of pixels, the row will continue until that many are found. Defaults to 1.
# Return:
#     List of image np.ndarray<pixel>
def verticalSegments(image, background, trim=True, minimum_width=1):
    row_count, col_count, _ = image.shape
    found_char = False
    chars = []
    start = -1
    for idx in range(col_count):
        column = image[:, idx, :]
        blank = (column == background).all()
        if blank and found_char:
            width = (idx - start) + 1
            if width < minimum_width:
                continue
            # We have reached the end of a character
            char = image[:, start:idx]
            chars.append(trimImage(char, background))
            if debug_find_chars:
                print("Found char from column ", start, " to column ", idx)
            found_char = False
        elif not blank and not found_char:
            # We have found the start of a row of characters
            found_char = True
            start = idx
    # See if we ended in a column
    if found_char:
        if debug_find_chars:
            print("Found chars from col ", start, " to end")
        char = image[:, start:]
        chars.append(trimImage(char, background))
    return chars


# dumpCharsToFile dumps images of the extracted characters
# Input:
#    imageRows: list of arrays of images
#    prefix: string
def dumpCharsToFiles(imageRows, prefix=""):
    for rowIdx, row in enumerate(image_rows):
        for charIdx, char in enumerate(row):
            name = "{prefix}r{rowIdx}c{charIdx}.png".format(prefix, rowIdx, charIdx)
            iio.imwrite(name, char)


# https://imageio.readthedocs.io/
im = iio.imread(filename)

if ignore_alpha:
    # Remove the alpha channel
    # Note: only the rightmost column and bottom row are translucent. The subpixels
    # are not
    im = im[:, :, :3]

# DO_NOT_SUBMIT: Experimentation
fg_color = np.array([0, 0, 0])
for rowIdx, row in enumerate(im):
    for colIdx, pixel in enumerate(row):
        if (pixel != fg_color).any():
            im[rowIdx][colIdx] = bg_color

image_rows_raw = horizontalSegments(im, bg_color, min_height)
if debug_find_rows:
    print("Found ", len(image_rows_raw), " rows of sizes: ")
    for row in image_rows_raw:
        print(row.shape)

image_rows = list(map(lambda r: verticalSegments(r, bg_color), image_rows_raw))

if debug_write_image_files:
    # Calculate distinct image shapes
    dimensionMap = {}
    for rowIdx, row in enumerate(image_rows):
        for charIdx, char in enumerate(row):
            dims = str(char.shape)
            filename = "r{0}c{1}".format(rowIdx, charIdx)
            dirname = "{0}x{1}".format(char.shape[0], char.shape[1])
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            iio.imwrite("{0}/{1}.png".format(dirname, filename), char)

            if dims in dimensionMap:
                dimensionMap[dims].append(filename)
            else:
                dimensionMap[dims] = [filename]
    print(len(dimensionMap), " unique dimensions")
    print(dimensionMap)

    # Notes: 31 shapes found.
    # Shapes split into multiple:
    # 36x36 and 36x37 should be merged
    # 29x30 and 29x31 should be merged
    # 30x30, 30x31
    # 31x29, 31x30
    # 31x32, 31x33
    # Shapes with multiple things:
    # 30x30
    # 31x30
    # 31x31

    # thoughts: if we crop this tightly we can't rely on image similarity images which require identical size
    # more advanced algorithms are better on photos but could be tried
    # Can we prune the subpixels?  What about a mask of "equals background or not"?
    #    -this clearly won't fix the different size issue, so apparently that won't be sufficient
    # Pruning any pixels not equal to (0,0,0) makes it worse - 47 distinct shapes rather than 31
    # The subpixels don't have alpha so we can't prune them that way
    # the answer is probably threshold math BUT how do we detect the cases where they're different sizes?
    # The search space (size 26) is small enough that what we can probably do is something like:
    # Add or subtract 1px from each edge (3^4 = 81 cases)
    #   add all those cases as the same letter in the hash table
    #   do difference math on any table hits of the same size and match if below a threshold

if debug_find_chars:
    for r, row in enumerate(image_rows):
        print("Row ", r, " contains ", len(row), " characters")

if debug_trim:
    for r, row in enumerate(image_rows):
        sizes = list(map(lambda r: r.shape, row))
        print("Row ", r, " sizes: ", sizes)
    # TODO: Row 0 characters 3, 6, 16 should be identical.  Confirm that they are being detected as such.
    # They have different sizes:
    # 4: (33, 27, 3)
    # 6: (35, 37, 3)
    # 16: (33, 32, 3)
    # Guess I'll have to dump to images and inspect
    # Another reason to look into image similarity....
    # OK, so the answer is subpixel aliasing.  Ugh.
    # row0 = image_rows[0]
    # r0c04 = row0[4]
    # r0c06 = row0[6]
    # r0c16 = row0[16]
    # iio.imwrite("r0c04.png", r0c04)
    # iio.imwrite("r0c06.png", r0c06)
    # iio.imwrite("r0c16.png", r0c16)
    # hash04 = ImageToLetterMap.ImageHash(r0c04)
    # hash06 = ImageToLetterMap.ImageHash(r0c06)
    # hash16 = ImageToLetterMap.ImageHash(r0c16)
    # print("4=6: ", hash04 == hash06)
    # print("4=16: ", hash04 == hash16)
    # print("6=16: ", hash06 == hash16)
    # print(r0c04.shape)
    # print(r0c06.shape)
    # print(r0c16.shape)

char_map = ImageToLetterMap(
    output_chars=ImageToLetterMap.upper_case + ImageToLetterMap.lower_case
)

# TODO: Refactor this into the ImageToLetterMap class once a good signature to handle
# lists and ndarray is determined
for rowIdx, row in enumerate(image_rows):
    for charIdx, char in enumerate(row):
        try:
            char_map.ensureExists(char)
        except Exception as ex:
            print("At row ", rowIdx, " character ", charIdx, ": ", ex)
            raise ex

image_chars = []
for row in image_rows:
    charRow = []
    for char in row:
        charRow.append(char_map.get(char))
        # image_chars.append(list(map(row, lambda c: char_map.get(c))))
    image_chars.append(charRow)
print(image_chars)
