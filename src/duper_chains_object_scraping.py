import boto3
import tools
import pickle


class S3ObjectRetrievalBase(object):
    def __init__(self, bucket_name):

        self.bucket_name = bucket_name
        try:
            if tools.bucket_exists(self.bucket_name):
                self.s3 = boto3.client("s3")

        # TODO: Make this less broad
        # NOTE: Do I even need this here?
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            print("AWS S3 bucket error.")


class S3ObjectRetrieval(S3ObjectRetrievalBase):
    def __init__(self, bucket_name, queue):
        S3ObjectRetrievalBase.__init__(self,
                                       bucket_name=bucket_name)
        self.queue = queue

    def scrape_s3_metadata(self):
        print("scrape_s3_metadata")
        kwargs = {"Bucket": self.bucket_name}

        while True:

            response = self.s3.list_objects_v2(**kwargs)
            try:
                contents = response["Contents"]
                batch_size = len(contents)//10
                for i in range(len(contents)):
                    batch = contents[i:i+batch_size]

                    pickled_batch = pickle.dumps(batch)
                    self.queue.put(pickled_batch)
                print("self.queue.put")

            except KeyError:
                return

            try:
                kwargs["ContinuationToken"] = response["NextContinuationToken"]

            except KeyError:
                break
