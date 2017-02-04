# EnlivenMinetest
Subgame for minetest with the goals of creating immersion and lessons for humanity.
This collection of scripts includes some scripts to help install and manage your git version of Minetest Server on Ubuntu Server or various *buntu flavors (a gui distro neither required nor recommended).

## How to use:
(requires GNU/Linux System and only tested on Ubuntu Server [14.04 to 16.04] and Lubuntu [14.04 to 16.04])
The installer script (in the "etc/change_world_name_manually_first" folder) downloads the git versions of all of the mods to the ENLIVEN folder which will be placed in your minetest games folder (one of the two folders listed below, otherwise fails)--but change the world name to the name of your world first.
* (optionally) place the enliven folder in the games folder here into the games folder on your server such as:
  /usr/local/share/minetest/games/
	(If you're not using the git version of Minetest on Ubuntu Server, try something like:
	/usr/share/games/minetest/games/ )
  although the installer script should create the initial version of the minetest.conf in there (NOTE: there is a different version of minetest.conf for clients, as described below)
* BEFORE running game-install-enliven.sh, make sure you FIRST CHANGE the value after "MT_MYWORLD_NAME="
Do not expect the mods from game-install-enliven-testing.sh to work. Also, do not run the file directly -- instead, paste the variables (before backup process) in game-install-enliven.sh into a terminal window, then paste the contents of game-install-enliven-test.sh
* mts-ENLIVEN starts server (place it in $HOME normally), but requires you to FIRST CHANGE the value after worldname to the name of your world
* Recommend your users download the minetest.conf from this folder and put it in their minetest folder for better graphics (opengl 3.0 shaders, smooth lighting)

## Customization
* Before using anything in the change_world_name_manually_first and subfolders, change the values of the variables in the folder name as noted before using.
* If you have a dedicated server, the value server_dedicated = false should be changed to server_dedicated = true in your SERVER's minetest.conf in the ENLIVEN folder that the installer creates.

## Security and Performance Notes
* The installer script changes owner and group for ENLIVEN's world.mt and world.mt.1st if present to $USER
* The included minetest.conf recommended for your clients includes the line enable_local_map_saving = true, which will cache the world locally on their machines. You can feel free to change that according to your preference.


## Naming conventions:
* The filenames without extensions 
* The abbreviation "mts" is for minetest server-specific scripts or variables
* du-show-big searches your hard drive for big files, in case $HOME/.minetest/debug.txt fills your drive, or a log rotate utility fails (going into a cumulative copy loop, or not) in regard to debug.txt, filling up your drive
* The network folder contains some stuff for networks, which is usually only useful for using Minetest in a network cafe or school.
(The purpose of minetest_userscript_localENLIVEN_server_only.vbs is to make sure the user only uses the hostname localENLIVEN, however this only changes the default, and cannot be enforced in any way as far as I know without recompiling the client.)

## Known issues:
* Installer script does not copy certain stuff to the config files due to permissions unless runs as root (the rest is designed to run as sudoer, and use sudo only as needed)
* minetestserver-update-from-git.sh usually doesn't work right. Normally just rename your minetest folder then clone it from git instead.
* make sure always cd $HOME/Downloads before downloading stuff (double check installer script)
* minetest_userscript_localENLIVEN_server_only.vbs logon script in network folder only works if you make C:\games\Minetest writable to Authenticated Users, in order for minetest.conf to be created via this script (feel free to offer comments on how to avoid making the entire Minetest folder writable to Authenticated Users [I haven't experimented with which of the files and subfolders can be set to do not inherit])
* minetest_userscript_localENLIVEN_server_only.vbs does not read the recommended minetest.conf, so it echoes the lines manually. Ideally it would analyze the recommended one and change the server settings.

### Known issues in mods:
* compassgps crashes server for some players upon use--see yelby in etc/debugging (wrap sorting in "if player~=nil then...end" to avoid)
