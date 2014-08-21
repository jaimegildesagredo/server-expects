FROM ubuntu:14.04

MAINTAINER Jaime Gil de Sagredo <jaimegildesagredo@gmail.com>

RUN apt-get update && \
    apt-get install -y python python-pip git

RUN apt-get install -y $TEST_AN_INSTALLED_PACKAGE && \
    apt-get remove -y $TEST_AN_UNINSTALLED_PACKAGE

ADD . /src

RUN cd /src && \
    python setup.py sdist && \
    pip install dist/server-expects-`python setup.py --version`.tar.gz &&\
    pip install --upgrade -r test-requirements.txt

WORKDIR /src

CMD ["mamba"]
