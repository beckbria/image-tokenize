import imagehash
from PIL import Image


class ImageToLetterMapEntry:
    def __init__(self, hash, letter):
        self.hash = hash
        self.letter = letter


# ImageToLetterMap represents a map from an image to a latin letter which can be used in a
# cryptogram
class ImageToLetterMap:
    upper_case = [*"ABCDEFGHIJKLMNOPQRSTUVWXYZ"]

    lower_case = [*"abcdefghijklmnopqrstuvwxyz"]

    numbers = [*"0123456789"]

    # Initialize a map from an array of image
    # Input:
    #     images: An iterable (numpy array or list) of images, where an image is
    #             np.ndarray[rows, cols]<pixel>
    #     output_chars: list of characters valid as output
    def __init__(self, images=[], output_chars=upper_case):
        self.__valid_characters = output_chars
        # TODO: ensure every entry in output_chars is unique
        self.__lookup = []
        self.__next_char_index = 0
        for im in images:
            self.ensureExists(im)

    # Ensure a record for an image exists in the map.
    # Input:
    #     image: A PIL Image or a list of PIL images
    # Return:
    #     Boolean: whether the element existed before calling this function
    def ensureExists(self, image_pil):
        if isinstance(image_pil, list):
            ret = True
            for im in image_pil:
                ret = self.ensureExists(im) and ret
            return ret

        if type(image_pil) is not Image.Image:
            raise Exception("Image of incorrect type " + str(type(image_pil)))

        if self.get(image_pil) is not None:
            return True

        if self.__next_char_index >= len(self.__valid_characters):
            raise Exception("Too many distinct images")

        self.__lookup.append(
            ImageToLetterMapEntry(
                hash=ImageToLetterMap.__imageHash(image_pil),
                letter=self.__valid_characters[self.__next_char_index],
            )
        )
        self.__next_char_index = self.__next_char_index + 1
        return False

    def get(self, image_pil):
        hash = ImageToLetterMap.__imageHash(image_pil)
        for known in self.__lookup:
            if known.hash == hash:
                return known.letter
        return None

    # __imageHash produces a hash of an ndarray which can be used as the key in a hash table
    # Input:
    #
    # Return:
    #   hash: byte array
    @staticmethod
    def __imageHash(image_pil):
        # Identifying different images is an interesting problem:
        #   * ndarray.toBytes() is tempting but sinze our characters can be of different sizes this
        #     is dangerous i.e. np.zeroes(3,2) has the same bytes as np.zeroes(2,3)
        #   * Stringifying is huge and expensive
        # Proposal: Use the bytes representation with the dimensions prepended
        # return str.encode(str(image.shape)) + image.tobytes()
        return imagehash.crop_resistant_hash(image_pil)

    # REMOVE AFTER DEBUGGING: Public version of the private hash function for testing
    @staticmethod
    def ImageHash(image_pil):
        return ImageToLetterMap.__imageHash(image_pil)
