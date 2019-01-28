import cv2
import glob
import sys
from image_augmentation import ImageAugmenter

problems = []
start = time.time()
print("starting at {}".format(start))
fns = glob.glob("../downloaded_images/*")[:100]
n = len(fns)
for i, fn in enumerate(fns):
    image = cv2.imread(fn)
    image_name = get_image_name_from_path(fn)
    try:
      augmenter = ImageAugmenter(image, image_name, 4, save=True)
    except:
      problems.append(image_name)

    sys.stdout.write("\r{:2.4f}%".format(100 * (i + 1) / n))


print('\n')
end = time.time()
print(end - start)
print(problems)

