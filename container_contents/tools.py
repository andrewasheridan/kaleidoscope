import os
import boto3

from itertools import takewhile


def get_image_name_from_path(path):

    # reverse the string and grab the text between the `.` and first `/` then reverse back
    s = path[::-1]
    s = "".join(takewhile(lambda x: x != "/", s))[::-1]
    return s


def new_image_name(base_image_name, char):
    # assumes base_image_name only has one `.` before the extension
    image_name = base_image_name.split(".")
    new_name = image_name[0] + char + "." + image_name[1]
    return new_name


def make_dir_if_DNE(dir):
    """Make dir if it does not exist"""
    os.makedirs(os.path.dirname(dir), exist_ok=True)


def bucket_exists(bucket_name):
    s3 = boto3.resource("s3")
    return s3.Bucket(bucket_name) in s3.buckets.all()


def get_max_filename_in_dir_and_increment(dir, prefix="batch_"):

    try:
        current_max_filename = max(glob.glob(dir + prefix + "*"))
    except ValueError:
        current_max_filename = None

    if current_max_filename:

        current_max_filename = current_max_filename.replace("_", " ")
        current_max_filename = current_max_filename.replace(".", " ")
        current_max_number = [
            int(s) for s in current_max_filename.split() if s.isdigit()
        ][0]
        new_number = "{0:0=10d}".format(current_max_number + 1)

    else:

        current_max_number = 0
        new_number = "{0:0=10d}".format(current_max_number)

    new_filename = prefix + new_number

    return new_filename