import imageio.v3 as iio
import numpy as np

# TODO: Take these constants as command line arguments
filename = "mit_2024_i_write_these_words.png"
bg_color = np.array([255,255,255])

# findRows finds rows of characters in the source image and returns 
# then as an array.  
# Input:
#     Type <pixel> is an np.ndarray corresponding to the number of bytes in a pixel of the image
#     image: np.ndarray[rows, cols]<pixel> - an image containing a series of characters on a 
#            constant background color. Rows of characters are separated by
#            at least one line of solid bgcolor pixels
#     background: pixel (np.ndarray)
#     
def findRows(image, background):
    rows, cols, _ = image.shape
    image_rows = []
    found_char = False
    start = -1
    for idx, row in enumerate(image):
        blank = (row == background).all()
        if blank and found_char:
            # We have reached the end of a row of characters
            image_rows.append(image[start:idx])
            # DO_NOT_SUBMIT
            print("Found chars from row ", start, " to row ", idx)
            found_char = False
        elif not blank and not found_char:
            # We have found the start of a row of characters
            found_char = True
            start = idx
    # See if we ended in a row
    if found_char:
        # DO_NOT_SUBMIT
        print("Found chars from row ", start, " to end")
        image_rows.append(image[start:])
    return image_rows


# https://imageio.readthedocs.io/
im = iio.imread(filename)
# Remove the alpha channel
im = im[:,:,:3]

image_rows_raw = findRows(im, bg_color)
print("Found ", len(image_rows_raw), " rows of sizes: ")
for row in image_rows_raw:
    print(row.shape)

# Problem: some rows are 41px high, some are 42px high, some are 5px followed by 35px (with one empty line?)
# I don't see the empty line in the image, looking closer....

# image_rows = list(image_rowsRaw.map(lambda r: r -> splitChars(r)))
# char_map = buildCharMap(image_rows)
# image_chars = transcribe(image_rows, char_map)
# print(image_chars)