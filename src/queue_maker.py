#!/usr/bin/env python
import constants
import duper_chains_object_scraping
import rediswq


queue = rediswq.RedisWQ(name="job2", host="redis")
scraper = duper_chains_object_scraping.S3ObjectRetrieval(
    bucket_name=constants.S3_ORIGIN_BUCKET,
    queue=queue,
)
scraper.scrape_s3_metadata()
