#!/usr/bin/env python
import boto3
import cv2
import constants
import os
import pickle
import time
import rediswq

from image_augmenter import KaleidoscopeAugmenter

host = "redis"

queue = rediswq.RedisWQ(name="job2", host="redis")
s3 = boto3.resource('s3', region_name=constants.AWS_REGION)
origin_bucket = s3.Bucket(constants.S3_ORIGIN_BUCKET)

os.makedirs(os.path.dirname(constants.DOWNLOAD_DIRECTORY), exist_ok=True)

while not queue.empty():
    start = time.time()
    item = queue.lease(lease_secs=10, block=True, timeout=2)

    if item is not None:
        batch = pickle.loads(item)

        for i, key in enumerate(batch):

            path = constants.DOWNLOAD_DIRECTORY + key["Key"]
            os.makedirs(os.path.dirname(path), exist_ok=True)
            origin_bucket.download_file(key["Key"], path)

            try:
                image = cv2.imread(path)
            except:
                raise ValueError('cv2 err')
            auger = KaleidoscopeAugmenter(image, key["Key"], 6, save=True)

        queue.complete(item)
        print("Batch processing time : {}".format(time.time() - start))
    else:
        print("Waiting for work")
