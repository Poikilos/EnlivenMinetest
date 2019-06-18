#!/usr/bin/bash

if [ -z "$original_src_path" ]; then
    original_src_path="$1"
fi
if [ -z "$original_src_path" ]; then
    if [ -f "linux-minetest-kit.zip" ]; then
        original_src_path="linux-minetest-kit.zip"
        echo "* no script argument, so using linux-minetest-kit.zip"
    else
        echo "* original_src_path (linux-minetest-kit.zip) not detected"
    fi
fi
if [ -z "$original_src_path" ]; then
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
# src_path: extracted name (always linux-mintetest-kit unless source is
#   archive, in which case src_path is detected)
src_path="linux-minetest-kit"
versions_path="$HOME/git/EnlivenMinetest/webapp/minetest-versions"
if [ ! -d "$versions_path" ]; then
    mkdir -p "$versions_path" || customDie "mkdir $versions_path FAILED"
fi
src_name=""
try_path="`pwd`/$original_src_path"
if [ -f "$original_src_path" ]; then
    echo "* detected file param..."
elif [ -d "$original_src_path" ]; then
    echo "* detected directory param..."
else
    customDie "$original_src_path is not a file or directory."
fi
cd /tmp || customDie "cannot cd to /tmp"
if [ -d versionize ]; then
    rm -Rf versionize || customDie "cannot remove /tmp/versionize"
fi
mkdir versionize || customDie "cannot create /tmp/versionize"
cd /tmp/versionize || customDie "cannot cd /tmp/versionize"
src_archive=
if [ -f "$original_src_path" ]; then
    echo "* detected full path..."
    try_path="$original_src_path"
    src_archive="$original_src_path"
elif [ -d "$original_src_path" ]; then
    echo "* detected full path..."
    try_path="$original_src_path"
fi

if [ -f "$try_path" ]; then
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

if [ ! -z "$src_archive" ]; then
    # The effectiveness of any bash extension extraction is debatable--
    # see
    # <https://stackoverflow.com/questions/965053/extract-filename-and-extension-in-bash>
    filename=$(basename -- "$fullfile")
    extension="${filename##*.}"
    filename="${filename%.*}"
    dst_archive="$versions_path/$filename-$version.$extension"
    if [ -f "$src_archive" ]; then
        mv "$src_archive" "$dst_archive" || customDie "Cannot mv '$src_archive' '$dst_archive'"
        echo "* moved archive to '$dst_archive'"
        echo
        echo
    else
        echo "* ERROR: '$src_archive' is not accessible from `pwd`--"
        echo "  skipping:"
        echo "    mv '$src_archive' '$dst_archive'"
        echo
        echo
    fi
fi
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
