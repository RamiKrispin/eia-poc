FROM python:3.10

ARG QUARTO_VER="1.3.450"
ARG VENV_NAME=my_project
ENV QUARTO_VER=$QUARTO_VER
ENV VENV_NAME=$VENV_NAME
RUN mkdir requirements
COPY requirements.txt install_requirements.sh install_quarto.sh install_dependencies.sh requirements/

RUN bash ./requirements/install_dependencies.sh
RUN bash ./requirements/install_requirements.sh $VENV_NAME
RUN bash ./requirements/install_quarto.sh $QUARTO_VER


