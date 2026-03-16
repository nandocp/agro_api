#! /bin/sh

podman build -f scripts/toolbox/Containerfile.db -t localhost/agro-test-db:latest .
