# Adapted from alexwlchan.net/2018/01/listing-s3-keys-redux/ (MIT License)

import boto3

# For type hinting / annotations
from botocore.client import BaseClient
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List


def get_s3_objects(bucket: str) -> Iterator:
    """
    :param: bucket: str
    """
    s3: BaseClient = boto3.client("s3")

    kwargs: Dict = {"Bucket": bucket}

    while True:

        response: Dict[str, Any] = s3.list_objects_v2(**kwargs)

        try:
            contents: List = response["Contents"]
        except KeyError:
            return

        obj: Dict[str, Any]
        for obj in contents:
            yield obj

        try:
            kwargs["ContinuationToken"] = response["NextContinuationToken"]
        except KeyError:
            break


def get_s3_keys(bucket: str) -> Iterator:
    """
    :param bucket: Name of bucket
    """
    obj: Dict[str, str]
    for obj in get_s3_objects(bucket):
        yield obj["Key"]


def get_list_of_s3_keys(bucket: str) -> List:
    """
    :param bucket: Name of bucket
    :rtype: List
    """
    return [key for key in get_s3_keys(bucket='bucket')]

