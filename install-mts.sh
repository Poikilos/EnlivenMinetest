#!/bin/bash
me=`basename "$0"`
echo
echo
echo
echo "Starting install..."
MY_NAME="install-mts.sh"
config_path="$HOME/.config/EnlivenMinetest"

date
customDie() {
    cat <<END

ERROR:
$1


END
    exit 1
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

install_git_mod_here(){
    git_url="$1"
    mod_name="$2"
    if [ -z "$git_url" ]; then
        customDie "install_git_mod_here requires a URL."
    fi
    if [ -z "$mod_name" ]; then
        customDie "install_git_mod_here requires a mod name as the second parameter."
    fi
    if [ ! -d "$mod_name" ]; then
        git clone "$git_url" "$mod_name"
    else
        cd "$mod_name" || customDie "(install_git_mod_here) 'cd \"$mod_name\"' failed in '`pwd`'"
        echo "* updating '`pwd`' from git..."
        git pull || echo "WARNING: (install_git_mod_here) 'git pull' failed in '`pwd`'"
        cd .. || customDie "(install_git_mod_here) 'cd ..' failed in '`pwd`'"
    fi
}
enable_server=true
dest_programs="$HOME"
#NOTE: $HOME is still used further down, for $HOME/.* and $HOME/i_am_dedicated_minetest_server flag file (which can be empty)
#TODO: change $HOME/i_am_dedicated_minetest_server to $HOME/.config/EnlivenMinetest/i_am_dedicated_minetest_server or rc file
extracted_name="linux-minetest-kit"
extracted_path="$config_path/$extracted_name"
cd "$config_path" || customDie "[$MY_NAME] cd \"$config_path\" failed."
flag_dir_rel="$extracted_name/mtsrc"
flag_dir="$extracted_path/mtsrc"
enable_client=false
custom_scripts_dir="$HOME"
custom_script_name="mts.sh"
if [ -f "$custom_scripts_dir/mts-CenterOfTheSun.sh" ]; then
    custom_script_name="mts-CenterOfTheSun.sh"
fi

scripting_rc_path=~/.config/EnlivenMinetest/scripting.rc

if [ -f ~/.config/EnlivenMinetest/scripting.rc ]; then
    echo "Running $scripting_rc_path..."
    source $scripting_rc_path
    # may contain any variables above, plus:
    # * enable_run_after_compile: if true, then run the server, such as
    #   ~/mts-CenterOfTheSun.sh
else
    echo "* skipping $scripting_rc_path (not present)"
    echo "  (can contain settings such as enable_run_after_compile)"
fi

pushd "$extracted_path" || customDie "pushd \"$extracted_path\" failed in \"`pwd`\""

extra_options=""
for var in "$@"
do
    if [ "@$var" = "@--client" ]; then
        enable_client=true
    elif [ "@$var" = "@--clean" ]; then
        enable_clean=true
    elif [ "@$var" = "@--noclean" ]; then
        enable_clean=false
    else
        customDie "Invalid argument: $var"
    fi
done

if [ -z "$enable_clean" ]; then
    enable_clean=true
fi

echo "enable_clean=\"$enable_clean\"..."

# flag_icon="$HOME/Desktop/org.minetest.minetest.desktop"
flag_client_dest_file="$dest_programs/minetest/bin/minetest"
flag_file="minetest/bin/minetestserver"
if [ -f "$flag_client_dest_file" ]; then
    enable_client=true
    echo "* automatically adding --client to compile since detected"
    echo "  '$flag_client_dest_file'"
    # echo "--press Ctrl C to cancel..."
    # sleep 2
fi
if [ "@$enable_client" = "@true" ]; then
    flag_file="minetest/bin/minetest"
    extra_options="--client"
fi
#if [ -f "$flag_file" ]; then
    #rm -f "$flag_file"
#fi
#if [ -f "$flag_file" ]; then
    #echo "ERROR: Nothing done since can't remove old '$flag_file'"
    #exit 1
#fi
enable_compile=true
if [ -d minetest ]; then
    enable_compile=false
    if [ "@$enable_client" = "@true" ]; then
        if [ ! -f minetest/bin/minetest ]; then
            enable_compile=true
            echo "* enabling compile (since no `pwd`/minetest/bin/minetest but client install is enabled)"
        fi
    fi
    if [ "@$enable_server" = "@true" ]; then
        if [ ! -f minetest/bin/minetestserver ]; then
            enable_compile=true
            echo "* enabling compile (since no `pwd`/minetest/bin/minetestserver)"
        fi
    fi
else
    echo "* enabling compile since missing `pwd`/minetest directory"
fi
if [ "@$enable_compile" = "@true" ]; then
    echo "* checking if the compile library script extracted the program source yet ($flag_dir)..."
    if [ ! -d "$flag_dir" ]; then
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
    echo "* using existing minetest..."
fi
if [ ! -f "$flag_file" ]; then
    customDie "The build did not complete since '$flag_file' is missing. Maybe you didn't compile the libraries. Running reset-minetest-install-source.sh should do that automatically, but you can also do: cd $extracted_path && ./mtcompile-libraries.sh build"
fi
dest_flag_file="$dest_programs/$flag_file"
if [ -f "$dest_flag_file" ]; then
    mv -f "$dest_flag_file" "$dest_flag_file.bak"
fi
if [ -f "$dest_flag_file" ]; then
    customDie "Install is incomplete because it can't move '$dest_flag_file'."
fi
if [ ! -d minetest ]; then
    customDie "Install is incomplete because `pwd`/minetest is missing."
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
                mkdir -p "$skins_bak" || customDie "* cannot create $skins_bak"
            fi
            rsync -rt "$skins_dst/" "$skins_bak"
        fi
        for var in $official_game_mod_list
        do
            if [ -d "$dest_enliven_mods/$var" ]; then
                echo "  - erasing '$dest_enliven_mods/$var'..."
                rm -Rf "$dest_enliven_mods/$var" || customDie "rm -Rf \"$dest_enliven_mods/$var\" failed"
                # See rsync further down for installation of each of these
            else
                echo "  - already clean: no '$dest_enliven_mods/$var'..."
            fi
        done
    fi
fi

enliven_warning=""
if [ -d "$dest_enliven_mods" ]; then
    pushd "$dest_enliven_mods" || customDie "'pushd \"$dest_enliven_mods\"' failed."
    install_git_mod_here https://github.com/BenjieFiftysix/sponge.git sponge
    install_git_mod_here https://github.com/poikilos/metatools.git metatools
    install_git_mod_here https://github.com/MinetestForFun/fishing.git fishing
    install_git_mod_here https://github.com/minetest-mods/throwing.git throwing
    install_git_mod_here https://github.com/minetest-mods/ccompass.git ccompass
    install_git_mod_here https://github.com/minetest-mods/throwing_arrows.git throwing_arrows

    popd || customDie "'popd' failed."
else
    enliven_warning="$enliven_warning* WARNING: Installing ENLIVEN mods was skipped since '$dest_enliven_mods' does not exist."
fi
if [ ! -z "$link_target" ]; then
    install_dest="$link_target"
    echo "* detected that $virtual_dest is a symlink to $link_target"
    echo "  (redirecting rsync to prevent symlink to dir conversion: installing to $install_dest"
    echo "   and recreating symlink '$virtual_dest' pointing to '$install_dest')..."
    rsync -rt "minetest/" "$install_dest" || customDie "Cannot rsync files from installer data `pwd`/minetest/ to $install_dest"
    if [ ! -d "$dest_programs/minetest" ]; then
        echo "* creating link to $install_dest directory as $dest_programs/minetest..."
        ln -s "$install_dest" "$dest_programs/minetest"
    fi
else
    echo "Installing minetest directory to '$dest_programs'..."
    rsync -rt --info=progress2 minetest/ $install_dest || customDie "Cannot rsync files from installer data `pwd`/minetest/ to $install_dest"
fi
if [ ! -f "$dest_flag_file" ]; then
    customDie "ERROR: not complete--couldn't install binary as '$dest_flag_file'"
fi

flag_dir="$dest_official_game"
if [ ! -d "$flag_dir" ]; then
    customDie "ERROR: missing $flag_dir"
fi
if [ ! -d "$dest_programs/minetest/games/ENLIVEN" ]; then
    echo "Copying $flag_dir to $dest_programs/minetest/games/ENLIVEN..."
    cp -R "$flag_dir" "$dest_programs/minetest/games/ENLIVEN"
    echo "name = ENLIVEN" > "$dest_programs/minetest/games/ENLIVEN/game.conf"
else

    for mod_name in $official_game_mod_list
    do
        echo "  - updating $mod_name from '$flag_dir/mods/$mod_name' to '$dest_programs/minetest/games/ENLIVEN/mods'..."
        rsync -rt --delete "$flag_dir/mods/$mod_name" "$dest_programs/minetest/games/ENLIVEN/mods"
    done
    # cp -f "$flag_dir/mods/LICENSE" "$dest_programs/minetest/games/ENLIVEN/mods/LICENSE"
    if [ -d "$skins_bak" ]; then
        echo "  - restoring skins from '$skins_bak'..."
        rsync -rt "$skins_bak/" "$skins_dst"
    fi
fi
popd

# pushd ..  # go from EnlivenMinetest/webapp to EnlivenMinetest
PATCHES_DIR="patches"
if [ -z "$REPO_PATH" ]; then
    REPO_PATH="$HOME/git/EnlivenMinetest"
fi
PATCHES_PATH="$REPO_PATH/patches"
if [ -d "$PATCHES_PATH" ]; then
    pushd "$REPO_PATH"

src="patches/subgame/menu"
dst="$dest_programs/minetest/games/ENLIVEN/menu"
echo "updating '$dst' from '$src/'..."
rsync -rt "$src/" "$dst"

src="patches/Bucket_Game-patched"
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
cp -f "patches/subgame/minetest.LAN-client-example.conf" "$dest_programs/minetest/minetest.ENLIVEN.LAN-client-example.conf" || customDie "Cannot copy minetest.ENLIVEN.LAN-client-example.conf"
cp -f "patches/subgame/minetest.server-example.conf"     "$dest_programs/minetest/minetest.ENLIVEN.server-example.conf" || customDie "Cannot copy minetest.ENLIVEN.server-example.conf"
cp -f "patches/subgame/minetest.client-example.conf"     "$dest_programs/minetest/minetest.ENLIVEN.client-example.conf" || customDie "Cannot copy minetest.ENLIVEN.client-example.conf"

echo "Writing '$game_minetest_conf_dest'..."
cp -f "patches/subgame/minetest.conf" "$game_minetest_conf_dest"

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
    cp -f "patches/subgame/minetest.client-example.conf" "$minetest_conf_dest"  || customDie "Cannot copy minetest.client-example.conf to $minetest_conf_dest"
    echo "Appending example settings (server region) to '$minetest_conf_dest'..."
    cat "patches/subgame/minetest.server-example.conf" >> "$minetest_conf_dest" || customDie "Cannot append minetest.server-example.conf"
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


enable_clear_icon_cache=false
if [ "@$enable_client" = "@true" ]; then
    dest_icons=$HOME/.local/share/applications
    dest_icon=$dest_icons/org.minetest.minetest.desktop
    # if [ -f "$dest_icon" ]; then
        # comment since never fixes broken icon anyway
        # TODO: fixed bad cache even if icon was rewritten properly after written improperly
        # * not tried yet:
        #   * rm $HOME/.kde/share/config/kdeglobals
        # enable_clear_icon_cache=true
    # fi
    echo "Writing icon '$dest_icon'..."
    cat "patches/deploy-patched/misc/org.minetest.minetest.desktop" | grep -v Icon | grep -v Path | grep -v Exec > "$dest_icon"
    # Icon must be an absolute path (other variables use $HOME in
    # desktop file above), so exclude it above and rewrite it below:
    echo "Icon=$dest_programs/minetest/misc/minetest-xorg-icon-128.png" >> "$dest_icon"
    echo "Path=$dest_programs/minetest/bin" >> "$dest_icon"
    echo "Exec=$dest_programs/minetest/bin/minetest" >> "$dest_icon"
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
fi

if [ -f $dest_programs/minetest/games/ENLIVEN/mods/codermobs/codermobs/animal_materials.lua ]; then
    if [ -d patches/mods-stopgap/animal_materials_legacy ]; then
        echo "* installing animal_materials_legacy (only needed for worlds created with old versions of Bucket_Game)"
        rsync -rt patches/mods-stopgap/animal_materials_legacy $dest_programs/minetest/games/ENLIVEN/mods/
    else
        echo "* MISSING patches/mods-stopgap/animal_materials"
    fi
else
    echo "* SKIPPING a stopgap mod since no animal_materials"
fi

if [ -f $dest_programs/minetest/games/ENLIVEN/mods/codermobs/codermobs/elk.lua ]; then
    if [ -d patches/mods-stopgap/elk_legacy ]; then
        echo "* installing elk_legacy (only needed for worlds created with old versions of Bucket_Game)"
        rsync -rt patches/mods-stopgap/elk_legacy $dest_programs/minetest/games/ENLIVEN/mods/
    else
        echo "* MISSING patches/mods-stopgap/elk_legacy"
    fi
else
    echo "* SKIPPING a stopgap mod since no elk.lua"
fi

if [ -d "$dest_programs/minetest/games/ENLIVEN/mods/coderbuild/nftools" ]; then
    if [ -d patches/mods-stopgap/nftools_legacy ]; then
        echo "* installing nftools_legacy (only needed for worlds created with old versions of Bucket_Game)"
        rsync -rt patches/mods-stopgap/nftools_legacy $dest_programs/minetest/games/ENLIVEN/mods/
    else
        echo "* MISSING patches/mods-stopgap/nftools_legacy"
    fi
else
    echo "* SKIPPING a stopgap mod since no nftools"
fi

popd
else
    cat <<END
$PATCHES_PATH is missing. To fix this, set the REPO_PATH environment variable like:

    REPO_PATH=$HOME/git/EnlivenMinetest $MY_NAME
    # (where $HOME/git/EnlivenMinetest is the actual repo path).
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
    if [ -d "$custom_scripts_dir" ]; then
        pushd "$custom_scripts_dir"
        if [ -f archive-minetestserver-debug.sh ]; then
            ./archive-minetestserver-debug.sh
            echo "NOTE: if you put archive-minetestserver-debug.sh"
            echo "  in `pwd`, it would run at this point if"
            echo "  marked executable."
        fi
        if [ -f "$custom_script_name" ]; then
            ./$custom_script_name
            echo "$custom_script_name finished (exit code $?)"
        else
            cat <<END
ERROR: enable_run_after_compile is true, but
  '$custom_script_name' is not in
  '$custom_scripts_dir'.
  Try setting custom_scripts_dir and custom_script_name in
  '$scripting_rc_path'
END
        fi
        popd
    else
        cat <<END
ERROR: enable_run_after_compile is true, but
  '$custom_scripts_dir'
  does not exist. Try setting custom_scripts_dir in
  '$scripting_rc_path'.
END
    fi
fi
echo "$enliven_warning"
echo
echo
