**To build & push this container:**
 
Navigate to `kaleidoscope/` and do:
```
docker build -t [user-id/poll-container-name:tag] -f ../containers/poll/Dockerfile .
docker push [user-id/poll-container-name:tag]
```

The container ID `[user-id/poll-container-name:tag]` should also be used in the yaml template `poll_template.yaml`
