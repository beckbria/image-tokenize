# trimImage removed empty rows and columns from the border of an image
# Input:
#     Type <pixel> is an np.ndarray corresponding to the number of bytes in a pixel of the image
#     image_numpy: np.ndarray[rows, cols]<pixel> - an image containing a series of characters on a
#            constant background color. Rows of characters are separated by
#            at least one line of solid bgcolor pixels
#     background: pixel (np.ndarray)
# Return:
#     image np.ndarray<pixel>
def trimImage(image_numpy, background):
    row_count, col_count, _ = image_numpy.shape
    first_row = -1
    last_row = -1
    first_col = -1
    last_col = -1
    for idx, row in enumerate(image_numpy):
        blank = (row == background).all()
        if not blank:
            last_row = idx
            if first_row < 0:
                first_row = idx
    for idx in range(col_count):
        column = image_numpy[:, idx, :]
        blank = (column == background).all()
        if not blank:
            last_col = idx
            if first_col < 0:
                first_col = idx
    return image_numpy[first_row : last_row + 1, first_col : last_col + 1]


# horizontalSegments finds rows of characters in the source image and returns
# then as an array.
# Input:
#     Type <pixel> is an np.ndarray corresponding to the number of bytes in a pixel of the image
#     image_numpy: np.ndarray[rows, cols]<pixel> - an image containing a series of characters on a
#            constant background color. Rows of characters are separated by
#            at least one line of solid bgcolor pixels
#     background: pixel (np.ndarray)
#     minimum_height: minimum row height. If a segment is detected with fewer than this number of pixels,
#            the row will continue until that many are found. Defaults to 1.
# Return:
#     List of image np.ndarray<pixel>
def horizontalSegments(image_numpy, background, minimum_height=1):
    image_rows_numpy = []
    found_char = False
    start = -1
    for idx, row in enumerate(image_numpy):
        blank = (row == background).all()
        if blank and found_char:
            height = (idx - start) + 1
            if height < minimum_height:
                continue
            # We have reached the end of a row of characters
            image_rows_numpy.append(image_numpy[start:idx])
            found_char = False
        elif not blank and not found_char:
            # We have found the start of a row of characters
            found_char = True
            start = idx
    # See if we ended in a row
    if found_char:
        image_rows_numpy.append(image_numpy[start:])
    return image_rows_numpy


# verticalSegments finds rows of characters in the source image and returns
# then as an array.
# Input:
#     Type <pixel> is an np.ndarray corresponding to the number of bytes in a pixel of the image
#     image_numpy: np.ndarray[rows, cols]<pixel> - an image containing a series of characters on a
#            constant background color. Rows of characters are separated by
#            at least one line of solid bgcolor pixels
#     background: pixel (np.ndarray)
#     trim: Should empty rows/columns be removed from images after tokenizing? Defaults to True.
#     minimum_width: minimum character width. If a segment is detected with fewer than this number
#            of pixels, the row will continue until that many are found. Defaults to 1.
# Return:
#     List of image np.ndarray<pixel>
def verticalSegments(image_numpy, background, trim=True, minimum_width=1):
    row_count, col_count, _ = image_numpy.shape
    found_char = False
    chars = []
    start = -1
    for idx in range(col_count):
        column = image_numpy[:, idx, :]
        blank = (column == background).all()
        if blank and found_char:
            width = (idx - start) + 1
            if width < minimum_width:
                continue
            # We have reached the end of a character
            char = image_numpy[:, start:idx]
            chars.append(trimImage(char, background))
            found_char = False
        elif not blank and not found_char:
            # We have found the start of a row of characters
            found_char = True
            start = idx
    # See if we ended in a column
    if found_char:
        char = image_numpy[:, start:]
        chars.append(trimImage(char, background))
    return chars
