# Kubernetes


## AWS Credentials

AWS Credentials are embedded in a Secret defined by `secret.yaml`, generated with `create_secret_yaml.py`:

```
python create_secret_yaml.py $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY $AWS_DEFAULT_REGION 

```
(Assumes AWS credentials are active environment variables)


## Kubernetes Setup
Install kubernetes operations manager and command line utility
`brew update && brew install kops kubectl`

Create a bucket to store operations state
```
aws s3api create-bucket --bucket chainsaw-kops-state-store --region us-east-1
aws s3api put-bucket-versioning --bucket chainsaw-kops-state-store  --versioning-configuration Status=Enabled
```

Set environment variables
```
export KOPS_CLUSTER_NAME=chainsaw.k8s.local
export KOPS_STATE_STORE=s3://chainsaw-kops-state-store
```

Create the cluster - make sure the zone is correct
```
kops create cluster --node-count=2 --node-size=m4.large --zones=us-east-1a
```

Edit the cluster - set min_nodes = 4, max_nodes = 13
```
kops edit cluster
```

Spin up the cluster - make take some time
```
kops update cluster --name ${KOPS_CLUSTER_NAME} --yes
```

Validate the cluster
```
kops validate cluster
```

Check the active nodes
```
kubectl get nodes
```


### Secrets, Pods, & Jobs
Add access to AWS credentials, Redis queue, queue-maker, and job
```
kubectl create -f secret.yaml
kubectl create -f secret-pod.yaml
kubectl create -f redis-pod.yaml
kubectl create -f queue-maker-pod.yaml
kubectl create -f job.yaml
```
