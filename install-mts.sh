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
    echo "Writing icon '$dest_icon'..."
    if [ ! -z "$_ICON" ]; then
        cat "$_SRC_SHORTCUT_PATH" | grep -v Icon | grep -v Path | grep -v Exec > "$dest_icon"
    else
        cat "$_SRC_SHORTCUT_PATH" | grep -v Path | grep -v Exec > "$dest_icon"
    fi
    # Icon must be an absolute path (other variables use $HOME in
    # desktop file above), so exclude it above and rewrite it below:
    echo "Path=$dest_programs/minetest/bin" >> "$dest_icon"
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

install_git_mod_here(){
    git_url="$1"
    mod_name="$2"
    if [ -z "$git_url" ]; then
        customExit "install_git_mod_here requires a URL."
    fi
    if [ -z "$mod_name" ]; then
        customExit "install_git_mod_here requires a mod name as the second parameter."
    fi
    if [ ! -d "$mod_name" ]; then
        git clone "$git_url" "$mod_name"
    else
        cd "$mod_name" || customExit "(install_git_mod_here) 'cd \"$mod_name\"' failed in '`pwd`'"
        echo "* updating '`pwd`' from git..."
        git pull || echo "WARNING: (install_git_mod_here) 'git pull' failed in '`pwd`'"
        cd .. || customExit "(install_git_mod_here) 'cd ..' failed in '`pwd`'"
    fi
}
enable_server=true
dest_programs="$HOME"
#NOTE: $HOME is still used further down, for $HOME/.* and $HOME/i_am_dedicated_minetest_server flag file (which can be empty)
#TODO: change $HOME/i_am_dedicated_minetest_server to $HOME/.config/EnlivenMinetest/i_am_dedicated_minetest_server or rc file
extracted_name="linux-minetest-kit"
extracted_path="$EM_CONFIG_PATH/$extracted_name"
cd "$EM_CONFIG_PATH" || customExit "[$MY_NAME] cd \"$EM_CONFIG_PATH\" failed."
flag_dir_rel="$extracted_name/mtsrc"
code_flag_dir_path="$extracted_path/mtsrc"
if [ -z "$CUSTOM_SCRIPTS_PATH" ]; then
    CUSTOM_SCRIPTS_PATH="$HOME"
fi
MT_POST_INSTALL_SCRIPT_1=archive-minetestserver-debug.sh
scripting_rc_path=~/.config/EnlivenMinetest/scripting.rc
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



if [ -f "$EM_CONFIG_PATH/scripting.rc" ]; then
    echo "Using $scripting_rc_path..."
    source $scripting_rc_path
    # may contain any variables above, plus:
    # * enable_run_after_compile: if true, then run the server, such as
    #   ~/mts-CenterOfTheSun.sh
else
    echo "* skipping $scripting_rc_path (not present)"
    echo "  (can contain settings such as enable_run_after_compile=true)"
fi

pushd "$extracted_path" || customExit "pushd \"$extracted_path\" failed in \"`pwd`\""

extra_options=""
for var in "$@"
do
    if [ "@$var" = "@--client" ]; then
        ENABLE_CLIENT=true
    elif [ "@$var" = "@--clean" ]; then
        enable_clean=true
    elif [ "@$var" = "@--noclean" ]; then
        enable_clean=false
    else
        customExit "Invalid argument: $var"
    fi
done

if [ -z "$enable_clean" ]; then
    enable_clean=true
fi

echo "enable_clean=\"$enable_clean\"..."

