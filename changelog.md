# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a
Changelog](https://keepachangelog.com/en/1.0.0/).


## [git] - 2024-01-06
### Removed
- Move mock_tnt to its own repo (https://github.com/Poikilos/mock_tnt).


## [git] - 2020-05-07
### Changed
- Make both `install-minetest-linux64.sh` and
  `install-mts.sh` use `minetestenv-in-place.rc`
- Test and fix `minetestenv-in-place.rc`.
- Rename variables.


## [git] - 2020-05-07
### Added
- bash script library (`minetestenv-in-place.rc`)

### Changed
- Move most shared functionality to `minetestenv-in-place.sh`.
- Rename variables.

### Removed
- sponge mod (since coderblocks now has one)



## [git] - 2020-03-29
### Added
- Add "Linux Server Install or Upgrade" section to
  [readme.md](readme.md).

### Fixed
- Fix counting of screenshots (`*` doesn't work in quotes)

### Changed
- Do not depend on pwd.
- Use more variables from scripting.rc if they are present.


## [git] - 2020-03-29
### Changed
- Use $HOME/.config/EnlivenMinetest to store downloads.

### Fixed
- Use instead of `-ne` for comparing strings.


## [git] - 2020-03-11
### Changed
- Generate readme-ENLIVEN.md `game-release.rc` when building ENLIVEN-mtg
  instead of emitting instructions to standard output and creating flag
  files.
  - `game-release.rc` stores information the script needs to read upon
    later runs (The file is now used instead of flag files).
  - `readme-ENLIVEN.md` stores information for the user or developer.
- Rename variables in `minetestenv.rc`.

### Fixed
- Use the new awards URL.

## [git] - 2020-02-27
### Added
- new super for map generators

### Fixed
- Changed uses of `os.rename` to `shutil.move` (prevents invalid cross-
  filesystem link errors).
  - Remove unnecessary and bare exception handler in
    correct_genresults_paths.
- fix missing "self" param for isMinWBRenderCount,
  isMinNWBRenderCount
- fix missing "self." when using isCDeployed,
  self.is_worldborder_chunk

### Removed
- (generators.py) verify_correct_map code (was commented already)

### Changed
- Use PEP8 for map generators.
  - Rename variables in map generators (and add succinct temp vars).
- (map generators) Move common code to `prepare_env`.


## [git] - 2019-09-20
### Added
- generate_Empty_at_each_vertex.py

### Changed
- rename generate_collision_box_lua.py to generate_lua_collisionbox.py
- generate_lua_collisionbox.py uses the world transform of the
  object instead of object location, so it accounts for rotation and
  scale now.
- store Blender-specific py files in utilities/blender


## [git] - 2019-05-29
### Added
(minetestenv.rc and utilities/deprecated/install-ENLIVEN-minetest_game.sh
* MT_MYGAMES_DIR (~/.minetest/games)

### Changed
(minetestenv.rc and utilities/deprecated/install-ENLIVEN-minetest_game.sh
* install game as non-root always
  - MT_MYGAME_DIR from `$SYSTEM_MT_GAMES_DIR/$MT_MYGAME_NAME`
    to `$MT_MYGAMES_DIR/$MT_MYGAME_NAME` (`$MT_MYGAMES_DIR/ENLIVEN`)
  - renamed MT_GAMES_DIR to SYSTEM_MT_GAMES_DIR
  - MT_BACKUP_GAMES_DIR from `$HOME/Backup$USR_SHARE_MINETEST/games`
    to `$HOME/.minetest/games-disabled`
  - MT_MYGAME_BAK from `$USR_SHARE_MINETEST/ENLIVEN_BAK`
    to `$MT_BACKUP_GAMES_DIR/ENLIVEN_BAK`


## [git] - 2018-03-27
### Added
* overrides for world.conf and world.mt (only if you have the directory
  ~/.minetest/worlds/CenterOfTheSun)
* (Getting Started page in web app) areas (self-protection) instructions


## [git] - 2018-03-25
**This is the first Changelog entry for the new Bucket_Game-based
ENLIVEN.**

### Added
* milk cows using Drinking Glass ( _to be merged with upstream_ with
  Bucket_Game)--see commits cb8c403 (improved textures), 3e76f33,
  cdea41f (bugfix), 5886a39 (add missing cow.lua code and found and
  improved other copy of codermobs_bucket_milk.png texture:
  mods/codermobs/codermobs/textures/codermobs_bucket_milk.png),
  c0756cc (added author and license info)
* bones messages for Bucket_Game (had already been merged with
  minetest_game: <https://github.com/minetest/minetest_game/pull/2082>;
  _to be merged upstream_ with Bucket_Game as well)
* Regarding the changes above, see
  patches/deprecated/merged-upstream/Bucket_Game/BG-1-milk-and-bones.diff
* remade non-root installer scripts in webapp directory a few days ago

### Changed
* improved sushi texture
* changed directory structure
  (changed install-ENLIVEN-minetest_game.sh to reflect that)
* renamed old install-ENLIVEN.sh to install-ENLIVEN-minetest_game.sh
* NOTE: install-ENLIVEN-minetest_game.sh is deprecated.
* use `src` instead of `etc` for name of directories that can be
  eliminated from install target
* improved details and formatting for old Changelog entries, and
  conformed them to <https://keepachangelog.com/en/1.0.0/>
* make install-mts.sh show instructions if user doesn't have a
  linux-minetest-kit/mtsrc directory yet


## [git] - 2018-10-07
* fixed lapis patching logic


## [git] - 2018-10-06
* fixed issue with not detecting pacman for installing minetestmapper
  deps
* cache repos for install as update (reduce download bandwidth and drive
  writes)
* further reduce drive writes with rsync
* use updated travelnet


## [git] - 2018-05-10
* moved fully working scripts from etc to root of repo
* renamed:
```bash
mv game-install-ENLIVEN install-ENLIVEN.sh
mv game-install-ENLIVEN-testing.sh patch-ENLIVEN-testing.sh #(formerly game-install-enliven-testing.sh)
mv minetestserver-install-git-all-backends.sh install-minetestserver-git-all-backends.sh
mv minetestserver-uninstall-git-leftovers.sh uninstall-minetestserver-git-leftovers.sh
mv minetestserver-uninstall-git.sh uninstall-minetestserver-git.sh
mv minetestserver-update-from-git.sh update-minetestserver-git.sh
mv noscreen noscreen-startweb.sh
mv startweb startweb.sh
mv stop-mts stop-mts.sh
mv archive-mts-debug archive-minetest-debug.sh
mv chat-history-mts chat-history-minetest.sh
mv du-show-big du-show-big.sh
mv mounter mounter.sh
mv unmounter unmounter.sh
```
* replaced uninstall-minetestserver-git.sh with
  uninstall-minetestserver-git.py (the shell script version was
  functionally identical to uninstall-minetestserver-git-leftovers.sh)


## [git] - 2018-03-13
* added mapfix mod since dynamic_liquid makes one block create a whole
  pond if set high above ground
* removed mapfix due to [improvements to minetest]
  (https://github.com/minetest/minetest/issues/2767)
  :edit 2019-03-25: Bucket_Game-based version of ENLIVEN includes mapfix
  (added upstream) due to remaining issues.
* removed dynamic_liquid since it makes oceans deplete as they go into
  caves (see <https://forum.minetest.net/viewtopic.php?t=16485>)


## [git] - 2018-03-08
* added technic_armor since is now in separate repo


## [git] - 2018-03-06
* added mob_horse


## [git] - 2018-02-23
* added woodcutting https://github.com/minetest-mods/woodcutting.git
  (sneek click to start auto-harvest tree, sneak again to cancel)
  NOT same as Jeija's timber mod


## [git] - 2018-02-21
* (installer now tries to detect 0.5.0 then install "MT_0.5.0-dev"
  branch of 3d armor) fix player halfway into ground when using 0.5.0
  with main branch after installing 3d_armor (must use `MT_0.5.0-dev`
  branch)
* added worldedge mod (teleports you when you hit the edge of the map)
  https://github.com/minetest-mods/worldedge


## [git] - 2018-02-19
* added ropes
* added digilines (I just found out it is used by technic and pipeworks)
* added armor_monoid (found out it is used by 3d_armor!): an api for
  creating multipliers for damage types


## [git] - 2018-02-18
* switched to FaceDeer's fork of caverealms which is integrated with
  mapgen v7's perlin noise and therefore with its biomes
* subterrane: fork of Caverealms, but is just an API and needs other
  mods to generate anything (required by FaceDeer's fork of caverealms)
* added:
  * lightning
  * mywalls (more wall styles; brick & stone brick walls)
  * mymasonhammer (cut stairs & ladders in blocks)
  * sounding_line (machine block that measures depth of water under it)
* switched from spawners to Wuzzy's tsm_pyramids and minetest-mods' loot
  (was already using trm_pyramids anyway which didn't seem to work with
  spawners' pyramids)
* add https://github.com/minetest-mods/ts_furniture
* add vote
* add stamina: hunger-based stamina https://github.com/minetest-mods/stamina
* SWITCH from tsm_chests_dungeon to loot (loot is maintained by
  minetest-mods; tsm generates treasure from trm treasure lists using
  treasurer) `https://github.com/minetest-mods/loot.git`
  - settings (for world.mt):
    * loot_vaults - Set to true to enable loot vault generation (default false)
    * loot_dungeons - Set to true to enable loot generation in dungeons (default true)
* SWITCH from farming redo to minetest-mods crops
  <https://github.com/minetest-mods/crops/archive/master.zip>
  (works with farming from minetest_game)
  "pumpkins, melons and potatoes are obtainable. The rest currently
  isn't." -sofar
  <https://forum.minetest.net/viewtopic.php?p=303059#p303059>
  so probably a trm_crops mod should be created


## [git] - 2018-02-17
* switched to minetest-mods hbsprint (which optionally uses hudbars,
  hbhunger, and player_monoids)
  https://github.com/minetest-mods/hbsprint.git
  * removed all other huds and hud mods until compatibility can be
    determined (they were causing health and food system to not work at
    all)
    * formerly used GunshipPenguin's sprint


## [git] - 2018-02-15
* moved mappers to <https://github.com/poikilos/minetestmapper-python>


## [git] - 2018-02-07
* forked trm_minetest_game to use proper dye list (submitted pull
  request to ClockGen since his is the only known git version of Wuzzy's
  which was on the [official treasurer thread]
  (https://forum.minetest.net/viewtopic.php?t=7292))


## [git] - 2018-02-08
### Added
* trm_pyramids (partial code in game-install-ENLIVEN completed)
  (a required treasure table so tsm_pyramids can provide treasure in
  pyramids)
* anvil mod
* sling mod: (throw any item or stack using sling--accounts for
  multiplayer)
* tsm_chests_dungeon mod (adds chests to the default dungeons) --
  <https://forum.minetest.org/viewtopic.php?f=9&t=17005>
### Changed
* switched links to use minetest-mods' versions of:
  * unified_inventory
  * throwing (& added throwing_arrows since now throwing is an API only)
  * pipeworks
  * moreores
  * biome_lib
  * plantlife_modpack


## [git] - 2018-02-06
### Changed
* refactored file structure
  * renamed games/ENLIVEN to patches/subgame
  * moved etc/Mods* to patches/mods*
* updated mod lists for 0.4.16
  * moved nyancat to
    patches/subgame/minetest_game-deprecated-mods-list.txt
    (wiki.minetest.net/Nyan_Cat says if you want it back, copy it from
    0.4.15)


## [git] - 2018-02-03
### Changed
* bump Python requirement to 3 (no more testing is planned to be done on
  python2) and use python3 binary when calling py files from scripts
    * (chunkymap-generator.bat, pythoninfo.py) if using Windows, check
      for various versions of Python3 and warn if fails (no longer check
      for Python2)
* (minetestinfo.py) account for Minetest 0.4.16 arch naming difference:
  minetest_game (from minetest-data package) becomes minetest (still
  check for minetest_game if minetest not present in minetest/games
  since 0.4.16 repack 3 via deb from Debian via Ubuntu still uses the
  folder name minetest_game)


## [git] - 2017-05-25
### Changed
* switched to poikilos fork of travelnet


## [git] - 2017-05-18
### Added
* Installer now available at
  [axlemedia.net]
  (http://www.axlemedia.net/index.php?htmlref=tutoring.html
  "Axle Media")
* Inno Setup Compiler project and related files


## [git] - 2017-05-15
### Added
* mock_tnt


## [git] - 2017-04-20
### Added
* Created ENLIVEN 0.4.15.3 Windows Installer


## [git] - 2017-04-02
### Changed
* changed maximum range from 20 to 30 for forcefield (see
  technic/machines folder)
* switched from kaeza to minetest-mods github repo for xban2
* fixed issue with redundant aliases in cme_to_spawners (see Mods,WIP
  folder)


## [git] - 2017-03-08
### Changed
* renamed the files in tenplus1's hud_hunger to use its nosprint version
of lua files in hud_hunger/hunger
* switched to hudbars, removed hud_hunger. Add line to SERVER's
  minetest.conf (using installer script):
  `hubars_bar_type = statbar_modern`


## [git] - 2017-03-07
### Changed
* switch to tenplus1's hud_hunger fork (BlockMen's has potential
  comparison of number to nil [crash] in hud/builtin.lua line 79, other
  issues, and is not maintained)


## [git] - 2017-03-06
### Removed
* computer-specific settings from minetest.conf (client version in this
  folder)
* ENLIVEN's copy of protector since TenPlus1 applied the fixes in the
  real repo


## [git] - 2017-02-22
### Changed
* NOTE: the protector fix from 2017-02-15 was merged by TenPlus1 today
* Fix protector crash (also sent to TenPlus1):
```lua
    if player and player:is_player() and player:get_hp() > 0 then -- ADDED THIS LINE
         -- hurt player if protection violated

         -- (a bunch of code is here for processing violations) --

    end -- ADDED THIS LINE
    return true
```


## [git] - 2017-02-15
### Changed
* (bones) Show player (and print to server console) where died (and say
  bones remain or why not) -- with this addition, you can search your
  server log for "player's bones" where player is playername whether
  bones remain or not.
* (homedecor_modpack/homedecor) Add optional non-adult beverage version
  of homedecor in homedecor_modpack (just changes display name &
  variable name of Wine rack and Beer tap and beer mug, and textures for
  beer mug)
* (protector) Avoid crash by not allowing non-player to dig protected
  area (may only happen when one of the owners of an area does it--that
  was the crash scenario)
  - changed
    `return protector.can_dig(1, pos, player:get_player_name(),
    true, 1)`
    to
    `return player and protector.can_dig(1, pos,
    player:get_player_name(), true, 1) or false`


## [git] - 2017-02-14
### Added
* (mobs) nonviolent textures that could be used in a school to the
  ENLIVEN/mods folder (they can be manually installed after ENLIVEN by
  copying them to the same place in your games/ENLIVEN folder on your
  installation of Minetest)


## [git] - 2017-02-06
### Added
* optional mods for migrating from cme and from tsm_pyramids to spawners
  (should allow mods that depend on cme to be installed, and use mobs
  instead, though no mods in ENLIVEN are known to require cme currently)
* optional trm_compassgps so that treasure could include a compass or
  map from the compassgps mod
* installation of trmp_minetest_game to the installer script, since
  treasurer requires one or more trms in order to work (tested and
  working now on tsm_railcorridors)

