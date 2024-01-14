import imageio.v3 as iio
import numpy as np

# TODO: Take these constants as command line arguments
filename = "mit_2024_i_write_these_words.png"
bg_color = np.array([255,255,255])
min_height = 40
ignore_alpha = True

# Debug output
debug_find_rows = False
debug_find_chars = False
debug_trim = False
debug_char_map = True

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
        column = image[:,idx,:]
        blank = (column == background).all()
        if not blank:
            last_col = idx
            if first_col < 0:
                first_col = idx
    return image[first_row:last_row+1,first_col:last_col+1]

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
#     trim: Should empty rows/columns be removed from images after tokenizing? Defaults to True.
#     minimum_width: minimum character width. If a segment is detected with fewer than this number 
#            of pixels, the row will continue until that many are found. Defaults to 1.
# Return:
#     List of image np.ndarray<pixel>
def verticalSegments(image, background, trim = True, minimum_width = 1):
    row_count, col_count, _ = image.shape
    found_char = False
    chars = []
    start = -1
    for idx in range(col_count):
        column = image[:,idx,:]
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

# ImageToLetterMap represents a map from an image to a latin letter which can be used in a 
# cryptogram
class ImageToLetterMap:
    upper_case = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]

    lower_case = [
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'
    ]

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    # Initialize a map from an array of image
    # Input:
    #     images: An iterable (numpy array or list) of images, where an image is 
    #             np.ndarray[rows, cols]<pixel>
    #     output_chars: list of characters valid as output
    def __init__(self, images = [], output_chars = upper_case):
        self.__valid_characters = output_chars
        # TODO: ensure every entry in output_chars is unique
        self.__lookup = {}
        self.__next_char_index = 0
        for im in images:
            self.ensureExists(im)

    # Ensure a record for an image exists in the map. 
    # Input:
    #     images: An iterable (numpy array or list) of images, where an image is 
    #             np.ndarray[rows, cols]<pixel>
    # Return:
    #     Boolean: whether the element existed before calling this function
    def ensureExists(self, image):
        hash = ImageToLetterMap.__imageHash(image)
        if hash in self.__lookup:
            return True
        if self.__next_char_index >= len(self.__valid_characters):
            raise Exception("Too many distinct images")
        self.__lookup[hash] = self.__valid_characters[self.__next_char_index]
        self.__next_char_index = self.__next_char_index + 1
        return False

    def get(self, image):
        return self.__lookup[ImageToLetterMap.__imageHash(image)]

    # __imageHash produces a hash of an ndarray which can be used as the key in a hash table
    # Input:
    #
    # Return:
    #   hash: byte array
    @staticmethod
    def __imageHash(image):
        # Identifying different images is an interesting problem:
        #   * ndarray.toBytes() is tempting but sinze our characters can be of different sizes this
        #     is dangerous i.e. np.zeroes(3,2) has the same bytes as np.zeroes(2,3)
        #   * Stringifying is huge and expensive
        # Proposal: Use the bytes representation with the dimensions prepended
        return str.encode(str(image.shape)) + image.tobytes()

    # REMOVE AFTER DEBUGGING: Public version of the private hash function for testing
    @staticmethod
    def ImageHash(image):
        return ImageToLetterMap.__imageHash(image)

# https://imageio.readthedocs.io/
im = iio.imread(filename)
if ignore_alpha:
    # Remove the alpha channel
    im = im[:,:,:3]

image_rows_raw = horizontalSegments(im, bg_color, min_height)
if debug_find_rows:
    print("Found ", len(image_rows_raw), " rows of sizes: ")
    for row in image_rows_raw:
        print(row.shape)

image_rows = list(map(lambda r: verticalSegments(r, bg_color), image_rows_raw))
if debug_find_chars:
    for r, row in enumerate(image_rows):
        print("Row ", r, " contains ", len(row), " characters")
if debug_trim:
    for r, row in enumerate(image_rows):
        sizes = list(map(lambda r: r.shape, row))
        print("Row ", r, " sizes: ", sizes)

char_map = ImageToLetterMap(output_chars = ImageToLetterMap.upper_case + ImageToLetterMap.lower_case)

# TODO: Row 0 characters 5, 7, 17 should be identical.  Confirm that they are being detected as such.
# They have different sizes: 
# 5: (33, 27, 3)
# 7: (35, 37, 3)
# 17: (33, 32, 3)
# Guess I'll have to dump to images and inspect
# Another reason to look into image similarity....
# row0 = image_rows[0]
# hash5 = ImageToLetterMap.ImageHash(row0[5])
# print(type(hash5))
# hash7 = ImageToLetterMap.ImageHash(row0[7])
# hash17 = ImageToLetterMap.ImageHash(row0[17])
# print("5=7: ", hash5 == hash7)
# print("5=17: ", hash5 == hash17)
# print("7=17: ", hash7 == hash17)
# print("5: \n", hash5, "\n\n")
# print("7: \n", hash7, "\n\n")
# print("17: \n", hash17, "\n\n")

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