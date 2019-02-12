![kaleidoscope](imgs/logo.png)

A distributed image processing pipeline I developed as for Insight Data Science as a Data Engineering Fellow.

## Description
Kaleidoscope takes in an image dataset and applies a series of chained transformations to augment the dataset. 
It performs these transformations in parallel using multiple replicated pods managed by Kubernetes, and saves the new images to an S3 bucket.

***
Imagine for a moment that you're a data scientist.
You'd like to train a model on a set of images, but the size of your dataset is small.
You realize you can leverage your existing small dataset through image augmentation. 

For example you could flip each image left-right, and double your training set.
You could randomly rotate each image a few degrees, and double the set again.
There are numerous transformations you can apply, and for each you double the size of your dataset. 

You find that your favorite machine learning frameworks has optional transformations built in, it can augment each image before feeding it into your network.
So you perform these transformations, and train your network.
Then you want to try a slightly different model, so you repeat the process from scratch. 
For each iteration of your model you are augmenting your dataset. 
The time spent on these augmentations, you could be training your models. 

You decide to write a script that does the transformations ahead of time, but you find that as the number of transformations increases linearly, the size of the dataset (and the number ofcomputations) increases geometrically.
Running this script just wont cut it. 
What if you could run multiple copies of the same script simultaneously, each on a subset of the dataset?

That's what kaleidoscope does.

### Details
To do the necessary transformations we turn to OpenCV, an open source computer vision library. 
Transformations are chained together, and applied so that work is not duplicated:
` TODO: Insert chaining pattern`

Given one image, and N transformations, 2^N images are generated.


![pipeline](imgs/pipeline.png)
### Usage
`# TODO: Fill This in`

![interface](imgs/interface.png)
### Other

#### AWS Credentials

AWS Credentials are embedded in a Secret defined by `secret.yaml`, generated with `create_secret_yaml.py`:
(Assumes AWS credentials are active environment variables)


#### Kubernetes Installation
Install kubernetes operations manager and command line utility
`brew update && brew install kops kubectl`

Set environment variables
```
export KOPS_CLUSTER_NAME=chainsaw.k8s.local
export KOPS_STATE_STORE=s3://chainsaw-kops-state-store
```



### Tree
```
|--- kaleidoscope
     |--- .gitignore
     |--- Kaleidoscope_Example.ipynb
     |--- MANIFEST.in
     |--- README.md
     |--- VERSION
     |--- setup.py
     |--- imgs
          |--- interface.png
          |--- logo.png
          |--- pipeline.png
     |--- kaleidoscope
          |--- __init__.py
          |--- constants.py
          |--- image_augmenter.py
          |--- interface.py
          |--- key_scraper.py
          |--- poll.py
          |--- queue_maker.py
          |--- rediswq.py
          |--- tools.py
          |--- transformations.py
          |--- worker.py
          |--- _create_yamls
               |--- __init__.py
               |--- _create_job_yaml.py
               |--- _create_poll_yaml.py
               |--- _create_queue_maker_yaml.py
               |--- _create_redis_master_yaml.py
               |--- _create_redis_service_yaml.py
               |--- _create_secret_store_yaml.py
               |--- _create_secret_yaml.py
               |--- _yaml_creation.py
          |--- yaml_templates
               |--- job_template.yaml
               |--- poll_template.yaml
               |--- queue_maker_template.yaml
               |--- redis_master_template.yaml
               |--- redis_service_template.yaml
               |--- secret_store_template.yaml
               |--- secret_template.yaml
          |--- containers
               |--- poll
                    |--- Dockerfile
               |--- queue-maker
                    |--- Dockerfile
                    |--- README.md
               |--- worker
                    |--- Dockerfile
                    |--- README.md
```

![](imgs/output.gif)
