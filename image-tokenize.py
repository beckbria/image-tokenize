import imageio.v3 as iio
import numpy as np

# TODO: Take these constants as command line arguments
filename = "mit_2024_i_write_these_words.png"
bg_color = np.array([255,255,255])
min_height = 40

# Debug output
debug_find_rows = False
debug_find_chars = False

# trimImage removed empty rows and columns from the border of an image
# Input:
#     Type <pixel> is an np.ndarray corresponding to the number of bytes in a pixel of the image
#     image: np.ndarray[rows, cols]<pixel> - an image containing a series of characters on a 
#            constant background color. Rows of characters are separated by
#            at least one line of solid bgcolor pixels
#     background: pixel (np.ndarray)
def trimImage(image, background):
    # TODO
    return image

# horizontalSegments finds rows of characters in the source image and returns 
# then as an array.  
# Input:
#     Type <pixel> is an np.ndarray corresponding to the number of bytes in a pixel of the image
#     image: np.ndarray[rows, cols]<pixel> - an image containing a series of characters on a 
#            constant background color. Rows of characters are separated by
#            at least one line of solid bgcolor pixels
#     background: pixel (np.ndarray)
#     minimum_height: minimum row height. If a segment is detected with fewer than this number of pixels,
#            the row will continue until that many are found    
def horizontalSegments(image, background, minimum_height = 1):
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
#     minimum_width: minimum character width. If a segment is detected with fewer than this number 
#            of pixels, the row will continue until that many are found  
def verticalSegments(image, background, minimum_width = 1):
    # TODO: Should we have a parameter to not trim characters?  For now trim them
    row_count, col_count, _ = image.shape
    found_char = False
    chars = []
    start = -1
    for idx in range(col_count):
        column = image[:,idx,:]
        # if debug_find_chars:
        #     print(column)
        blank = (column == background).all()
        if blank and found_char:
            width = (idx - start) + 1
            if width < minimum_width:
                continue
            # We have reached the end of a character
            char = image[:,start:idx]
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
        char = image[:,start:]
        chars.append(trimImage(char, background))
    return chars

# https://imageio.readthedocs.io/
im = iio.imread(filename)
# Remove the alpha channel
im = im[:,:,:3]

image_rows_raw = horizontalSegments(im, bg_color, min_height)
if debug_find_rows:
    print("Found ", len(image_rows_raw), " rows of sizes: ")
    for row in image_rows_raw:
        print(row.shape)

# Problem: some rows are 41px high, some are 42px high. 
# Immediate problem: should we prepend or append an empty row in the 41px?
# Long-term: how do we detect this more reliably?  Image similarity?
#     Proposed solution: After splitting into characters, trim empty rows from characters
#     Not every character will be the same height but that's OK so long as every instance
#     of the character is the same

image_rows = list(map(lambda r: verticalSegments(r, bg_color), image_rows_raw))
if debug_find_chars:
    for r, row in enumerate(image_rows):
        print("Row ", r, " contains ", len(row), " characters")

# char_map = buildCharMap(image_rows)
# image_chars = transcribe(image_rows, char_map)
# print(image_chars)