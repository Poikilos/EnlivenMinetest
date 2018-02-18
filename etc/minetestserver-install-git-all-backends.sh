#remove non-git version first:
sudo apt update
echo "This script compiles AND installs minetestserver (NOT run-in-place, but rather system-wide) with leveldb, redis, and defaults postgresql, doxygen, sqlite3"
echo
echo
echo "If you want to install the client on your server (not normal practice), change -DBUILD_CLIENT=FALSE to -DBUILD_CLIENT=TRUE before continuing this script."
echo "Removing the non-git (packaged) version first (Press Ctrl C  to cancel)..."
sleep 1
echo "3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
sleep 1
echo
sudo apt remove minetest-server
sudo apt remove minetest

sudo apt install libncurses5-dev libgettextpo-dev doxygen libspatialindex-dev libpq-dev postgresql-server-dev-all
# added libpq-dev postgresql-server-dev-all (or specific version) are BOTH needed for PostgreSQL development as per https://stackoverflow.com/questions/13920383/findpostgresql-cmake-wont-work-on-ubuntu
# if you skip the above, the below says missing: GetText, Curses, ncurses, Redis, SpatialIndex, Doxygen
sudo apt install -y git build-essential libirrlicht-dev libgettextpo0 libfreetype6-dev cmake libbz2-dev libpng12-dev libjpeg8-dev libxxf86vm-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-openssl-dev libluajit-5.1-dev liblua5.1-0-dev libleveldb-dev
cd
if [ ! -d "Downloads" ]; then
   mkdir Downloads
fi
if [ -d minetest ]; then
  echo "ERROR: Nothing done since 'minetest' already exists in `pwd`--delete it before cloning, or run the included update script to update."
fi
git clone https://github.com/minetest/minetest.git
git pull --all  # see https://forum.minetest.net/viewtopic.php?f=42&t=3837&start=125#p306449
cd minetest/games
git clone https://github.com/minetest/minetest_game.git
git pull --all
cd ..
# heavily modified from forum url above due to hints from AUR files obtained via git clone https://aur.archlinux.org/minetest-git-leveldb.git
echo "ENABLE_CURSES enables server-side terminal via --terminal option"
cmake . -DENABLE_GETTEXT=on -DENABLE_CURSES=on -DENABLE_FREETYPE=on -DENABLE_LEVELDB=on -DENABLE_CURL=on -DENABLE_GETTEXT=on -DENABLE_REDIS=on -DENABLE_POSTGRESQL=on -DBUILD_SERVER=on -DBUILD_CLIENT=off -DRUN_IN_PLACE=off -DCMAKE_BUILD_TYPE=Release
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
echo "sudo xargs rm < install_manifest.txt"
echo "# as per http://irc.minetest.net/minetest/2015-08-06"
# based on https://forum.minetest.net/viewtopic.php?f=42&t=3837 (below)
# sudo apt-get install -y git build-essential libirrlicht-dev libgettextpo0 libfreetype6-dev cmake libbz2-dev libpng12-dev libjpeg8-dev libxxf86vm-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-openssl-dev libluajit-5.1-dev liblua5.1-0-dev libleveldb-dev; cd; git clone https://github.com/minetest/minetest.git; cd minetest/games; git clone https://github.com/minetest/minetest_game.git; cd ..; cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1; make -j$(nproc); sudo make install; minetest; echo -e "\n\n\e[1;33mYou can run Minetest again by typing \"minetest\" in a terminal or selecting it in an applications menu.\nYou can install mods in ~/.minetest/mods, too.\e[0m"
