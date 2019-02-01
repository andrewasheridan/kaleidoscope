# Kubernetes


## Secret generation

AWS Credentials are embedded in a Secret defined by `secret.yaml`. This file is generated using `create_secret_yaml.py`

### usage example:

Assuming AWS credentials are stored in `bash_profile` as `$AWS_ACCESS_KEY_ID` `$AWS_SECRET_ACCESS_KEY` `$AWS_DEFAULT_REGION`  

```
python create_secret_yaml.py $AWS_ACCESS_KEY_ID $AWS_SECRET_ACCESS_KEY $AWS_DEFAULT_REGION 

```
