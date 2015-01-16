#!/bin/bash -e

export DEBIAN_FRONTEND=noninteractive

apt-get update
apt-get install -y software-properties-common

add-apt-repository -y ppa:fkrull/deadsnakes
add-apt-repository -y ppa:pypy/ppa

apt-get update
apt-get update
apt-get remove -y ruby1.8
apt-get install -y python python3.3 python3.4 pypy python-virtualenv git ruby1.9.1-full
easy_install pip

# Fix busser crash with default ruby symlink in 14.04
rm -f /usr/bin/ruby
ln -s /usr/bin/ruby1.9.1 /usr/bin/ruby

cat `dirname $0`/data/ubuntu-14.04-environment.sh > /etc/bash.bashrc
. /etc/bash.bashrc

apt-get install -y --force-yes $TEST_AN_INSTALLED_DEB_NAME=$TEST_AN_INSTALLED_DEB_VERSION
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

# Path
function ensure_user() {
    if ! grep $1 /etc/passwd
    then
        useradd $1
    fi
}

function ensure_group() {
    if ! grep $1 /etc/group
    then
        groupadd $1
    fi
}

touch $TEST_AN_EXISTENT_FILE_PATH
ensure_user $TEST_AN_EXISTENT_FILE_OWNER
ensure_group $TEST_AN_EXISTENT_FILE_GROUP
chown $TEST_AN_EXISTENT_FILE_OWNER:$TEST_AN_EXISTENT_FILE_GROUP $TEST_AN_EXISTENT_FILE_PATH
chmod $TEST_AN_EXISTENT_FILE_MODE $TEST_AN_EXISTENT_FILE_PATH

mkdir -pv $TEST_AN_EXISTENT_DIRECTORY_PATH
ensure_user $TEST_AN_EXISTENT_DIRECTORY_OWNER
ensure_group $TEST_AN_EXISTENT_DIRECTORY_GROUP
chown $TEST_AN_EXISTENT_DIRECTORY_OWNER:$TEST_AN_EXISTENT_DIRECTORY_GROUP $TEST_AN_EXISTENT_DIRECTORY_PATH
chmod $TEST_AN_EXISTENT_DIRECTORY_MODE $TEST_AN_EXISTENT_DIRECTORY_PATH