# flag_icon="$HOME/Desktop/org.minetest.minetest.desktop"
good_src_mts="$extracted_path/minetest/bin/minetestserver"
good_src_mt="$extracted_path/minetest/bin/minetest"
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
    extra_options="--client"
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
    if [ "@$enable_server" = "@true" ]; then
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
    cd "$extracted_path" || customExit "cd \"$extracted_path\" failed."
    if [ -f "mtcompile-program.pl" ]; then
        # perl mtcompile-program.pl build >& program.log
        echo "Compiling via perl (this may take a while--output redirected to `pwd`/program.log)..."
        perl mtcompile-program.pl build --server $extra_options >& program.log
    else
        # NOTE: no pl in $extracted_name, assuming bash:
        if [ -f mtcompile-program.sh ]; then
        echo "Compiling via bash (this may take a while--output redirected to `pwd`/program.log)..."
            bash -e mtcompile-program.sh build --server $extra_options >& program.log
        else
            echo
            echo "ERROR: Install cannot finish since there is no"
            echo " mtcompile-program.pl nor mtcompile-program.pl"
            echo " in the extracted $extracted_name directory."
            echo
            echo
        fi
    fi
    end=`date +%s`
    compile_time=$((end-start))
    echo "Compiling the program finished in $compile_time seconds."
    cp $extracted_path/release.txt $extracted_path/minetest/ || customWarn "Cannot copy $extracted_path/release.txt to $extracted_path/minetest/"
else
    echo "* using existing $extracted_path/minetest..."
fi
if [ ! -f "$this_src_flag_path" ]; then
    customExit "The build did not complete since '$this_src_flag_path' is missing. Maybe you didn't compile the libraries. Running reset-minetest-install-source.sh should do that automatically, but you can also do: cd $extracted_path && ./mtcompile-libraries.sh build"
fi
if [ -f "$this_dst_flag_path" ]; then
    mv -f "$this_dst_flag_path" "$this_dst_flag_path.bak"
fi
if [ -f "$this_dst_flag_path" ]; then
    customExit "Install is incomplete because it can't move '$this_dst_flag_path'."
fi
if [ ! -d "$extracted_path/minetest" ]; then
    customExit "Install is incomplete because \"$extracted_path/minetest\" is missing."
fi
virtual_dest="$dest_programs/minetest"
link_target=`readlink $virtual_dest`
# install_dest="/tank/local/owner/minetest"
install_dest="$virtual_dest"
dest_official_game="$dest_programs/minetest/games/Bucket_Game"
dest_enliven="$dest_programs/minetest/games/ENLIVEN"
skins_dst="$dest_enliven/mods/codercore/coderskins/textures"
skins_bak="$HOME/Backup/ENLIVEN/mods/codercore/coderskins/textures"
official_game_mod_list="coderbuild codercore coderedit coderfood codermobs decorpack mtmachines"
dest_enliven_mods="$dest_enliven/mods"
if [ "@$enable_clean" = "@true" ]; then
    echo "* cleaning destination..."
    if [ -d "$dest_official_game" ]; then
        echo "  - erasing '$dest_official_game'..."
        rm -Rf "$dest_official_game"
    fi
    if [ -d "$dest_enliven" ]; then
        if [ -d "$skins_dst" ]; then
            echo "  - Backing up '$skins_dst' to '$skins_bak'..."
            if [ ! -d "$skins_bak" ]; then
                mkdir -p "$skins_bak" || customExit "* cannot create $skins_bak"
            fi
            rsync -rt "$skins_dst/" "$skins_bak"
        fi
        for var in $official_game_mod_list
        do
            if [ -d "$dest_enliven_mods/$var" ]; then
                echo "  - erasing '$dest_enliven_mods/$var'..."
                rm -Rf "$dest_enliven_mods/$var" || customExit "rm -Rf \"$dest_enliven_mods/$var\" failed"
                # See rsync further down for installation of each of these
            else
                echo "  - already clean: no '$dest_enliven_mods/$var'..."
            fi
        done
    fi
fi

enliven_warning=""
if [ -d "$dest_enliven_mods" ]; then
    pushd "$dest_enliven_mods" || customExit "'pushd \"$dest_enliven_mods\"' failed."
    install_git_mod_here https://github.com/BenjieFiftysix/sponge.git sponge
    install_git_mod_here https://github.com/poikilos/metatools.git metatools
    install_git_mod_here https://github.com/MinetestForFun/fishing.git fishing
    install_git_mod_here https://github.com/minetest-mods/throwing.git throwing
    install_git_mod_here https://github.com/minetest-mods/ccompass.git ccompass
    install_git_mod_here https://github.com/minetest-mods/throwing_arrows.git throwing_arrows

    popd || customExit "'popd' failed."
else
    enliven_warning="$enliven_warning* WARNING: Installing ENLIVEN mods was skipped since '$dest_enliven_mods' does not exist."
