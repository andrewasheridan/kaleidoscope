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

# sys.stdout.write("Worker with sessionID: " + q.sessionID())
# sys.stdout.write("Initial queue state: empty=" + str(q.empty()))

while not q.empty():

    item = q.lease(lease_secs=10, block=True, timeout=2)

    if item is not None:

        batch = pickle.loads(item)

        # sys.stdout.write(batch[:-1])
        # print("Working on " + itemstr)

        time.sleep(10)  # Put your actual work here instead of sleep.

        q.complete(item)

    else:

        print("Waiting for work")
        
# sys.stdout.write("Queue empty, exiting")
