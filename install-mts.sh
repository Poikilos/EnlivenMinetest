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
# ^ same as install-minetest-linux64.sh, versionize.sh

INSTALL_MTS_NAME="install-mts.sh"

echo "* starting install from source..."
date

ENABLE_SERVER=true
dest_programs="$HOME"
#NOTE: $HOME is still used further down, for $HOME/.* and $HOME/i_am_dedicated_minetest_server flag file (which can be empty)
#TODO: change $HOME/i_am_dedicated_minetest_server to $HOME/.config/EnlivenMinetest/i_am_dedicated_minetest_server or rc file
EXTRACTED_SRC_NAME="linux-minetest-kit"
# EM_CONFIG_PATH is from "minetestenv-in-place.rc".
EXTRACTED_SRC_PATH="$EM_CONFIG_PATH/$EXTRACTED_SRC_NAME"
flag_dir_rel="$EXTRACTED_SRC_NAME/mtsrc"
code_flag_dir_path="$EXTRACTED_SRC_PATH/mtsrc"
if [ ! -d "$code_flag_dir_path" ]; then
    echo
    echo
    echo "ERROR: The minetest sources directory \"$code_flag_dir_path\" is missing. Try running reset-minetest-install-source.sh first."
    echo
    exit 1
fi
cd "$EM_CONFIG_PATH" || customExit "[$INSTALL_MTS_NAME] cd \"$EM_CONFIG_PATH\" failed."
if [ -z "$CUSTOM_SCRIPTS_PATH" ]; then
    CUSTOM_SCRIPTS_PATH="$HOME"
fi
MT_POST_INSTALL_SCRIPT_1=archive-minetestserver-debug.sh
# scripting_rc_path is set in minetestenv-in-place.rc
if [ -z "$MT_POST_INSTALL_SCRIPT_2" ]; then
    MT_POST_INSTALL_SCRIPT_2="mts.sh"
    if [ -f "$CUSTOM_SCRIPTS_PATH/mts-CenterOfTheSun.sh" ]; then
        MT_POST_INSTALL_SCRIPT_2="mts-CenterOfTheSun.sh"
    else
        if [ ! -f $CUSTOM_SCRIPTS_PATH/$MT_POST_INSTALL_SCRIPT_2 ]; then
            cat <<END
* If $MT_POST_INSTALL_SCRIPT_2 were in $CUSTOM_SCRIPTS_PATH, then it
  will run after compiling is finished. You can also set
  MT_POST_INSTALL_SCRIPT_2 to determine what filename to run, and set
  CUSTOM_SCRIPTS_PATH to determine where it (and
  $MT_POST_INSTALL_SCRIPT_1 which runs first if present there) is
  located. You can set the variables in
  $scripting_rc_path or the environment.
END
        fi
    fi
fi
if [ -z "$ENABLE_CLIENT" ]; then
    ENABLE_CLIENT=false
fi

#pushd "$EXTRACTED_SRC_PATH" || customExit "pushd \"$EXTRACTED_SRC_PATH\" failed in \"`pwd`\""

extra_options=""
#enable_client_only=false

custom_src_option=""
#PATCH_BUILD=$REPO_PATH/utilities/mtcompile-program-local.pl
PATCH_BUILD=$REPO_PATH/utilities/mtcompile-program-local.py
# ^ custom_src_option requires $PATCH_BUILD to exist.

for var in "$@"
do
    if [[ $var = --MT_SRC* ]]; then
        custom_src_option="$var"
    elif [ "@$var" = "@--client" ]; then
        ENABLE_CLIENT=true
    elif [ "@$var" = "@--clean" ]; then
        #enable_clean=true
        echo "* --clean is deprecated."
    elif [ "@$var" = "@--no-server" ]; then
        ENABLE_CLIENT=true
        ENABLE_SERVER=false
    elif [ "@$var" = "@--noclean" ]; then
        #enable_clean=false
        #echo "* --noclean is deprecated."
        extra_options="$extra_options --noclean"
    elif [ "@$var" = "@--portable" ]; then
        extra_options="$extra_options --portable"
    else
        customExit "Invalid argument: $var"
    fi
done

# if [ -z "$enable_clean" ]; then
#     enable_clean=true
# fi

# echo "enable_clean=\"$enable_clean\"..."


