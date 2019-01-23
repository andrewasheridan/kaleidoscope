# download one file and print the contents of the images dir

import os
import glob

import boto3

s3_bucket_identifier = 'chainsaw-dogs-and-cats'

s3 = boto3.resource('s3', region_name='us-east-1')
bucket = s3.Bucket(s3_bucket_identifier)

origin_filename = '0.jpg'
destination_filename = origin_filename
destination_dir = 'images/' # make sure this has the slash at the end

os.makedirs(os.path.dirname(destination_dir), exist_ok=True)
bucket.download_file(origin_filename, destination_dir + destination_filename)
