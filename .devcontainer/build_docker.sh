#!/bin/bash

echo "Build the docker"

docker build . -f Dockerfile.multiple \
               --progress=plain \
               --build-arg QUARTO_VER="1.3.450" \
               --build-arg VENV_NAME="forecasting-poc" \
               -t rkrispin/forecast-poc:0.0.0.9003

if [[ $? = 0 ]] ; then
echo "Pushing docker..."
docker push rkrispin/forecast-poc:0.0.0.9003
else
echo "Docker build failed"
fi