#remove non-git version first:
echo "Removing the non-git (packaged) version first..."
echo "If you want to install the client on your server (not normal practice), change -DBUILD_CLIENT=FALSE to -DBUILD_CLIENT=TRUE before continuing this script."
sudo apt-get remove minetest-server
sudo apt-get remove minetest

sudo apt-get install libncurses5-dev libgettextpo-dev doxygen libspatialindex-dev
#if you skip the above, the below says missing: GetText, Curses, ncurses, Redis, SpatialIndex, Doxygen
sudo apt-get install -y git build-essential libirrlicht-dev libgettextpo0 libfreetype6-dev cmake libbz2-dev libpng12-dev libjpeg8-dev libxxf86vm-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-openssl-dev libluajit-5.1-dev liblua5.1-0-dev libleveldb-dev; cd; git clone https://github.com/minetest/minetest.git; cd minetest/games; git clone https://github.com/minetest/minetest_game.git; cd ..; cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 -DBUILD_SERVER=TRUE -DBUILD_CLIENT=FALSE; make -j$(nproc); sudo make install;
# minetest;
echo -e "\n\n\e[1;33mYou can run Minetest Server by typing \"minetestserver\" in a terminal.\e[0m"

# based on https://forum.minetest.net/viewtopic.php?f=42&t=3837 (below)
# sudo apt-get install -y git build-essential libirrlicht-dev libgettextpo0 libfreetype6-dev cmake libbz2-dev libpng12-dev libjpeg8-dev libxxf86vm-dev libgl1-mesa-dev libsqlite3-dev libogg-dev libvorbis-dev libopenal-dev libcurl4-openssl-dev libluajit-5.1-dev liblua5.1-0-dev libleveldb-dev; cd; git clone https://github.com/minetest/minetest.git; cd minetest/games; git clone https://github.com/minetest/minetest_game.git; cd ..; cmake . -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1; make -j$(nproc); sudo make install; minetest; echo -e "\n\n\e[1;33mYou can run Minetest again by typing \"minetest\" in a terminal or selecting it in an applications menu.\nYou can install mods in ~/.minetest/mods, too.\e[0m"