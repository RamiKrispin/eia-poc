#!/bin/bash

echo "Build the docker"

docker buildx build . -f Dockerfile \
               --platform linux/amd64, linux/arm64 \
               --progress=plain \
               --build-arg QUARTO_VER="1.3.450" \
               --build-arg VENV_NAME="forecasting-poc" \
               -t rkrispin/forecast-poc:0.0.0.9002

if [[ $? = 0 ]] ; then
echo "Pushing docker..."
docker push rkrispin/forecast-poc:0.0.0.9002
else
echo "Docker build failed"
fi