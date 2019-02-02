# Kubernetes


## AWS Credentials

AWS Credentials are embedded in a Secret defined by `secret.yaml`. 
This file is generated using `create_secret_yaml.py`:

```
python create_secret_yaml.py $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY $AWS_DEFAULT_REGION 

```
(Assumes AWS credentials are active environment variables)


## Kubernetes Setup

```
TODO: Insert cluster activation & validation commands
kubectl create -f secret.yaml
kubectl create -f secret-pod.yaml
kubectl create -f redis-pod.yaml
kubectl create -f queue-maker-pod.yaml
TODO: Insert worker pod creation command
```
