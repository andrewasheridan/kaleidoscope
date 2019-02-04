#!/usr/bin/env python
import os
import sys
import time
import pickle
import rediswq
import boto3
import glob
import cv2
from image_augmentation import ImageAugmenter
from tools import get_image_name_from_path

time.sleep(10)
host = "redis"
# Uncomment next two lines if you do not have Kube-DNS working.
# import os
# host = os.getenv("REDIS_SERVICE_HOST")

queue = rediswq.RedisWQ(name="job2", host="redis")
s3 = boto3.resource('s3', region_name='us-east-1')
origin_bucket = s3.Bucket('chainsaw-dogs-and-cats')
destination_dir = './downloaded_images/'
os.makedirs(os.path.dirname(destination_dir), exist_ok=True)

while not queue.empty():
    # print("queue not empty")

    item = queue.lease(lease_secs=10, block=True, timeout=2)

    if item is not None:
        print("item not None")

        batch = pickle.loads(item)
        # num_keys = len(batch)
        # batch is now a list of s3 objs
        for i, key in enumerate(batch):

            path = destination_dir + key["Key"]
            print(path)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            # print('path = '+ path)
            # print('key = '+ key["Key"])
            origin_bucket.download_file(key["Key"], path)

            try:
                image = cv2.imread(path)
            except:
                raise ValueError('cv2 err')
            auger = ImageAugmenter(image, key["Key"], 6, save=True)















            # sys.stdout.write("\r{:2.2f}%".format(100*(i+1)/num_keys))

        q.complete(item)

    else:

        print("Waiting for work")

time.sleep(60)
        
print("Queue empty, exiting")

# save location = chainsaw-augmented-images