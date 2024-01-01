#!/bin/ash

QUARTO_VER=$1

apk add curl tar


mkdir -p /opt/quarto/${QUARTO_VER}


curl -o quarto.tar.gz -L \
    "https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VER}/quarto-${QUARTO_VER}-linux-amd64.tar.gz"


tar -zxvf quarto.tar.gz \
    -C "/opt/quarto/${QUARTO_VER}" \
    --strip-components=1

rm quarto.tar.gz