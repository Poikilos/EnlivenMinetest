#!/bin/bash
# The git repo ONLY includes the core engine: http://localhost:3000/minetest/minetest.git
# The build kit should be used, & has "patched Irrlicht, the new LuaJit, built-in LevelDB and Snappy support, Bucket Game, Bucket City, Wonder World, the schems collection, and other pieces"

customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
}

cd webapp || customDie "You must run this script from the directory containing the webapp directory."
if [ ! -d linux-minetest-kit ]; then
    bash reset-minetest-install-source.sh
fi
bash install-mts.sh --client --server


exit 0
# IGNORE EVERYTHING BELOW, it forces the git version

msg="Installing minetestserver ONLY (no param specified). If you want to install the client on your server (not normal practice) or are on a computer with a graphical desktop, add client or both param when calling this script."
warnings=""
enable_postgres=false
enable_redis=false
MAKEDEBUG=false
TIDYUP=true
postgresql_line="-DENABLE_POSTGRESQL=0"
redis_line="-DENABLE_REDIS=0"
server_line="-DBUILD_SERVER=1"
client_line="-DBUILD_CLIENT=1"
#build_what="-DBUILD_SERVER=1 -DBUILD_CLIENT=1"

for var in "$@"
do
  if [ "$var" == "--remove-release" ]; then
    if [ ! -f git_flag ]; then
      if [ -d minetest ]; then
        rm -fr minetest
      fi
    fi
  fi
done

force_enable_server=false
force_enable_client=false

for var in "$@"
do
  if [ "$var" == "--postgres" ]; then
    enable_postgres=true
    postgresql_line="-DENABLE_POSTGRESQL=1"
  elif [ "$var" == "--redis" ]; then
    enable_redis=true
    redis_line="-DENABLE_REDIS=1"
  elif [ "$var" == "--server" ]; then
    server_line="-DBUILD_SERVER=1"
    if [ "$force_enable_client" = "false" ]; then
      client_line="-DBUILD_CLIENT=0"
    fi
    force_enable_server=true
    #build_what="-DBUILD_SERVER=on -DBUILD_CLIENT=off"
  elif [ "$var" == "--client" ]; then
    if [ "$force_enable_server" = "false" ]; then
      server_line="-DBUILD_SERVER=0"
    fi
    client_line="-DBUILD_CLIENT=1"
    force_enable_client=true
    #build_what="-DBUILD_SERVER=off -DBUILD_CLIENT=on"
  elif [ "$var" == "--no-tidyup" ]; then
    TIDYUP=false
  elif [ "$var" == "--git" ]; then
    touch git_flag
    if [ ! -d minetest ]; then
      git clone http://git.minetest.org:3000/minetest/minetest.git
    else
      cd minetest
      git pull
      cd ..
    fi
  elif [ "$var" == "--debug" ]; then
    MAKEDEBUG=true
  fi
done

echo "Backends:"
echo "* leveldb (by default)"
echo "* sqlite3 (by default)"
if [ "$enable_redis" = "true" ]; then
  echo "* redis"
else
  echo "  (skipping redis--not used by default in this version)"
fi
if [ "$enable_postgres" = "true" ]; then
  echo "* postgres"
else
  echo "  (skipping postgresql--not used by default in this version)"
fi

if [ "$1" = "both" ]; then
  msg="Installing minetest client AND server (param specified: both)."
elif [ "$1" = "client" ]; then
  msg="Installing minetest client ONLY (param specified: client)."
else
  if [ ! -z "$XDG_CURRENT_DESKTOP" ]; then
    warnings="WARNING: Detected $XDG_CURRENT_DESKTOP...you probably meant to install client or both (use client or both param after this script)"
  fi
fi
echo $msg
echo $warnings
echo
echo
if [ ! -z "$warnings" ]; then
  echo "You may want to cancel and correct warnings above..."
  echo "(If you do not press Ctrl C, install will continue anyway)"
  echo "3..."
  sleep 1
  echo "2..."
  sleep 1
  echo "1..."
  sleep 1
fi

cd
if [ ! -d "Downloads" ]; then
   mkdir Downloads
fi
cd Downloads
#if [ -d minetest ]; then
  #echo "ERROR: Nothing done since 'minetest' already exists in `pwd`--delete it before cloning, or run the included update script to update."
  #echo "Ctrl C or this window will exit..."
  #echo "3..."
  #sleep 1
  #echo "2..."
  #sleep 1
  #echo "1..."
  #sleep 1
  #cd minetest
