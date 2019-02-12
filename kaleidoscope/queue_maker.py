#!/usr/bin/env python
#                                                _
#                                               | |
#   __ _ _   _  ___ _   _  ___   _ __ ___   __ _| | _____ _ __
#  / _` | | | |/ _ \ | | |/ _ \ | '_ ` _ \ / _` | |/ / _ \ '__|
# | (_| | |_| |  __/ |_| |  __/ | | | | | | (_| |   <  __/ |
#  \__, |\__,_|\___|\__,_|\___| |_| |_| |_|\__,_|_|\_\___|_|
#     | |                   ______
#     |_|                  |______|

"""
queue_maker.py

Places items in the Redis work queue
"""
import constants
import key_scraper
import rediswq
import os

S3_ORIGIN_BUCKET = os.environ['ORIGIN_S3']

queue = rediswq.RedisWQ(name=constants.JOB_NAME, host=constants.HOST)


def queue_maker(queue, bucket_name):
    """
    Populates the redis queue using KaleidoscopeKeyScraper.
    Expects the Redis service and pod to be active, expects files to be uploaded
    :param queue: The RedisWQ()
    :param bucket_name: bucket where original files are located
    :return: None
    """
    scraper = key_scraper.KaleidoscopeKeyScraper(
        bucket_name=bucket_name,
        queue=queue,
    )
    scraper.add_keys_to_queue()

    return None


queue_maker(queue, S3_ORIGIN_BUCKET)
