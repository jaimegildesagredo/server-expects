#!/bin/bash -e

VENV=$HOME/venv
SOURCE=$HOME/src

virtualenv $HOME/venv
. $VENV/bin/activate

mkdir -p $SOURCE
cp -R /vagrant/* $SOURCE

cd $SOURCE

./dev/install.sh
./dev/tests.sh
