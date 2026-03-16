#! /bin/bash

podman stop --filter name=agro_api_db > /dev/null 2>&1
podman rm --filter name=agro_api_db > /dev/null 2>&1
