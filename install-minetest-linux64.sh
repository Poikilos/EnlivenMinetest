#!/bin/bash
me=`basename "$0"`
echo
echo
echo
echo "Starting install..."
MY_NAME="install-mts.sh"
EM_CONFIG_PATH="$HOME/.config/EnlivenMinetest"
date

customExit() {
    errorCode=1
    if [ ! -z "$2" ]; then
        errorCode="$2"
    fi
    cat <<END

ERROR:
$1


END
    exit $errorCode
}

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


install_shortcut(){
    enable_clear_icon_cache=false

    _SRC_SHORTCUT_PATH=$1
    if [ ! -f "$_SRC_SHORTCUT_PATH" ]; then
        customExit "\"$_SRC_SHORTCUT_PATH\" is missing."
    fi
    _DST_SHORTCUT_NAME=$2
    # _CAPTION is optional (original "Name" is kept if not specified)
    _EXEC=$3
    _WORKING_DIR=$4
    _ICON=$5
    _CAPTION=$6
    dest_icons=$HOME/.local/share/applications
    dest_icon=$dest_icons/$_DST_SHORTCUT_NAME
    if [ ! -d "$dest_icons" ]; then
        mdkir -p "$dest_icons" || customExit "mkdir -p \"$dest_icons\" failed."
    fi
    # if [ -f "$dest_icon" ]; then
        # comment since never fixes broken icon anyway
        # TODO: fixed bad cache even if icon was rewritten properly after written improperly
        # * not tried yet:
        #   * rm $HOME/.kde/share/config/kdeglobals
        # enable_clear_icon_cache=true
    # fi
    echo "* writing icon '$dest_icon'..."
    if [ ! -z "$_ICON" ]; then
        if [ ! -z "$_CAPTION" ]; then
            cat "$_SRC_SHORTCUT_PATH" | grep -v "^Icon=" | grep -v "^Path=" | grep -v "^Exec=" | grep -v "^Name=" > "$dest_icon"
        else
            cat "$_SRC_SHORTCUT_PATH" | grep -v "^Icon=" | grep -v "^Path=" | grep -v "^Exec=" > "$dest_icon"
        fi
    else
        if [ ! -z "$_CAPTION" ]; then
            cat "$_SRC_SHORTCUT_PATH" | grep -v "^Path=" | grep -v "^Exec=" | grep -v "^Name=" > "$dest_icon"
        else
            cat "$_SRC_SHORTCUT_PATH" | grep -v "^Path=" | grep -v "^Exec=" > "$dest_icon"
        fi
    fi
    # Icon must be an absolute path (other variables use $HOME in
    # desktop file above), so exclude it above and rewrite it below:
    echo "Path=$dest_programs/minetest/bin" >> "$dest_icon"
    if [ ! -z "$_CAPTION" ]; then
        echo "Name=$_CAPTION" >> "$dest_icon"
    fi
    if [ ! -z "$_ICON" ]; then
        echo "Icon=$_ICON" >> "$dest_icon"
    fi
    echo "Exec=$_EXEC" >> "$dest_icon"
    if [ "@$enable_clear_icon_cache" = "@true" ]; then
        if [ -f "`command -v gnome-shell`" ]; then
            echo "Refreshing Gnome icons..."
            gnome-shell --replace & disown
            sleep 10
        fi
        if [ -f "$HOME/.cache/icon-cache.kcache" ]; then
            echo "clearing $HOME/.cache/icon-cache.kcache..."
            rm $HOME/.cache/icon-cache.kcache
        fi
        if [ -f "`command -v kquitapp5`" ]; then
            echo "Refreshing KDE icons..."
            if [ "`command -v kstart5`" ]; then
                kquitapp5 plasmashell && kstart5 plasmashell
            else
                kquitapp5 plasmashell && kstart plasmashell
            fi
            sleep 15
        fi
        if [ -f "`command -v xfce4-panel`" ]; then
            echo "Refreshing Xfce icons..."
            xfce4-panel -r && xfwm4 --replace
            sleep 5
        fi
        if [ -f "`command -v lxpanelctl`" ]; then
            echo "Refreshing LXDE icons..."
            lxpanelctl restart && openbox --restart
            sleep 5
        fi
    fi
}
# ^ same as install-minetest-linux64.sh
install_my_shortcut(){
    #requires SHORTCUT_PATH to already be set to a valid Minetest ".desktop" file.
    EXEC_PATH="$INSTALL_PATH/bin/minetest"
    if [ ! -f "$EXEC_PATH" ]; then
        echo "* WARNING: The Minetest executable is not present: \"$EXEC_PATH\""
    fi
    WORKING_DIR_PATH="$INSTALL_PATH/bin"
    if [ ! -d "$WORKING_DIR_PATH" ]; then
        echo "* WARNING: The Minetest working directory is not present: \"$WORKING_DIR_PATH\""
    fi
    MT_ICON="$INSTALL_PATH/misc/minetest-xorg-icon-128.png"
    if [ ! -f "$MT_ICON" ]; then
        echo "* WARNING: The Minetest icon is not present: \"$MT_ICON\""
    fi
    install_shortcut "$SHORTCUT_PATH" "org.minetest.minetest.desktop" "$EXEC_PATH" "$WORKING_DIR_PATH" "$MT_ICON" "Final Minetest"
}

