#  _
# | |
# | | _____ _   _     ___  ___ _ __ __ _ _ __   ___ _ __
# | |/ / _ \ | | |   / __|/ __| '__/ _` | '_ \ / _ \ '__|
# |   <  __/ |_| |   \__ \ (__| | | (_| | |_) |  __/ |
# |_|\_\___|\__, |   |___/\___|_|  \__,_| .__/ \___|_|
#            __/ |_____                 | |
#           |___/______|                |_|
"""
key_scraper.py

scans S3 bucket for keys
adds keys to existing redis queue
"""
import boto3
import tools
import pickle


class KaleidoscopeKeyScraper(object):
    def __init__(self, bucket_name, queue, max_grabs=10):

        self.bucket_name = bucket_name
        self.s3 = self._add_s3_client()
        self.queue = queue
        self.max_grabs = max_grabs
        self.num_grabs = 0

    def _add_s3_client(self):
        try:
            if tools.bucket_exists(self.bucket_name):
                return boto3.client("s3")

        # TODO: Make this less broad
        # NOTE: Do I even need this here?
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            print("AWS S3 bucket error.")

    def _add_batches_to_queue(self, objects):
        num_objects = len(objects)
        batch_size = 10

        for i in range(num_objects // batch_size):
            batch = objects[i*batch_size:(i + 1) * batch_size]
            pickled_batch = pickle.dumps(batch)
            self.queue.put(pickled_batch)

    def add_keys_to_queue(self):

        kwargs = {"Bucket": self.bucket_name}

        while True:
            response = self.s3.list_objects_v2(**kwargs)

            try:
                objects = response["Contents"]
                self._add_batches_to_queue(objects)
                self.num_grabs += 1
            except KeyError:
                return

            try:
                kwargs["ContinuationToken"] = response["NextContinuationToken"]
            except KeyError:
                break
