# Developer Notes

## Building
* scripts and sources for recreating ENLIVEN subgame are at the
  EnlivenMinetest project page:
  https://github.com/Poikilos/EnlivenMinetest
### Further steps needed to recreate:
* extract entire zip from sfan5
* run postinstall.bat
* change version number in %USERPROFILE%\Documents\GitHub\EnlivenMinetest\winclient\install ENLIVEN.iss
* change version number in %USERPROFILE%\Documents\GitHub\EnlivenMinetest\winclient\launcher-src\ENLIVEN.pro

### additional notes
* The recommended minetest.conf for subgame, including for server, is in
  the ENLIVEN subgame folder (also available at [EnlivenMinetest on
  GitHub](https://github.com/Poikilos/EnlivenMinetest)


## Planning
- [ ] Review octacian's [Per-player
  Gamemodes](https://github.com/octacian/gamemode) and see if still
  relevant.
- [ ] Fix attribution for Fireball:
  Copyright (c) 2010-2011 Perttu Ahola <celeron55@gmail.com>
  (CC BY-SA 3.0) according to
  https://github.com/minetest/minetest/blob/stable-0.3/README.txt
  - Found
    [here](https://github.com/minetest/minetest/blob/stable-0.3/data/fireball.png)
    thanks to [PilzAdam](https://github.com/PilzAdam/mobs/issues/11)
- [ ] optimize or improve decoblocks
  - Is it the same as the one from decoblocks game? See:
    <https://minetest.org/forum/viewtopic.php?f=15&t=6420&sid=21c1c7e61a1b4e61661ceaae3b41519a>
- [ ] recommend fork of misfit model 3d to modders, if it works
  - <https://github.com/zturtleman/mm3d/issues?q=is%3Aopen+is%3Aissue>
  - Blender 2.8 replaces 2.79 on Fedora 30 now, so export plugins for
    Blender to b3d do not work yet
    - [ ] See if Joric's is easier to port or already ported.
- [ ] make new non-magical items based on traxie21 potions if that is a good start.
- [ ] Review the state of
  [More-creeps-and-weirdoes-blender-models](https://github.com/Poikilos/More-creeps-and-weirdoes-blender-models)
  and see if any more work is necessary
- [ ] Read <https://oldcoder.org/general/artwork/watercodia.html>
- [ ] Review armor settings and ensure they don't interfere with
  [Kinetic Combat](https://wiki.minetest.org/main/ideas/kinetic_combat.html) plans.
  - <https://github.com/stujones11/minetest-3d_armor/blob/master/settingtypes.txt>
  - [[Modpack] 3D Armor [0.4.8] [minetest-3d_armor]](https://forum.minetest.org/viewtopic.php?t=4654)
- [ ] Review MineClone2's ["Missing features in
  Minetest..."](https://repo.or.cz/MineClone/MineClone2.git/blob_plain/HEAD:/MISSING_ENGINE_FEATURES.md)
  - See which were implemented in MineClone2 and how.
- [ ] Review user-submitted mob textures at [Post your - Textures for
  Mobs](https://forum.minetest.org/viewtopic.php?f=4&t=10623) and use
  any that are better.
- [ ] Review textures packs and consider using one instead of default,
  or including one or more, or adding interface to add more
  automatically.
  - [PixelPerfection - By XSSheep](https://forum.minetest.org/viewtopic.php?t=14289)
  - [[16x] PixelBOX Reloaded](https://forum.minetest.org/viewtopic.php?t=14132)
  - Only on .net site: [[16x] VILJA PIX 2.0 (modified by Jozet)](https://forum.minetest.net/viewtopic.php?t=19881)
  - [mini8x](https://forum.minetest.org/viewtopic.php?t=14633)
  - Only on .net site: [[16px] Isabella II - Minetest Community Edition](https://forum.minetest.net/viewtopic.php?t=21523)
- [ ] Try Jordach's [[Game] Big Freaking Dig
  [0.5]](https://forum.minetest.org/viewtopic.php?f=15&t=9036) on Final
  Minetest.
- [ ] (only on .net site) Review issues regarding
  [damage_per_second](https://forum.minetest.net/viewtopic.php?f=6&t=18369)

### minetest.org build speeds

#### linux-minetest-kit ~200527
* Intel i7-4770K
  * libraries ~3m
  * program ~4m

### Regression Tests
* Use of input in python, where should never be used except in
  poikilos.py (some/all of that may be moved to parsing.py in
  <https://github.com/Poikilos/pycodetool>) and minetestinfo.py for
  first-time setup or when `interactive_enable` is `True`

### C++ Debugging
These steps are only needed for debug builds.

GUI:
* Try the "Scope" Geany plugin (`geany-plugins-scope`) which is a "Graphical GDB frontend".

CLI (Command-Line Interface):
* build minetest with --debug option
* cd to linux-minetest-kit/minetest/bin directory
* type (you must put ./ before minetest to ensure that gdb will use your
  debug build instead of a version your system path):
  `gdb ./minetest`
* After the symbols finish loading, complete the following within gdb:
  `run`
  * If the program terminates, gdb will tell you what debug symbol
    packages are needed for your distro.
  * When you are done debugging, type:
    quit
* Try debugging again after the proper packages are installed.
