"""writes AWS credentials to file using template
Usage:
python create_secret_yaml.py $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY $AWS_DEFAULT_REGION 
"""
import base64

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("secrets", nargs="*")

secrets = parser.parse_args().secrets


def write_secret_yaml(
    key, secret_key, region, name="secret-secret", filename="secret.yaml"
):
    """Summary
    Writes AWS credentials to yaml file
    """
    key = base64.b64encode(key.encode())
    secret_key = base64.b64encode(secret_key.encode())
    region = base64.b64encode(region.encode())

    template = """apiVersion: v1
kind: Secret
metadata:
  name: {}
data:
  AWS_DEFAULT_REGION: {}
  AWS_ACCESS_KEY_ID: {}
  AWS_SECRET_ACCESS_KEY: {}"""

    template = template.format(name, region.decode(), key.decode(), secret_key.decode())

    with open(filename, "w") as yaml:
        yaml.write(template)


write_secret_yaml(*secrets)
