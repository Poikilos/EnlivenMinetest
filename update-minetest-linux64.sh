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
    if [ $? -ne 0 ]; then
    #if [ ! -f "$MT_BASH_RC_PATH" ]; then
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
# ^ same as install-mts.sh

#INSTALL_SCRIPT_NAME="update-minetest-linux64.sh"

echo "* starting download..."
date

if [ -z "$INSTALL_MODE" ]; then
    INSTALL_MODE="move"
fi
DL_NAME=minetest-linux64.zip
RELEASE_ARC_URL="https://downloads.minetest.org/$DL_NAME"
DL_PATH=$HOME/Downloads/$DL_NAME
EXTRACTED_NAME=minetest-linux64
if [ -z "$INSTALL_PATH" ]; then
    INSTALL_PATH="$HOME/minetest"
fi
SHORTCUT_PATH="$INSTALL_PATH/misc/net.minetest.minetest.desktop"
TRY_ORG_PATH="$INSTALL_PATH/misc/org.minetest.minetest.desktop"
if [ -f "$TRY_ORG_PATH" ]; then
    SHORTCUT_PATH="$TRY_ORG_PATH"
fi

mkdir -p "$EM_TMP"
EXTRACTED_PATH="$EM_TMP/$EXTRACTED_NAME"
if [ -d "$EXTRACTED_PATH" ]; then
    rm -Rf "$EXTRACTED_PATH" || customExit "Deleting the old $EXTRACTED_PATH failed."
fi

exitAndDeleteDownload(){
    if [ -f "$DL_PATH" ]; then
        echo "* removing \"$DL_PATH\" since it didn't work..."
        rm -f "$DL_PATH"
    fi
    customExit "$1" $2
}

if [ -d "$HOME/minetest-linux64" ]; then
    if [ ! -d "$INSTALL_PATH" ]; then
        mv "$HOME/minetest-linux64" "$INSTALL_PATH"
        # ^ so that code below can find an existing installation
    fi
fi

if [ -f "$HOME/$DL_NAME" ]; then
    DL_PATH="$HOME/$DL_NAME"
fi

if [ -z "$ENABLE_DL" ]; then
    ENABLE_DL=false
fi

for var in "$@"
do
    if [ "@$var" = "@--update" ]; then
        # This doesn't do much yet.
        ENABLE_DL=true
    fi
done

if [ ! -f "`command -v unzip`" ]; then
    cat <<END
You are missing the unzip command.
END
    if [ -f "`command -v apt-get`" ]; then
        cat<<END
Try:
sudo apt-get update -y
sudo apt-get install -y unzip
END
    elif [ -f "`command -v dnf`" ]; then
        cat<<END
Try:
sudo dnf install -y unzip
END
    fi
    exit 1
fi

if [ ! -f "$DL_PATH" ]; then
    ENABLE_DL=true
fi



old_release_line=
old_release_version=
detect_installed_mt_version "1st" "bak"

if [ -z "$old_release_version" ]; then
    customExit "Detecting old_release_version failed."
fi

RELEASE_TXT_URL="https://downloads.minetest.org/release.txt"
detect_mt_version_at "$EM_TMP" "https://downloads.minetest.org/release.txt" "new"

if [ "@$old_release_version" = "@$new_release_version" ]; then
    install_mt_in_place_shortcut "$SHORTCUT_PATH" "$INSTALL_PATH"
    #if [ ! -f "$SHORTCUT_PATH" ]; then
    #fi
    #show_os_release
    echo
    echo
    echo "Version $new_release_version is already installed at $INSTALL_PATH. There is nothing to do."
    echo
    exit 0
fi

if [ "@$ENABLE_DL" = "@true" ]; then
    if [ ! -d "$HOME/Downloads" ]; then
        mkdir -p "$HOME/Downloads"
    fi
    curl "$RELEASE_ARC_URL" -o "$DL_PATH" || exitAndDeleteDownload "The download failed."
else
    echo "* using existing $DL_PATH..."
fi
cd "$EM_TMP" || customExit "cd \"$EM_TMP\" failed."

killall minetest 2>/dev/null 1>&2

if [ -d "$EM_TMP/$EXTRACTED_NAME" ]; then
    rm -Rf "$EM_TMP/$EXTRACTED_NAME" || customExit "* removing the old \"$EM_TMP/$EXTRACTED_NAME\" failed."
fi
unzip "$DL_PATH" > /dev/null || customExit "Extracting $DL_PATH failed."

UNUSED_MT_PATH="$INSTALL_PATH.$old_release_version"
installOrUpgradeMinetest "$EXTRACTED_PATH" "$INSTALL_PATH" "$UNUSED_MT_PATH"
echo "Installing Final Minetest $new_release_version to $INSTALL_PATH is complete."
echo "  - old:$old_release_version; new:$new_release_version"
echo "* installing ENLIVEN..."
installOrUpgradeENLIVEN "$INSTALL_PATH"
install_mt_in_place_shortcut "$SHORTCUT_PATH" "$INSTALL_PATH"
echo
