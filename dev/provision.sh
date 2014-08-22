#!/bin/bash -e

# FIXME: ...
if [[ -d /vagrant ]];
then
    . /vagrant/dev/environment.sh
else
    . `dirname $0`/environment.sh
fi

apt-get install -y $TEST_AN_INSTALLED_DEB_NAME=$TEST_AN_INSTALLED_DEB_VERSION
apt-get remove -y $TEST_AN_UNINSTALLED_DEB

pip install $TEST_AN_INSTALLED_EGG_NAME==$TEST_AN_INSTALLED_EGG_VERSION
pip install -e $TEST_AN_INSTALLED_EDITABLE_EGG_URL
pip uninstall -y $TEST_AN_UNINSTALLED_EGG || echo 'Already uninstalled'
