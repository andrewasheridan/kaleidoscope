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
