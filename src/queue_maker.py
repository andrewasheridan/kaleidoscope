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
import duper_chains_object_scraping
import rediswq


queue = rediswq.RedisWQ(name="job2", host="redis")
scraper = duper_chains_object_scraping.S3ObjectRetrieval(
    bucket_name=constants.S3_ORIGIN_BUCKET,
    queue=queue,
)
scraper.scrape_s3_metadata()
