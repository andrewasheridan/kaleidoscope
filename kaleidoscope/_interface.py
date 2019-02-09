import boto3
import os
import subprocess
import sys

from kaleidoscope.create_secret_yaml import create_secret_yaml
from kaleidoscope.create_secret_store_yaml import create_secret_store_yaml
from kaleidoscope.create_redis_service_yaml import create_redis_service_yaml
from kaleidoscope.create_redis_master_yaml import create_redis_master_yaml
from kaleidoscope.create_queue_maker_yaml import create_queue_maker_yaml


# import kaleidoscope.create_secret_yaml as create_secret_yaml
# import kaleidoscope.create_secret_store_yaml as create_secret_store_yaml
# cluster = Cluster("kaleidoscope")
# "Cluster not ready. If you have previously created a cluster, please wait longer try again."
# "If you have not created a cluster, please do Cluster.create_cluster()"

# cluster.create_cluster(dry_run=False)
# "Cluster creation may take up to 10 minutes. Check status with Cluster.cluster_ready()"

# cluster.cluster_ready()
# "Cluster not ready"

# <10 minutes later>
# cluster. cluster_ready()
# "cluster ready -
# TODO: validate_cluster()


class Cluster(object):
    def __init__(self, cluster_name_prefix='kaleidoscope', verbose=True):

        self._vprint = sys.stdout.write if verbose else lambda *a, **k: None

        self.cluster_name_prefix = cluster_name_prefix
        self.cluster_name = self.cluster_name_prefix + ".k8s.local"
        self.kops_state_store_name = self.cluster_name_prefix + "-kops-state-store"
        self.original_images_bucket = self.cluster_name_prefix + "-original-images-bucket"
        self.augmented_images_bucket = self.cluster_name_prefix + "-augmented-images-bucket"

        # TODO: Find way to install homebrew, kops, kubectl via pip / setup.py, maybe?
        # kubectl and kops need to be installed via homebrew
        if not self._package_message_non_zero("kubectl", " -h"):
            install_command = "`brew update && brew install kops kubectl`"
            raise AssertionError("cannot find kubectl. Install via homebrew with " + install_command)

        # TODO: Find a way to install this via setup.py
        # NOTE: I had trouble passing the `--upgrade` argument in setup
        if not self._package_message_non_zero("aws", " help"):
            install_command = "`pip install awscli --upgrade --user`"
            raise AssertionError("cannot find awscli. Install with " + install_command)

        # need a place to store kops state
        if not self._bucket_exists(self.kops_state_store_name):
            self._create_cluster_state_store()

        self._check_environmental_variables()

        # TODO: Test if cluster created (but how?)
        if not self._cluster_ready():
            self._vprint("\rCluster not ready. If you have created a cluster, please wait longer try again."
                         + " If you have not created a cluster, please do Cluster.create_cluster()")

        # need a place to store original images
        if not self._bucket_exists(self.original_images_bucket):
            self._create_bucket(self.original_images_bucket)

        # need a place to store augmented images
        if not self._bucket_exists(self.augmented_images_bucket):
            self._create_bucket(self.augmented_images_bucket)

    def _package_message_non_zero(self, package, args):
        """Checks if a package exists in this environment by finding the output length of a message"""
        # TODO: Make this more robust
        self._vprint(f"\r{package}: checking installation")
        command = package + args
        output = self._pass_command_to_shell(command)

        return bool(len(output))

    def _bucket_exists(self, bucket_name):
        self._vprint(f"\r{bucket_name}: Checking existence")
        s3 = boto3.resource("s3")
        return s3.Bucket(self.bucket_name) in s3.buckets.all()

    @staticmethod
    def _create_bucket(bucket_name):
        create = "aws s3api create-bucket --bucket "\
                 + bucket_name\
                 + " --region us-east-1"

        subprocess.run(create.split())

    def _create_cluster_state_store(self):
        self._vprint(f"\r{self.kops_state_store_name}: Not found - Creating")
        self._create_bucket(self.kops_state_store_name)

        apply_versioning = "aws s3api put-bucket-versioning --bucket "\
                           + self.kops_state_store_name\
                           + " --versioning-configuration Status=Enabled"
        subprocess.run(apply_versioning.split())

        # TODO: confirm existence of state store
        self._vprint(f"\r{self.kops_state_store_name}: Should be created")

    def _check_environmental_variables(self):
        self._vprint("\rEnvironment variables: confirming")
        message = "please run this command in Terminal and try again:"
        if os.environ["KOPS_CLUSTER_NAME"] != f"{self.cluster_name}":
            message += f"""'export KOPS_CLUSTER_NAME="{self.cluster_name}"' >> $HOME/.bash_profile"""
            raise EnvironmentError(message)

        if os.environ["KOPS_STATE_STORE"] != f"s3://{self.kops_state_store_name}":
            message += f"""'export KOPS_STATE_STORE="s3://{self.kops_state_store_name}"' >> $HOME/.bash_profile"""
            raise EnvironmentError(message)
        self._vprint("\rEnvironment variables: confirmed")

    def _cluster_ready(self):
        """Checks if a package exists in this environment by finding the output length of a message"""
        command = "kops validate cluster"
        self._vprint(f"\r$: {command}")
        output = self._pass_command_to_shell(command)
        message = f"Your cluster {self.cluster_name} is ready"
        # sys.stdout.write(output)
        return message in output

    def validate_cluster(self):
        return self._cluster_ready()

    @staticmethod
    def _pass_command_to_shell(command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        output = output.decode().strip()
        return output

    def _spin_up_cluster(self, dry_run=True, raw_output=False):
        arg = " --yes" if not dry_run else ""
        command = f"kops update cluster --name {self.cluster_name}{arg}"
        self._vprint(f"\r$: {command}")
        output = self._pass_command_to_shell(command)
        if raw_output:
            print(output)
        self._vprint("\rSpinning up cluster, this may take some time (5+ minutes")

    def create_cluster(self, node_count=10, node_size="m4.large", region="us-east-1a", dry_run=False, raw_output=False):
        command = f"kops create cluster --node-count={node_count} --node-size={node_size} --zones={region}"
        self._vprint(f"\r$: {command}")
        output = self._pass_command_to_shell(command)
        if raw_output:
            print(output)
        self._spin_up_cluster(dry_run=dry_run,raw_output=raw_output)

    def delete_cluster(self, dry_run=False, raw_output=False):
        arg = " --yes" if not dry_run else ""
        command = f"kops delete cluster{arg}"
        self._vprint(f"\r$: {command}")
        output = self._pass_command_to_shell(command)
        if raw_output:
            print(output)
        self._vprint(f"\rCluster deleted")

    @staticmethod
    def configure_base_cluster(self):
        create_secret_yaml()
        create_secret_store_yaml()
        create_redis_service_yaml()
        create_redis_master_yaml()

    def upload(self, local_images_directory):

        command = f"aws s3 cp {local_images_directory} s3://{self.kops_state_store_name} --recursive --quiet"
        self._pass_command_to_shell()
        os.system()

