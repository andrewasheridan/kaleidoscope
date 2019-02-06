#                      _              _       
#                     | |            | |      
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___ 
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#

"""
constants.py

various fixed values used elsewhere
"""

# ID of S3 bucket used for retrieving files from
S3_ORIGIN_BUCKET = "chainsaw-dogs-and-cats"

# location of AWS hardware
AWS_REGION = 'us-east-1'

# place to store downloaded imaged
DOWNLOAD_DIRECTORY = './downloaded_images/'

# directory to save augmented images before sending to S3
TMP_SAVE_DIR = "./aug_img_tmp/"

# should reflect number of distinct transformations in transformations.py
NUM_POSSIBLE_TRANSFORMS = 6

# available OpenCV image file types
# loaded images should be checked that their format is in this list
# docs.opencv.org/3.0-beta/modules/imgcodecs/doc/reading_and_writing_images.html#imread
OPENCV_FILETYPES = [
    ".bmp",
    ".dib",
    ".jpeg",
    ".jpg",
    ".jpe",
    ".jp2",
    ".png",
    ".webp",
    ".pbm",
    ".pgm",
    ".ppm",
    ".sr",
    ".ras",
    ".tiff",
    ".tif",
]

# S3_KEYS_DIR = "../s3_keys/"
#
# METADATA_BATCH_PREFIX = "batch_"
