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

# place to store downloaded imaged
DOWNLOAD_DIRECTORY = './downloaded_images/'

# directory to save augmented images before sending to S3
TMP_SAVE_DIR = "./aug_img_tmp/"

# should reflect number of distinct transformations in transformations.py
NUM_POSSIBLE_TRANSFORMS = 6