fi
if [ ! -z "$link_target" ]; then
    install_dest="$link_target"
    echo "* detected that $virtual_dest is a symlink to $link_target"
    echo "  (redirecting rsync to prevent symlink to dir conversion: installing to $install_dest"
    echo "   and recreating symlink '$virtual_dest' pointing to '$install_dest')..."
    rsync -rt "$extracted_path/minetest/" "$install_dest" || customExit "Cannot rsync files from installer data $extracted_path/minetest/ to $install_dest"
    if [ ! -d "$dest_programs/minetest" ]; then
        echo "* creating link to $install_dest directory as $dest_programs/minetest..."
        ln -s "$install_dest" "$dest_programs/minetest"
    fi
else
    echo "Installing \"$extracted_path/minetest\" directory to \"$dest_programs\"..."
    rsync -rt --info=progress2 $extracted_path/minetest/ $install_dest || customExit "Cannot rsync files from installer data $extracted_path/minetest/ to $install_dest"
fi
if [ ! -f "$this_dst_flag_path" ]; then
    customExit "ERROR: not complete--couldn't install binary as '$this_dst_flag_path'"
fi

dst_game_flag_dir_path="$dest_official_game"
if [ ! -d "$dst_game_flag_dir_path" ]; then
    customExit "ERROR: missing $dst_game_flag_dir_path"
fi
if [ ! -d "$dest_programs/minetest/games/ENLIVEN" ]; then
    echo "Copying $dst_game_flag_dir_path to $dest_programs/minetest/games/ENLIVEN..."
    cp -R "$dst_game_flag_dir_path" "$dest_programs/minetest/games/ENLIVEN"
    echo "name = ENLIVEN" > "$dest_programs/minetest/games/ENLIVEN/game.conf"
else

    for mod_name in $official_game_mod_list
    do
        echo "  - updating $mod_name from '$dst_game_flag_dir_path/mods/$mod_name' to '$dest_programs/minetest/games/ENLIVEN/mods'..."
        rsync -rt --delete "$dst_game_flag_dir_path/mods/$mod_name" "$dest_programs/minetest/games/ENLIVEN/mods"
    done
    # cp -f "$dst_game_flag_dir_path/mods/LICENSE" "$dest_programs/minetest/games/ENLIVEN/mods/LICENSE"
    if [ -d "$skins_bak" ]; then
        echo "  - restoring skins from '$skins_bak'..."
        rsync -rt "$skins_bak/" "$skins_dst"
    fi
fi
popd

# pushd ..  # go from EnlivenMinetest/webapp to EnlivenMinetest
# PATCHES_DIR_NAME="patches"
if [ -z "$REPO_PATH" ]; then
    REPO_PATH="$HOME/git/EnlivenMinetest"
fi
PATCHES_PATH="$REPO_PATH/patches"
if [ -d "$PATCHES_PATH" ]; then
    # pushd "$REPO_PATH"

src="$PATCHES_PATH/subgame/menu"
dst="$dest_programs/minetest/games/ENLIVEN/menu"
echo "updating '$dst' from '$src/'..."
rsync -rt "$src/" "$dst"

src="$PATCHES_PATH/Bucket_Game-patched"
dst="$dest_programs/minetest/games/ENLIVEN"
echo "updating '$dst' from '$src/'..."
rsync -rt "$src/" "$dst"
if [ -d "$dst/mods/coderfood/food_basic/etc" ]; then
  rm -Rf "$dst/mods/coderfood/food_basic/etc"
fi

minetest_conf_dest="$dest_programs/minetest/minetest.conf"
game_minetest_conf_dest="$dest_programs/minetest/games/ENLIVEN/minetest.conf"

# Bucket_Game doesn't come with a minetest.conf, only minetest.conf.example* files
# if [ ! -f "$dest_programs/minetest/minetest.Bucket_Game-example.conf" ]; then
#     cp -f "$$minetest_conf_dest" "$dest_programs/minetest/minetest.Bucket_Game-example.conf"
# fi

client_example_dest="$dest_programs/minetest/minetest.ENLIVEN.client-example.conf"

