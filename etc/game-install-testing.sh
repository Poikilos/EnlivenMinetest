echo "Installing Enliven TESTING patch (run this after game-install-enliven.sh)"
echo "* You have to manually paste the environment variable settings from the beginning of game-install-enliven.sh here, so you have them."
echo "* Only install these mods if you know what you are doing! These mods may become part of enliven later, but are not thoroughly tested for stability and compatibility. Thanks, expertmm."
echo "Known issues:"
echo "* advanced_npc: 0.4.15 git (Jan 2017) has error with advanced_npc even with secure.enable_security = false ()"
echo "* torches: removes ceiling torches"

#TODO:
# * possibly add aliases for mobf_traders--Sokomine seems to indicate that this worldgen mod spawns the villagers manually: https://github.com/Sokomine/mg_villages/issues/5
# * add splash icon AND splash background for Enliven subgame
# * clicking barrel just rotates it (destroying watever you had left in it)
# * try https://github.com/Sokomine/mines_with_shafts and see if has treasure
# * try https://github.com/Sokomine/village_gambit additional village type for mg_villages
# * merge /home and unifiedinventory home (and make both require home priv)

#TODO for enliven main branch:
# * shift click to pull out maximum number of items you can create (such as multiple stacks of stairs from wood)
# * kick players at certain time intervals (if play span when logged in is not current play span, then kick) such as for schools
# * remove recipe for flint&steel (obsidian shard+Wrought Iron Ingot [default:steel_ingot])
# * detect whether tnt is disabled, and make obtaining it obtain a note or something (or somehow disable spawning of item in rail corridor chests where I found some)
# * rename minetest-chunkymap to minetestoffline or something
# * add recommended minetest.conf settings (provide python script to test, requiring minetestoffline)
# * analyze game-install-enliven-testing-FULLDEBUG.txt
# * possibly disable fire:flint_and_steel usage other than fake fire (fake fire fork used is in homedecor_modpack)
# * make spawners have drops -- similar drops as [cme] creatures:*_spawner
# * test whether abandoned mines will still be littered with empty chests if CHESTS_GENERATE or SPAWNERS_GENERATE instead of both are on in settings.txt in spawners mod folder (mine chests had stuff before adding spawners mod [mobs mod had been added])
# * make bones write where&whose bones were placed to log (see "dungeon spawner placed at" in spawners for lua example)
# * resolve mg_villages error:
#2017-01-30 03:08:37: ERROR[Main]: ServerError: AsyncErr: ServerThread::run Lua: Runtime error from mod 'default' in callback item_OnPlace(): ...e/minetest/games/enliven/mods/mg_villages/protection.lua:215: attempt to concatenate field 'mts_path' (a nil value)
#2017-01-30 03:08:37: ERROR[Main]: stack traceback:
#2017-01-30 03:08:37: ERROR[Main]:  ...e/minetest/games/enliven/mods/mg_villages/protection.lua:215: in function 'on_rightclick'
#2017-01-30 03:08:37: ERROR[Main]:  ...ocal/share/minetest/games/enliven/mods/default/torch.lua:67: in function <...ocal/share/minetest/games/enliven/mods/default/#torch.lua:61>
#2017-01-30 03:08:37: ACTION[Server]: singleplayer leaves game. List of players:
#2017-01-30 03:08:37: ACTION[Main]: [fishing] Server shuts down. saving trophies table
# * resolve issue where signslib uses small Helvetica Narrow font even if extrafonts is used properly by 31px/* (largest) being copied to signslib/textures/ (see below)
# * check whether special_picks large picks can break protection
# * change uses of maxwear=x to uses=1/x as per minetest server startup warnings: plantlife_modpack/vines/shear.lua and worldedit_commands/wand.lua
# * sometimes sorting compassgps by location crashes (only on the included user file named yelby in the etc folder)
if [ ! -d "$MT_MYGAME_MODS_PATH" ]; then
  echo "bad MT_MYGAME_MODS_PATH=$MT_MYGAME_MODS_PATH, so you must be doing it wrong."
  exit 1
fi

#https://forum.minetest.net/viewtopic.php?t=14359
#This mod is part of minetest_game 0.4.15!
#TODO: With exception of the wieldlight
#add_git_mod torches torches https://github.com/BlockMen/torches.git

# This mod is part of minetest_game 0.4.15!
# add_git_mod moresnow moresnow https://github.com/Sokomine/moresnow

echo "Installing adrido's (NOT MasterGollum's which is incompatible with moreblocks) darkage..."
#linked from MasterGollum's: https://forum.minetest.net/viewtopic.php?id=3213
add_git_mod darkage darkage https://github.com/adrido/darkage.git

# used by mg_villages
add_git_mod cottages cottages https://github.com/Sokomine/cottages.git

# advanced_npc: see also https://github.com/hkzorman/advanced_npc/wiki
add_git_mod advanced_npc advanced_npc https://github.com/hkzorman/advanced_npc.git

#forum post (special_picks by cx384): https://forum.minetest.net/viewtopic.php?f=11&t=9574
add_git_mod special_picks special_picks https://github.com/cx384/special_picks.git

# no longer needed since ENLIVEN main branch now uses expertmm travelnet:
# add_git_mod travelnet travelnet https://github.com/Sokomine/travelnet.git

add_git_mod mg mg https://github.com/minetest-mods/mg.git

#used by mg_villages fork by Sokomine
add_git_mod handle_schematics handle_schematics https://github.com/Sokomine/handle_schematics.git
# mg_villages no longer needed (?) since minetest-mods now maintains an mg with villages
#forum post (Sokomine's mg_villages provides villages for all mapgens and is based on is fork of Nores mg mapgen): https://forum.minetest.net/viewtopic.php?f=9&t=13116
#add_git_mod mg_villages mg_villages https://github.com/Sokomine/mg_villages.git

