To build & push this container navigate to `kaleidoscope/` and do:
```
docker build -t [user-id/worker-container-name:tag] -f ../containers/worker/Dockerfile .
docker push [user-id/worker-container-name:tag]
```

The container ID `[user-id/worker-container-name:tag]` should also be used in the yaml template `job_template.yaml`
