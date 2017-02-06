# EnlivenMinetest
EnlivenMinetest is a subgame for minetest with the goals of providing immersion and lessons for humanity.
This collection of scripts includes some scripts to help install and manage your git version of Minetest Server on Ubuntu Server or various *buntu flavors (a gui distro neither required nor recommended).
EnlivenMinetest project assists you in setting up ENLIVEN subgame and provides scripts to run it on minetestserver as current user (must be sudoer).

DISCLAIMERS:
* Please see included LICENSE.txt (MIT license normally)
* The original EnlivenMinetest project is found at https://github.com/expertmm/EnlivenMinetest
* Any script code related to redis has not been successfully tested.
* Make sure you convert your world to leveldb and place it in your server's worlds folder $HOME/.minetest/worlds/, as this set of scripts hasn't been tested with any other database nor worlds folder location, and nightly backup scripts cater to leveldb.


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
* If you have used cme or tsm_pyramids is your world before, fix issue where cme is required by certain mods by manually placing the folders from etc\Mods,WIP into your mods folder (this may be automated in the future), so mobs (including spawners:mummy) will be used instead.
(There are also WIP TRMs in there to go with the ENLIVEN subgame)
Otherwise just install everything EXCEPT cme_to_spawners & tsm_pyramids_to_spawners.
(NOTE: spawners makes pyramids now, so tsm_pyramids )
* Recommend your users download the minetest.conf from this folder and put it in their minetest folder for better graphics (opengl 3.0 shaders, smooth lighting)

### Customization
* Before using anything in the change_world_name_manually_first and subfolders, change the values of the variables in the folder name as noted before using.
* If you have a dedicated server, the value server_dedicated = false should be changed to server_dedicated = true in your SERVER's minetest.conf in the ENLIVEN folder that the installer creates.

### Security and Performance Notes
* The installer script changes owner and group for ENLIVEN's world.mt and world.mt.1st if present to $USER
* The included minetest.conf recommended for your clients includes the line enable_local_map_saving = true, which will cache the world locally on their machines. You can feel free to change that according to your preference.


## Changes:
* (2017-02-06) Added optional trm_compassgps so that treasure could include a compass or map from the compassgps mod
* (2017-02-06) Added optional mods for migrating from cme and from tsm_pyramids to spawners (should allow mods that depend on cme to be installed, and use mobs instead, though no mods in ENLIVEN are known to require cme currently)

## Naming conventions:
* The filenames without extensions 
* The abbreviation "mts" is for minetest server-specific scripts or variables
* du-show-big searches your hard drive for big files, in case $HOME/.minetest/debug.txt fills your drive, or a log rotate utility fails (going into a cumulative copy loop, or not) in regard to debug.txt, filling up your drive
* The network folder contains some stuff for networks, which is usually only useful for using Minetest in a network cafe or school.
(The purpose of minetest_userscript_localENLIVEN_server_only.vbs is to make sure the user only uses the hostname localENLIVEN, however this only changes the default, and cannot be enforced in any way as far as I know without recompiling the client.)


## Known issues:
* Preciousness in trm_compassgps has not been audited
* Installer script does not copy certain stuff to the config files due to permissions unless runs as root (the rest is designed to run as sudoer, and use sudo only as needed)
* minetestserver-update-from-git.sh usually doesn't work right. Normally just rename your minetest folder then clone it from git instead.
* make sure always cd $HOME/Downloads before downloading stuff (double check installer script)
* minetest_userscript_localENLIVEN_server_only.vbs logon script in network folder only works if you make C:\games\Minetest writable to Authenticated Users, in order for minetest.conf to be created via this script (feel free to offer comments on how to avoid making the entire Minetest folder writable to Authenticated Users [I haven't experimented with which of the files and subfolders can be set to do not inherit])
* minetest_userscript_localENLIVEN_server_only.vbs does not read the recommended minetest.conf, so it echoes the lines manually. Ideally it would analyze the recommended one and change the server settings.
* minetest_game mods and modpacks are owned by root in the end, for some reason. This may cause serious problems on your server. Change the owner to your current user.

### Known issues in mods:
* compassgps crashes server for some players upon use--see yelby in etc/debugging (wrap sorting in "if player~=nil then...end" in mods/compassgps/init.lua to avoid):
```lua
function compassgps.sort_by_distance(table,a,b,player)
  --print("sort_by_distance a="..compassgps.pos_to_string(table[a]).." b="..pos_to_string(table[b]))
  if player ~= nil then
    local playerpos = player:getpos()
    local name=player:get_player_name()
    --return compassgps.distance3d(playerpos,table[a]) < compassgps.distance3d(playerpos,table[b])
    if distance_function[name] then
      return distance_function[name](playerpos,table[a]) <
             distance_function[name](playerpos,table[b])
    else
      return false  --this should NEVER happen
    end
  end
end --sort_by_distance
```
