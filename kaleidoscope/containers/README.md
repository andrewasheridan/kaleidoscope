`kaleidoscope/containers`

This directory contains one subdirectory for each of three different Docker Containers.
Inside each directory is a `Dockerfile` and a README.md which explains how to build the Containers.

Note: A local version of [Docker](https://www.docker.com) must be installed to build and push containers.

| Directory        | Description |
| --- |:---|
| poll      | Logs how many items are left on the queue |
| queue-maker      | Adds batches of image pointers to a redis work queue      |
| worker | Transforms batches of images and saves to S3      |