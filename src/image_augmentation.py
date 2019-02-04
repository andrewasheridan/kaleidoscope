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
from itertools import takewhile
import cv2
import time
import glob
import boto3
import os
from subprocess import call


class BaseImageAugmenter(object):

    def __init__(self, image, image_name, num_transformations):
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
        """Summary
        
        Returns
        -------
        TYPE
            Description
        """
        print("_generate_transformations")
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
        print("_generate_augmented_image_names")
        # reverse the string and grab the text between the `.` and first `/` then reverse back
        s = self._image_name[::-1]
        s = "".join(takewhile(lambda x: x != "/", s))[::-1]

        words_to_append = self._generate_chars_to_append()
        name, extension = s.split(".")
        aug_image_names = [self._image_name[:-len(s)] + name + word + "." + extension for word in words_to_append]
        aug_image_names.sort(key=lambda item: (len(item), item))
        print("_generate_augmented_image_names end")
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
        print("_generate_chars_to_append")
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
        print("_generate_chars_to_append end")
        return words


class ImageAugmenter(BaseImageAugmenter):

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
        )
        print("ImageAugmenter")
        # TODO: Change behavior to calling generate_images and save directly
        self._images = self.generate_images()
        if save:
            self.save()

    def generate_images(self):
        """Summary
        
        Returns
        -------
        TYPE
            Description
        """
        print("generate_images")
        images = {}

        for mod in self._aug_image_names:
            name, extension = mod.split(".")

            f = self._transformations[name[-1:]]

            new_image = self.image.copy()
            images[mod] = f(new_image, self._image_name)
        print("generate_images end")
        return images

    # TODO: Change save from local to S3
    def save(self):
        """Summary
        """
        print("save")
        s3 = boto3.resource('s3', region_name='us-east-1')
        dest_bucket = s3.Bucket('chainsaw-augmented-images')

        temp_save_dir = './aug_img_tmp/'

        for image_name in self._images:
            # print()
            print("image_name")
            
            os.makedirs(os.path.dirname(temp_save_dir + image_name), exist_ok=True)
            cv2.imwrite(temp_save_dir + image_name, self._images[image_name])
            # print(glob.glob("*"))
            # print(glob.glob(temp_save_dir + "*"))
            # dest_loc = temp_save_dir + image_name
            # dest_loc = dest_loc[2:]
            total = 0 
            for root, dirs, files in os.walk(temp_save_dir): 
                total += len(files) 
            # print('total files = {}'.format(total))
            # dest_bucket.upload_file(temp_save_dir + image_name,image_name)
        print('attempting s3 sync')
        os.system("aws s3 sync " + temp_save_dir + " s3://chainsaw-augmented-images")
        print('after s3 sync attempt')

        # cv2.imwrite(temp_save_dir + self._image_name, self.image) # base image should save it...
        # images_to_upload = glob.glob(temp_save_dir + "*")



        

        # for fn in images_to_upload:
            # dest_bucket.upload_file(fn, fn)




