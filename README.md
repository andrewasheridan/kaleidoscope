# super-duper-chainsaw
# TODO: Update this readme it is out of date!

## Description
Image augmentation preprocessing


### Context
Data scientists working on image based machine learning models often desire to augment small datasets during preprocessing to create larger training, testing, and validation datasets. In addition to normalization, the transformations applied during this augmentation process can include but are not limited to rotations, translations, and random cropping.

'super-duper-chainsaw' is a pipeline with the ability to compute a wide variety of transformations on a dataset of arbitrary size in a timely manner.

'super-duper-chainsaw' will perform distributed image transformations with variable cluster scales based on the size of the dataset and the transformations applied.
The resulting information dataset will then be accessible for download or accessible via an API.


### Need
#### Image Data
[Stanford Dog Database](http://vision.stanford.edu/aditya86/ImageNetDogs/)

700MB :  20,000 Images : 120 Breeds

Other Data: Any image dataset

#### Technologies
S3, Spark, MySQL, AWS API (?)


### Vision
Upon submission of a URL to a S3 bucket or to a file of archived dataset a random image is selected and a series of transformations area applied.
From a presented set of sample transformations the user selects the ones they desire.
After selection a dashboard is unveiled to track progress, upon completion the dashboard reconfigures to show instructions for accessing the new dataset.

### Limitations / Trade-offs / Future Considerations
One difficulty will be to balance the cost of computation with processing time. 

### Dependencies
OpenCV  -   `conda install -c conda-forge opencv`
boto3   -   `conda install -c conda-forge boto3`

### Tree
```
|--- super-duper-chainsaw
     |--- .gitignore
     |--- README.md
     |--- src
          |--- app.py
          |--- constants.py
          |--- duper_chain_worker_processing.py
          |--- duper_chains_object_scraping.py
          |--- image_augmentation.py
          |--- object_loading.py
          |--- queue_maker.py
          |--- rediswq.py
          |--- tools.py
          |--- transformations.py
          |--- worker.py
     |--- kubernetes
          |--- kubernetes_config
               |--- README.md
               |--- create_secret_yaml.py
               |--- job.yaml
               |--- queue-maker-pod.yaml
               |--- redis-pod.yaml
               |--- secret-pod.yaml
          |--- containers
               |--- queue-maker
                    |--- Dockerfile
                    |--- README.md
               |--- worker
                    |--- Dockerfile
                    |--- README.md
```
