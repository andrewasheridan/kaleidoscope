#                                         _
#                                        | |
#   __ _ _   _  __ _ _ __ ___   ___ _ __ | |_ ___ _ __
#  / _` | | | |/ _` | '_ ` _ \ / _ \ '_ \| __/ _ \ '__|
# | (_| | |_| | (_| | | | | | |  __/ | | | ||  __/ |
#  \__,_|\__,_|\__, |_| |_| |_|\___|_| |_|\__\___|_|
#               __/ |
#              |___/
"""image_augmenter.py

    Holds image augmentation class KaleidoscopeAugmenter
"""
import constants
import cv2
import os
import shutil
import transformations

from itertools import takewhile
from numpy import ndarray
from random import shuffle
from string import ascii_lowercase


class KaleidoscopeAugmenter(object):

    def __init__(self, image, image_name, num_transformations, save=True):

        self._image = self._resize_raw_image(image)
        self._image_name = image_name

        # TODO: Pass in preset list of transformations instead of a list
        # Only have 6 transformations currently
        if num_transformations <= constants.NUM_POSSIBLE_TRANSFORMS:
            self._num_transformations = num_transformations
        else:
            raise ValueError("No more than {} transformations possible.".format(constants.NUM_POSSIBLE_TRANSFORMS))

        self._aug_image_names = self._generate_augmented_image_names()
        self._transforms = self._generate_shuffled_transforms()

        # TODO: Change behavior to calling generate_images and save directly
        self._images = self.generate_images()
        if save:
            self.save()

    @staticmethod
    def _resize_raw_image(image):

        # TODO: Add conversion to ndarray when possible
        if type(image) is ndarray:
            return transformations.random_square_crop_with_resize(image)
        else:
            raise TypeError(
                "`image` must be np.ndarray not {}".format(type(image))
            )

    def _generate_shuffled_transforms(self):

        n = self._num_transformations
        rand_tees = [
            transformations.rotate_and_zoom,
            transformations.adjust_contrast,
            transformations.adjust_brightness,
            transformations.adjust_saturation,
            transformations.flip_left_right,
            transformations.noisy,
        ]
        shuffle(rand_tees)
        
        transforms = {ascii_lowercase[i]: rand_tees[i] for i in range(0, n)}
        return transforms

    def _generate_augmented_image_names(self):

        # reverse the string and grab the text between the `.` and first `/` then reverse back
        s = self._image_name[::-1]
        s = "".join(takewhile(lambda x: x != "/", s))[::-1]

        words_to_append = self._generate_chars_to_append()
        name, extension = s.split(".")
        aug_image_names = [
            self._image_name[:-len(s)] + name + word + "." + extension
            for word in words_to_append
        ]
        aug_image_names.sort(key=lambda item: (len(item), item))
        return aug_image_names

    # TODO: Explain how this works and provide example
    # TODO: Find a slicker way
    def _generate_chars_to_append(self):

        # NOTE: there is *surely* a slicker way to do this
        # trying to do https://stackoverflow.com/a/16241785/10918177
        # but with letters
        n = self._num_transformations
        words = []

        for i in range(1, 1 << n):
            s = "{0:0{1:d}b}".format(i, n)
            word = ""

            for j in range(0, n):
                if s[j] == "1":
                    word += ascii_lowercase[j]

            words.append(word)
        return words

    def generate_images(self):

        images = {}

        for mod in self._aug_image_names:
            name, extension = mod.split(".")

            transform = self._transforms[name[-1:]]

            new_image = self._image.copy()
            images[mod] = transform(new_image, self._image_name)
        return images

    def save(self):

        for image_name in self._images:

            os.makedirs(os.path.dirname(constants.TMP_SAVE_DIR + image_name), exist_ok=True)
            cv2.imwrite(constants.TMP_SAVE_DIR + image_name, self._images[image_name])

        os.system("aws s3 cp " + constants.TMP_SAVE_DIR + " s3://chainsaw-augmented-images --recursive")
        shutil.rmtree(constants.TMP_SAVE_DIR)

