FROM python:3.10

ARG VENV_NAME=my_project
ENV VENV_NAME=$VENV_NAME
RUN mkdir requirements
COPY requirements.txt install_requirements.sh requirements/

# RUN python3 -m venv /opt/$VENV_NAME  \
#     && export PATH=/opt/$VENV_NAME/bin:$PATH \
#     && echo "source /opt/$VENV_NAME/bin/activate" >> ~/.bashrc

# RUN source /opt/$VENV_NAME/bin/activate 
# RUN pip3 install -r ./requirements/requirements.txt

RUN bash ./requirements/install_requirements.sh $VENV_NAME


