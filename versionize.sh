#!/bin/bash
#!/bin/bash
clear
me=`basename "$0"`
echo
echo
echo
scripting_rc_path=~/.config/EnlivenMinetest/scripting.rc
if [ -f "$EM_CONFIG_PATH/scripting.rc" ]; then
    echo "* [$MT_ENV_RUP_NAME] using $scripting_rc_path..."
    source $scripting_rc_path
fi
if [ -z "$REPO_PATH" ]; then
    REPO_PATH="$HOME/git/EnlivenMinetest"
fi
MT_BASH_RC_NAME="minetestenv-in-place.rc"
CURRENT_MT_SCRIPTS_DIR="$HOME/.local/bin"
MT_BASH_RC_PATH="$CURRENT_MT_SCRIPTS_DIR/$MT_BASH_RC_NAME"
TRY_CURRENT_MT_SCRIPTS_DIR="$REPO_PATH"
TRY_MT_BASH_RC_PATH="$TRY_CURRENT_MT_SCRIPTS_DIR/$MT_BASH_RC_NAME"
if [ -f "$TRY_MT_BASH_RC_PATH" ]; then
    CURRENT_MT_SCRIPTS_DIR="$TRY_CURRENT_MT_SCRIPTS_DIR"
    MT_BASH_RC_PATH="$TRY_MT_BASH_RC_PATH"
#fi
#if [ ! -f "$MT_BASH_RC_PATH" ]; then
else
    if [ ! -d "$CURRENT_MT_SCRIPTS_DIR" ]; then
        mkdir -p "$CURRENT_MT_SCRIPTS_DIR"
    fi
    MT_BASH_RC_URL=https://raw.githubusercontent.com/poikilos/EnlivenMinetest/master/$MT_BASH_RC_NAME
    curl $MT_BASH_RC_URL -o "$MT_BASH_RC_PATH"
    if [ $? -ne 0 ]; then
    #if [ ! -f "$MT_BASH_RC_PATH" ]; then
        # This is necessary on cygwin for some reason.
        curl $MT_BASH_RC_URL > "$MT_BASH_RC_PATH"
    fi
    #if [ $? -ne 0 ]; then
    if [ ! -f "$MT_BASH_RC_PATH" ]; then
        # This is necessary on cygwin for some reason.
        wget -O "$MT_BASH_RC_PATH" $MT_BASH_RC_URL
    fi
    if [ $? -ne 0 ]; then
        echo
        echo "ERROR: Downloading $MT_BASH_RC_URL to $MT_BASH_RC_PATH failed."
        echo
        sleep 10
        exit 1
    fi
fi
if [ ! -f "$MT_BASH_RC_PATH" ]; then
    echo
    echo "$MT_BASH_RC_PATH is not present."
    echo
    sleep 10
    exit 1
fi
source $MT_BASH_RC_PATH
# ^ same as install-mts.sh, update-minetest-linux64.sh

echo
echo "Collecting version..."
EM_CONFIG_PATH=$HOME/.config/EnlivenMinetest
cd "$EM_CONFIG_PATH" || customExit "[versionize.sh] cd \"$EM_CONFIG_PATH\" failed."
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
customExit() {
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
    mkdir -p "$versions_path" || customExit "mkdir $versions_path FAILED"
fi
src_name=""
try_path="$EM_CONFIG_PATH/$original_src_path"
if [ -f "$original_src_path" ]; then
    echo "* detected file param..."
elif [ -d "$original_src_path" ]; then
    echo "* detected directory param..."
else
    customExit "$original_src_path is not a file or directory."
fi
cd /tmp || customExit "cannot cd to /tmp"
if [ -d versionize ]; then
    rm -Rf versionize || customExit "cannot remove /tmp/versionize"
fi
mkdir versionize || customExit "cannot create /tmp/versionize"
cd /tmp/versionize || customExit "cannot cd /tmp/versionize"
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
        customExit "unzip $try_path did not result in a directory!"
    fi
    src_path="`pwd`/$src_name"
    destroy_msg=" (but will be destroyed on next run)"
    if [ ! -d "$src_path" ]; then
        customExit "$src_path from unzip $try_path is not a directory!"
    fi
elif [ -d "$try_path" ]; then
    src_path="$try_path"
    src_name="`basename $src_path`"
else
    customExit "$try_path is not a file or directory."
fi

KIT_RELEASE_TXT=$src_path/release.txt
BIN_RELEASE_TXT=$src_path/minetest/release.txt
if [ ! -f "$BIN_RELEASE_TXT" ]; then
    if [ -f "$KIT_RELEASE_TXT" ]; then
        # This is expected to occur since we only now unzipped it.
        #if [ -d "BIN_RELEASE_TXT=$src_path/minetest" ]; then
        cp "$KIT_RELEASE_TXT" "$BIN_RELEASE_TXT"
        #fi
    fi
fi
detect_mt_version_at "$src_path"
if [ -z "$new_release_version" ]; then
    detect_mt_version_at "$src_path/minetest"
fi
# ^ DOES exit if no 6-digit version is detected when no 3rd param
#   is provided.

if [ -z "$new_release_version" ]; then
    echo "new_release_version from $src_path/minetest is blank."
    exit 1
fi

echo "src_name=$src_name"
echo "src_path=$src_path"
echo "new_release_version=$new_release_version"
# dest_path="$versions_path/$src_name-$new_release_version"
dest_path="$versions_path/linux-minetest-kit-$new_release_version"
echo "dest_path=$dest_path"

if [ ! -z "$src_archive" ]; then
    echo "* Collecting src_archive '$src_archive'"
    # The effectiveness of any bash extension extraction is debatable--
    # see
    # <https://stackoverflow.com/questions/965053/extract-filename-and-extension-in-bash>
    filename=$(basename -- "$src_archive")
    extension="${filename##*.}"
    filename="${filename%.*}"
    dst_archive="$versions_path/$filename-$new_release_version.$extension"
    if [ -f "$dst_archive" ]; then
        customWarn "This will overwrite '$dst_archive' with '$src_archive'."
    fi
    if [ -f "$src_archive" ]; then
        mv "$src_archive" "$dst_archive" || customExit "Cannot mv '$src_archive' '$dst_archive'"
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
mv "$src_path" "$dest_path" || customExit "Failed to move to 'dest_path'"
echo
echo "Done $0."
echo
echo
