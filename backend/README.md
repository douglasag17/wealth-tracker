# wealth-tracker

[Docker image FastAPI](https://fastapi.tiangolo.com/deployment/docker/#build-a-docker-image-for-fastapi)

```shell
docker stop wealth-tracker-container

docker rm wealth-tracker-container

docker images

docker rmi <image_id>

docker build -t wealth-tracker-image .

docker run -d --name wealth-tracker-container -p 80:80 wealth-tracker-image
```

Go to: http://127.0.0.1/docs
