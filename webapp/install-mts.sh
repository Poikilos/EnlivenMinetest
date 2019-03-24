#!/bin/bash
echo
echo
echo
echo "Starting install..."
date
echo "Checking if program is compiled..."
extracted_name=linux-minetest-kit
flag_dir="$extracted_name/mtsrc"
if [ ! -d "$flag_dir" ]; then
    echo "ERROR: missing $flag_dir"
    exit 1
fi
pushd "$extracted_name"
enable_client=false
extra_options=""
if [ "@$1" = "@--client" ]; then
    extra_options="--client"
    enable_client=true
fi
flag_icon="$HOME/Desktop/org.minetest.minetest.desktop"
flag_file="minetest/bin/minetestserver"
if [ -f "$flag_icon" ]; then
    extra_options="--client"
    enable_client=true
    echo "automatically adding --client to compile since detected"
    echo "'$flag_icon'--press Ctrl C to cancel..."
    flag_file="minetest/bin/minetest"
    sleep 2
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
            echo "Recompiling since client was not built before..."
        fi
    fi
fi
if [ "@$enable_compile" = "@true" ]; then
    start=`date +%s`
    if [ -f "mtcompile-program.pl" ]; then
        # perl mtcompile-program.pl build >& program.log
        echo "Compiling via perl..."
        perl mtcompile-program.pl build --server $extra_options >& program.log
    else
        # NOTE: no pl in $extracted_name, assuming bash:
        echo "Compiling via bash..."
        bash -e mtcompile-program.sh build --server $extra_options >& program.log
    fi
    end=`date +%s`
    compile_time=$((end-start))
    echo "Compiling program finished in $compile_time seconds."
else
    echo "using existing minetest..."
fi
if [ ! -f "$flag_file" ]; then
    echo "ERROR: Build did not complete--missing '$flag_file'"
    exit 1
fi
dest_flag_file="$HOME/$flag_file"
if [ -f "$dest_flag_file" ]; then
    mv -f "$dest_flag_file" "$dest_flag_file.bak"
fi
if [ -f "$dest_flag_file" ]; then
    echo "ERROR: not complete since can't move old '$dest_flag_file'"
    exit 1
fi
if [ ! -d minetest ]; then
    echo "ERROR: can't install since missing `pwd`/minetest"
    exit 1
fi
try_dest="/tank/local/owner/minetest"
if [ -d "$try_dest" ]; then
    echo "Installing minetest as symlink '$HOME/minetest' pointing to '$try_dest'..."
    rsync -rt minetest/ $try_dest
    if [ ! -d "$HOME/minetest" ]; then
        ln -s $try_dest $HOME/minetest
    fi
else
    echo "Installing minetest to '$HOME'..."
    rsync -rt minetest/ $HOME/minetest
    if [ ! -f "$dest_flag_file" ]; then
        echo "ERROR: not complete--couldn't create '$dest_flag_file'"
        exit 1
    fi
fi

flag_dir="$HOME/minetest/games/Bucket_Game"
if [ ! -d "$flag_dir" ]; then
    echo "ERROR: missing $flag_dir"
    exit 1
fi
if [ ! -d "$HOME/minetest/games/ENLIVEN" ]; then
    echo "Copying $flag_dir to $HOME/minetest/games/ENLIVEN..."
    cp -R "$flag_dir" "$HOME/minetest/games/ENLIVEN"
    echo "name = ENLIVEN" > "$HOME/minetest/games/ENLIVEN/game.conf"
else
    mod_name=coderbuild
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    mod_name=codercore
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    mod_name=coderedit
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    mod_name=coderfood
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    mod_name=codermobs
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    mod_name=decorpack
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    mod_name=mtmachines
    echo "updating $mod_name..."
    rsync -rt "$flag_dir/mods/$mod_name" "$HOME/minetest/games/ENLIVEN/mods"
    # cp -f "$flag_dir/mods/LICENSE" "$HOME/minetest/games/ENLIVEN/mods/LICENSE"
fi
popd
cd ..
src="patches/subgame/menu"
dst="$HOME/minetest/games/ENLIVEN/menu"
echo "updating '$dst' from '$src/'..."
rsync -rt "$src/" "$dst"

src="patches/Bucket_Game-patched"
dst="$HOME/minetest/games/ENLIVEN"
echo "updating '$dst' from '$src/'..."
rsync -rt "$src/" "$dst"

# Bucket_Game doesn't come with a minetest.conf, only minetest.conf.example* files
# if [ ! -f "$HOME/minetest/minetest.Bucket_Game-example.conf" ]; then
#     cp -f "$HOME/minetest/minetest.conf" "$HOME/minetest/minetest.Bucket_Game-example.conf"
# fi

client_example_dest="$HOME/minetest/minetest.ENLIVEN.client-example.conf"
# client conf writing only ever happens once, unless you manually delete $client_example_dest file:
if [ ! -f "$client_example_dest" ]; then
    if [ -f "$HOME/minetest/minetest.conf" ]; then
        echo "Backing up minetest.conf..."
        if [ ! -f "$HOME/minetest/minetest.conf.1st" ]; then
            cp -f "$HOME/minetest/minetest.conf" "$HOME/minetest/minetest.conf.1st"
        else
            cp -f "$HOME/minetest/minetest.conf" "$HOME/minetest/minetest.conf.bak"
        fi
    fi
    echo "Installing minetest.conf and ENLIVEN example conf files..."
    cp -f "patches/subgame/minetest.client-example.conf" "$HOME/minetest/minetest.conf"
    cp -f "patches/subgame/minetest.LAN-client-example.conf" "$HOME/minetest/minetest.ENLIVEN.LAN-client-example.conf"
    cp -f "patches/subgame/minetest.server-example.conf" "$HOME/minetest/minetest.ENLIVEN.server-example.conf"
    cp -f "patches/subgame/minetest.client-example.conf" "$client_example_dest"
fi
server_minetest_conf_dest="$HOME/minetest/games/ENLIVEN/minetest.conf"
if [ -f "$server_minetest_conf_dest" ]; then
    echo
    echo "NOTE: $server_minetest_conf_dest will be overwritten (minetest.org releases allow you to put a world.conf file in your world, so that should be customized instead)..."
    echo
fi
echo "Writing '$server_minetest_conf_dest'..."
cp -f "patches/subgame/minetest.server-example.conf" "$server_minetest_conf_dest"
if [ -f "$HOME/i_am_dedicated_minetest_server" ]; then
    echo "server_dedicated = true" >> "$server_minetest_conf_dest"
else
    echo "server_dedicated = false" >> "$server_minetest_conf_dest"
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
    echo "Icon=$HOME/minetest/misc/minetest-xorg-icon-128.png" >> "$dest_icon"
    echo "Path=$HOME/minetest/bin" >> "$dest_icon"
    echo "Exec=$HOME/minetest/bin/minetest" >> "$dest_icon"
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
echo "Done."
echo
echo

