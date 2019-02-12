#!/usr/bin/env python
"""
              _ _
             | | |
  _ __   ___ | | |
 | '_ \ / _ \| | |
 | |_) | (_) | | |
 | .__/ \___/|_|_|
 | |
 |_|
"""
import constants
import rediswq
import time

PRINT_DELAY = 5

queue = rediswq.RedisWQ(name=constants.JOB_NAME, host=constants.HOST)


def poll(queue, print_delay):
    """
    poll checks the number of remaining items in the redis queue and prints the value.
    This value is retrieved from the pod named `poll` using `kubectl logs poll`.

    :param queue: RedisWQ() - object that has some items in its database
    :param print_delay: int - a delay between prints so the output is not overwhelming
    :return: None
    """
    while not queue.empty():

        main_q_size, _ = queue.get_queue_sizes
        time.sleep(print_delay)
        print(f"{main_q_size}")

    return None


poll(queue, PRINT_DELAY)
