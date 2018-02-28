# ENLIVEN
ENLIVEN is a subgame for minetest with the goals of providing immersion and lessons for humanity.

## Primary Features of EnlivenMinetest Project
* Server installer for ENLIVEN on linux server (Ubuntu so far)
* Client installer for single-player ENLIVEN, including on Windows
* automatically install Minetest client with a usable minetest.conf (for improved graphics)

## Primary Features of ENLIVEN subgame
* birthstones, improved fork: <https://github.com/poikilos/minetest-birthstones>

### Planned Features
* maintain a table of short descriptions of mods
* see also EnlivenMinetest/etc/game-install-enliven-testing.sh
* slimenodes fork: make glue replaceable with animal hide; disable jump or reduce bouncy value, otherwise bouncing gets higher indefinitely
* https://github.com/minetest-mods/tutor
* https://github.com/minetest-mods/chat_anticurse
* https://github.com/minetest-mods/cozy (sitting and laying down player animations)--compare with emote https://github.com/minetest-mods/emote.git

#### Possible Additions
* make a ruins mod that generates ruins with: statues, mese, stone with chipped paint or paintings, tan shale blocks with and without engravings
* SWITCH to https://github.com/minetest-mods/inspector (instead of metatools mod)
  https://github.com/minetest-mods/inspector
* SWITCH to frame: "non-laggy item frame"--& make mod to alias-out the existing (homedecor?) ones in ENLIVEN
  https://github.com/minetest-mods/frame
* SWITCH to mob-engine (based on cme) by minetest-mods team
  https://github.com/minetest-mods/mob-engine
  https://forum.minetest.net/viewtopic.php?t=17106
* timer: "A persistent timer class that can be restarted after server shutdown"
  https://github.com/minetest-mods/timer