DL_NAME=minetest-linux64.zip
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

if [ -z "$MY_TMP" ]; then
    MY_TMP=/tmp/minetest-webinstall
fi
mkdir -p "$MY_TMP"
EXTRACTED_PATH="$MY_TMP/$EXTRACTED_NAME"

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
        ENABLE_DL=true
    fi
done

if [ ! -f "$DL_PATH" ]; then
    ENABLE_DL=true
fi

old_release_line=
if [ -f "$INSTALL_PATH/release.txt" ]; then
    old_release_line="`cat $INSTALL_PATH/release.txt | grep Release`"
fi
old_version=
if [ ! -z "$old_release_line" ]; then
    old_version="${old_release_line##* }"  # get second word
else
    old_version="1st"
    if [ -d "$INSTALL_PATH.1st" ]; then
        old_version="bak"
    fi
fi

release_line=
RELEASE_TXT_URL="https://downloads.minetest.org/release.txt"
if [ ! -f "$MY_TMP/release.txt" ]; then
    curl $RELEASE_TXT_URL -o "$MY_TMP/release.txt" || customExit "curl $RELEASE_TXT_URL failed."
fi
release_line="`cat $MY_TMP/release.txt | grep Release`"
if [ -z "$release_line" ]; then
    cat "$MY_TMP/release.txt"
    customExit "Obtaining a Release line from $RELEASE_TXT_URL failed (got '$release_line')."
fi
version=
if [ ! -z "$release_line" ]; then
    version="${release_line##* }"  # get second word
else
    version="new"
fi

#version_len=${#version}
#if [ "$version_len" -ne "6" ]; then
#    customExit "Unexpected version scheme (not 6 characters): '$version' near '$release_line' in file $release_txt_path"
#fi

if [ "@$old_version" = "@$version" ]; then
    #if [ ! -f "$SHORTCUT_PATH" ]; then
    install_my_shortcut
    #fi
    customExit "Version $version is already installed at $INSTALL_PATH. There is nothing to do."
fi

if [ "@$ENABLE_DL" = "@true" ]; then
    if [ ! -d "$HOME/Downloads" ]; then
        mkdir -p "$HOME/Downloads"
    fi
    curl https://downloads.minetest.org/$DL_NAME -o "$DL_PATH" || exitAndDeleteDownload "The download failed."
else
    echo "* using existing $DL_PATH..."
fi
cd "$MY_TMP" || customExit "cd \"$MY_TMP\" failed."
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
killall minetest 2>/dev/null 1>&2

