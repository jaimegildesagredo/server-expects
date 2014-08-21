FROM ubuntu:12.04

MAINTAINER Jaime Gil de Sagredo <jaimegildesagredo@gmail.com>

RUN apt-get update && \
    apt-get install -y python python-pip git

ADD . /src

RUN . /src/.test-env.sh && \
    apt-get install -y $TEST_AN_INSTALLED_DEB_NAME=$TEST_AN_INSTALLED_DEB_VERSION && \
    apt-get remove -y $TEST_AN_UNINSTALLED_DEB

RUN cd /src && \
    python setup.py sdist && \
    pip install dist/server-expects-`python setup.py --version`.tar.gz &&\
    pip install --upgrade -r test-requirements.txt

RUN . /src/.test-env.sh && \
    cd /src && \
    mamba
