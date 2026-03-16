#! /bin/bash

# For now, to run DB, comment (or uncomment) the engine used
# docker run --name agro_api_db -p 5432:5432 -dit -e POSTGRES_HOST_AUTH_METHOD=trust -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres docker.io/postgis/postgis:18-3.6-alpine
podman volume create --ignore agro_api_db > /dev/null 2>&1
podman run --name agro_api_db \
    -p 5432:5432 \
    -dit \
    -e POSTGRES_HOST_AUTH_METHOD=trust \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=postgres \
    -v agro_api_db:/var/lib/postgresql \
    --replace \
    docker.io/postgis/postgis:18-3.6-alpine "$@" > /dev/null 2>&1
