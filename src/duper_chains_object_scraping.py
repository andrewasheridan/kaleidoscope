import boto3
import tools
import pickle


class S3ObjectRetrievalBase(object):
    def __init__(self, bucket_name):

        self.bucket_name = bucket_name
        try:
            if tools.bucket_exists(self.bucket_name):
                self.s3 = boto3.client("s3")
        except:
            print()
            raise ValueError(
                "Bucket error: {} does not exist (or something else)".format(
                    self.bucket_name
                )
            )


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
