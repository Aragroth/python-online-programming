docker network rm dind
docker network create --subnet 172.19.0.0/16 dind

docker stop some-docker

docker run -itd --privileged --rm \
        --name some-docker \
        --network dind \
        --ip 172.19.0.2 \
        -e DOCKER_TLS_CERTDIR='' \
        docker:dind -H 0.0.0.0:2375

docker logs some-docker

docker run -it --rm \
        -e DOCKER_HOST="tcp://172.19.0.2:2375" \
        --network dind \
        docker



docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)