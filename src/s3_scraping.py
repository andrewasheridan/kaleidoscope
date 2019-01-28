# Adapted from alexwlchan.net/2018/01/listing-s3-keys-redux/ (MIT License)

import boto3
import glob
import pickle
import os

S3_KEYS_DIR = "../s3_keys/"


def save_batch_keys(batch_keys):

    # make key dir if it doesnt exist 
    os.makedirs(os.path.dirname(S3_KEYS_DIR), exist_ok=True)

    try:
        current_max_filename = max(glob.glob(S3_KEYS_DIR + "batch_*"))
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

    new_filename = "../s3_keys/batch_" + new_number + ".pickle"

    with open(new_filename, "wb") as file:
        pickle.dump(batch_keys, file)


def get_s3_objects(bucket):
    """
    :param bucket:
    :rtype: Iterator[Any]
    """
    s3 = boto3.client("s3")

    kwargs = {"Bucket": bucket}

    while True:

        response = s3.list_objects_v2(**kwargs)

        try:
            contents = response["Contents"]
            save_batch_keys(contents)
        except KeyError:
            return

        for obj in contents:
            yield obj

        try:
            kwargs["ContinuationToken"] = response["NextContinuationToken"]

        except KeyError:
            break

        # else:


def get_s3_keys(bucket):
    """
    :param bucket: Name of bucket
    """
    for obj in get_s3_objects(bucket):
        yield obj["Key"]


def get_list_of_s3_keys(bucket):
    """
    :param bucket: Name of bucket
    :rtype: List[str]
    """
    return [key for key in get_s3_keys(bucket=bucket)]


s3_keys = get_list_of_s3_keys("chainsaw-dogs-and-cats")
print(len(s3_keys))
