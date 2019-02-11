#   _                        __                           _   _
#  | |                      / _|                         | | (_)
#  | |_ _ __ __ _ _ __  ___| |_ ___  _ __ _ __ ___   __ _| |_ _  ___  _ __  ___
#  | __| '__/ _` | '_ \/ __|  _/ _ \| '__| '_ ` _ \ / _` | __| |/ _ \| '_ \/ __|
#  | |_| | | (_| | | | \__ \ || (_) | |  | | | | | | (_| | |_| | (_) | | | \__ \
#   \__|_|  \__,_|_| |_|___/_| \___/|_|  |_| |_| |_|\__,_|\__|_|\___/|_| |_|___/
#
"""
transformations.py

Various transformations used in the ImageAugmenter Class
"""
import cv2
import numpy as np
import random


def random_square_crop_with_resize(
    image, new_side_len=400, interpolation=cv2.INTER_LANCZOS4
):
    """
    Takes in a rectangular image, reshapes it to be a square based on the shortest side,
    re-sizes the square have size `new_side_len`

    :param image: (np.ndarray) - 2d, 3 channel image
    :param new_side_len: side length of the output square image
    :param interpolation: type of resizing interpolation
    :return: re-sized square image
    """

    height, width, _ = image.shape

    # TODO: Catch these `zero-images` before passing into this func
    # Sometimes an image is passed in that has 0 height or width
    # I don't know why exactly, but they don't help, so they gotta go
    if 0 in [height, width]:
        return None

    # FIXME: Code is repeated in both if conditions - abstract this
    if height < width:

        # Shrink proportionally so the shorter side is of size `new_side_len`
        new_height = new_side_len
        new_width = int(width * new_height / height)

        image_resized = cv2.resize(
            image, (new_width, new_height), interpolation=interpolation
        )

        # some images are already square, others need to be made square
        if image_resized.shape[0] == image_resized.shape[1]:
            image_square = image_resized
        else:

            # a square fits inside a rectangle -  figure out the extra space in the image
            extra_width = new_width - new_side_len
            margin = extra_width // 2
            rand_adjustment = random.randint(0, margin) * random.choice([1, -1])

            # take into account the side length not being an even number
            shift = 1 if margin % 2 == 1 else 0

            # crop the rectangle down to a square
            image_square = image_resized[
                :, margin - rand_adjustment : -(margin + shift + rand_adjustment), :
            ]

    # FIXME: Code is repeated in both if conditions - abstract this
    elif width < height:

        # Shrink proportionally so the shorter side is of size `new_side_len`
        new_width = new_side_len
        new_height = int(height * new_width / width)

        image_resized = cv2.resize(
            image, (new_width, new_height), interpolation=interpolation
        )

        # some images are already square, others need to be made square
        if image_resized.shape[0] == image_resized.shape[1]:
            image_square = image_resized
        else:

            # a square fits inside a rectangle -  figure out the extra space in the image
            extra_height = new_height - new_side_len
            margin = extra_height // 2
            rand_adjustment = random.randint(0, margin) * random.choice([1, -1])

            # take into account the side length not being an even number
            shift = 1 if margin % 2 == 1 else 0

            # crop the rectangle down to a square
            image_square = image_resized[
                margin - rand_adjustment : -(margin + shift + rand_adjustment), :, :
            ]

    else:
        # the image is already a square, just resize it
        image_square = cv2.resize(
            image, (new_side_len, new_side_len), interpolation=interpolation
        )

    return image_square


