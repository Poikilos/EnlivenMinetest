# ENLIVEN
ENLIVEN is a subgame for minetest with the goals of providing immersion and lessons for humanity.
(see also webapp/README.md)

## Primary Features of EnlivenMinetest Project
* Server installer for ENLIVEN on linux server (Ubuntu so far)
* Client installer for single-player ENLIVEN, including on Windows
* automatically install Minetest client with a usable minetest.conf (for improved graphics)

## Primary Features of ENLIVEN subgame
* birthstones, improved fork: <https://github.com/poikilos/birthstones>

### Planned Features
There are several improvements I may implement in new or existing mods. For more information and status, see my [Minetest Kanboard](https://poikilos.dyndns.org/kanboard/?controller=BoardViewController&action=readonly&token=f214530d2f1294d90279631ce66b2e8b8569c6f15faf3773086476158bc8).
* maintain a table of short descriptions of mods
* see also EnlivenMinetest/etc/game-install-enliven-testing.sh
* https://github.com/minetest-mods/tutor
* https://github.com/minetest-mods/chat_anticurse
* https://github.com/minetest-mods/cozy (sitting and laying down player animations)--compare with emote https://github.com/minetest-mods/emote.git

#### node.js server manager
* capture log
  * do not store redundant messages such as hunger_ng debug mode (see <https://pastebin.com/dDBg40vf>) or saving playereffects
  * detect restarts (even if no 'separator'--see <https://pastebin.com/Jv3vkhFA>)

#### Root Script Deprecation Process
##### Goals
* Remove anything running as root, by running as user in web server group, or as name (unpriveleged) user who also runs (minetestserver and) a node.js app
##### Finished
* etc/change_hardcoded_world_name_first/mts-ENLIVEN deprecated by mtsenliven.py
* began work on new non-root installers, in webapp directory.

The [ENLIVEN project](https://github.com/poikilos/EnlivenMinetest) (aka EnlivenMinetest) includes tools for installing and maintaining the server and client for internet and LAN use, and now includes the mtanalyze (formerly minetest-chunkymap) project which includes many tools including chunkymap. The server and client are just the Minetest server and client repackaged (or just web installer scripts in the case of the server), and therefore 100% compatible with other copies of Minetest server and client of the same version--including using other subgames, which client will download from servers as usual.

DISCLAIMERS:
* Please read the Sources and License section of this document. You must agree to the licenses mentioned in order to use and copy this program.
* Any script code related to redis has not been successfully tested.
* Make sure you convert your world to leveldb and place it in your server's worlds folder $HOME/.minetest/worlds/, as this set of scripts hasn't been tested with any other database nor worlds folder location, and nightly backup scripts cater to leveldb.

## How to use:

### Windows Client:
Click "Releases" for the installer, which has the singleplayer and multiplayer client for ENLIVEN.
* alternate download site is [axlemedia.net](http://www.axlemedia.net/index.php?htmlref=tutoring.html "Axle Media")
* you must install to C:\Games\ENLIVEN (or possibly other path without spaces, as long as you don't move the launcher) in order for ENLIVEN to run.
ENLIVEN subgame is a subgame of Minetest
The ENLIVEN client runs Minetest, which can be used as a client for other Minetest servers with different subgames, but has these advantages:
* is able to be installed automatically
* comes with high quality OpenGL graphics settings in minetest.conf for modern computers
* is able to run ENLIVEN subgame in singleplayer mode without any changes

### Server:
EnlivenMinetest project assists you in setting up ENLIVEN subgame and provides scripts to run it on minetestserver as current user (must be sudoer).
Some of the included scripts help install and manage your git version of Minetest Server on Ubuntu Server or various *buntu flavors (a gui distro neither required nor recommended for minetestserver running ENLIVEN). See also https://github.com/poikilos/minetest-chunkymap for a map non-redis servers, and some offline minetest management tools.
(minetestserver requires GNU/Linux System -- only tested using apt on Ubuntu Server [14.04 to 16.04] and Lubuntu [14.04 to 16.04])
The installer script (in the "etc/change_world_name_manually_first" folder) downloads the git versions of all of the mods to the ENLIVEN folder which will be placed in your minetest games folder (one of the two folders listed below, otherwise fails)--but change the world name to the name of your world first.
* (optionally) place the ENLIVEN folder in the games folder here into the games folder on your server such as:
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
* Recommend your users use the binary installer (Windows client) from "Releases" at https://github.com/poikilos/EnlivenMinetest/releases or the alternate site above to install, otherwise installation requires a good minetest.conf downloaded such as from the winclient/launcher folder and placed in their minetest folder. The one here has better graphics (opengl 3.0 shaders, smooth lighting).

### mtanalyze
* mtanalyze is a set of tools including a live map for Minetest servers and singleplayer if using LevelDB
* for more information, see README.md in mtanalyze folder.

#### Customization
* The farming plugin is overwritten with farming redo.
* Before using anything in the change_world_name_manually_first and subfolders, change the values of the variables in the folder name as noted before using.
* If you have a dedicated server, the value server_dedicated = false should be changed to server_dedicated = true in your SERVER's minetest.conf in the ENLIVEN folder that the installer creates.

#### Security and Performance Notes
* The installer script changes owner and group for ENLIVEN's world.mt and world.mt.1st if present to $USER
* The included minetest.conf recommended for your clients includes the line enable_local_map_saving = true, which will cache the world locally on their machines. You can feel free to change that according to your preference.


## Naming conventions:
* The filenames without extensions
* The abbreviation "mts" is for minetest server-specific scripts or variables
* du-show-big searches your hard drive for big files, in case $HOME/.minetest/debug.txt fills your drive, or a log rotate utility fails (going into a cumulative copy loop, or not) in regard to debug.txt, filling up your drive
* The network folder contains some stuff for networks, which is usually only useful for using Minetest in a network cafe or school.
(The purpose of minetest_userscript_localENLIVEN_server_only.vbs is to make sure the user only uses the hostname localENLIVEN, however this only changes the default, and cannot be enforced in any way as far as I know without recompiling the client.)

## Changes
see CHANGELOG.md

## Planned Features
* add NPCs (possibly mobs via https://github.com/Bremaweb/adventuretest/tree/master/mods/mobs )
* add https://github.com/minetest-mods/smartfs ?
* install whatever mod allows making a sign to see awards
* use player_monoids instead of playereffects for mock_tnt?
* pyramids have empty chests (still?): possibly fork spawners so pyramids use treasurer like Wuzzy's fork of pyramids does: <https://forum.minetest.net/viewtopic.php?f=9&t=10336>
* ENLIVEN Windows binary release installer should be signed via a code signing license to avoid browser warnings and possible issues with virus scanners (NOTE: Squirrel.Windows has signing available such as via:
./src\.nuget\NuGet.exe pack .\ENLIVEN.<version>.nuspec
squirrel --releasify .\ENLIVEN.<version>.nupkg <your code signing options here>
* ENLIVEN/games/ENLIVEN contents should be updated (unchanged from minetest_game):
    * game_api.txt should differentiate between ENLIVEN and minetest_game
    * README.txt should differentiate between ENLIVEN and minetest_game
    * settingtypes.txt should document minetest.conf settings for various mods
    * LICENSE.txt should note correct author of header and anything else specified
* Mods in Mods,WIP need LICENSE and README with author, and removal of default in depends.txt where not dependent on default
* Preciousness in trm_compassgps has not been audited
* Installer script does not copy certain stuff to the config files due to permissions unless runs as root (the rest is designed to run as sudoer, and use sudo only as needed)
* minetestserver-update-from-git.sh usually doesn't work right. Normally just rename your minetest folder then clone it from git instead.
* make sure always cd $HOME/Downloads before downloading stuff (double check installer script)
* minetest_userscript_localENLIVEN_server_only.vbs logon script in network folder only works if you make C:\games\Minetest writable to Authenticated Users, in order for minetest.conf to be created via this script (feel free to offer comments on how to avoid making the entire Minetest folder writable to Authenticated Users [I haven't experimented with which of the files and subfolders can be set to do not inherit])
* minetest_userscript_localENLIVEN_server_only.vbs does not read the recommended minetest.conf, so it echoes the lines manually. Ideally it would analyze the recommended one and change the server settings.
* minetest_game mods and modpacks are owned by root in the end, for some reason. This may cause serious problems on your server. Change the owner to your current user.
* (minetestoffline.py) (status:closed reason:no solution) assumes name specified in file is same as id (filename)

### Known issues in mods:
* Crafting wool with dark green dye makes green wool (should make dark green), therefore making pool table is impossible.
  see https://github.com/minetest/minetest_game/issues/1940
* Technic manual is not complete. Contribute info on drills and mining? See https://github.com/minetest-mods/technic/blob/master/manual.md
* regular doors and chests are not protected via protection block/symbol
* homedecor doors are not protected via protection block/symbol
* players can use chests (other than protected chests) in a protected area in which they aren't added to the protection node
* unpriveleged players can pick up spawners and then place them (and, spawners catch things on fire)
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
* And more:
```
2017-02-13 18:15:32: WARNING[Main]: NodeDefManager: Ignoring CONTENT_IGNORE redefinition
2017-02-13 18:15:32: WARNING[Main]: Field "tile_images": Deprecated; new name is "tiles".
2017-02-13 18:15:32: WARNING[Main]: Field "metadata_name": Deprecated; use on_add and metadata callbacks
2017-02-13 18:15:32: ERROR[Main]: get_biome_list: failed to get biome 'taiga'
2017-02-13 18:15:32: ERROR[Main]: get_biome_list: failed to get biome 'snowy_grassland'
2017-02-13 18:15:32: ERROR[Main]: get_biome_list: failed to get biome 'grassland'
2017-02-13 18:15:32: ERROR[Main]: get_biome_list: failed to get biome 'coniferous_forest'
2017-02-13 18:15:32: ERROR[Main]: get_biome_list: failed to get biome 'deciduous_forest'
2017-02-13 18:15:32: ERROR[Main]: get_biome_list: failed to get biome 'savanna'
2017-02-13 18:15:32: ERROR[Main]: get_biome_list: failed to get biome 'rainforest'
2017-02-13 18:15:32: ERROR[Main]: register_ore: couldn't get all biomes
2017-02-13 18:15:33: WARNING[Main]: Not registering alias, item with same name is already defined: mushroom:brown_natural -> flowers:mushroom_fertile_brown
2017-02-13 18:15:33: WARNING[Main]: Not registering alias, item with same name is already defined: mushroom:red_natural -> flowers:mushroom_fertile_red
2017-02-13 18:15:33: WARNING[Main]: Not registering alias, item with same name is already defined: farming_plus:orange -> ethereal:orange
2017-02-13 18:15:34: WARNING[Main]: Field "noise_threshhold": Deprecated: new name is "noise_threshold".
2017-02-13 18:15:34: WARNING[Main]: Undeclared global variable "HUD_ENABLE_HUNGER" accessed at ...e/minetest/games/ENLIVEN/mods/hud_hunger/hud/builtin.lua:41
2017-02-13 18:15:35: WARNING[Main]: Field "maxwear" is deprecated; replace with uses=1/maxwear
2017-02-13 18:15:35: ACTION[Main]: [Mod] Fishing - Crabman77's (MFF team) version [1.0.0] [fishing] Loaded...
2017-02-13 18:15:35: WARNING[Main]: Field "noise_threshhold": Deprecated: new name is "noise_threshold".
2017-02-13 18:15:36: WARNING[Main]: Node 'light_source' value exceeds maximum, limiting to maximum: technic:forcefield
2017-02-13 18:15:37: WARNING[Main]: Not registering alias, item with same name is already defined: tsm_pyramids:mummy -> spawners:mummy
2017-02-13 18:15:37: WARNING[Main]: Not registering alias, item with same name is already defined: creatures:chicken -> mobs_animal:chicken
2017-02-13 18:15:37: WARNING[Main]: Not registering alias, item with same name is already defined: creatures:sheep -> mobs_animal:sheep_white
2017-02-13 18:15:37: WARNING[Main]: Not registering alias, item with same name is already defined: mobs_animal:sheep -> mobs_animal:sheep_white
2017-02-13 18:15:37: WARNING[Main]: Not registering alias, item with same name is already defined: creatures:ghost -> mobs_monster:spider
2017-02-13 18:15:37: WARNING[Main]: Not registering alias, item with same name is already defined: creatures:mummy -> spawners:mummy
2017-02-13 18:15:37: WARNING[Main]: Not registering alias, item with same name is already defined: creatures:zombie -> mobs_monster:stone_monster
```
* The following issues may be caused by having cme enabled on the server before server was updated to ENLIVEN latest (mobs only):
```
2017-02-13 18:20:59: ERROR[Server]: LuaEntity name "creatures:zombie_spawner_dummy" not defined
2017-02-13 18:21:15: WARNING[Emerge-0]: Map::getNodeMetadata(): Block not found
2017-02-13 18:21:15: WARNING[Emerge-0]: Map::removeNodeMetadata(): Block not found
2017-02-13 18:44:02: ACTION[Server]: thefox963 digs mesecons:wire_11010000_on at (-340,16,60)
2017-02-13 18:44:02: WARNING[Server]: Undeclared global variable "digiline" accessed at ...es/ENLIVEN/mods/mesecons/mesecons_luacontroller/init.lua:274
```

## Building
* scripts and sources for recreating ENLIVEN subgame are at the EnlivenMinetest project page: https://github.com/poikilos/EnlivenMinetest
Further steps needed to recreate:
* extract entire zip from sfan5
* run postinstall.bat
* change version number in C:\Users\Owner\Documents\GitHub\EnlivenMinetest\winclient\install ENLIVEN.iss
* change version number in C:\Users\Owner\Documents\GitHub\EnlivenMinetest\winclient\launcher-src\ENLIVEN.pro

### additional notes
* The recommended minetest.conf for subgame, including for server, is in the ENLIVEN subgame folder (also available at [EnlivenMinetest on GitHub](https://github.com/poikilos/EnlivenMinetest)

## Sources and License
Authors: poikilos (Jake Gustafson)
ENLIVEN project (aka EnlivenMinetest), including launcher (ENLIVEN application) and ENLIVEN subgame, is released under the LGPL v2.1 license (see LICENSE), except media which is released under the CC-BY-SA 3.0 license (see LICENSE). There are other exceptions to this license and authorship where specified below and in subfolders.
Source code is available at [https://github.com/poikilos/EnlivenMinetest](https://github.com/poikilos/EnlivenMinetest).

### Minetest
Minetest is included with releases--for Minetest license, please read README.txt in Minetest's doc folder which is provided in releases.
* Included build is sfan5's build from https://minetest.kitsunemimi.pw/builds
  release: minetest-0.4.15-8729e7d-win64

#### Differences from sfan5's build
(changed by EnlivenMinetest project)
* removed Voxelgarden subgame
* added minetest.conf similar to the one generated by ENLIVEN scripts for schools vbscript, except with public servers enabled
* added files specific to ENLIVEN, including launcher (ENLIVEN application), ENLIVEN subgame (including optional child-friendly changes for schools), other files, and licenses of added files.

### Qt
Qt 5.7.0 files are under the LGPLv3 unless required by licenses in qtlicenses folder.
Sources for Qt 5.7.0 are available via http://www.qt.io
The following files belong to Qt 5.7.0:
iconengines\*
imageformats\*
platforms\*
translations\*
D3Dcompiler_47.dll
libEGL.dll
libgcc_s_dw2-1.dll
libGLESV2.dll
libstdc++-6.dll
libwinpthread-1.dll
opengl32sw.dll
Qt5Core.dll
Qt5Gui.dll
Qt5Svg.dll
Qt5Widgets.dll

## Developer Notes

### minetest.org build speeds
* Intel i7-4770K
  * libraries ~3m
  * program ~4m

### Regression Tests
* Use of input in python, where should never be used except in poikilos.py and minetestinfo.py for first-time setup or when interactive_enable is True
