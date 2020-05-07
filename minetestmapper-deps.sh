#!/bin/bash

customExit() {
    echo
    echo
    echo "ERROR:"
    echo "$1"
    echo "You'll need to manually install:"
    echo "libgd sqlite3 LevelDB hiredis Postgres"
    echo
    echo
    exit 1
}


PACKAGE_TYPE=
if [ -f "`command -v apt`" ]; then
    INSTALL_CMD="apt -y install"
    PACKAGE_TYPE="deb"
elif [ -f "`command -v apt-get`" ]; then
    INSTALL_CMD="apt-get -y install"
    PACKAGE_TYPE="deb"
elif [ -f "`command -v dnf`" ]; then
    INSTALL_CMD="dnf -y install"
    PACKAGE_TYPE="rpm"
elif [ -f "`command -v yum`" ]; then
    INSTALL_CMD="yum -y install"
    PACKAGE_TYPE="rpm"
else
    customExit "Your package system is not implemented in this script."
fi
if [ "@$PACKAGE_TYPE" = "@deb" ]; then
    sudo $INSTALL_CMD libgd-dev libsqlite3-dev libleveldb-dev libhiredis-dev libpq-dev
elif [ "@$PACKAGE_TYPE" = "@rpm" ]; then
    sudo $INSTALL_CMD gd-devel sqlite-devel leveldb-devel hiredis-devel libpq-devel
else
    customExit "The package names for your OS are unknown."
fi