def rotate_and_zoom(image):
    """
    Rotates an image a random amount and zooms in so no blank areas are shown

    :param image: Incoming image (already square)
    :return: randomly rotated image
    """
    side_len = image.shape[0]
    angle = random.randint(1, 359)

    rotation_matrix = cv2.getRotationMatrix2D((side_len // 2, side_len // 2), angle, 1)
    image = cv2.warpAffine(image, rotation_matrix, (side_len, side_len))

    # Given a square image and a fixed `frame` size, when you rotate the image there are areas that will have zeros.
    # To hide the blank areas we zoom the image in, but how much?
    # This formula was found empirically. I assume there is some nice geometry that can provide a better answer.
    # (side length / 8) * sin func that maxes at 45 deg * 1.41 (~ square_root(2))
    x = abs(int(side_len // 8 * np.sin(np.deg2rad(45 + angle // 45 + angle % 45)) * 1.41))
    image = image[x:-x, x:-x, :]
    # the image is now smaller than it should be, because we have cut out the zeroes area

    # resize back to the original size
    image = cv2.resize(image, (side_len, side_len), interpolation=cv2.INTER_LANCZOS4)

    return image


def adjust_contrast(image):
    """
    Randomly adjust the contrast of an image (adjusts the alpha channel)
    :param image: incoming image, should be square
    :return: adjusted image
    """

    # 0.5 <= alpha <= 2.0
    # These values found empirically
    alpha = 0.5 + 1.5 * random.random()
    image = cv2.convertScaleAbs(image, alpha=alpha, beta=0)

    return image


def adjust_brightness(image):
    """
    Randomly adjust the brightness of an image (adjusts the beta channel)
    :param image:  incoming image, should be square
    :return: adjusted image
    """

    # 0 <= beta < 100
    beta = random.random() * 100
    image = cv2.convertScaleAbs(image, alpha=1, beta=beta)

    return image


def adjust_saturation(image):
    """
    Randomly adjust the saturation of an image
    :param image: incoming image, should be square
    :return: adjusted image
    """

    # 0 <= saturation_adjustment < 3
    saturation_adjustment = random.random() * 3

    # break image into hue, saturation, and vibrance
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype("float32")
    hue, saturation, vibrance = cv2.split(img_hsv)

    # apply saturation adjustment to image
    saturation = saturation * saturation_adjustment
    saturation = np.clip(saturation, 0, 255)
    img_hsv = cv2.merge([hue, saturation, vibrance])

    # convert back to regular image format
    image = cv2.cvtColor(img_hsv.astype("uint8"), cv2.COLOR_HSV2BGR)

    return image


def flip_left_right(img):
    """
    Flip the image along the vertical central axis
    :param img: incoming image, should be square
    :return: adjusted image
    """

    img = np.fliplr(img)
    return img


def noisy(image):
    """
    Apply a randomly type of noise to the image
    :param image: incoming image, should be square
    :return: adjusted image
    """

    # XXX: This function looks like a mess
    # FIXME: Just make this better overall
    # NOTE: Why is it all one function and not a few?

    noise_type = random.choice(["gauss", "s&p", "speckle"])

    if noise_type == "gauss":
        # Adds gaussian noise to an image

        height, width, channels = image.shape

        # These values found empirically
        mean = 0
        var = 2
        sigma = var ** 0.5

        # generate gaussian noise
        gauss = np.random.normal(mean, sigma, image.shape)
        gauss = gauss.reshape(height, width, channels)

        # apply noise to image
        noisy_image = image + gauss
        noisy_image = noisy_image.astype("uint8")

        return noisy_image

    elif noise_type == "s&p":
        # Adds `salt and pepper` noise to an image

        prob = 0.01
        #     def add_salt_and_pepper(gb, prob):

        # random number used for selecting pixels to alter
        rnd = np.random.rand(image.shape[0], image.shape[1], image.shape[2])

        # not exactly clear what is happening here
        noisy_image = image.copy()
        noisy_image[rnd < prob] = 0
        noisy_image[rnd > 1 - prob] = 255

        return noisy_image

    elif noise_type == "speckle":
        # Adds `speckle` noise to an image
        # How is this different from regular gaussian noise? I honestly don't recall. It does look different though...

        height, width, channels = image.shape

        gauss = np.random.randn(height, width, channels) / 255
        gauss = gauss.reshape(height, width, channels)

        noisy_image = image + image * gauss
        noisy_image = noisy_image.astype("uint8")
        return noisy_image