upgradeAndMerge(){
    UPGRADE_TYPE="$1"
    if [ ! -d "$INSTALL_PATH/$UPGRADE_TYPE" ]; then
        customExit "* WARNING: $UPGRADE_TYPE upgrade is skipped since $INSTALL_PATH/$UPGRADE_TYPE is not present."
    else
        echo "* upgrading $UPGRADE_TYPE"
        for UPGRADE_PATH in `find $INSTALL_PATH/$UPGRADE_TYPE -maxdepth 1`
        do
            UPGRADE_NAME="`basename $UPGRADE_PATH`"
            if [ "$UPGRADE_PATH" = "$INSTALL_PATH/$UPGRADE_TYPE" ]; then
                echo "  * examining $UPGRADE_PATH..."
            elif [ -d "$UPGRADE_PATH" ]; then
                echo "  * upgrading $UPGRADE_NAME..."
                if [ -d "$INSTALL_PATH.$old_version/$UPGRADE_TYPE/$UPGRADE_NAME" ]; then
                    rm -Rf "$INSTALL_PATH.$old_version/$UPGRADE_TYPE/$UPGRADE_NAME" || customExit "* rm -Rf \"$INSTALL_PATH.$old_version/$UPGRADE_TYPE/$UPGRADE_NAME\" failed."
                    mv "$UPGRADE_PATH" "$INSTALL_PATH.$old_version/$UPGRADE_TYPE/$UPGRADE_NAME" || customExit "mv \"$UPGRADE_PATH\" \"$INSTALL_PATH.$old_version/$UPGRADE_TYPE/$UPGRADE_NAME\""
                fi
            else
                echo "  * upgrading $UPGRADE_NAME..."
                mv -f "$UPGRADE_PATH" "$INSTALL_PATH.$old_version/$UPGRADE_TYPE/$UPGRADE_NAME" || customExit "mv \"$UPGRADE_PATH\" \"$INSTALL_PATH.$old_version/$UPGRADE_TYPE/$UPGRADE_NAME\""
            fi
        done
        rmdir "$INSTALL_PATH/$UPGRADE_TYPE" || customExit "rmdir \"$INSTALL_PATH/$UPGRADE_TYPE\" failed."
        mv "$INSTALL_PATH.$old_version/$UPGRADE_TYPE" "$INSTALL_PATH/" || customExit "mv \"$INSTALL_PATH.$old_version/$UPGRADE_TYPE\" \"$INSTALL_PATH/\""
    fi
}

if [ -d "$MY_TMP/$EXTRACTED_NAME" ]; then
    rm -Rf "$MY_TMP/$EXTRACTED_NAME" || customExit "* removing the old \"$MY_TMP/$EXTRACTED_NAME\" failed."
fi
unzip "$DL_PATH" || customExit "Extracting $DL_PATH failed."

if [ -d "$EXTRACTED_PATH" ]; then
    # cd "$HOME" || customExit "cd \"$HOME\" failed."
    if [ -d "$INSTALL_PATH" ]; then
        if [ -d "$INSTALL_PATH.$old_version" ]; then
            customExit "You already have an old copy of \"$INSTALL_PATH.$old_version\". You must rename it or backup your world and other data then remove it before proceeding."
        fi
        if [ ! -f "`command -v basename`" ]; then
            customExit "Install cannot continue because the basename command is not present."
        fi
        if [ ! -f "`command -v find`" ]; then
            customExit "Install cannot continue because the find command is not present."
        fi
        mv "$INSTALL_PATH" "$INSTALL_PATH.$old_version"
        mv "$EXTRACTED_PATH" "$INSTALL_PATH"
        upgradeAndMerge "games"
        upgradeAndMerge "worlds"
        upgradeAndMerge "mods"
        if [ -f "$INSTALL_PATH.$old_version/minetest.conf" ]; then
            mv "$INSTALL_PATH.$old_version/minetest.conf" "$INSTALL_PATH/minetest.conf"
        fi
    else
        mv "$EXTRACTED_PATH" "$INSTALL_PATH"
    fi
    # curl https://downloads.minetest.org/release.txt -o "$INSTALL_PATH/release.txt"
else
    customExit "Extracting \"$DL_PATH\" did not result in $EXTRACTED_PATH."
fi
echo "Installing Final Minetest $version to $INSTALL_PATH is complete."
