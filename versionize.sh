#!/bin/bash
echo
echo "Collecting version..."
MY_NAME="versionize.sh"
EM_CONFIG_PATH=$HOME/.config/EnlivenMinetest
cd "$EM_CONFIG_PATH" || customDie "[$MY_NAME] cd \"$EM_CONFIG_PATH\" failed."
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
customWarn() {
    cat <<END

WARNING:
$1


END
    echo -en "\a" > /dev/tty0  # beep (You must specify a tty path if not in console mode)
    echo "Press Ctrl+C to cancel..."
    sleep 1
    echo -en "\a" > /dev/tty0
    echo "3..."
    sleep 1
    echo -en "\a" > /dev/tty0
    echo "2..."
    sleep 1
    echo -en "\a" > /dev/tty0
    echo "1..."
    sleep 1
}
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
src_path="$EM_CONFIG_PATH/linux-minetest-kit"
versions_path="$EM_CONFIG_PATH/minetest-versions"
if [ ! -d "$versions_path" ]; then
    mkdir -p "$versions_path" || customDie "mkdir $versions_path FAILED"
fi
src_name=""
try_path="$EM_CONFIG_PATH/$original_src_path"
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
if [ -f "$original_src_path" ]; then
    echo "* detected archive file full path..."
    try_path="$original_src_path"
elif [ -d "$original_src_path" ]; then
    echo "* detected directory full path..."
    try_path="$original_src_path"
fi

src_archive=
if [ -f "$try_path" ]; then
    src_archive="$try_path"
    echo "* set src_archive to '$try_path'"
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
release_txt_path="$src_path/minetest/release.txt"
if [ ! -f "$release_txt_path" ]; then
    try_release_txt_path="$src_path/release.txt"
    if [ ! -f "$try_release_txt_path" ]; then
        echo
        echo
        echo "* '$src_path' remains$destroy_msg."
        customDie "Missing $release_txt_path (or $src_path/release.txt)"
    else
        echo "Missing $release_txt_path (usually copied from $try_release_txt_path by EnlivenMinetest compille script(s)); reverting to $try_release_txt_path"
        release_txt_path="$try_release_txt_path"
    fi
fi
release_line="`head -n 1 $release_txt_path`"
version="${release_line##* }"  # get second word
version_len=${#version}
if [ "$version_len" -ne "6" ]; then
    customDie "Unexpected version scheme (not 6 characters): '$version' near '$release_line' in file $release_txt_path"
fi
echo "src_name=$src_name"
echo "src_path=$src_path"
echo "version=$version"
# dest_path="$versions_path/$src_name-$version"
dest_path="$versions_path/linux-minetest-kit-$version"
echo "dest_path=$dest_path"

if [ ! -z "$src_archive" ]; then
    echo "* Collecting src_archive '$src_archive'"
    # The effectiveness of any bash extension extraction is debatable--
    # see
    # <https://stackoverflow.com/questions/965053/extract-filename-and-extension-in-bash>
    filename=$(basename -- "$src_archive")
    extension="${filename##*.}"
    filename="${filename%.*}"
    dst_archive="$versions_path/$filename-$version.$extension"
    if [ -f "$dst_archive" ]; then
        customWarn "This will overwrite '$dst_archive' with '$src_archive'."
    fi
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
else
    echo "* There is no src_archive to collect."
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
echo "Done $0."
echo
echo
