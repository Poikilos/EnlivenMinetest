#!/bin/bash
if [ -d "linux-minetest-kit" ]; then
    >&2 echo "Error: linux-minetest-kit is already here. To update it safely, rename it, otherwise do:"
    >&2 echo "    rm -rf '`pwd`/linux-minetest-kit'"
    exit 1
fi
# cd ~
ZIP_NAME=linux-minetest-kit.zip
REMOTE_ZIP=mtio:/opt/minebest/assemble/prod/linux-minetest-kit.zip
rsync -tvP $REMOTE_ZIP .
code=$?
if [ $code -ne 0 ]; then
    >&2 echo "Error: 'rsync -tvP $REMOTE_ZIP .' failed in \"`pwd`\". Make sure it was built on the other server or change $0 to match the correct location."
    exit $code
fi
unzip $ZIP_NAME
code=$?
if [ $code -ne 0 ]; then
    >&2 echo "Error: 'unzip $ZIP_NAME' failed in \"`pwd`\"."
    exit $code
fi
exit 0
