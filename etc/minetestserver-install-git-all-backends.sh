#!/bin/bash
#this is the recommended script for servers
#remove non-git version first:
if [ -f "`command -v apt`" ]; then
  sudo apt update
fi
echo "This script compiles AND installs minetestserver (NOT run-in-place, but rather system-wide) with leveldb, redis, and defaults postgresql, doxygen, sqlite3"
echo
echo
echo "If you want to install the client on your server (not normal practice), add client or both param when calling this script."
echo "Removing the non-git (packaged) version first (Press Ctrl C  to cancel)..."
sleep 1
echo "3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
sleep 1
echo
if [ -f "`command -v apt`" ]; then
  sudo apt -y remove minetest-server
  sudo apt -y remove minetest
  sudo apt -y install libncurses5-dev libgettextpo-dev doxygen libspatialindex-dev libpq-dev postgresql-server-dev-all
  # added libpq-dev postgresql-server-dev-all (or specific version) are BOTH needed for PostgreSQL development as per https://stackoverflow.com/questions/13920383/findpostgresql-cmake-wont-work-on-ubuntu
  # if you skip the above, the below says missing: GetText, Curses, ncurses, Redis, SpatialIndex, Doxygen
  sudo apt -y install git build-essential libirrlicht-dev libgettextpo0 libfreetype6-dev cmake libbz2-dev libxxf86vm-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-openssl-dev libluajit-5.1-dev liblua5.1-0-dev libleveldb-dev
  # Ubuntu Xenial:
  sudo apt -y install libpng12-dev libjpeg8-dev
  # Debian:
  sudo apt -y install libpng-dev libjpeg-dev
elif [ -f "`command -v pacman`" ]; then
  sudo pacman -R --noconfirm minetest-server
  sudo pacman -R --noconfirm minetest
  echo "detected arch-based distro (tested only on antergos)..."
  # NOTE: the regular packages include headers on arch-based distros:
  sudo pacman -Syyu --noconfirm git spatialindex postgresql-libs doxygen postgresql-libs hiredis redis irrlicht gettext freetype2 bzip2 libpng libjpeg-turbo libxxf86vm mesa glu sqlite libogg libvorbis openal curl luajit leveldb ncurses redis hiredis gmp
  #can't find equivalent to libjpeg8-dev libxxf86vm-dev mesa sqlite libogg vorbis
elif [ -f "`command -v dnf`" ]; then
  sudo dnf -y remove minetest-server
  sudo dnf -y remove minetest
  #see poikilos post at https://forum.minetest.net/viewtopic.php?f=42&t=3837&start=125
  sudo dnf -y install -y gcc-c++ freetype-devel spatialindex-devel postgresql-devel doxygen irrlicht-devel gettext freetype cmake bzip2-devel libpng libjpeg-turbo libXxf86vm mesa-libGLU libsqlite3x-devel libogg-devel libvorbis-devel openal-devel curl-devel luajit-devel lua-devel leveldb-devel ncurses-devel redis hiredis-devel gmp-devel
  cd
  #git clone https://github.com/minetest/minetest.git
  #cd minetest/games
  #git clone https://github.com/minetest/minetest_game.git
  #cd ..
  #cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 -DENABLE_REDIS=1 -DENABLE_POSTGRESQL=1
  #make -j$(nproc)
  #sudo make install
  #minetest
  # echo -e "\n\n\e[1;33mYou can run Minetest again by typing \"minetest\" in a terminal or selecting it in an applications menu.\nYou can install mods in ~/.minetest/mods, too.\e[0m"
fi

cd
if [ ! -d "Downloads" ]; then
   mkdir Downloads
fi
cd Downloads
if [ -d minetest ]; then
  echo "ERROR: Nothing done since 'minetest' already exists in `pwd`--delete it before cloning, or run the included update script to update."
  echo "Ctrl C or this window will exit..."
  echo "3..."
  sleep 1
  echo "2..."
  sleep 1
  echo "1..."
  sleep 1
  #cd minetest
else
  git clone https://github.com/minetest/minetest.git
fi
#cd minetest
git pull --all  # see https://forum.minetest.net/viewtopic.php?f=42&t=3837&start=125#p306449
cd minetest/games
if [ ! -d minetest_game ]; then
  git clone https://github.com/minetest/minetest_game.git
else
  cd minetest_game
  git pull --all
  cd ..
fi
git pull --all
cd ..
# heavily modified from forum url above due to hints from AUR files obtained via git clone https://aur.archlinux.org/minetest-git-leveldb.git
echo "ENABLE_CURSES enables server-side terminal via --terminal option"
build_what="-DBUILD_SERVER=on -DBUILD_CLIENT=off"
if [ "$1" = "both" ]; then
  build_what="-DBUILD_SERVER=on -DBUILD_CLIENT=on"
elif [ "$1" = "client" ]; then
  build_what="-DBUILD_SERVER=off -DBUILD_CLIENT=on"
fi
cmake . -DENABLE_GETTEXT=on -DENABLE_CURSES=on -DENABLE_FREETYPE=on -DENABLE_LEVELDB=on -DENABLE_CURL=on -DENABLE_GETTEXT=on -DENABLE_REDIS=on -DENABLE_POSTGRESQL=on -DRUN_IN_PLACE=off -DCMAKE_BUILD_TYPE=Release $build_what
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
