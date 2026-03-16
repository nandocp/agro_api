#! /bin/sh

echo 'Initializing agro-api db'
$(pwd)/scripts/toolbox/dbinit.sh

echo 'Initializing agro-api toolbox'
toolbox create --image agro_api-toolbox:latest agro_api_box > /dev/null 2>&1
toolbox enter agro_api_box

echo 'Cleaning db container'
$(pwd)/scripts/toolbox/dbstop.sh

echo 'Cleaning agro-api container'
podman stop agro_api_box > /dev/null 2>&1
podman rm agro_api_box > /dev/null 2>&1
