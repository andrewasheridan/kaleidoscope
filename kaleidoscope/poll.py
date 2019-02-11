#!/usr/bin/env python
import rediswq
import time
import sys

host = "redis"
queue = rediswq.RedisWQ(name="job2", host="redis")

while not queue.empty():

    main_q_size, _ = queue.get_queue_sizes
    time.sleep(5)
    print(f"{main_q_size}")