# flag_icon="$HOME/Desktop/org.minetest.minetest.desktop"
good_src_mts="$EXTRACTED_SRC_PATH/minetest/bin/minetestserver"
good_src_mt="$EXTRACTED_SRC_PATH/minetest/bin/minetest"
this_src_flag_path="$good_src_mts"
good_dst_mts="$dest_programs/minetest/bin/minetestserver"
good_dst_mt="$dest_programs/minetest/bin/minetest"
this_dst_flag_path="$good_dst_mts"
if [ -f "$good_dst_mt" ]; then
    ENABLE_CLIENT=true
    echo "* automatically adding --client to compile since detected"
    echo "  '$good_dst_mt'"
    # echo "--press Ctrl C to cancel..."
    # sleep 2
fi
if [ "@$ENABLE_CLIENT" = "@true" ]; then
    this_src_flag_path="$good_src_mt"
    this_dst_flag_path="$good_dst_mt"
fi
server_option="--server"
client_option="--client"
if [ "@$ENABLE_SERVER" != "@true" ]; then
    server_option=""
fi
if [ "@$ENABLE_CLIENT" != "@true" ]; then
    client_option=""
fi
#if [ -f "$this_src_flag_path" ]; then
    #rm -f "$this_src_flag_path"
#fi
#if [ -f "$this_src_flag_path" ]; then
    #echo "ERROR: Nothing done since can't remove old '$this_src_flag_path'"
    #exit 1
#fi
enable_compile=true

has_any_binary=false
if [ -f "$good_src_mts" ]; then
    has_any_binary=true
fi
if [ -f "$good_src_mt" ]; then
    has_any_binary=true
fi
if [ "@$has_any_binary" == "@true" ]; then
    enable_compile=false
    if [ "@$ENABLE_CLIENT" = "@true" ]; then
        if [ ! -f "$good_src_mt" ]; then
            enable_compile=true
            echo "* enabling compile (since no `pwd`/minetest/bin/minetest but client install is enabled)"
        fi
    fi
    if [ "@$ENABLE_SERVER" = "@true" ]; then
        if [ ! -f "$good_src_mts" ]; then
            enable_compile=true
            echo "* enabling compile (since no `pwd`/minetest/bin/minetestserver)"
        fi
    fi
else
    echo "* enabling compile since neither \"$good_src_mts\" nor \"$good_src_mt\" are present."
fi

if [ "@$enable_compile" = "@true" ]; then
    echo "* checking if the compile library script extracted the program source yet ($code_flag_dir_path)..."
    if [ ! -d "$code_flag_dir_path" ]; then
        cat <<END
ERROR: missing $flag_dir_rel
- If you do not have an extracted minetest source directory which
  is normally extracted by the library build script, you must add
  that--it can be automatically added by running:

  bash reset-minetest-install-source.sh


END
        exit 1
    fi

    start=`date +%s`
    cd "$EXTRACTED_SRC_PATH" || customExit "cd \"$EXTRACTED_SRC_PATH\" failed."
    if [ ! -z "$custom_src_option" ]; then
        if [ ! -f "$PATCH_BUILD" ]; then
            customExit "$PATCH_BUILD must exist when using the --MT_SRC=<path> (custom local copy of minetest source) option"
        fi
        echo "* starting PATCH_BUILD ($PATCH_BUILD build $server_option $extra_options $custom_src_option"
        $PATCH_BUILD build $server_option $client_option $extra_options $custom_src_option >& program.log
    elif [ -f "mtcompile-program.pl" ]; then
        # perl mtcompile-program.pl build >& program.log
        echo "Compiling via perl (this may take a while--output redirected to `pwd`/program.log)..."
        perl mtcompile-program.pl build $server_option $client_option $extra_options >& program.log
    else
        # NOTE: no pl in $EXTRACTED_SRC_NAME, assuming bash:
        if [ -f mtcompile-program.sh ]; then
        echo "Compiling via bash (this may take a while--output redirected to `pwd`/program.log)..."
            bash -e mtcompile-program.sh build $server_option $client_option $extra_options >& program.log
        else
            echo
            echo "ERROR: Install cannot finish since there is no"
            echo " mtcompile-program.pl nor mtcompile-program.pl"
            echo " in the extracted $EXTRACTED_SRC_NAME directory."
            echo
            echo
        fi
    fi
    if [ $? -ne 0 ]; then
        customExit "Building failed. See `pwd`/program.log"
    fi
    end=`date +%s`
    compile_time=$((end-start))
    echo "Compiling the program finished in $compile_time seconds."
    cp $EXTRACTED_SRC_PATH/release.txt $EXTRACTED_SRC_PATH/minetest/ || customWarn "[install-mts.sh] Cannot copy $EXTRACTED_SRC_PATH/release.txt to $EXTRACTED_SRC_PATH/minetest/"
