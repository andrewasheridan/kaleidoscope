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

# This environmental variable is set in the Docker Container the script runs in
# It is set when the Pod is created with `kubectl create -f job.yaml` or during Interface().transform()
DESTINATION_S3 = os.environ["DESTINATION_S3"]


class KaleidoscopeAugmenter(object):
    def __init__(self, image, image_name, num_transformations):
        """
        Augments `image` by chaining together transformations. Saves to S3 bucket.

        :param image: Raw original image, 2d 3-channel np.ndarray
        :param image_name: filename of the original image
        :param num_transformations: how many transformations to chain for this image
        """
        self._image_name = image_name

        # normalize the original image size before transforming
        self._image = self._resize_raw_image(image)

        # TODO: Pass in a list of transformation functions as an argument instead of using a hardcoded list
        # Only have 6 transformations currently, and only want to do one of each type
        if num_transformations <= constants.NUM_POSSIBLE_TRANSFORMS:
            self._num_transformations = num_transformations
        else:
            raise ValueError(
                "No more than {} transformations possible.".format(
                    constants.NUM_POSSIBLE_TRANSFORMS
                )
            )
        self._transforms = self._generate_shuffled_transforms()

        # _aug_image_names are used as a guide to apply the transformations
        self._aug_image_names = self._generate_augmented_image_names()

        self._images = self._generate_images()
        self._save()

    @staticmethod
    def _resize_raw_image(image):
        """
        Re-sizes the raw image into a randomly cropped square
        """

        # TODO: Add conversion to ndarray when possible
        # NOTE: Is `image` ever NOT an ndarray?
        if type(image) is ndarray:
            return transformations.random_square_crop_with_resize(image)
        else:
            raise TypeError("`image` must be np.ndarray not {}".format(type(image)))

    def _generate_shuffled_transforms(self):
        """
        Shuffles the transformation list so it is different for each original image
        :return: Dict of transformations
        """

        possible_transforms = [
            transformations.rotate_and_zoom,
            transformations.adjust_contrast,
            transformations.adjust_brightness,
            transformations.adjust_saturation,
            transformations.flip_left_right,
            transformations.noisy,
        ]
        shuffle(possible_transforms)

        # keys are letters ("a", "b", etc)
        # values are transformation functions
        transforms = {ascii_lowercase[i]: possible_transforms[i] for i in range(0, self._num_transformations)}
        return transforms

    def _generate_augmented_image_names(self):
        """
        Generates new file names for the augmented images images
        :return: list of filenames
        """

        # from `path/filename.extension` get filename
        # this looks the same as os.basename(path)
        # TODO: test os.basename(_image_name)
        s = self._image_name[::-1]
        s = "".join(takewhile(lambda x: x != "/", s))[::-1]

        # add chars to end of filename, before extension
        words_to_append = self._generate_chars_to_append()
        name, extension = s.split(".")
        aug_image_names = [
            self._image_name[: -len(s)] + name + word + "." + extension
            for word in words_to_append
        ]

        # sort the names, shortest first, then alphabetical
        aug_image_names.sort(key=lambda item: (len(item), item))
        return aug_image_names

    # TODO: Explain how this works and provide example
    # TODO: Find a slicker way
    # Note: Maybe move this function up above _generate_augmented_image_names
    def _generate_chars_to_append(self):
        """
        Generates a list of characters.

        :usage:
        _generate_chars_to_append(4)
        output : ['d', 'c', 'cd', 'b', 'bd', 'bc', bcd', 'a', 'ad', 'ac', acd', 'ab', 'abd', 'abc', 'abcd']

        This list is used to keep track of which images need which transformations.

        :return:
        """

        # NOTE: there is *surely* a slicker way to do this.
        # Trying to do https://stackoverflow.com/a/16241785/10918177 but with letters
        words = []

        # Generate the (unordered) sets and represent them with a set of bits.
        for i in range(1, 1 << self._num_transformations):
            s = "{0:0{1:d}b}".format(i, self._num_transformations)
            word = ""

            # generate the corresponding letters
            # 0001 = "a", 0010 = "b", etc
            for j in range(0, self._num_transformations):
                if s[j] == "1":
                    word += ascii_lowercase[j]

            words.append(word)
        return words

    def _generate_images(self):
        """
        Generates the augmented images by applying transformations according to the names in _aug_image_names
        :return: dict of images
        """

        # keys = image names
        # values = transformed image
        images = {}

        for augmented_name in self._aug_image_names:
            name, extension = augmented_name.split(".")

            # take the last character of `name` and use it as a key to get a transform
            transform = self._transforms[name[-1:]]

            new_image = self._image.copy()
            images[augmented_name] = transform(new_image, self._image_name)
        return images

    def _save(self):
        """
        Save the collection of images to S3
        :return:
        """
        # NOTE: This would be faster if it skipped the 'save locally' step
        for image_name in self._images:

            os.makedirs(
                os.path.dirname(constants.TMP_SAVE_DIR + image_name), exist_ok=True
            )

            # save locally
            cv2.imwrite(constants.TMP_SAVE_DIR + image_name, self._images[image_name])

        # TODO: Test using boto3 instead of a call the command line.
        os.system(
            "aws s3 cp "
            + constants.TMP_SAVE_DIR
            + f" s3://{DESTINATION_S3} --recursive --quiet"
        )

        # delete the local files
        shutil.rmtree(constants.TMP_SAVE_DIR)
