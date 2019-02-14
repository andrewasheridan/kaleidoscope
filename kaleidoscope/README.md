`kaleidoscope/`
***
**Used in the kaleidoscope python package:**

|File|Description|
|:---|:---|
|`interface.py`| `Interface()` class, used to interact with Kubernetes cluster, including cluster creation, file uploading, augmentation, and downloading. 

***
**Used in the kaleidoscope Kubernetes cluster:**

|File|Description|Used In|
|:---|:---|---:|
|`rediswq.py`| `RedisWQ()` class, a work queue based on Redis| Pod "redis-master"|
|`queue_maker.py`| Groups image pointers into batches and loads them into a Redis work queue | Pod "queue-maker"|
|`key_scraper.py`| `KaleidoscopeKeyScraper()` class, reads image pointers from S3| Pod "queue-maker"|
|`poll.py`| Prints number of elements in main queue to stdout | Pod "poll"|
|`worker.py`| Retrieves batch from `RedisWQ()`, downloads, augments, and transfers images so S3 | Job "job-wq-50"|
|`image_augmenter.py`| Takes one image and outputs 2<sup>N</sup> images for N random transformations| Job "job-wq-50"|
|`transformations.py`| Various OpenCV transformations| Job "job-wq-50"|
|`constants.py`| Various fixed values| Various places|


|Directory|Description|
|:---|:---|
|`yaml_creation/` | kaleidoscope submodule with various functions used to load templates, modify, and write yaml files. |
|`yaml_templates/` | Templates for Kubernetes Secrets, Pods, Services, and Jobs |
|`containers/` | Dockerfile configurations for "queue-maker", "job-wq-50", and "poll" |
