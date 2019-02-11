"""
This interface is intended as a convenience.
All the interactions here are possible with text editors and via the command line.

The `kaleidoscope` pipeline was originally intended to be one utilized purely through the command line,
as a result this interface class currently consists in large part as wrappers for command line utilities.

This is not ideal... but it works

The current implementation is a result of all of the initial explorations of Kubernetes, the configurations,
cluster development and testing all being done purely in the command line.

ALL or ALMOST ALL of these functions can and should be removed and replaced with those from `kubernetes-python`,
the official python package. That this has not happened yet is solely due to time restrictions.

"""
import boto3
import os
import subprocess
import sys
import itertools
import time

import kaleidoscope._create_yamls as _create_yamls


class Interface(object):
    def __init__(self, cluster_name_prefix='kaleidoscope', verbose=True):
        """Interface for kaleidoscope"""

        # for verbose printing
        self._vprint = sys.stdout.write if verbose else lambda *a, **k: None

        self.cluster_name = cluster_name_prefix + ".k8s.local"
        self.kops_state_store_name = cluster_name_prefix + "-kops-state-store"
        self.original_images_bucket = cluster_name_prefix + "-original-images-bucket"
        self.augmented_images_bucket = cluster_name_prefix + "-augmented-images-bucket"

        # kubectl and kops need to be installed via homebrew
        if not self._package_message_non_zero("kubectl", " -h"):
            install_command = "`brew update && brew install kops kubectl`"
            raise AssertionError("cannot find kubectl. Install via homebrew with " + install_command)

        # TODO: Find a way to pass `--upgrade --user` in setup.py install_requires
        # awscli and kops need to be installed with --upgrade arg (according to AWS docs)
        if not self._package_message_non_zero("aws", " help"):
            install_command = "`pip install awscli --upgrade --user`"
            raise AssertionError("cannot find awscli. Install with " + install_command)

        # need a place to store kops state (kubernetes cluster information)
        if not self._bucket_exists(self.kops_state_store_name):
            self._create_cluster_state_store()

        # certain environment variables must be set by the user
        self._check_environmental_variables()

        # TODO: Test if cluster created (but how?)
        if self._cluster_ready():
            self._vprint("\rCluster appears to be ready")
            self._configure_base_cluster()
            self._activate_base_components()
        else:
            print("\rCluster not ready.\n If you have created a cluster, please wait longer try again."
                  + " If you have not created a cluster, please do Cluster.create_cluster()\n")

    def create_image_buckets(self):
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
        return s3.Bucket(bucket_name) in s3.buckets.all()

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
        if error:
            raise OSError(error)
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

    def _configure_base_cluster(self):
        _create_yamls._create_secret_yaml()
        _create_yamls._create_secret_store_yaml()
        _create_yamls._create_redis_service_yaml()
        _create_yamls._create_redis_master_yaml()
        _create_yamls._create_queue_maker_yaml(self.original_images_bucket)
        _create_yamls._create_poll_yaml()

    def _activate_secret(self):
        self._vprint("\rPlanting Secret")
        command = f"kubectl create -f secret.yaml"
        self._pass_command_to_shell(command)

    def _activate_secret_store(self):
        self._vprint("\rCreating Secret")
        command = f"kubectl create -f secret_store.yaml"
        self._pass_command_to_shell(command)

    def _activate_redis_service(self):
        self._vprint("\rCreating Redis Service")
        command = f"kubectl create -f redis_service.yaml"
        self._pass_command_to_shell(command)

    def _activate_redis_master(self):
        self._vprint("\rStarting Redis Master")
        command = f"kubectl create -f redis_master.yaml"
        self._pass_command_to_shell(command)

    def _activate_queue_maker(self):
        self._vprint("\rStarting Queue Maker")
        command = f"kubectl create -f queue_maker.yaml"
        self._pass_command_to_shell(command)

    def _activate_poll(self):
        self._vprint("\rStarting Poll")
        command = f"kubectl create -f poll.yaml"
        self._pass_command_to_shell(command)

    def _activate_base_components(self):
        self._activate_secret()
        self._activate_secret_store()
        self._activate_redis_service()
        self._activate_redis_master()
        self._vprint("\rReady to upload")
        # NOTE: above line assumes no upload yet

    # TODO: Change uploader to boto3, add vrpint for each uploaded image, add percent complete
    def upload_images(self, local_images_directory=None, s3_origin=None):

        self._vprint("\rUploading ...")
        # TODO: Maybe this should check that the bucket is available first...
        if s3_origin:
            command = f"aws s3 cp s3://{s3_origin} s3://{self.original_images_bucket} --recursive --quiet"
        elif local_images_directory:
            command = f"aws s3 cp {local_images_directory} s3://{self.original_images_bucket} --recursive --quiet"
        else:
            raise ValueError('at least one image origin must be not None')
        self._pass_command_to_shell(command)
        self._vprint("\rUploading ... Complete")
        self._activate_queue_maker()
        self._vprint("\rReady to transform")

    def transform(self, num_workers):
        self._activate_poll()
        self._vprint("\rStarting Workers")
        _create_yamls._create_job_yaml(origin_s3_bucket=self.original_images_bucket,
                                       destination_s3_bucket=self.augmented_images_bucket,
                                       num_workers=num_workers)
        command = f"kubectl create -f job.yaml"
        self._pass_command_to_shell(command)

    def _get_progress(self):
        command = "kubectl logs poll"
        # self._vprint(f"\r$: {command}")
        output = self._pass_command_to_shell(command)
        output = output.splitlines()
        if len(output) > 0:
            counts = output[-1].split(":")
        # if len(counts) > 0:
            progress = int(counts[0])
        else:
            progress = None
        return progress

    def progress(self, delay=4, total=100*4):

        spinner = itertools.cycle(['-', '/', '|', '\\'])
        main = None
        for i in range(total):

            # if i % delay == 0:
            main = self._get_progress()

            batch_size = 10
            if main:
                sys.stdout.write("\r~{} original images remaining  {}".format(batch_size*(main+1), next(spinner)))
                sys.stdout.flush()
            time.sleep(1)
