#!/bin/bash
me=`basename "$0"`
echo
echo
echo
echo "Starting install..."
date
customDie() {
    cat <<END

ERROR:
$1


END
    exit 1
}
dest_programs="$HOME"
#NOTE: $HOME is still used further down, for $HOME/.* and $HOME/i_am_dedicated_minetest_server flag file (which can be empty)
#TODO: change $HOME/i_am_dedicated_minetest_server to $HOME/.config/EnlivenMinetest/i_am_dedicated_minetest_server or rc file
extracted_name=linux-minetest-kit
flag_dir_rel="$extracted_name/mtsrc"
flag_dir="`pwd`/$flag_dir_rel"
pushd "$extracted_name"
enable_client=false
extra_options=""
if [ "@$1" = "@--client" ]; then
    enable_client=true
fi
if [ "@$2" = "@--client" ]; then
    enable_client=true
fi
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
else
    echo "* using existing minetest..."
fi
if [ ! -f "$flag_file" ]; then
    customDie "The build did not complete since '$flag_file' is missing."
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
    rsync -rt minetest/ $install_dest || customDie "Cannot rsync files from installer data `pwd`/minetest/ to $install_dest"
fi
if [ ! -f "$dest_flag_file" ]; then
    customDie "ERROR: not complete--couldn't install binary as '$dest_flag_file'"
fi

flag_dir="$dest_programs/minetest/games/Bucket_Game"
if [ ! -d "$flag_dir" ]; then
    customDie "ERROR: missing $flag_dir"
fi
if [ ! -d "$dest_programs/minetest/games/ENLIVEN" ]; then
    echo "Copying $flag_dir to $dest_programs/minetest/games/ENLIVEN..."
    cp -R "$flag_dir" "$dest_programs/minetest/games/ENLIVEN"
    echo "name = ENLIVEN" > "$dest_programs/minetest/games/ENLIVEN/game.conf"
else
    mod_name=coderbuild
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$dest_programs/minetest/games/ENLIVEN/mods"
    mod_name=codercore
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$dest_programs/minetest/games/ENLIVEN/mods"
    mod_name=coderedit
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$dest_programs/minetest/games/ENLIVEN/mods"
    mod_name=coderfood
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$dest_programs/minetest/games/ENLIVEN/mods"
    mod_name=codermobs
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$dest_programs/minetest/games/ENLIVEN/mods"
    mod_name=decorpack
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$dest_programs/minetest/games/ENLIVEN/mods"
    mod_name=mtmachines
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$dest_programs/minetest/games/ENLIVEN/mods"
    # cp -f "$flag_dir/mods/LICENSE" "$dest_programs/minetest/games/ENLIVEN/mods/LICENSE"
fi
popd

pushd ..
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

# Bucket_Game doesn't come with a minetest.conf, only minetest.conf.example* files
# if [ ! -f "$dest_programs/minetest/minetest.Bucket_Game-example.conf" ]; then
#     cp -f "$dest_programs/minetest/minetest.conf" "$dest_programs/minetest/minetest.Bucket_Game-example.conf"
# fi

client_example_dest="$dest_programs/minetest/minetest.ENLIVEN.client-example.conf"
# client conf writing only ever happens once, unless you manually delete $client_example_dest file:
if [ ! -f "$client_example_dest" ]; then
    if [ -f "$dest_programs/minetest/minetest.conf" ]; then
        echo "Backing up minetest.conf..."
        if [ ! -f "$dest_programs/minetest/minetest.conf.1st" ]; then
            cp -f "$dest_programs/minetest/minetest.conf" "$dest_programs/minetest/minetest.conf.1st"
        else
            cp -f "$dest_programs/minetest/minetest.conf" "$dest_programs/minetest/minetest.conf.bak"
        fi
    fi
    echo "Installing minetest.conf and ENLIVEN example conf files..."
    cp -f "patches/subgame/minetest.client-example.conf" "$dest_programs/minetest/minetest.conf"
    cp -f "patches/subgame/minetest.LAN-client-example.conf" "$dest_programs/minetest/minetest.ENLIVEN.LAN-client-example.conf"
    cp -f "patches/subgame/minetest.server-example.conf" "$dest_programs/minetest/minetest.ENLIVEN.server-example.conf"
    cp -f "patches/subgame/minetest.client-example.conf" "$client_example_dest"
fi
server_minetest_conf_dest="$dest_programs/minetest/games/ENLIVEN/minetest.conf"

if [ -f "$server_minetest_conf_dest" ]; then
    cat << END
NOTE: minetest.org releases allow you to put a world.conf file in your
  world, so that is the file you should edit manually in your world
  --this installer overwrites $server_minetest_conf_dest and
  worlds/CenterOfTheSun settings (the author Poikilos' world).

END
fi
echo "Writing '$server_minetest_conf_dest'..."
cp -f "patches/subgame/minetest.server-example.conf" "$server_minetest_conf_dest"
echo "" >> "$server_minetest_conf_dest"
echo "# Added automatically by $me:" >> "$server_minetest_conf_dest"
if [ -f "$HOME/i_am_dedicated_minetest_server" ]; then
    echo "server_dedicated = true" >> "$server_minetest_conf_dest"
else
    echo "server_dedicated = false" >> "$server_minetest_conf_dest"
fi
echo "" >> "$server_minetest_conf_dest"
echo "" >> "$server_minetest_conf_dest"


world_override_src="overrides/worlds/CenterOfTheSun"
world_override_dst="$HOME/.minetest/worlds/CenterOfTheSun"
world_conf_src="$world_override_src/world.conf"
world_conf_dst="$world_override_dst/world.conf"
world_mt_src="$world_override_src/world.mt"
world_mt_dst="$world_override_dst/world.mt"
if [ -d "$world_override_dst" ]; then
    echo "You have the CenterOfTheSun world. Listing any changes..."
    if [ -f "$world_conf_src" ]; then
        if [ -f "$world_conf_dst" ]; then
            echo " * overwrite world.conf with $world_conf_src"
        else
            echo " * add the world.conf from $world_conf_src"
        fi
        cp -f "$world_conf_src" "$world_conf_dst"
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
settings_dump="`pwd`/settings-dump.txt"
settings_types_list="`pwd`/settingstypes-list.txt"
echo "Creating $settings_dump..."
#grep -r `pwd`/linux-minetest-kit/minetest/games/Bucket_Game -e "setting_get" > $settings_dump
pushd linux-minetest-kit/minetest/games
grep -r Bucket_Game -e "setting_get" > $settings_dump
grep -r Bucket_Game -e "minetest.settings:get" >> $settings_dump
find Bucket_Game -name "settingtypes.txt" > $settings_types_list
popd
echo "Done."
echo
echo