#else
zip_name="linux-minetest-kit.zip"
extracted_name="linux-minetest-kit"
wget -O $zip_name https://downloads.minetest.org/$zip_name
if [ ! -f "$zip_name" ]; then
  echo "ERROR: Nothing done since $zip_name could not be downloaded."
  exit 1
fi

unzip -u "$zip_name"
# -o  overwrite non-interactively
# -u  update files, create if necessary

if [ ! -d "$extracted_name" ]; then
  echo "ERROR: Nothing done since after extracting $zip_name, there is"
  echo "  still no directory: $extracted_name"
  exit 2
fi

cd "$extracted_name"

bash -e mtcompile-libraries.sh build >& libraries.log
bash -e mtcompile-program.sh build >& program.log

exit 0

if [ ! -d minetest ]; then
  git clone https://github.com/minetest/minetest.git
  cd minetest
else
  cd minetest
  echo "updating: `pwd`"
  git pull  # --all  # see https://forum.minetest.net/viewtopic.php?f=42&t=3837&start=125#p306449
fi
cd games
if [ ! -d minetest_game ]; then
  git clone https://github.com/minetest/minetest_game.git
else
  cd minetest_game
  echo "updating: `pwd`"
  git pull  # --all
  cd ..
fi
#(does nothing since currently in games folder) git pull --all
#echo "in: `pwd`"
cd ..
#echo "in: `pwd`"
#echo "..."
#sleep 10
# heavily modified from forum url above due to hints from AUR files obtained via git clone https://aur.archlinux.org/minetest-git-leveldb.git
echo "ENABLE_CURSES enables server-side terminal via --terminal option"
build_what="-DBUILD_SERVER=on -DBUILD_CLIENT=off"
if [ "$1" = "both" ]; then
  build_what="-DBUILD_SERVER=on -DBUILD_CLIENT=on"
  echo "Building minetest and minetestserver (only)..."
elif [ "$1" = "client" ]; then
  build_what="-DBUILD_SERVER=off -DBUILD_CLIENT=on"
  echo "Building minetest CLIENT (only)..."
else
  echo "Building minetestserver..."
fi

echo "3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
sleep 1
cmake .$ext_lua -DENABLE_GETTEXT=on -DENABLE_CURSES=on -DENABLE_FREETYPE=on -DENABLE_LEVELDB=on -DENABLE_CURL=on -DENABLE_GETTEXT=on -DENABLE_REDIS=on -DENABLE_POSTGRESQL=on -DRUN_IN_PLACE=off -DCMAKE_BUILD_TYPE=Release $build_what
# NOTE: as long as -DRUN_IN_PLACE=off, above installs correctly without -DCMAKE_INSTALL_PREFIX=/usr which for some reason is used by https://aur.archlinux.org/minetest-git.git
#  -DCMAKE_BUILD_TYPE=Release as per https://aur.archlinux.org/minetest-git.git
make -j$(nproc)
sudo make install
if [ -f "`command -v update-desktop-database`" ]; then
  echo "updating desktop database as per https://aur.archlinux.org/minetest-git.git"
  update-desktop-database &>/dev/null && update-desktop-database -q
fi
if [ -f "`command -v gtk-update-icon-cache`" ]; then
  echo "updating gtk icon cache as per https://aur.archlinux.org/minetest-git.git"
  gtk-update-icon-cache   &>/dev/null && gtk-update-icon-cache -q -t -f usr/share/icons/hicolor
fi
# minetest;
echo -e "\n\n\e[1;33mYou can run Minetest Server by typing \"minetestserver\" in a terminal, but using mtsenliven.py is recommended instead and keeps a config file for what world and subgame you want via minetestinfo.py.\e[0m"
echo "The only known uninstall method is:"
echo "  cd $HOME/Downloads/minetest"
echo "  sudo xargs rm < install_manifest.txt"
echo "  # as per http://irc.minetest.net/minetest/2015-08-06"
# based on https://forum.minetest.net/viewtopic.php?f=42&t=3837 (below)
# sudo apt-get install -y git build-essential libirrlicht-dev libgettextpo0 libfreetype6-dev cmake libbz2-dev libpng12-dev libjpeg8-dev libxxf86vm-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-openssl-dev libluajit-5.1-dev liblua5.1-0-dev libleveldb-dev; cd; git clone https://github.com/minetest/minetest.git; cd minetest/games; git clone https://github.com/minetest/minetest_game.git; cd ..; cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1; make -j$(nproc); sudo make install; minetest; echo -e "\n\n\e[1;33mYou can run Minetest again by typing \"minetest\" in a terminal or selecting it in an applications menu.\nYou can install mods in ~/.minetest/mods, too.\e[0m"

