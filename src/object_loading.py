import os
import glob

import boto3
import pickle
import sys

test_batch_of_keys_filename = '../s3_keys/batch_0000000001.pickle'

destination_dir = '../downloaded_images/'

 # make sure this has the slash at the end
os.makedirs(os.path.dirname(destination_dir), exist_ok=True)

s3_bucket_identifier = 'chainsaw-dogs-and-cats'
region_name = 'us-east-1'


s3 = boto3.resource('s3', region_name=region_name)

# check for s3 bucket 
try:
	bucket_exists = s3.Bucket(s3_bucket_identifier) in s3.buckets.all()
	if not bucket_exists:
		raise ValueError

except ValueError:
	print('bucket DNE')

bucket = s3.Bucket(s3_bucket_identifier)

with open (test_batch_of_keys_filename, 'rb') as fp:
    test_batch_of_keys = pickle.load(fp)

num_keys = len(test_batch_of_keys)
for i, key in enumerate(test_batch_of_keys):

	bucket.download_file(key["Key"], destination_dir + key["Key"])
	sys.stdout.write("\r{:2.2f}%".format(100*(i+1)/num_keys))
