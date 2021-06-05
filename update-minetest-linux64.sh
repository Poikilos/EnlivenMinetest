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
fi
#if [ ! -f "$MT_BASH_RC_PATH" ]; then
if [ ! -d "$REPO_PATH" ]; then
    if [ -f "$MT_BASH_RC_PATH" ]; then
        echo "* updating \"$MT_BASH_RC_PATH\"..."
        rm $MT_BASH_RC_PATH
    fi
    # ^ Always upgrade the rc file manually if it is not in the repo.
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
else
    echo "* using existing $MT_BASH_RC_PATH"
    echo "  * To update it, run: cd \"$REPO_PATH\" && git pull"
    echo "    * If that doesn't work run the following:"
    echo "      mv $REPO_PATH /tmp/EnlivenMinetest.old && git clone https://github.com/poikilos/EnlivenMinetest $REPO_PATH"
fi
if [ ! -f "$MT_BASH_RC_PATH" ]; then
    echo
    echo "$MT_BASH_RC_PATH is not present."
    echo
    sleep 10
    exit 1
fi
source $MT_BASH_RC_PATH
# ^ same as install-mts.sh, versionize.sh, minetestenv.rc

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
    SHORTCUT_PATH="$TRY_ORG_PATH"ungitify_mod
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

findAndInstallENLIVENOrAskDL() {
    if [ ! -d "$INSTALL_PATH/games/ENLIVEN" ]; then
        if [ ! -d "$REPO_PATH" ]; then
            if [ -f "`command -v git`" ]; then
                mkdir -p "$REPO_PATH"
                rmdir --ignore-fail-on-non-empty "$REPO_PATH"
                git clone https://github.com/poikilos/EnlivenMinetest "$REPO_PATH"
            else
                echo "* INFO: Installing ENLIVEN has been skipped. This script and the ENLIVEN build script require git for that. On Ubuntu or Debian, first try 'sudo apt-get -y install git' or if on Fedora, try 'sudo dnf -y install git'. Otherwise, try to find git in your \"Software\" or other software center application."
            fi
        else
            echo "* ENLIVEN build scripts were detected in: $REPO_PATH"
            echo "  To update them, run: cd \"$REPO_PATH\" && git pull"
        fi
    fi
    if [ -d "$REPO_PATH" ]; then
        # If it didn't
        installOrUpgradeENLIVEN "$INSTALL_PATH"
        code=$?
        if [ $code -eq 2 ]; then
            echo "  * skipped"
        elif [ $code -eq 0 ]; then
            echo "  * Installing ENLIVEN to $INSTALL_PATH/games is complete."
        else
            echo "(installOrUpgradeMinetest failed with error code $code)"
        fi
    fi
}

installAmhiPatchIfPresent() {
    aGameID=amhi_game
    aMinetest="$INSTALL_PATH"
    if [ -d "$aMinetest/games/amhi_game" ]; then
        if [ -d "$REPO_PATH/patches/$aGameID" ]; then
            echo "* patching $aGameID from $REPO_PATH/patches/$aGameID..."
            if [ "`command -v rsync`" ]; then
                rsync -rt --ignore-times "$REPO_PATH/patches/$aGameID/" "$aMinetest/games/amhi_game/"
            else
                if [ ! -d "$aMinetest/games/amhi_game/menu" ]; then
                    mkdir -p "$aMinetest/games/amhi_game/menu"
                fi
                "  using cp for known files since rsync is not present..."
                cp -f $REPO_PATH/patches/$aGameID/menu/icon.* $aMinetest/games/amhi_game/menu/
            fi
            if [ $? -eq 0 ]; then
                echo "  OK"
            else
                echo "  FAILED"
            fi
        fi
    fi
}


if [ "@$old_release_version" = "@$new_release_version" ]; then
    install_mt_in_place_shortcut "$SHORTCUT_PATH" "$INSTALL_PATH"
    #if [ ! -f "$SHORTCUT_PATH" ]; then
    #fi
    #show_os_release
    echo
    echo
    echo "* Adding the icon is complete. See the Desktop or applications (under Games usually--otherwise, search for Final Minetest in the Activities menu if in GNOME or GNOME-based Ubuntu versions 18.04 or later and you do not have a desktop icons extension enabled)."
    echo
    installAmhiPatchIfPresent
    findAndInstallENLIVENOrAskDL
    echo
    echo "Version $new_release_version is already installed at $INSTALL_PATH."
    echo "There is nothing more to do."
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
code=$?
if [ $code -eq 2 ]; then
    echo "Final Minetest wasn't upgraded. See the message above."
elif [ $code -eq 0 ]; then
    echo "Installing Final Minetest $new_release_version to $INSTALL_PATH is complete."
else
    echo "(installOrUpgradeMinetest failed with error code $code)"
fi
echo "  - old:$old_release_version; new:$new_release_version"

installAmhiPatchIfPresent
findAndInstallENLIVENOrAskDL

install_mt_in_place_shortcut "$SHORTCUT_PATH" "$INSTALL_PATH"
echo
