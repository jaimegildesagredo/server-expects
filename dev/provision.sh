#!/bin/bash -e

# FIXME: ...
if [[ -d /vagrant ]];
then
    . /vagrant/dev/environment.sh
else
    . `dirname $0`/environment.sh
fi

export DEBIAN_FRONTEND=noninteractive

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
