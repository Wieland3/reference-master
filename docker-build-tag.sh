#!/bin/bash

# This script is used to build and tag the docker image
docker build --no-cache --platform linux/amd64 -t reference-master:latest .
