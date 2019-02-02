#!/usr/bin/env python
print("queue_maker.py")
import duper_chains_object_scraping
import pickle
import rediswq
import time
import tools

# host = "redis"
# # Uncomment next two lines if you do not have Kube-DNS working.
# # import os
# # host = os.getenv("REDIS_SERVICE_HOST")

q = rediswq.RedisWQ(name="job2", host="redis")
# print("Worker with sessionID: " + q.sessionID())
# print("Initial queue state: empty=" + str(q.empty()))
print("QM:rediswq.RedisWQ created")

scraper = duper_chains_object_scraping.S3ObjectRetrieval(
    bucketname="chainsaw-dogs-and-cats"
)
s3_keys = scraper.get_list_of_s3_keys()
print(len(s3_keys))
# for i in range(100):

#     # print(i)
#     time.sleep(3)

# batch = [i+j**2 for j in range(5)]
# time.sleep(15)
# pickled_batch = pickle.dumps(batch)
# print(batch)

# q.put(pickled_batch)


#
