To build & push this container navigate to `kaleidoscope/` and do:
```
docker build -t [user-id/queue-maker-container-name:tag] -f ../containers/queue-maker/Dockerfile .
docker push [user-id/queue-maker-container-name:tag]
```

The container ID `[user-id/queue-maker-container-name:tag]` should also be used in the yaml template `queue_maker_template.yaml`
