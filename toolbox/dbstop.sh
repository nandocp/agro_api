#! /bin/bash

podman stop --filter name=agro_api_db
podman rm --filter name=agro_api_db
