#!/bin/bash -e

VENV=$HOME/server-expects-venv
SOURCE=$HOME/server-expects-src

rm -rf $VENV
virtualenv $VENV
. $VENV/bin/activate

mkdir -p $SOURCE
cp -R /vagrant/* $SOURCE

cd $SOURCE

./dev/install.sh
./dev/tests.sh