* https://github.com/xisd/trmp_Pack (but only the mods from it mods matching ENLIVEN mods)
  (NOT the same as [trm_pack by Wuzzy](https://forum.minetest.net/viewtopic.php?pid=113052#p113052), which has mostly stuff from weird mods or stuff already in trmp_minetest_game)
  * add modpack but remove fire items (flint and steel?)
  * https://github.com/xisd/trmp_Pack.git
* craftguide
* privilegeareas: Privileges granted depending on areas -- https://github.com/minetest-mods/privilegeareas/archive/master.zip
* castle_farming: floor&wall animal hide mats, straw bales, and straw training dummy
  https://github.com/minetest-mods/castle_farming
* mapfix: fixes flow and light issues
  https://github.com/minetest-mods/mapfix
* maptools: admin pickaxe and admin blocks&items to control building, movement, and light; also permanent fire, fake fire, and igniters
  https://github.com/minetest-mods/maptools
  https://forum.minetest.net/viewtopic.php?f=11&t=1882
* myroofs: sloped roofs in red, green, and dark gray--compare with existing (homedecor?) roofs in ENLIVEN
  https://github.com/minetest-mods/myroofs
* baked clay (Ethereal NG integrates with it, mobs redo, and farming redo)
* Updated pipeworks fork by HybridDog: https://github.com/HybridDog/pipeworks


##### low-pri
* (forum replies report lag) weather: https://github.com/Jeija/minetest-mod-weather ( https://forum.minetest.net/viewtopic.php?t=5245 )
* https://github.com/minetest-mods/BobBlocks (blocks that look like they have single-color LED panel on each side, light poles, and settable damaging traps)
* drawers: https://github.com/minetest-mods/drawers.git
* https://github.com/minetest-mods/pontoons (brown blocks with x that can be placed parallel with water's surface by right-clicking water)
* https://github.com/minetest-mods/trash_can (wood trash can and green dumpster)
* https://github.com/minetest-mods/breadcrumbs (special sign: right-click sign to see stream of particles to previous sign)
* https://github.com/minetest-mods/round_trunks
* https://github.com/minetest-mods/mywoodslopes
* make fork of trmp_minetest_game that has random wear for tools (see <https://forum.minetest.net/viewtopic.php?p=120285&sid=0ece6da0fc44facebc9d1f044bb033d5#p120285> for setting properties)
* character_creator: https://forum.minetest.net/viewtopic.php?f=11&t=13138
* diet, but maybe add hunger monoid when simple carbs are eaten & make hunger monoid cumulatively reduce satiation (instead of using diet):
  https://github.com/minetest-mods/diet.git
* make new decor nodes (in order of priority first): corner closed and/or open curtains (for curtains on each window both touching corner) electric range, couch
* possibly replace Immersive Sounds [ambience]: https://forum.minetest.net/viewtopic.php?t=2807
  with technic_ambience: http://realbadangel.pl/technic_ambience.zip
* dungeon_loot (but "loot" mod should already cover that with default settings)

#### Root Script Deprecation Process
##### Goals
* Remove anything running as root, by running as user in web server group, or as name (unpriveleged) user who also runs (minetestserver and) a node.js app
##### Finished
* etc/change_hardcoded_world_name_first/mts-ENLIVEN deprecated by mtsenliven.py

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

## Changes:
### (2018-02-23)
* added woodcutting https://github.com/minetest-mods/woodcutting.git
  (sneek click to start auto-harvest tree, sneak again to cancel)
  NOT same as Jeija's timber mod
### (2018-02-21)
* (installer now tries to detect 0.5.0 then install "MT_0.5.0-dev" branch of 3d armor) fix player halfway into ground when using 0.5.0 with main branch after installing 3d_armor (must use `MT_0.5.0-dev` branch)
* added worldedge mod (teleports you when you hit the edge of the map)
  https://github.com/minetest-mods/worldedge
### (2018-02-19)
* added ropes
* added digilines (I just found out it is used by technic and pipeworks)
* added armor_monoid (found out it is used by 3d_armor!): an api for creating multipliers for damage types
### (2018-02-18)
* switched to FaceDeer's fork of caverealms which is integrated with mapgen v7's perlin noise and therefore with its biomes
* subterrane: fork of Caverealms, but is just an API and needs other mods to generate anything (required by FaceDeer's fork of caverealms)
* added:
  * lightning
  * mywalls (more wall styles; brick & stone brick walls)
  * mymasonhammer (cut stairs & ladders in blocks)
  * sounding_line (machine block that measures depth of water under it)
* switched from spawners to Wuzzy's tsm_pyramids and minetest-mods' loot (was already using trm_pyramids anyway which didn't seem to work with spawners' pyramids)
* add https://github.com/minetest-mods/ts_furniture
* add vote
* add stamina: hunger-based stamina https://github.com/minetest-mods/stamina
* SWITCH from tsm_chests_dungeon to loot (loot is maintained by minetest-mods; tsm generates treasure from trm treasure lists using treasurer)
  https://github.com/minetest-mods/loot.git
  settings (for world.mt):
  * loot_vaults - Set to true to enable loot vault generation (default false)
  * loot_dungeons - Set to true to enable loot generation in dungeons (default true)
* SWITCH from farming redo to minetest-mods crops <https://github.com/minetest-mods/crops/archive/master.zip>
  (works with farming from minetest_game)
  "pumpkins, melons and potatoes are obtainable. The rest currently isn't." -sofar <https://forum.minetest.net/viewtopic.php?p=303059#p303059>
  so probably a trm_crops mod should be created
### (2018-02-17)
* switched to minetest-mods hbsprint (which optionally uses hudbars, hbhunger, and player_monoids) https://github.com/minetest-mods/hbsprint.git
  * removed all other huds and hud mods until compatibility can be determined (they were causing health and food system to not work at all)
    * formerly used GunshipPenguin's sprint
### (2018-02-15)
* moved mappers to <https://github.com/poikilos/minetestmapper-python>
### (2018-02-07)
* forked trm_minetest_game to use proper dye list (submitted pull request to ClockGen since his is the only known git version of Wuzzy's which was on the [official treasurer thread](https://forum.minetest.net/viewtopic.php?t=7292))
### (2018-02-08)
* trm_pyramids added (partial code in game-install-ENLIVEN completed)
  (a required treasure table so tsm_pyramids can provide treasure in pyramids)
* switched links to use minetest-mods' versions of:
  * unified_inventory
  * throwing (& added throwing_arrows since now throwing is an API only)
  * pipeworks
  * moreores
  * biome_lib
  * plantlife_modpack
* added anvil mod
* added sling mod: (throw any item or stack using sling--accounts for multiplayer)
* added tsm_chests_dungeon mod (adds chests to the default dungeons) -- https://forum.minetest.net/viewtopic.php?f=9&t=17005
### (2018-02-06)
* refactored file structure
  * renamed games/ENLIVEN to patches/subgame
  * moved etc/Mods* to patches/mods*
* updated mod lists for 0.4.16
  * added
  * moved nyancat to patches/subgame/minetest_game-deprecated-mods-list.txt
    (wiki.minetest.net/Nyan_Cat says if you want it back, copy it from 0.4.15)
### (2018-02-03)
* bump Python requirement to 3 (no more testing is planned to be done on python2) and use python3 binary when calling py files from scripts
    * (chunkymap-generator.bat, pythoninfo.py) if using Windows, check for various versions of Python3 and warn if fails (no longer check for Python2)
* (minetestinfo.py) account for Minetest 0.4.16 arch naming difference: minetest_game (from minetest-data package) becomes minetest (still check for minetest_game if minetest not present in minetest/games since 0.4.16 repack 3 via deb from Debian via Ubuntu still uses the folder name minetest_game)
### (2017-05-25)
* switched to expertmm fork of travelnet
### (2017-05-18)
* Installer now available at [axlemedia.net](http://www.axlemedia.net/index.php?htmlref=tutoring.html "Axle Media") -- added project and related files for Inno Setup Compiler.
### (2017-05-15)
* added mock_tnt: doesn't destroy blocks, can coexist with regular tnt mod (all tnt is replaced with mock_tnt if tnt is disabled). This mod is helpful for when multiplayer servers have tnt disabled but players have acquired 'unknown item' (tnt:tnt) as loot. The Unknown Explosive says 'unknown item' on it, as a seemless replacement :)
### (2017-04-20)
* Released ENLIVEN 0.4.15.3
### (2017-04-02)
* changed maximum range from 20 to 30 for forcefield (see technic/machines folder)
* switched from kaeza to minetest-mods github repo for xban2
* fixed issue with redundant aliases in cme_to_spawners (see Mods,WIP folder)
### (2017-03-08)
*  renamed the files in tenplus1's hud_hunger to use its nosprint version of lua files in hud_hunger/hunger
* switched to hudbars, removed hud_hunger. Add line to SERVER's minetest.conf (using installer script): hubars_bar_type = statbar_modern
### (2017-03-07)
* change to tenplus1's hud_hunger fork (BlockMen's has potential comparison of number to nil [crash] in hud/builtin.lua line 79, other issues, and is not maintained)
### (2017-03-06)
* remove computer-specific settings from minetest.conf (client version in this folder)
* remove ENLIVEN's copy of protector since TenPlus1 applied the fixes in the real repo
### (2017-02-22)
* NOTE: the protector fix from 2017-02-15 was merged by TenPlus1 today
* Fix protector crash (also sent to TenPlus1):
```lua
    if player and player:is_player() and player:get_hp() > 0 then -- ADDED THIS LINE
         -- hurt player if protection violated

         -- (a bunch of code is here for processing violations) --

    end -- ADDED THIS LINE
    return true
```
### (2017-02-15)
* (change bones) Show player (and print to server console) where died (and say bones remain or why not) -- with this addition, you can search your server log for "player's bones" where player is playername whether bones remain or not.
* (change homedecor_modpack/homedecor) Add optional non-adult beverage version of homedecor in homedecor_modpack (just changes display name & variable name of Wine rack and Beer tap and beer mug, and textures for beer mug)
* (change protector) Avoid crash by not allowing non-player to dig protected area (may only happen when one of the owners of an area does it--that was the crash scenario)
        changed
        return protector.can_dig(1, pos, player:get_player_name(), true, 1)
        to
        return player and protector.can_dig(1, pos, player:get_player_name(), true, 1) or false
### (2017-02-14)
* (change mobs) Added some nonviolent textures that could be used in a school to the ENLIVEN/mods folder (they can be manually installed after ENLIVEN by copying them to the same place in your games/ENLIVEN folder on your installation of Minetest)
### (2017-02-06)
* Added optional mods for migrating from cme and from tsm_pyramids to spawners (should allow mods that depend on cme to be installed, and use mobs instead, though no mods in ENLIVEN are known to require cme currently)
* Added optional trm_compassgps so that treasure could include a compass or map from the compassgps mod
* Added installation of trmp_minetest_game to the installer script, since treasurer requires one or more trms in order to work (tested and working now on tsm_railcorridors)

## Naming conventions:
* The filenames without extensions
* The abbreviation "mts" is for minetest server-specific scripts or variables
* du-show-big searches your hard drive for big files, in case $HOME/.minetest/debug.txt fills your drive, or a log rotate utility fails (going into a cumulative copy loop, or not) in regard to debug.txt, filling up your drive
* The network folder contains some stuff for networks, which is usually only useful for using Minetest in a network cafe or school.
(The purpose of minetest_userscript_localENLIVEN_server_only.vbs is to make sure the user only uses the hostname localENLIVEN, however this only changes the default, and cannot be enforced in any way as far as I know without recompiling the client.)

## Planned Features
* add NPCs (possibly mobs via https://github.com/Bremaweb/adventuretest/tree/master/mods/mobs )
* add https://github.com/minetest-mods/smartfs ?
* Do not allow teleporting to travelnet teleporters in an area protected from you by protection mod (even if the source teleporter is yours), but allow teleporting to areas where you cannot modify (such as advanced area protection areas where, by default, use is allowed and modify is not). Locked travelnet will not be used by this mod--instead, this less-cumbersome change is planned.
* Log where bones were placed to debug.txt, possibly by way of the following chat message:
    after the existing line:
    minetest.set_node(pos, {name = "bones:bones", param2 = param2})
    add the new line (not sure if the format call is really ok--it was copied from compassgps:
    minetest.chat_send_player(player:get_player_name(), S("Bones placed at %s."):format(pos))

## Known issues:
* minetestserver git installer doesn't take into account that minetest_game is NOT updated automatically and must overwrite existing one (should be /usr/local/share/minetest/games/minetest_game --tested on Ubuntu 17.10 Artful)
* missing nodes if switched world from older version (such as 0.4.15-git):
  * nyancat:nyancat_rainbow (make transitional mod that makes node but not worldgen, and always install it? for now is fixed by stopgap mod)
  * homedecor:bed_black_regular
  * homedecor:bed_white_regular
  * tsm_mines and tsm_railcorridors not tested with mapgen v7 (with other ENLIVEN mods)
* make a use for the following items:
  * cavestuff:desert_pebble_1
  * cavestuff:pebble_1
  * trunks:apple_tree_trunkroot
  * trunks:beech_trunkroot
  * default:sign_wall_wood
  * trunks:birch_trunkroot
  * trunks:fir_trunkroot
  * trunks:jungletreeroot
  * trunks:oak_trunkroot
  * trunks:palm_trunkroot
  * trunks:pine_treeroot
  * trunks:rubber_tree_trunk_emptyroot
  * trunks:rubber_tree_trunkroot
  * trunks:sequoia_trunkroot
  * trunks:spruce_trunkroot
  * trunks:treeroot
  * trunks:twig_1 (can make twig blocks so far)
* when using transitional mods included with EnlivenMinetest, neither type of shears work on mobs redo sheep--though mobs:shears (Steel Shears) are supposed to via right-click: https://github.com/tenplus1/mobs_redo
* tsm_railcorridors only has cobwebs if mobs_monster is installed (but I may want to switch to minetest-mods' mob-engine https://github.com/minetest-mods/mob-engine.git which is a fork of cme)
* spawners to spawners modpack transitional mod included here does not transition dungeon spawners such as `spawners:mobs_stone_monster_spawner_waiting` (in private test world near (?, -1458, -12)
* worlds made with older version of enliven use Echoes' throwing, so the following differences must be fixed possibly with a new mod:
  * Old throwing items that are not in throwing_arrows:
    * throwing:arrow_steel
    * throwing:arrow_obsidian
    * throwing:arrow_diamond
    * throwing:arrow_fireworks_blue
    * throwing:arrow_fireworks_red
    * throwing:arrow_torch
  * Old throwing items that are also in new throwing_arrows:
    * throwing:arrow_stone
    * throwing:arrow_gold
    * throwing:arrow_build
    * throwing:arrow_teleport
  * New minetest-mods/throwing_arrows which uses minetest-mods/throwing:
    * Item throwing:arrow 99
    * Item throwing:arrow_build 99
    * Item throwing:arrow_dig 99
    * Item throwing:arrow_drop 99
    * Item throwing:arrow_fire 99
    * Item throwing:arrow_gold 99
    * Item throwing:arrow_teleport 99
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
* Mining Drill mk3 duplication bug
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
Authors: expertmm (Jacob Gustafson)
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

### Regression Tests
* Use of input in python, where should never be used except in expertmm.py and minetestinfo.py for first-time setup or when interactive_enable is True
