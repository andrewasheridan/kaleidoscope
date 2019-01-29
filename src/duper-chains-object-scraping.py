import boto3
import constants
import tools

class S3ObjectRetrievalBase(object):
    def __init__(self,
        bucketname):

        self.bucketname = bucketname
        try:
            if tools.bucket_exists(self.bucketname):
                self.s3 = boto3.client("s3")
            except:
                raise ValueError("Bucket error: {} does not exist".format(self.bucketname))

class S3ObjectRetrieval(S3ObjectRetrievalBase):
    def __init__(self, bucketname):
        S3ObjectRetrievalBase.__init__(self, bucketname=bucketname)

    def _save_batch_keys(self):

        tools.get_max_filename_in_dir_and_increment(dir=constants.S3_KEYS_DIR, prefix=constants.METADATA_BATCH_PREFIX)
        tools.save_obj(batch_keys)


    def scrape_s3_metadata(self):

        kwargs = {"Bucket": bucket}

        while True:

            response = self.s3.list_objects_v2(**kwargs)
            try:
                contents = response["Contents"]
                self._save_batch_keys(contents)

            except KeyError:
                return


            for obj in contents:
                yield obj

            try:
                kwargs["ContinuationToken"] = response["NextContinuationToken"]

            except KeyError:
                break


