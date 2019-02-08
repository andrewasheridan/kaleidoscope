To build & push this container navigate to `container_contents/src/` and do:


    docker build -t [user-id/container-name:tag] -f ../containers/worker/Dockerfile .
    docker push [user-id/container-name:tag]
    