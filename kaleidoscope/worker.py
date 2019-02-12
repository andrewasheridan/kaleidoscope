#!/usr/bin/env python
#                      _
#                     | |
#  __      _____  _ __| | _____ _ __
#  \ \ /\ / / _ \| '__| |/ / _ \ '__|
#   \ V  V / (_) | |  |   <  __/ |
#    \_/\_/ \___/|_|  |_|\_\___|_|
"""
worker.py

Script to be installed in the job pods created using `job.yaml`
"""
import boto3
import cv2
import constants
import os
import pickle
import rediswq

from image_augmenter import KaleidoscopeAugmenter

# HOST = "redis"
# JOB_NAME = "job2"

# This environmental variable is set in the Docker Container the script runs inside of.
# It is set when the Pod is created with `kubectl create -f job.yaml` or during Interface().transform()
ORIGIN_S3 = os.environ['ORIGIN_S3']
AWS_DEFAULT_REGION = os.environ['AWS_DEFAULT_REGION']

queue = rediswq.RedisWQ(name=constants.JOB_NAME, host=constants.HOST)


def worker(queue):
    s3 = boto3.resource('s3', region_name=AWS_DEFAULT_REGION)
    origin_bucket = s3.Bucket(ORIGIN_S3)

    os.makedirs(os.path.dirname(constants.DOWNLOAD_DIRECTORY), exist_ok=True)

    while not queue.empty():
        item = queue.lease(lease_secs=10, block=True, timeout=2)

        if item is not None:
            batch = pickle.loads(item)

            for i, key in enumerate(batch):

                image_pointer = key["Key"]
                download_path = constants.DOWNLOAD_DIRECTORY + image_pointer
                os.makedirs(os.path.dirname(download_path), exist_ok=True)
                origin_bucket.download_file(image_pointer, download_path)

                try:
                    image = cv2.imread(download_path)
                except:
                    raise ValueError('cv2 err')

                # TODO: make the number of transformations settable in Interface()
                auger = KaleidoscopeAugmenter(image, image_pointer, 6)
                # TODO: Add in calls to auger.transform, auger.save
            queue.complete(item)

        else:
            print("Waiting for work")


worker(queue)
