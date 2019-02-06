#!/usr/bin/env python
import os
import pickle
import rediswq
import boto3
import cv2
from image_augmenter import KaleidoscopeAugmenter

host = "redis"

queue = rediswq.RedisWQ(name="job2", host="redis")
s3 = boto3.resource('s3', region_name='us-east-1')
origin_bucket = s3.Bucket('chainsaw-dogs-and-cats')
destination_dir = './downloaded_images/'
os.makedirs(os.path.dirname(destination_dir), exist_ok=True)

while not queue.empty():
    item = queue.lease(lease_secs=10, block=True, timeout=2)

    if item is not None:
        batch = pickle.loads(item)

        for i, key in enumerate(batch):

            path = destination_dir + key["Key"]
            os.makedirs(os.path.dirname(path), exist_ok=True)
            origin_bucket.download_file(key["Key"], path)

            try:
                image = cv2.imread(path)
            except:
                raise ValueError('cv2 err')
            auger = KaleidoscopeAugmenter(image, key["Key"], 6, save=True)

        queue.complete(item)

    else:
        print("Waiting for work")
