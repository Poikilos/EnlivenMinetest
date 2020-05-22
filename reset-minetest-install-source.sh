#!/bin/bash


# ## Developer notes
# ### Error checking
# The following matches *may* be errors (no `$` before variable):
# - `-d "[^$ 1234567890@]`
# - `-f "[^$ 1234567890@]`
# - `-z "[^$ 1234567890@]`
# - `[ "[^$ 1234567890@]`
# - `= "[^$ 1234567890@]`
echo
echo
echo
echo "Starting cleanup and library rebuild..."
date
MY_NAME="reset-minetest-install-source.sh"
EM_CONFIG_PATH=$HOME/.config/EnlivenMinetest

zip_name=linux-minetest-kit.zip
EM_TMP=/tmp/EnlivenMinetest
if [ ! -d "$EM_TMP" ]; then
    mkdir -p "$EM_TMP"
fi
TMP_DL_PATH="$EM_TMP/$zip_name"
extracted_name=linux-minetest-kit
EM_CONFIG_PATH=~/.config/EnlivenMinetest
extracted_path="$EM_CONFIG_PATH/$extracted_name"
if [ ! -d "$EM_CONFIG_PATH" ]; then
    mkdir -p "$EM_CONFIG_PATH"
fi

in_use_name=minetest
#not reliable with bash -e (if not running, check throws error):
#running=`ps ax | grep -v grep | grep $in_use_name | wc -l`
#if [ $running -gt 0 ]; then
#  echo "killing minetest processes..."
#  killall $in_use_name
#fi
url=https://downloads.minetest.org
release_txt_url=http://downloads.minetest.org/release.txt
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

