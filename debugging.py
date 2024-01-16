import imageio.v3 as iio
from imagemap import ImageToLetterMap
import os


def writeFilesBySize(image_rows_numpy):
    # Calculate distinct image shapes
    dimensionMap = {}
    for rowIdx, row in enumerate(image_rows_numpy):
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


def printSizes(image_rows_numpy):
    for r, row in enumerate(image_rows_numpy):
        sizes = list(map(lambda r: r.shape, row))
        print("Row ", r, " sizes: ", sizes)


def verifyEqualGlyphs(image_rows_pil):
    # Row 0 characters 3, 6, 16 should be identical.  Confirm that they are being detected as such.
    row0 = image_rows_pil[0]
    r0c04 = row0[4]
    r0c06 = row0[6]
    r0c16 = row0[16]
    hash04 = ImageToLetterMap.ImageHash(r0c04)
    hash06 = ImageToLetterMap.ImageHash(r0c06)
    hash16 = ImageToLetterMap.ImageHash(r0c16)
    print("4=6: ", hash04 == hash06)
    print("4=16: ", hash04 == hash16)
    print("6=16: ", hash06 == hash16)