else
    echo "* using existing $EXTRACTED_SRC_PATH/minetest..."
fi
if [ ! -f "$this_src_flag_path" ]; then
    customExit "The build did not complete since '$this_src_flag_path' is missing. Maybe you didn't compile the libraries. Running reset-minetest-install-source.sh should do that automatically, but you can also do: cd $EXTRACTED_SRC_PATH && ./mtcompile-libraries.sh build"
fi
if [ -f "$this_dst_flag_path" ]; then
    mv -f "$this_dst_flag_path" "$this_dst_flag_path.bak"
fi
if [ -f "$this_dst_flag_path" ]; then
    customExit "Install is incomplete because it can't move '$this_dst_flag_path'."
fi
if [ ! -d "$EXTRACTED_SRC_PATH/minetest" ]; then
    customExit "Install is incomplete because \"$EXTRACTED_SRC_PATH/minetest\" is missing."
fi



echo "* finished compiling."
INSTALL_PATH="$HOME/minetest"
echo "* installing Minetest..."
if [ -z "$EM_TMP" ]; then
    customWarn "EM_TMP was not set."
    EM_TMP="/tmp/EnlivenMintest"
fi
tmp_mt_copy=$EM_TMP/minetest
if [ -d "$tmp_mt_copy" ]; then
    echo "* removing old $tmp_mt_copy..."
    rm -Rf "$tmp_mt_copy" || customExit "rm -Rf \"$tmp_mt_copy\" failed."
elif [ ! -d "$EM_TMP" ]; then
    mkdir -p "$EM_TMP" || customExit "mkdir -p \"$EM_TMP\" failed."
fi
old_release_line=
old_release_version=
detect_installed_mt_version "1st" "bak"
echo "* making temporary copy at $tmp_mt_copy..."
cp -R "$EXTRACTED_SRC_PATH/minetest" "$tmp_mt_copy"
if [ -f "$EXTRACTED_SRC_PATH/release.txt" ]; then
    cp $EXTRACTED_SRC_PATH/release.txt "$tmp_mt_copy/"
else
    if [ ! -f "$tmp_mt_copy/release.txt" ]; then
        echo "[install-mts.sh] WARNING: $tmp_mt_copy/release.txt and $EXTRACTED_SRC_PATH/release.txt are missing."
    fi
fi
detect_mt_version_at "$tmp_mt_copy"
installOrUpgradeMinetest "$tmp_mt_copy" "$INSTALL_PATH"
echo "  - old:$old_release_version; new:$new_release_version"
echo "* installing ENLIVEN..."
installOrUpgradeENLIVEN "$INSTALL_PATH"
echo "* analyzing settings..."
analyzeGameSettings $EXTRACTED_SRC_PATH/minetest/games/Bucket_Game

if [ "@$enable_run_after_compile" = "@true" ]; then
    echo "Trying to run minetest or other custom post-install script"
    echo "(enable_run_after_compile is true in '$scripting_rc_path')."
    if [ -d "$CUSTOM_SCRIPTS_PATH" ]; then
        cd "$CUSTOM_SCRIPTS_PATH" || customExit "cd $CUSTOM_SCRIPTS_PATH failed."
        if [ -f "$MT_POST_INSTALL_SCRIPT_1" ]; then
            ./$MT_POST_INSTALL_SCRIPT_1
            echo "NOTE: if you put $MT_POST_INSTALL_SCRIPT_1"
            echo "  in `pwd`, it would run at this point if"
            echo "  marked executable."
        fi
        if [ -f "$MT_POST_INSTALL_SCRIPT_2" ]; then
            ./$MT_POST_INSTALL_SCRIPT_2
            echo "$MT_POST_INSTALL_SCRIPT_2 finished (exit code $?)"
        else
            cat <<END
ERROR: enable_run_after_compile is true, but
  '$MT_POST_INSTALL_SCRIPT_2' is not in
  '$CUSTOM_SCRIPTS_PATH'.
  Try setting CUSTOM_SCRIPTS_PATH and MT_POST_INSTALL_SCRIPT_2 in
  '$scripting_rc_path'
END
        fi
        # popd
    else
        cat <<END
ERROR: enable_run_after_compile is true, but
  '$CUSTOM_SCRIPTS_PATH'
  does not exist. Try setting CUSTOM_SCRIPTS_PATH in
  '$scripting_rc_path'.
END
    fi
fi
echo "* done"
echo "$enliven_warning"
echo
echo
