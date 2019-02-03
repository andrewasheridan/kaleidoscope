#!/usr/bin/env python

import sys
import time
import pickle
import rediswq

host = "redis"
# Uncomment next two lines if you do not have Kube-DNS working.
# import os
# host = os.getenv("REDIS_SERVICE_HOST")

q = rediswq.RedisWQ(name="job2", host="redis")

print("Worker with sessionID: " + q.sessionID())
print("Initial queue state: empty=" + str(q.empty()))

while not q.empty():

    print('q.not empty')
    item = q.lease(lease_secs=10, block=True, timeout=2)

    if item is not None:

        batch = pickle.loads(item)

        print(batch[:-1])
        # print("Working on " + itemstr)

        time.sleep(10)  # Put your actual work here instead of sleep.

        q.complete(item)

    else:

        print("Waiting for work")

time.sleep(300)
        
print("Queue empty, exiting")
