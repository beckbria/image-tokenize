import imageio.v3 as iio

# TODO: Take these constants as command line arguments
filename = "mit_2024_i_write_these_words.png"
bgcolor = (255, 255, 255)

# https://imageio.readthedocs.io/
im = iio.imread(filename)
#print(im.shape)

# imageRowsRaw = findRows(im)    # findRows(im, bgcolor)
# imageRows = list(imageRowsRaw.map(lambda r: r -> splitChars(r)))
# charMap = buildCharMap(imageRows)
# imageChars = transcribe(imageRows, charMap)
# print(imageChars)