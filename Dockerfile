FROM ubuntu:14.04

MAINTAINER Jaime Gil de Sagredo <jaimegildesagredo@gmail.com>

RUN apt-get update && \
    apt-get install -y python python-pip git

RUN apt-get install -y python-requests && \
    apt-get remove -y python-django

ADD . /src

RUN cd /src && \
    python setup.py sdist && \
    pip install dist/server-expects-`python setup.py --version`.tar.gz &&\
    pip install --upgrade -r test-requirements.txt

WORKDIR /src

CMD ["mamba"]
