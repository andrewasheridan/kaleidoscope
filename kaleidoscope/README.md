`kaleidoscope/`

This directory contains three subdirectories and various `.py` files.
The subdirectories contain Docker Container configurations (Dockerfiles), Kubernetes Pod configuration files, and their templates.


|File|Description|Used In|
|:---|:---|---:|
|`interface.py`| `Interface()` class, used to interact with Kubernetes cluster | <font color="#d40f5e">kaleidoscope</font> Python package|
|`rediswq.py`| `RedisWQ()` class, a work queue based on Redis| Kubernetes Pod "redis-master"|
|`queue_maker.py`| Groups image pointers into batches and loads them into a Redis work queue | Kubernetes Pod "queue-maker"|
|`key_scraper.py`| `KaleidoscopeKeyScraper()` class, reads image pointers from S3| Kubernetes Pod "queue-maker"|
|`poll.py`| Prints number of elements in main queue to stdout | Kubernetes Pod "poll"|
|`worker.py`| Retrieves batch from `RedisWQ()`, downloads, augments, and transfers images so S3 | Kubernetes Job "job-wq-50"|
|`image_augmenter.py`| Takes one image and outputs 2<sup>N</sup> images for N random transformations| Kubernetes Job "job-wq-50"|
|`transformations.py`| Various OpenCV transformations| Kubernetes Job "job-wq-50"|
|`constants.py`| Various fixed values| Multiple places|


|Directory|Description|Used In|
|:---|:---|---:|
|`yaml_creation/` | Submodule with various functions used to load templates, modify, and write yaml files. | <font color="#d40f5e">kaleidoscope</font> Python package|
|`yaml_templates/` | Templates for Kubernetes Secrets, Pods, Services, and Jobs | <font color="#d40f5e">kaleidoscope</font> Python package|
|`containers/` | Dockerfile configurations for "queue-maker", "job-wq-50", and "poll" |  Image construction (development)|
