#!/bin/bash -e

VENV=$HOME/venv
SOURCE=$HOME/src

rm -rf $VENV
virtualenv $VENV
. $VENV/bin/activate

mkdir -p $SOURCE
cp -R /vagrant/* $SOURCE

cd $SOURCE

./dev/install.sh
./dev/tests.sh
