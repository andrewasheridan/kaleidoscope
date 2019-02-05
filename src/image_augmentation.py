"""image_augmentation.py
    
    Holds image augmentation classes, but not trasformations (see transoformations.py)
"""

# TODO: Cleanup Imports
from numpy import ndarray
from string import ascii_lowercase
from transformations import random_square_crop_with_resize
from transformations import rotate_and_zoom
from transformations import adjust_contrast
from transformations import adjust_brightness
from transformations import adjust_saturation
from transformations import flip_left_right
from transformations import noisy
from random import shuffle
from itertools import takewhile
import cv2
import os
import shutil


class BaseImageAugmenter(object):

    def __init__(self, image, image_name, num_transformations):

        print("BaseImageAugmenter:")
        # TODO: Add conversion to ndarray when possible
        if type(image) is ndarray:
            self.image = random_square_crop_with_resize(image)
        else:
            raise TypeError(
                "`image` must be np.ndarray not {}".format(type(image))
            )

        # TODO: Add conversino to str when possible
        if type(image_name) is str:
            self._image_name = image_name
        else:
            raise TypeError("`image_name` must be str not {}".format(type(image_name)))

        # TODO: Pass in preset list of transformations instead of a list
        # Only have 6 transformations currently
        if num_transformations <= 6:
            self._num_transformations = num_transformations
        else:
            raise ValueError("No more than 6 transformations possible.")

        self._aug_image_names = self._generate_augmented_image_names()
        self._transformations = self._generate_transformations()

    def _generate_transformations(self):

        n = self._num_transformations
        rand_tees = [
            rotate_and_zoom,
            adjust_contrast,
            adjust_brightness,
            adjust_saturation,
            flip_left_right,
            noisy,
        ]
        shuffle(rand_tees)
        
        transformations = {ascii_lowercase[i]: rand_tees[i] for i in range(0, n)}
        return transformations


    def _generate_augmented_image_names(self):

        # reverse the string and grab the text between the `.` and first `/` then reverse back
        s = self._image_name[::-1]
        s = "".join(takewhile(lambda x: x != "/", s))[::-1]

        words_to_append = self._generate_chars_to_append()
        name, extension = s.split(".")
        aug_image_names = [self._image_name[:-len(s)] + name + word + "." + extension for word in words_to_append]
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


class KaleidoscopeAugmenter(BaseImageAugmenter):
    def __init__(self, image, image_name, num_transformations, save=True):

        BaseImageAugmenter.__init__(
            self,
            image=image,
            image_name=image_name,
            num_transformations=num_transformations,
        )
        # TODO: Change behavior to calling generate_images and save directly
        self._images = self.generate_images()
        if save:
            self.save()

    def generate_images(self):

        images = {}

        for mod in self._aug_image_names:
            name, extension = mod.split(".")

            f = self._transformations[name[-1:]]

            new_image = self.image.copy()
            images[mod] = f(new_image, self._image_name)
        return images

    def save(self):

        temp_save_dir = './aug_img_tmp/'

        for image_name in self._images:

            os.makedirs(os.path.dirname(temp_save_dir + image_name), exist_ok=True)
            cv2.imwrite(temp_save_dir + image_name, self._images[image_name])

        os.system("aws s3 cp " + temp_save_dir + " s3://chainsaw-augmented-images --recursive")
        shutil.rmtree(temp_save_dir)
