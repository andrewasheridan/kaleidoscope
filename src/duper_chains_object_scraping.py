import boto3
import constants
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

    # def _save_batch_keys(self):

    #     tools.get_max_filename_in_dir_and_increment(
    #         dir=constants.S3_KEYS_DIR, prefix=constants.METADATA_BATCH_PREFIX
    #     )
    #     tools.save_obj(batch_keys)

    def scrape_s3_metadata(self):
        print("scrape_s3_metadata")
        kwargs = {"Bucket": self.bucket_name}

        while True:

            response = self.s3.list_objects_v2(**kwargs)
            try:
                contents = response["Contents"]
                n=len(contents)//10
                for i in range(len(contents)):
                    batch = contents[i:i+n]
                # [l[i:i + n] for i in range(0, len(l), n)]

                # TODO: replace with add_to_redis_queue
                # self._save_batch_keys(contents)
                    pickled_batch = pickle.dumps(batch)
                    self.queue.put(pickled_batch)
                print("self.queue.put")

            except KeyError:
                return

            # for obj in contents:
            #     yield obj

            try:
                kwargs["ContinuationToken"] = response["NextContinuationToken"]

            except KeyError:
                break
