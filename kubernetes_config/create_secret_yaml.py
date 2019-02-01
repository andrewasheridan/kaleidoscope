import base64

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("secrets", nargs="*")

args = parser.parse_args()
secrets = args.secrets
key, secret_key, region = secrets


def writeConfig(key, secret_key, region, name="secret-secret"):

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
  AWS_SECRET_ACCESS_KEY: {}
            """

    with open("somefile.yaml", "w") as yfile:
        yfile.write(
            template.format(name, region.decode(), key.decode(), secret_key.decode())
        )


# usage:
writeConfig(key=key, secret_key=secret_key, region=region)
