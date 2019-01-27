from numpy import ndarray


class ImageAugmenter(object):

    def __init__(self, image, image_name, transformations):

        if type(image) is ndarray:
            self.image = image
        else:
            raise TypeError(
                "`image` must be numpy array not {}".format(type(image))
            )

        if type(image_name) is str:
            self.image_name = image_name
        else:
            raise TypeError(
                "`image_name` must be str not {}".format(type(image_name))
            )

        if type(transformations) is list:
            self.transformations = transformations
        else:
            raise TypeError(
                "`transformations` must be list not {}".format(type(transformations))
            )



