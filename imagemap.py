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
    # Input: image_pil: A PIL Image or a list of PIL images
    # Return: The letter corresponding to this image
    def ensureExists(self, image_pil):
        if isinstance(image_pil, list):
            ret = True
            for im in image_pil:
                ret = self.ensureExists(im) and ret
            return ret

        if type(image_pil) is not Image.Image:
            raise Exception("Image of incorrect type " + str(type(image_pil)))

        hash = ImageToLetterMap.__imageHash(image_pil)
        existing = self.__get(hash)
        if existing is not None:
            # DO_NOT_SUBMIT
            print("Found duplicate ", existing)
            return existing

        if self.__next_char_index >= len(self.__valid_characters):
            raise Exception("Too many distinct images")

        letter = self.__valid_characters[self.__next_char_index]
        # DO_NOT_SUBMIT
        print("Inserting letter ", letter)
        self.__lookup.append(ImageToLetterMapEntry(hash=hash, letter=letter))
        self.__next_char_index = self.__next_char_index + 1
        return letter

    def get(self, image_pil):
        return self.__get(ImageToLetterMap.__imageHash(image_pil))

    def __get(self, hash):
        for known in self.__lookup:
            if known.hash == hash:
                return known.letter
        return None

    @staticmethod
    def __imageHash(image_pil):
        # Too Permissive
        # return imagehash.crop_resistant_hash(image_pil)
        # Doesn't tolerate different subpixel crops
        # return imagehash.average_hash(image_pil)

    # REMOVE AFTER DEBUGGING: Public version of the private hash function for testing
    @staticmethod
    def ImageHash(image_pil):
        return ImageToLetterMap.__imageHash(image_pil)
