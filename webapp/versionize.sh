#!/usr/bin/bash

if [ -z "$1" ]; then
    echo "You must specify a zip file path OR directory path."
    exit 1
fi
customDie() {
    echo
    echo "ERROR:"
    echo "  $1"
    echo
    echo
    exit 1
}
destroy_msg=""
src_path="linux-minetest-kit"
versions_path="$HOME/git/EnlivenMinetest/webapp/minetest-versions"
if [ ! -d "$versions_path" ]; then
    mkdir -p "$versions_path" || customDie "mkdir $versions_path FAILED"
fi
src_name=""
try_path="`pwd`/$1"
if [ -f "$1" ]; then
    echo "* detected file param..."
elif [ -d "$1" ]; then
    echo "* detected directory param..."
else
    customDie "$1 is not a file or directory."
fi
cd /tmp || customDie "cannot cd to /tmp"
if [ -d versionize ]; then
    rm -Rf versionize || customDie "cannot remove /tmp/versionize"
fi
mkdir versionize || customDie "cannot create /tmp/versionize"
cd /tmp/versionize || customDie "cannot cd /tmp/versionize"
if [ -f "$1" ]; then
    echo "* detected full path..."
    try_path="$1"
elif [ -d "$1" ]; then
    echo "* detected full path..."
    try_path="$1"
fi

if [ -f "$try_path" ]; then
    # if [ ! -d "$src_path" ]; then
    unzip "$try_path"
    src_name="`ls`"
    if [ ! -d "$src_name" ]; then
        customDie "unzip $try_path did not result in a directory!"
    fi
    src_path="`pwd`/$src_name"
    destroy_msg=" (but will be destroyed on next run)"
    if [ ! -d "$src_path" ]; then
        customDie "$src_path from unzip $try_path is not a directory!"
    fi
elif [ -d "$try_path" ]; then
    src_path="$try_path"
    src_name="`basename $src_path`"
else
    customDie "$try_path is not a file or directory."
fi
if [ ! -f "$src_path/release.txt" ]; then
    echo
    echo
    echo "* '$src_path' remains$destroy_msg."
    customDie "Missing $src_path/release.txt"
fi
release_line="`head -n 1 $src_path/release.txt`"
version="${release_line##* }"  # get second word
version_len=${#version}
if [ "$version_len" -ne "6" ]; then
    customDie "Unexpected version scheme (not 6 characters): '$version'"
fi
echo "src_name=$src_name"
echo "src_path=$src_path"
echo "version=$version"
# dest_path="$versions_path/$src_name-$version"
dest_path="$versions_path/linux-minetest-kit-$version"
echo "dest_path=$dest_path"
if [ -d "$dest_path" ]; then
    echo
    echo "There is nothing to do. Directory $dest_path exists."
    echo "* '$src_path' remains$destroy_msg."
    echo
    echo
    exit 0
fi
mv "$src_path" "$dest_path" || customDie "Failed to move to 'dest_path'"
echo
echo "Done."
echo
echo