echo "Installing minetest.ENLIVEN.*-example.conf files..."
cp -f "$PATCHES_PATH/subgame/minetest.LAN-client-example.conf" "$dest_programs/minetest/minetest.ENLIVEN.LAN-client-example.conf" || customExit "Cannot copy minetest.ENLIVEN.LAN-client-example.conf"
cp -f "$PATCHES_PATH/subgame/minetest.server-example.conf"     "$dest_programs/minetest/minetest.ENLIVEN.server-example.conf" || customExit "Cannot copy minetest.ENLIVEN.server-example.conf"
cp -f "$PATCHES_PATH/subgame/minetest.client-example.conf"     "$dest_programs/minetest/minetest.ENLIVEN.client-example.conf" || customExit "Cannot copy minetest.ENLIVEN.client-example.conf"

echo "Writing '$game_minetest_conf_dest'..."
cp -f "$PATCHES_PATH/subgame/minetest.conf" "$game_minetest_conf_dest"

# client conf writing only ever happens once, unless you manually delete $minetest_conf_dest:
if [ ! -f "$minetest_conf_dest" ]; then
    # if [ -f "$minetest_conf_dest" ]; then
        # echo "Backing up minetest.conf..."
        # if [ ! -f "$minetest_conf_dest.1st" ]; then
            # cp -f "$minetest_conf_dest" "$minetest_conf_dest.1st"
        # else
            # cp -f "$minetest_conf_dest" "$minetest_conf_dest.bak"
        # fi
    # fi
    echo "Writing minetest.conf (client region)..."
    cp -f "$PATCHES_PATH/subgame/minetest.client-example.conf" "$minetest_conf_dest"  || customExit "Cannot copy minetest.client-example.conf to $minetest_conf_dest"
    echo "Appending example settings (server region) to '$minetest_conf_dest'..."
    cat "$PATCHES_PATH/subgame/minetest.server-example.conf" >> "$minetest_conf_dest" || customExit "Cannot append minetest.server-example.conf"
else
    echo "$minetest_conf_dest exists (remove it if you want the installer to write an example version)"
fi


if [ -f "$minetest_conf_dest" ]; then
    cat << END
