To build & push this container navigate to `container_contents/` and do:

```
docker build -t [user-id/container-name:tag] -f ../containers/queue-maker/Dockerfile .
docker push [user-id/container-name:tag]
```