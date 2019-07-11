# EnlivenMinetest
(see also webapp/README.md)
by [Poikilos](https://github.com/poikilos)

1. ENLIVEN is a subgame for minetest with the goals of providing
   immersion and lessons for humanity.
2. The [ENLIVEN project](https://github.com/poikilos/EnlivenMinetest)
   (aka EnlivenMinetest) includes tools for installing and maintaining
   the server and client for internet and LAN use, and now includes the
   mtanalyze (formerly minetest-chunkymap) project which includes many
   tools including chunkymap. The server and client are just the
   Minetest server and client repackaged (or just web installer scripts
   in the case of the server), and therefore 100% compatible with other
   copies of Minetest server and client of the same version--including
   using other subgames, which client will download from servers as
   usual.

## Primary Features of EnlivenMinetest Project
* Server installer for ENLIVEN on linux server (Ubuntu so far)
* Client installer for single-player ENLIVEN, including on Windows
* automatically install Minetest client with a usable minetest.conf (for
  improved graphics)

## Primary Features of ENLIVEN subgame
* birthstones, improved fork: <https://github.com/poikilos/birthstones>
  (also part of Bucket_Game)
* See also overrides/worlds/CenterOfTheSun/world.conf

### Planned Features
There are several improvements I may implement in new or existing mods.
See the [Issues](https://github.com/poikilos/EnlivenMinetest/issues)
section of the GitHub project.
* See also install-ENLIVEN-minetest_game.sh for a full list of mods from
  the old ENLIVEN that will probably be added to the new ENLIVEN which
  is based on Bucket_Game (many of the mods are already present because
  they are in Bucket_Game!)
* Issues not yet added to the GitHub project's Issues are at
  [Minetest Kanboard](https://poikilos.dyndns.org/kanboard/?controller=BoardViewController&action=readonly&token=f214530d2f1294d90279631ce66b2e8b8569c6f15faf3773086476158bc8)
* Disable potentially (stuff in Bucket_Game not matching theme):
  - codermobs gems (see codermobs_gem_*.png such as
    codermobs_gem_fire.png)

#### node.js server manager
* capture log
  * do not store redundant messages such as hunger_ng debug mode (see
    <https://pastebin.com/dDBg40vf>) or saving playereffects
  * detect restarts (even if no 'separator'--see
    <https://pastebin.com/Jv3vkhFA>)

## DISCLAIMERS
* Please read the Sources and License section of this document. You must
  agree to the licenses mentioned in order to use and copy this program.
* Any script code related to redis has not been successfully tested.
* Make sure you convert your world to leveldb and place it in your
  server's worlds folder $HOME/.minetest/worlds/, as this set of scripts
  hasn't been tested with any other database nor worlds folder location,
  and nightly backup scripts cater to leveldb.


## Install

#### Linux
* Open terminal, then:
```bash
if [ ! -d webapp ]; then
    echo "ERROR: this will only work from the extracted or cloned EnlivenMinetest directory"
    echo "Press Ctrl C, or this terminal will exit..."
    sleep 1
    echo "3..."
    sleep 1
    echo "2..."
    sleep 1
    echo "1..."
    sleep 1
    exit 1
fi
cd webapp
# the next command downloads the latest linux-build-kit, CLEARS the
# webapp/linux-build-kit/minetest directory, and compiles the libraries.
# Do not put anything important in that directory--the latter install
# script installs the game to $HOME/minetest and that is the copy of
# minetest you should use (such as via the icon).
bash reset-minetest.sh
bash install-mts.sh --client
```
* Icon will be added as:
  `$HOME/.local/share/applications/org.minetest.minetest.desktop`
  (your window manager should automatically detect the change--if not,
  you may need to restart your window manager. If it still doesn't show,
  contact the maintainer of your window manager. This works in KDE on
  Fedora 29. Workaround: copy the icon from there to your desktop.)

## How to use

### Windows Client
Click "Releases" for the installer, which has the singleplayer and
multiplayer client for ENLIVEN.
* alternate download site is
  [expertmultimedia.com](http://www.expertmultimedia.com/index.php?htmlref=tutoring.html "Expert Multimedia")
* you must install to C:\Games\ENLIVEN (or possibly other path without
  spaces, as long as you don't move the launcher) in order for ENLIVEN
  to run.

#### ENLIVEN subgame is a subgame of Minetest
The ENLIVEN client runs Minetest, which can be used as a client for
other Minetest servers with different subgames, but has these
advantages:
* is able to be installed automatically
* comes with high quality OpenGL graphics settings in minetest.conf for
  modern computers
* is able to run ENLIVEN subgame in singleplayer mode without any
  changes

### Server

#### Install on linux server
* open terminal (root NOT recommended)
* IF you are a decicated server, first run
  `touch $HOME/i_am_dedicated_minetest_server` then run:
```bash
if [ ! -d webapp ]; then
    echo "ERROR: this will only work from the extracted or cloned EnlivenMinetest directory"
    echo "Press Ctrl C, or this terminal will exit..."
    sleep 1
    echo "3..."
    sleep 1
    echo "2..."
    sleep 1
    echo "1..."
    sleep 1
    exit 1
fi
cd webapp
bash reset-minetest.sh
bash install-mts.sh
# If you want to install the client, you should instead run
# bash install-mts.sh --client
# (defaults to client if $HOME/Desktop/org.minetest.minetest.desktop
# file exists)
```

### mtanalyze
(not maintained, kept for legacy use--if you fix anything, please submit
a pull request)
* mtanalyze is a set of tools including a live map for Minetest servers
  and singleplayer if using LevelDB
* for more information, see README.md in mtanalyze folder.

#### Customization
* The farming plugin is overwritten with farming redo in the
  minetest_game based install script. Bucket_Game already has something
  good, apparently based on farming redo.
* Before using anything in the change_world_name_manually_first and
  subfolders, change the values of the variables in the folder name as
  noted before using.
* If you have a dedicated server, the value server_dedicated = false
  should be changed to server_dedicated = true in your SERVER's
  minetest.conf in the ENLIVEN folder that the installer creates.

#### Security and Performance Notes
* The root installer script (deprecated) changes owner and group for
  ENLIVEN's world.mt and world.mt.1st if present to $USER
* The included minetest.conf recommended for your clients
  (patches/subgame/minetest.*client.conf) includes the line
  `enable_local_map_saving = true`, which will cache the world locally
  on their machines. You can feel free to change that according to your
  preference.

## Naming conventions:
* The filenames without extensions
* The abbreviation "mts" is for minetest server-specific scripts or
  variables
* du-show-big searches your hard drive for big files, in case
  $HOME/.minetest/debug.txt fills your drive, or a log rotate utility
  fails (going into a cumulative copy loop, or not) in regard to
  debug.txt, filling up your drive
* The network folder contains some stuff for networks, which is usually
  only useful for using Minetest in a network cafe or school.
  (The purpose of minetest_userscript_localENLIVEN_server_only.vbs is to
  make sure the user only uses the hostname localENLIVEN, however this
  only changes the default, and cannot be enforced in any way as far as
  I know without recompiling the client.)

## Changes
see CHANGELOG.md

## Network Deployment
* minetest_userscript_localENLIVEN_server_only.vbs logon script in
  network folder only works if you make C:\games\Minetest writable to
  Authenticated Users, in order for minetest.conf to be created via this
  script (feel free to offer comments on how to avoid making the entire
  Minetest folder writable to Authenticated Users [I haven't
  experimented with which of the files and subfolders can be set to do
  not inherit])
* minetest_userscript_localENLIVEN_server_only.vbs does not read the
  recommended minetest.conf, so it echoes the lines manually. Ideally it
  would analyze the recommended one and change the server settings.

## Building
* scripts and sources for recreating ENLIVEN subgame are at the
  EnlivenMinetest project page:
  https://github.com/poikilos/EnlivenMinetest
### Further steps needed to recreate:
* extract entire zip from sfan5
* run postinstall.bat
* change version number in %USERPROFILE%\Documents\GitHub\EnlivenMinetest\winclient\install ENLIVEN.iss
* change version number in %USERPROFILE%\Documents\GitHub\EnlivenMinetest\winclient\launcher-src\ENLIVEN.pro

### additional notes
* The recommended minetest.conf for subgame, including for server, is in
  the ENLIVEN subgame folder (also available at [EnlivenMinetest on
  GitHub](https://github.com/poikilos/EnlivenMinetest)

## Sources and License
Authors: poikilos (Jake Gustafson)
ENLIVEN project (aka EnlivenMinetest), including launcher (ENLIVEN
application) and ENLIVEN subgame, is released under the LGPL v2.1
license (see LICENSE), except media which is released under the CC BY-SA
3.0 license (see LICENSE). There are other exceptions to this license
and authorship where specified below and in subfolders.
Source code is available at
[https://github.com/poikilos/EnlivenMinetest](https://github.com/poikilos/EnlivenMinetest).

### Minetest
Minetest is included with releases--for Minetest license, please read
README.txt in Minetest's doc folder which is provided in releases.
* Included build is sfan5's build from
  https://minetest.kitsunemimi.pw/builds release:
  minetest-0.4.15-8729e7d-win64

#### Windows Releases
##### Differences from sfan5's build
(changed by EnlivenMinetest project)
* removed Voxelgarden subgame
* added minetest.conf similar to the one generated by ENLIVEN scripts
  for schools vbscript, except with public servers enabled
* added files specific to ENLIVEN, including launcher (ENLIVEN
  application), ENLIVEN subgame (including optional child-friendly
  changes for schools), other files, and licenses of added files.

### Qt
* Qt 5.7.0 files are under the LGPLv3 unless required by licenses in
  qtlicenses folder.
* Sources for Qt 5.7.0 are available via http://www.qt.io
* The following files belong to Qt 5.7.0:
```
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
```

## Developer Notes

### minetest.org build speeds
* Intel i7-4770K
  * libraries ~3m
  * program ~4m

### Regression Tests
* Use of input in python, where should never be used except in
  poikilos.py and minetestinfo.py for first-time setup or when
  `interactive_enable` is `True`

### C++ Debugging
These steps are only needed for debug builds:
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
