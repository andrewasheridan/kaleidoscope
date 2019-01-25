# Adapted from alexwlchan.net/2018/01/listing-s3-keys-redux/ (MIT License)

import boto3


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
        except KeyError:
            return

        for obj in contents:
            yield obj

        try:
            kwargs["ContinuationToken"] = response["NextContinuationToken"]
        except KeyError:
            break


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


s3_keys = get_list_of_s3_keys('chainsaw-dogs-and-cats')
print(len(s3_keys))