NOTE: minetest.org releases allow you to put a world.conf file in your
  world, so that is the file you should edit manually in your world
  --this installer overwrites $minetest_conf_dest and
  worlds/CenterOfTheSun settings (the author Poikilos' world).
  Continue to place server settings such as announce in
  $minetest_conf_dest.
  Leave $game_minetest_conf_dest intact, as it defines the game.
  If you have suggestions for changes or configurability, please use the
  issue tracker at <https://github.com/poikilos/EnlivenMinetest>.

END
fi


world_override_src="overrides/CenterOfTheSun/minetest/worlds/CenterOfTheSun"
world_override_dst="$HOME/.minetest/worlds/CenterOfTheSun"
world_override_dst="$HOME/.minetest/worlds/CenterOfTheSun"
try_world_override_dst="$HOME/minetest/worlds/CenterOfTheSun"
if [ -d "$try_world_override_dst" ]; then
    world_override_dst="$try_world_override_dst"
fi
world_conf_src="$world_override_src/world.conf"
world_conf_dst="$world_override_dst/world.conf"
world_mt_src="$world_override_src/world.mt"
world_mt_dst="$world_override_dst/world.mt"
override_more="overrides/CenterOfTheSun/games/ENLIVEN"
appends="overrides/CenterOfTheSun/append"
minetest_conf_append="$appends/minetest.conf"
if [ -d "$world_override_dst" ]; then
    echo "You have the CenterOfTheSun world. Listing any changes..."
    if [ -f "$world_conf_src" ]; then
        if [ -f "$world_conf_dst" ]; then
            echo " * overwrite $world_conf_dst with $world_conf_src"
        else
            echo " * add the world.conf from $world_conf_src"
        fi
        cp -f "$world_conf_src" "$world_conf_dst"
    fi
    if [ -f "$minetest_conf_append" ]; then
        cat "$minetest_conf_append" >> "$minetest_conf_dest"
    fi
fi




if [ "@$ENABLE_CLIENT" = "@true" ]; then
    #params: _SRC_SHORTCUT_PATH, _DST_SHORTCUT_NAME, _EXEC, _WORKING_DIR, _ICON, _CAPTION:
    SHORTCUT_PATH="$PATCHES_PATH/deploy-patched/misc/org.minetest.minetest.desktop"
    EXEC_PATH="$dest_programs/minetest/bin/minetest"
    WORKING_DIR_PATH="$dest_programs/minetest/bin"
    MT_ICON="$dest_programs/minetest/misc/minetest-xorg-icon-128.png"
    install_shortcut "$SHORTCUT_PATH" "org.minetest.minetest.desktop" "$EXEC_PATH" "$WORKING_DIR_PATH" "$MT_ICON" "Final Minetest"
fi

if [ -f $dest_programs/minetest/games/ENLIVEN/mods/codermobs/codermobs/animal_materials.lua ]; then
    if [ -d $PATCHES_PATH/mods-stopgap/animal_materials_legacy ]; then
        echo "* installing animal_materials_legacy (only needed for worlds created with old versions of Bucket_Game)"
        rsync -rt $PATCHES_PATH/mods-stopgap/animal_materials_legacy $dest_programs/minetest/games/ENLIVEN/mods/
    else
        echo "* MISSING $PATCHES_PATH/mods-stopgap/animal_materials"
    fi
else
    echo "* SKIPPING a stopgap mod since no animal_materials"
fi

if [ -f $dest_programs/minetest/games/ENLIVEN/mods/codermobs/codermobs/elk.lua ]; then
    if [ -d $PATCHES_PATH/mods-stopgap/elk_legacy ]; then
        echo "* installing elk_legacy (only needed for worlds created with old versions of Bucket_Game)"
        rsync -rt $PATCHES_PATH/mods-stopgap/elk_legacy $dest_programs/minetest/games/ENLIVEN/mods/
    else
        echo "* MISSING $PATCHES_PATH/mods-stopgap/elk_legacy"
    fi
else
    echo "* SKIPPING a stopgap mod since no elk.lua"
fi

if [ -d "$dest_programs/minetest/games/ENLIVEN/mods/coderbuild/nftools" ]; then
    if [ -d $PATCHES_PATH/mods-stopgap/nftools_legacy ]; then
        echo "* installing nftools_legacy (only needed for worlds created with old versions of Bucket_Game)"
        rsync -rt $PATCHES_PATH/mods-stopgap/nftools_legacy $dest_programs/minetest/games/ENLIVEN/mods/
    else
        echo "* MISSING $PATCHES_PATH/mods-stopgap/nftools_legacy"
    fi
else
    echo "* SKIPPING a stopgap mod since no nftools"
fi

# popd
else
    cat <<END
$PATCHES_PATH is missing. To fix this, set:

    REPO_PATH=$HOME/git/EnlivenMinetest
    # in \"$scripting_rc_path\" or the environment.
END
fi

settings_dump="`pwd`/settings-dump.txt"
settings_types_list="`pwd`/settingtypes-list.txt"
# grep -r `pwd`/linux-minetest-kit/minetest/games/Bucket_Game -e "setting_get" > $settings_dump
pushd linux-minetest-kit/minetest/games
if [ ! -f "$settings_dump" ]; then
    echo "Creating $settings_dump..."
    grep -r Bucket_Game -e "setting_get" > $settings_dump
    grep -r Bucket_Game -e "minetest.settings:get" >> $settings_dump
else
    echo "* $settings_dump was already created"
fi
if [ ! -f "$settings_types_list" ]; then
    echo "Creating $settings_types_list..."
    find Bucket_Game -name "settingtypes.txt" > $settings_types_list
else
    echo "* $settings_types_list was already created"
fi
popd
echo "* finished compiling."
if [ -f "$extracted_path/release.txt" ]; then
    versionLine=`cat $extracted_path/release.txt | grep Release`
    echo "  - version: $versionLine"
fi
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
        popd
    else
        cat <<END
ERROR: enable_run_after_compile is true, but
  '$CUSTOM_SCRIPTS_PATH'
  does not exist. Try setting CUSTOM_SCRIPTS_PATH in
  '$scripting_rc_path'.
END
    fi
fi
echo "$enliven_warning"
echo
echo
