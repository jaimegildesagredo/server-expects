FROM ubuntu:12.04

MAINTAINER Jaime Gil de Sagredo <jaimegildesagredo@gmail.com>

RUN apt-get update && \
    apt-get install -y python python-pip git

ADD . /src

RUN /src/dev/test-provision.sh

RUN cd /src && \
    python setup.py sdist && \
    pip install dist/server-expects-`python setup.py --version`.tar.gz &&\
    pip install --upgrade -r test-requirements.txt

RUN . /src/dev/test-environment.sh && \
    cd /src && \
    mamba
