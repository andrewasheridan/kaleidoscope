import boto3
import tools
import pickle


class KaleidoscopeKeyScraper(object):
    def __init__(self, bucket_name, queue):

        self.bucket_name = bucket_name
        self.s3 = self._add_s3_client()
        self.queue = queue

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
        batch_size = num_objects // 10

        for i in range(num_objects):
            batch = objects[i:i + batch_size]
            pickled_batch = pickle.dumps(batch)
            self.queue.put(pickled_batch)

    def add_keys_to_queue(self):

        kwargs = {"Bucket": self.bucket_name}

        while True:
            response = self.s3.list_objects_v2(**kwargs)

            try:
                objects = response["Contents"]
                self._add_batches_to_queue(objects)
            except KeyError:
                return

            try:
                kwargs["ContinuationToken"] = response["NextContinuationToken"]
            except KeyError:
                break
