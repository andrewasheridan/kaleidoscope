import cv2
import random
import numpy as np 


def random_square_crop_with_resize(
    image, new_side_len=400, interpolation=cv2.INTER_LANCZOS4
):

    height, width, _ = image.shape

    if 0 in [height, width]:
        return None

    if height < width:

        new_height = new_side_len
        new_width = int(width * new_height / height)

        image_resized = cv2.resize(
            image, (new_width, new_height), interpolation=interpolation
        )
        if image_resized.shape[0] == image_resized.shape[1]:
            image_square = image_resized
        else:
            extra_width = new_width - new_side_len
            margin = extra_width // 2
            rand_adjustment = random.randint(0, margin) * random.choice([1, -1])

            if margin % 2 == 1:
                shift = 1
            else:
                shift = 0

            image_square = image_resized[
                :, margin - rand_adjustment : -(margin + shift + rand_adjustment), :
            ]

        
    if width < height:

        new_width = new_side_len
        new_height = int(height * new_width / width)

        image_resized = cv2.resize(
            image, (new_width, new_height), interpolation=interpolation
        )
        if image_resized.shape[0] == image_resized.shape[1]:
            image_square = image_resized
        else:
            extra_height = new_height - new_side_len
            margin = extra_height // 2
            rand_adjustment = random.randint(0, margin) * random.choice([1, -1])

            if margin % 2 == 1:
                shift = 1
            else:
                shift = 0

            image_square = image_resized[
                margin - rand_adjustment : -(margin + shift + rand_adjustment), :, :
            ]

        if width == height:
            image_square = cv2.resize(
                image, (new_side_len, new_side_len), interpolation=interpolation
            )
#         print('h=w')
    return image_square


def rotate_and_zoom(image, image_name):
    # image must be square
    s = image.shape[0]

    ang = random.randint(1,359)

    rotation_matrix = cv2.getRotationMatrix2D((s//2, s//2), ang, 1)
    try:
    	image = cv2.warpAffine(image, rotation_matrix, (s, s))
    except:
    	print('rot: ', s, ang, image_name)

    # TODO: Explain this
    # 1.41 ~ root(2), this sin func maxes at 45 deg, s//8 found empircally
    x = abs(int(s//8 * np.sin(np.deg2rad(45 + ang // 45 + ang % 45)) * 1.41))
    image = image[x:-x, x:-x, :]

    try:
        image = cv2.resize(image, (s, s), interpolation=cv2.INTER_LANCZOS4)
    except:
        print('rot: ', s, x, ang, image_name)
    return image


def adjust_contrast(image, image_name,):
    alpha = 0.5 + 1.5 * random.random()
    try:
        image = cv2.convertScaleAbs(image, alpha=alpha, beta=0)
    except:
        print('cont: ', image_name, alpha)
    return image


def adjust_brightness(image, image_name,):
    beta = random.random() * 100
    try:
        image = cv2.convertScaleAbs(image, alpha=1, beta=beta)
    except:
        print('brit: ', image_name, beta)
    return image


def adjust_saturation(image, image_name,):
    satadj = random.random() * 3
    try:
        imghsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype("float32")
        h, s, v = cv2.split(imghsv)
        s = s*satadj
        s = np.clip(s,0,255)
        imghsv = cv2.merge([h,s,v])
        image = cv2.cvtColor(imghsv.astype("uint8"), cv2.COLOR_HSV2BGR)
    except:
        print('sat: ', image_name, satadj)
    return image


def flip_left_right(img, image_name,):
    
    try:
        img = np.fliplr(img)
    except:
        print('lr: ', image_name)
    return img

def noisy(image, image_name,):
    try:

        noise_typ = random.choice(['gauss', 's&p', 'poisson', 'speckle'])

    # def noisy_1(noise_typ, image):

        if noise_typ == "gauss":
            
            row, col, ch = image.shape
            mean = 0
            var = 2
            sigma = var ** 0.5
            gauss = np.random.normal(mean, sigma, image.shape)
            gauss = gauss.reshape(row, col, ch)
            noisy_img = image + gauss
            return noisy_img.astype('uint8')
        
        elif noise_typ == "s&p":
            prob = 0.01
    #     def add_salt_and_pepper(gb, prob):
            '''Adds "Salt & Pepper" noise to an image.
            gb: should be one-channel image with pixels in [0, 1] range
            prob: probability (threshold) that controls level of noise'''

            rnd = np.random.rand(image.shape[0], image.shape[1], image.shape[2])
            noisy_img = image.copy()
            noisy_img[rnd < prob] = 0
            noisy_img[rnd > 1 - prob] = 255
            return noisy_img
        elif noise_typ == "poisson":
            vals = len(np.unique(image))
            vals = 2 ** np.ceil(np.log2(vals))
            noisy_img = np.random.poisson(image * vals) / float(vals)
            return noisy_img.astype('uint8')
        elif noise_typ == "speckle":
            row, col, ch = image.shape
            gauss = np.random.randn(row, col, ch) / 255
            gauss = gauss.reshape(row, col, ch)
            noisy_img = image + image * gauss
            return noisy_img.astype('uint8')
    except:
        print(noise_typ, image_name)






import sys
import glob
from tools import get_image_name_from_path
from tools import new_image_name


# fns = glob.glob("../downloaded_images/*")[:20]

# for i, fn in enumerate(fns):
#     image = cv2.imread(fn)
#     image = random_square_crop_with_resize(image)
#     image_name = new_image_name(get_image_name_from_path(fn), "a")
#     cv2.imwrite("../teed/" + image_name, image)
#     print("\r{:2.2f}%".format(100 * (i + 1) / len(fns)))
