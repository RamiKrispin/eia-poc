#!/usr/bin/env bash

VENV_NAME=$1

python3 -m venv /opt/$VENV_NAME  \
    && export PATH=/opt/$VENV_NAME/bin:$PATH \
    && echo "source /opt/$VENV_NAME/bin/activate" >> ~/.bashrc

source /opt/$VENV_NAME/bin/activate 

pip3 install  --no-cache-dir -r ./requirements/requirements.txt