customExit () {
    exitCode=1
    if [ ! -z "$2" ]; then
        exitCode=$2
    fi
    echo "ERROR:"
    echo "$1"
    exit $exitCode
}
available_release_line=`curl http://downloads.minetest.org/release.txt | head -n 1`
# echo "Release data: $available_release_line"  # "Release *" where * is YYMMDD
# See <https://unix.stackexchange.com/questions/174037/extracting-the-second-word-from-a-string-variable>
available_version=$(echo $available_release_line | awk '{print $2}')
# OR: available_version="${available_release_line##* }"  # get second word
if [ ${#available_version} -ne 6 ]; then
    customExit "The available version is not recognized: $available_version"
fi
INSTALL_PATH="$HOME/minetest"
installed_release_line=`head -n 1 $INSTALL_PATH/release.txt`
installed_version=$(echo $installed_release_line | awk '{print $2}')
compiled_release_line=`head -n 1 $extracted_path/release.txt`
extracted_path_msg=
if [ ! -d "$extracted_path" ]; then
    extracted_path_msg="(not present)"
fi
compiled_version=$(echo $compiled_release_line | awk '{print $2}')
echo "installed_version: $installed_version ($INSTALL_PATH/release.txt)"
echo "compiled_version: $compiled_version$extracted_path_msg ($extracted_path/release.txt)"
echo "available_version: $available_version ($release_txt_url)"
enable_offline=false
enable_keep=false
enable_rebuild=false
for var in "$@"
do
    if [ "@$var" = "@--offline" ]; then
        enable_offline=true
    elif [ "@$var" = "@--keep" ]; then
        enable_keep=true
    elif [ "@$var" = "@--rebuild" ]; then
        enable_rebuild=true
    else
        customExit "Invalid argument: $var"
    fi
done

if [ "@$installed_version" = "@$available_version" ]; then
    if [ "@$enable_rebuild" = "@false" ]; then
        echo "You already have the latest version. Use the \"--rebuild\" option to rebuild anyway."
        exit 1
    fi
fi
if [ "@$compiled_version" != "@$installed_version" ]; then
    if [ ! -z "$compiled_version" ]; then
        echo "ERROR: You have not yet installed version $compiled_version which you already compiled (you have installed $installed_version)."
        echo "You should run ./install-mts.sh instead (with --client option if you want more than minetestserver)"
        exit 2
    else
        # You do not have the source code at all.
        if [ "@$installed_version" = "@$available_version" ]; then
            echo "WARNING: You already have release $installed_version, but the source code preparation will continue since you do not have a detectable version of the source code (no release.txt containing \"Release <release>\")."
        else
            echo "* The source code preparation will continue since you do not have a detectable version of the source code (no release.txt containing \"Release <release>\")."
        fi
    fi
fi

cd "$EM_CONFIG_PATH" || customExit "[$MY_NAME] cd \"$EM_CONFIG_PATH\" failed."
if [ "@$enable_keep" = "@true" ]; then
    enable_offline=true
fi
if [ ! -z "$compiled_version" ]; then
    if [ "$compiled_version" = "$available_version" ]; then
        enable_offline=true
        echo "* --offline has been automatically enabled since the compiled_version $compiled_version is the same as the available version."
    fi
fi

if [ "@$enable_offline" = "@true" ]; then
    if [ ! -f "$zip_name" ]; then
        if [ "@$enable_keep" = "@true" ]; then
            if [ ! -d "$extracted_path" ]; then
                customExit "* Offline install is impossible without '`pwd`/$zip_name' (or '$extracted_path' with the --keep option)."
            else
                echo "* keeping existing \"$extracted_path\"..."
            fi
        else
            customExit "* Offline install is impossible without '`pwd`/$zip_name' (or '$extracted_path' when using the --keep option)."
        fi
    fi
else
    if [ -d "$EM_CONFIG_PATH/$zip_name" ]; then
        customExit "Remove the invalid directory \"$EM_CONFIG_PATH/$zip_name\" first so that a file with that path can be created."
    fi
    if [ -d "$TMP_DL_PATH" ]; then
        customExit "Remove the invalid directory \"$TMP_DL_PATH\" first so that a file with that path can be created."
    fi
    if [ ! -f "`command -v wget`" ]; then
        # if [ ! -f "`command -v curl`" ]; then
        #     customExit "You must install curl or wget to use this script."
        # fi
        curl $url/$zip_name -o "$TMP_DL_PATH"
        if [ $? -ne 0 ]; then
            # This is necessary on cygwin for some reason.
            curl $url/$zip_name > "$TMP_DL_PATH"
            if [ $? -ne 0 ]; then
                if [ -f "$TMP_DL_PATH" ]; then
                    rm "$TMP_DL_PATH"
                fi
                customExit "curl $url/$zip_name failed."
            fi
        fi
    else
        wget -O "$TMP_DL_PATH" $url/$zip_name
        if [ $? -ne 0 ]; then
            if [ -f "$TMP_DL_PATH" ]; then
                rm "$TMP_DL_PATH"
            fi
            customExit "wget $url/$zip_name failed to write $TMP_DL_PATH."
        fi
    fi
    mv "$TMP_DL_PATH" "$EM_CONFIG_PATH/$zip_name"
    if [ $? -ne 0 ]; then
        customExit "mv \"$TMP_DL_PATH\" \"$EM_CONFIG_PATH/$zip_name\" failed."
    fi
    echo "* moved the sucessful download to \"$EM_CONFIG_PATH/$zip_name\""
fi

if [ "@$enable_keep" = "@true" ]; then
    if [ ! -d "$extracted_path" ]; then
        enable_keep=false
        echo "* WARNING: --keep is not possible when $extracted_path does not exist, so the option has been automatically turned off."
    fi
fi

if [ "@$enable_keep" = "@true" ]; then
    echo "* using existing $extracted_path since \"--keep\" is enabled"
else
    if [ -d "$extracted_path" ]; then
        # NOTE: ls -lR provides a count, so it is not suitable unless output
        # is parsed. `| wc -l` is easier (word count).
        screenshot_count=0
        if [ -d "$extracted_path/screenshots" ]; then
            screenshot_count=`ls $extracted_path/screenshots/*.png | wc -l`
        fi
        if [ $screenshot_count -gt 0 ]; then
            mv $extracted_path/screenshots/*.png ~/ || customExit "can't move screenshots from $extracted_path/screenshots/*.png"
            rmdir --ignore-fail-on-non-empty "$extracted_path/screenshots"
        fi
        if [ `ls $extracted_path/minetest/bin/*.png | wc -l` -gt 0 ]; then
            # if [ ! -d screenshots ]; then mkdir screenshots; fi
            # NOTE: system-wide install of minetest puts screenshots in ~/ (cwd)
            mv $extracted_path/minetest/bin/*.png ~/ || customExit "can't move png screenshots from $extracted_path/minetest/bin/*.png"
        fi
        if [ `ls $extracted_path/minetest/bin/*.jpg | wc -l` -gt 0 ]; then
            # if [ ! -d screenshots ]; then mkdir screenshots; fi
            # NOTE: system-wide install of minetest puts screenshots in ~/ (cwd)
            mv $extracted_path/minetest/bin/*.jpg ~/ || customExit "can't move jpg screenshots from $extracted_path/minetest/bin/*.png"
        fi
        echo "* removing old \"$extracted_path\" (since you did not specify \"--keep\")"
        rm -Rf "$extracted_path" || customExit "can't remove $extracted_name"
    fi
fi

if [ ! -d "$extracted_path" ]; then
    if [ ! -f "`command -v unzip`" ]; then
        customExit "unzip is missing. You must install it or manually extract $zip_name to \"$extracted_path\" to use this script."
    fi
    unzip -u $zip_name || customExit "unzip \"$zip_name\" failed in \"`pwd`\". Try removing it and re-downloading it."
    # if [ ! -d "" ]; then
    #     customExit "Unzipping \"$zip_name\" in \"`pwd`\" did not result in a readable directory named \"$extracted_name\" there."
    # fi
    if [ ! -d "$extracted_name" ]; then
        customExit "Unzipping \"$zip_name\" in \"`pwd`\" did not result in a readable directory named \"$extracted_name\" there."
    fi
#else
#    if [ ! -d "$extracted_name" ]; then
#        customExit "There is no readable directory: \"`pwd`\" (that or the zip is necessary for --keep)."
#    fi
fi

cd "$extracted_path" || customExit "cd \"`pwd`\" failed."

cat "$extracted_path/release.txt"
echo "If you already compiled the libraries in `pwd`, run install-mts.sh to install minetest from source (with the --client option to include the client)"
echo "compiling libraries..."
date
start=`date +%s`
if [ ! -f "`command -v patch`" ]; then
    customExit "patch is missing. You must install patch to use mtcompile-libraries.sh in linux-minetest-kit. Ubuntu: sudo apt install -y patch  Fedora: sudo dnf install -y patch"
fi
bash -e mtcompile-libraries.sh build >& libraries.log
mtLibrariesCompileResult=$?
if [ -z "$DEPS" ]; then
    DEPS=
fi
if [ -z "$DEPS_INSTALL" ]; then
    DEPS_INSTALL=
fi
FEDORA_DEPS="gcc-c++ irrlicht-devel gettext freetype cmake bzip2-devel libpng libjpeg-turbo libXxf86vm mesa-libGLU libsqlite3x-devel libogg-devel libvorbis-devel openal-devel curl-devel luajit-devel lua-devel leveldb-devel ncurses-devel redis hiredis-devel gmp-devel libtool"
FEDORA_DEPS_INSTALL="sudo dnf install -y $FEDORA_DEPS"
UBUNTU_DEPS="libncurses5-dev libgettextpo-dev doxygen libspatialindex-dev libpq-dev postgresql-server-dev-all git build-essential libirrlicht-dev libgettextpo0 libfreetype6-dev cmake libbz2-dev libpng12-dev libjpeg8-dev libxxf86vm-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-openssl-dev libluajit-5.1-dev liblua5.1-0-dev libleveldb-dev"
UBUNTU_DEPS_INSTALL="sudo apt-get update && sudo apt-get install -y $UBUNTU_DEPS"
DEPS_INSTALL_MSG="something like    $UBUNTU_DEPS_INSTALL     #or     $FEDORA_DEPS_INSTALL"
if [ ! -f "`command -v dnf`" ]; then
    DEPS_INSTALL="$FEDORA_DEPS_INSTALL"
elif [ -f "`command -v yum`" ]; then
    FEDORA_DEPS_INSTALL="sudo yum install -y $FEDORA_DEPS"
    DEPS_INSTALL="$FEDORA_DEPS_INSTALL"
elif [ -f "`command -v apt`" ]; then
    UBUNTU_DEPS_INSTALL="sudo apt update && sudo apt install -y $UBUNTU_DEPS"
    DEPS_INSTALL="$UBUNTU_DEPS_INSTALL"
elif [ -f "`command -v apt-get`" ]; then
    DEPS_INSTALL="$UBUNTU_DEPS_INSTALL"
fi
if [ ! -z "$DEPS_INSTALL" ]; then
    DEPS_INSTALL_MSG="$DEPS_INSTALL"
fi
if [ $mtLibrariesCompileResult -ne 0 ]; then
    cat "$extracted_path/libraries.log"
    echo
    INSTALL_SOURCE_LOG=$HOME/EnlivenMinetest-install-source.log
    echo "Try running" > $INSTALL_SOURCE_LOG
    echo "    $DEPS_INSTALL_MSG" >> $INSTALL_SOURCE_LOG
    echo "Make sure you have installed the dependencies (listed in $INSTALL_SOURCE_LOG)."
    if [ ! -z "`grep "libtoolize is needed" $extracted_path/libraries.log`" ]; then
        echo "You need to install the libtool package to compile the libraries."
    fi
    customExit "Compiling libraries failed (code $mtLibrariesCompileResult). See the contents of $extracted_path/libraries.log shown above." $mtLibrariesCompileResult
fi
end=`date +%s`
compile_time=$((end-start))
echo "Compiling libraries finished in $compile_time seconds."
echo "  (see $extracted_path/libraries.log in case of any errors)"
#echo "compiling program..."
#bash -e mtcompile-program.sh build >& program.log
echo "done."
echo
echo
echo
echo
echo
cd ..
echo "Check libraries.log for errors, then..."
echo "- Run the following manually for SERVER only (no graphical client unless an old copy of ~/minetest/bin/minetest is detected):"
echo "  bash install-mts.sh"
echo "- Run the following manually for both minetestserver and minetest:"
echo "  bash install-mts.sh --client"
echo
echo
