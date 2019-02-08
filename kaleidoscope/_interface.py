import boto3
import os
import subprocess
import sys

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


class Cluster(object):
    def __init__(self, cluster_name_prefix='kaleidoscope'):

        self.cluster_name_prefix = cluster_name_prefix
        self.cluster_name = self.cluster_name_prefix + ".k8s.local"
        self.kops_state_store_name = self.cluster_name_prefix + "-kops-state-store"

        # TODO: Find way to install homebrew, kops, kubectl via pip / setup.py
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

        if not self._cluster_ready():
            print("Cluster not ready. If you have created a cluster, please wait longer try again.")
            print("If you have not created a cluster, please do Cluster.create_cluster()")

    def _package_message_non_zero(self, package, args):
        """Checks if a package exists in this environment by finding the output length of a message"""
        command = package + args
        output = self._pass_command_to_shell(command)

        # TODO: Make this more robust
        return bool(len(output))

    @staticmethod
    def _bucket_exists(bucket_name):
        s3 = boto3.resource("s3")
        return s3.Bucket(bucket_name) in s3.buckets.all()

    def _create_cluster_state_store(self):
        create = "aws s3api create-bucket --bucket "\
                 + self.kops_state_store_name\
                 + " --region us-east-1"

        subprocess.run(create.split())

        apply_versioning = "aws s3api put-bucket-versioning --bucket "\
                           + self.kops_state_store_name\
                           + " --versioning-configuration Status=Enabled"
        subprocess.run(apply_versioning.split())

    def _check_environmental_variables(self):
        message = "please run this command in Terminal and try again:"
        if os.environ["KOPS_CLUSTER_NAME"] != f"{self.cluster_name}":
            message += f"""'export KOPS_CLUSTER_NAME="{self.cluster_name}"' >> $HOME/.bash_profile"""
            raise EnvironmentError(message)

        if os.environ["KOPS_STATE_STORE"] != f"s3://{self.kops_state_store_name}":
            message += f"""'export KOPS_STATE_STORE="s3://{self.kops_state_store_name}"' >> $HOME/.bash_profile"""
            raise EnvironmentError(message)

    def _cluster_ready(self):
        """Checks if a package exists in this environment by finding the output length of a message"""
        output = self._pass_command_to_shell("kops validate cluster")
        message = f"Your cluster {self.cluster_name} is ready"
        sys.stdout.write(output)
        return message in output

    def cluster_ready(self):
        self._cluster_ready()

    @staticmethod
    def _pass_command_to_shell(command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        output = output.decode().strip()
        return output

    def _spin_up_cluster(self, dry_run=True):
        arg = " --yes" if dry_run else ""
        command = f"kops update cluster --name {self.cluster_name}{arg}"
        sys.stdout.write(self._pass_command_to_shell(command))
        print("spinning up cluster, this may take some time (5+ minutes")

    def create_cluster(self, node_count=10, node_size="m4.large", region="us-east-1a", dry_run=True):
        command = f"kops create cluster --node-count={node_count} --node-size={node_size} --zones={region}"
        sys.stdout.write(self._pass_command_to_shell(command))
        self._spin_up_cluster(dry_run=dry_run)

    def delete_cluster(self, dry_run=True):
        arg = " --yes" if dry_run else ""
        command = f"kops delete cluster{arg}"
        self._pass_command_to_shell(command)



    def build(self):
        print("Building " + self.cluster_name_prefix)

