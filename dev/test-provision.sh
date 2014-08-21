#!/bin/bash -e

source `dirname $0`/test-environment.sh

apt-get install -y $TEST_AN_INSTALLED_DEB_NAME=$TEST_AN_INSTALLED_DEB_VERSION
apt-get remove -y $TEST_AN_UNINSTALLED_DEB

pip install $TEST_AN_INSTALLED_EGG_NAME
pip uninstall -y $TEST_AN_UNINSTALLED_EGG || echo 'Already uninstalled'
