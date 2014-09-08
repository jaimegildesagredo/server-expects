#!/bin/bash -e

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get update
apt-get remove -y ruby1.8
apt-get install -y python python-virtualenv git ruby1.9.1-full

pip install `dirname $0`/data/server-expects.tar.gz

cat `dirname $0`/data/ubuntu-12.04-environment.sh > /etc/bash.bashrc
. /etc/bash.bashrc

apt-get install -y $TEST_AN_INSTALLED_DEB_NAME=$TEST_AN_INSTALLED_DEB_VERSION
apt-get remove -y $TEST_AN_UNINSTALLED_DEB

pip install $TEST_AN_INSTALLED_EGG_NAME==$TEST_AN_INSTALLED_EGG_VERSION
pip install -e $TEST_AN_INSTALLED_EDITABLE_EGG_URL
pip uninstall -y $TEST_AN_UNINSTALLED_EGG || echo 'Already uninstalled'

virtualenv $TEST_A_VIRTUALENV_PATH
$TEST_A_VIRTUALENV_PATH/bin/pip install $TEST_A_VIRTUALENV_INSTALLED_EGG
$TEST_A_VIRTUALENV_PATH/bin/pip uninstall -y $TEST_A_VIRTUALENV_UNINSTALLED_EGG || echo 'Already uninstalled'

rm -rf $TEST_A_NONEXISTENT_VIRTUALENV_PATH

echo "$TEST_AN_UNREACHABLE_IP $TEST_AN_UNREACHABLE_HOST" >> /etc/hosts

# MySQL
apt-get install -y mysql-server

if ! mysql -u"$TEST_A_MYSQL_EXISTENT_USER" -p"$TEST_A_MYSQL_VALID_PASSWORD" -e 'SELECT 1'
then
    mysql -e "CREATE USER '$TEST_A_MYSQL_EXISTENT_USER' IDENTIFIED BY '$TEST_A_MYSQL_VALID_PASSWORD'"
fi

mysql -e "CREATE DATABASE IF NOT EXISTS $TEST_A_MYSQL_EXISTENT_DATABASE"
mysql -e "GRANT SELECT ON $TEST_A_MYSQL_EXISTENT_DATABASE.* TO '$TEST_A_MYSQL_EXISTENT_USER' IDENTIFIED BY '$TEST_A_MYSQL_VALID_PASSWORD'"
mysql -e "DROP DATABASE IF EXISTS $TEST_A_MYSQL_NONEXISTENT_DATABASE"
