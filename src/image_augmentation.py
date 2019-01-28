"""image_augmentation.py
    
    Holds image augmentation classes, but not trasformations (see transoformations.py)
"""

# TODO: Cleanup Imports
from numpy import ndarray, sin, deg2rad
from string import ascii_lowercase
from transformations import random_square_crop_with_resize
from transformations import rotate_and_zoom
from transformations import adjust_contrast
from transformations import adjust_brightness
from transformations import adjust_saturation
from transformations import flip_left_right
from transformations import noisy
from random import shuffle, randint
from tools import get_image_name_from_path
import cv2
import time


class BaseImageAugmenter(object):

    def __init__(self, image_name, num_transformations, save=True):
        """Base class for ImageAugmenter
        
        Parameters
        ----------
        image_name : str
            Image name with extension ex: `dog.jpg`
        num_transformations : int
            Number of randomt transformations to apply
        save : bool, optional, default=True
            For debugging - Anything not saved is lost
        """
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
        """Summary
        
        Returns
        -------
        TYPE
            Description
        """
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

        # print(self._aug_image_names)

    def _generate_augmented_image_names(self):
        """Summary
        
        Returns
        -------
        TYPE
            Description
        """
        words_to_append = self._generate_chars_to_append()
        name, extension = self._image_name.split(".")
        aug_image_names = [name + word + "." + extension for word in words_to_append]
        aug_image_names.sort(key=lambda item: (len(item), item))
        return aug_image_names

    # TODO: Explain how this works and provide example
    # TODO: Find a slicker way
    def _generate_chars_to_append(self):
        """Summary
        
        Returns
        -------
        TYPE
            Description
        """
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


class ImageAugmenter(object):

    """Summary
    
    Attributes
    ----------
    image : TYPE
        Description
    """

    def __init__(self, image, image_name, num_transformations, save=True):
        """Summary
        
        Parameters
        ----------
        image : TYPE
            Description
        image_name : TYPE
            Description
        num_transformations : TYPE
            Description
        save : bool, optional
            Description
        
        Raises
        ------
        TypeError
            Description
        ValueError
            Description
        """
        BaseImageAugmenter.__init__(
            self,
            image=image,
            image_name=image_name,
            num_transformations=num_transformations,
            save=save,
        )
        
        # TODO: Change behavior to calling transform and save directly
        self._images = self.transform()
        if save:
            self.save()



    def transform(self):
        """Summary
        
        Returns
        -------
        TYPE
            Description
        """
        images = {}

        for mod in self._aug_image_names:
            name, extension = mod.split(".")

            f = self._transformations[name[-1:]]

            new_image = self.image.copy()
            images[mod] = f(new_image, self._image_name)

        return images

    # TODO: Change save from local to S3
    def save(self, dir="../auger/"):
        """Summary
        """
        for image_name in self._images:
            cv2.imwrite(dir + image_name, self._images[image_name])
            cv2.imwrite(dir + self._image_name, self.image)


# import cv2
# import glob
# import sys

# problems = []
# start = time.time()
# print("starting at {}".format(start))
# fns = glob.glob("../downloaded_images/*")
# n = len(fns)
# for i, fn in enumerate(fns):
#     image = cv2.imread(fn)
#     image_name = get_image_name_from_path(fn)
#     try:
#       augmenter = ImageAugmenter(image, image_name, 1, save=False)
#     except:
#       problems.append(image_name)

#     sys.stdout.write("\r{:2.4f}%".format(100 * (i + 1) / n))


# print('\n')
# end = time.time()
# print(end - start)
# print(problems)


# image = cv2.imread("../downloaded_images/10243.jpg")
