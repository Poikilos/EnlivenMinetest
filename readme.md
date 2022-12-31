# EnlivenMinetest
by [Poikilos](https://github.com/Poikilos)

ENLIVEN is a subgame for minetest with the goals of providing
immersion and lessons for humanity.

ENLIVEN is a work in progress, but the goals are:
- Immersion: Create an experience where UI and UX are intuitive so that
  they don't distract from storytelling or in other cases the "feeling"
  (such as survival or creativity).
- [Ramping](https://poikilos.org/2019/08/17/ramping-in-sandbox-games/):
  What is done so far includes making minor changes to mods to make
  a clear techtree that can't be short-circuited in "cheap" (both
  economically and in terms of fairness) ways. There is more work to be
  done here.
- Better combat: Not much is done here yet other than mod integration
  and some minor tweaks and workarounds. There are many very specific
  changes that would improve "immersion" and "ramping" of combat as
  those terms are defined above. The biggest challenge has been
  breaking down the problem into concrete and specific issues that can
  actually be solved, rather than a general feeling of being "not
  immersive" or not having "ramping". For progress on this process of
  identifying and solving combat issues, see:
  [Improve Mob Behaviors, AI, Combat, Pathing a.k.a. Pathfinding](https://github.com/Poikilos/EnlivenMinetest/issues/64).

The [EnlivenMinetest project](https://github.com/Poikilos/EnlivenMinetest)
(a.k.a. ENLIVEN project) includes tools for installing, building, and
maintaining (such as developer scripts) the ENLIVEN and Minetest
(engine) itself.

The official game server (world) is called **center** (or "Center of
the Sun"). The address and port for that and other worlds are listed at
[minetest.io](https://minetest.io).

To better understand what the issue board covers, see
[Project Status](#project-status) below.

For notes on current development discussions, see the
"[Work in Progress](#work-in-progress)" section.


## Compatibility
If you build ENLIVEN yourself, you may be able to get it working with
several versions of Minetest but probably not ones from the .net site.
Bucket_Game from minetest.org is now the basis, so Final Minetest and
Finetest (and probably MultiCraft 2 on which Finetest is based) are the
targets for game compatibility.
- See also: "Why not make it compatible with..." under [Frequently Asked Questions](#frequently-asked-questions).

## Frequently Asked Questions

**Q**: What is included?

**A**: The installer includes the Minetest engine, the ENLIVEN "game"
(Lua mods) and configuration file(s). ENLIVEN tries to emphasize
Minetest as an engine, whereas ENLIVEN is the game. One way this
approach improves the user experience is that ENLIVEN includes
minetest.conf settings that should probably be default. For example,
tone mapping and other graphical improvements that are basically
universal to gaming and intuitively expected (such as is clear from
vision biology in the case of tone mapping).
* See also overrides/worlds/CenterOfTheSun/world.conf

**Q**: "Why not make it compatible with versions from the .net site to get [feature x]?"

**A**: The Minetest 5 (.net site) core devs have decided to reduce
compatibility and be the tail wagging the dog, not the many people who
enjoy or used to enjoy making mods and games. If you want to be
associated with that team, you are free to use their software. This
project is for single player and people who want to play games with our
community at [minetest.io](https://minetest.io/) and the Final Minetest
engine community [minetest.org](https://minetest.org/). MultiCraft (and
hence Finetest) aimed for dual compatibility with MT4 and MT5 but
successive versions of 5.x even hindered that (as predicted here) by
breaking mod (and network protocol) compatibility multiple times. It
doesn't just harm dozens or perhaps hundreds of mods, but also harms
and increases development and maintenance cost for the many copies of
those mods in games, and for the many copies of those games on servers
and those for single-player use. When the API is changed, the problem
isn't in x number of mods, it is in that times the number of games,
times the number of servers (often customized further), and all of
those innumerable people have to make up for the tail trying to wag the
dog, or all that work simply gets discarded if they are unavailable or
unwilling to make up for it and perform all of that work that is
redundant (or doubly redundant in the case of servers). See also:
- [Minetest's Scope Issue](https://poikilos.org/2020/05/09/minetest-scope-issue/)
- [Ramping in Sandbox Games](https://poikilos.org/2019/08/17/ramping-in-sandbox-games/)
- [Use animalmaterials and basic_materials for Minetest mods: low-level dependencies for better architecture](https://poikilos.org/2022/05/04/use-animalmaterials-and-basic_materials-for-minetest-mods-low-level-dependencies-for-better-architecture/)
- and comments related to API stability at [A Technical Explanation of the Minetest.org and Minetest.net Split](https://poikilos.org/2019/05/06/minetest-org-and-minetest-net-split/)


## Related Projects
- https://github.com/Poikilos/b3view: My fork of b3view is required to use the utilities/blender/count_objects.py script.

The following subprojects were moved to other repos for clarity and better git practices:
- https://github.com/Poikilos/node-enliven-minetest: deferred, core feature replaced by in-game skin changing; uploading new skins may be re-added, but with a moderator approval system.
- https://github.com/Hierosoft/hierosoft (WIP Minetest "launcher" backend)
  - replaces deprecated https://github.com/Poikilos/launch-enliven
- https://github.com/Poikilos/mtanalyze
  - mostly used for upgrading run-in-place installs of any Minetest version, but has some WIP code for live maps that should be upgraded to work with Leaflet.js or replaced by MTSatellite.
  - also has some code for editing conf files using Python
    - This part will be moved to https://github.com/Poikilos/voxboxor


## Project Status
The [Issues](https://github.com/Poikilos/EnlivenMinetest/issues) page
of the repo's web interface is used to track issues in ENLIVEN, the
Center of the Sun server that uses it, Bucket_Game on which it is
based, and Final Minetest which runs it. In many cases the issues are
upstream and fixes can lead to pull requests, or resolve issues that
are ignored or tagged as `wontfix` upstream. In several cases the
upstream mod related to the issue is no longer maintained or only works
with backward compatibility present in Final Minetest or MultiCraft2
code.

However, this project has led to upstream improvements.

Several patches here have been accepted to upstream mods, such as:
- https://github.com/minetest/minetest_game/pull/2082
- https://notabug.org/TenPlus1/farming/pulls/11
- https://github.com/D00Med/vehicles/pull/62#issuecomment-1368081408
- https://github.com/minetest-mods/ts_furniture/pull/6
- https://github.com/minetest-mobs-mods/dmobs/pull/4
- https://github.com/minetest-mods/loot/pull/2
- https://github.com/Napiophelios/LapisLazuli/pull/4
- https://github.com/Kilarin/compassgps/pull/16
- https://github.com/minetest-mods/hbsprint/pull/11
- https://github.com/minetest-mods/technic/pull/318
 
or proposed such as:
- https://github.com/Poikilos/animalmaterials/blob/master/readme.md

or rejected for unspecified reasons :), such as:
- https://notabug.org/TenPlus1/mobs_monster/issues/1
- https://github.com/minetest-mods/unified_inventory/issues/187#issuecomment-1300311311
- redcrab issue #1 deleted by rubenwardy :( [missing license](https://github.com/rubenwardy/redcrab/issues/1)
- https://github.com/Skandarella/animalworld/pull/7

or I'm uncredited for unspecified reasons :), such as:
- https://notabug.org/TenPlus1/pie/commits/master/textures/pie_inv.png
  - fixes https://notabug.org/TenPlus1/pie/issues/1

In some cases I may use maintained versions of unmaintained mods or ones where I have differences of direction such as:
- https://github.com/Poikilos/slimenodes
- https://github.com/Poikilos/prestibags
- https://github.com/Poikilos/mobs_sky
- https://github.com/Poikilos/metatools
- https://github.com/Poikilos/orichalcum
- https://github.com/Poikilos/throwing
- https://github.com/Poikilos/throwing_arrows
- https://github.com/Poikilos/titanium
- https://github.com/Poikilos/vines (still not working for me, forked or not, on any version of Minetest)
- https://github.com/Poikilos/compassgps
- https://github.com/Poikilos/whinny (mostly for Bucket_Game)
- https://github.com/Poikilos/travelnet -- see:
  - https://github.com/Sokomine/travelnet/pull/45
  - https://github.com/Sokomine/travelnet/pull/46
  - https://github.com/Sokomine/travelnet/pull/47
- https://github.com/Poikilos/birthstones
- https://github.com/Poikilos/xtraarmor
- https://github.com/Poikilos/tsm_pyramids (mostly for Bucket_Game)
- https://github.com/Poikilos/ts_furniture
- https://github.com/Poikilos/filter (@MoNTE48 proposed it to comission me, but though it was exactly to his specifications it had ~547 lines instead of 500 so he rejected it :clown_face: )
- https://github.com/Poikilos/loot
- https://github.com/Poikilos/nether (provides nodes separately from the realm--See  [Use animalmaterials and basic_materials for Minetest mods: low-level dependencies for better architecture](https://poikilos.org/2022/05/04/use-animalmaterials-and-basic_materials-for-minetest-mods-low-level-dependencies-for-better-architecture/))
- https://github.com/Poikilos/hbsprint (WIP)
- https://github.com/Poikilos/bushes_soil (for multiplayer balancing)
- https://github.com/Poikilos/emeralds (mostly for Bucket_Game)
- https://github.com/Poikilos/camera (WIP)
- https://github.com/Poikilos/homedecor_ua (for schools, so teachers don't get in trouble for game content :) )
- and several improvements in [Bucket_Game-branches](Bucket_Game-branches) folder

Or new mods, such as:
- https://github.com/Poikilos/trmp_minetest_game
- and several mods that assist with transition between mods in the 

You can apply whatever patches here you want (if applicable), but they
are already in ENLIVEN (at least if you build it, otherwise the old
installer may not have the latest changes). Most of the patches are
also in Bucket_Game. The newest build script uses Bucket_Game as a
content database. It has specific goals that make it small (such as in
node definition count) in comparison to Bucket_Game.

### Planned Features
There are several improvements I may implement in new or existing mods.
See the [Issues](https://github.com/Poikilos/EnlivenMinetest/issues)
section of the GitHub project.
* See also install-ENLIVEN-minetest_game.sh for a full list of mods from
  the old ENLIVEN that will probably be added to the new ENLIVEN which
  is based on Bucket_Game (many of the mods are already present because
  they are in Bucket_Game!)
* Issues not yet added to the GitHub project's Issues are at [Minetest
  Kanboard](https://poikilos.dyndns.org/kanboard/?controller=BoardViewController&action=readonly&token=f214530d2f1294d90279631ce66b2e8b8569c6f15faf3773086476158bc8)

#### Planned Removals
Disable or remove these Bucket_Game mods/features potentially (not matching theme):
- codermobs gems (see codermobs_gem_*.png such as codermobs_gem_fire.png)
- lmb_blocks
- mychisel


## DISCLAIMERS
* Please read the Sources and License section of this document. You must
  agree to the licenses mentioned in order to use and copy this program.
* Any script code related to redis has not been successfully tested.
* https://github.com/Poikilos/EnlivenMinetest/issues/594


## Building Minetest
This project is mostly for building ENLIVEN, but there are some scripts
here to help build the engine as well: See [doc/building-minetest.md](doc/building-minetest.md).


## Configuration Files
(configuring the build of ELIVEN [the mod set only, not binaries])
You can place zero or more of the following variables in
$HOME/.config/EnlivenMinetest/scripting.rc:
```
CUSTOM_SCRIPTS_PATH
MT_POST_INSTALL_SCRIPT_2  # relative to CUSTOM_SCRIPTS_PATH
REPO_PATH  # Set this if your copy of the repo is not ~/git/EnlivenMinetest
ENABLE_CLIENT  # =true if you want install-mts.sh to install the client.
```
- If ~/minetest/bin/minetest is present, that has the same effect as
  `ENABLE_CLIENT=true`.

You can place a script called mts.sh in your home (or
CUSTOM_SCRIPTS_PATH) directory to run it after install (you can put
archive-minetestserver-debug.sh there too to run first). A suggested use
is to put a line in mts.sh that starts the server, so that the server
starts after the installation or upgrade is complete.


## How to use

### Windows Client
Click "Releases" for the installer, which has the singleplayer and
multiplayer client for ENLIVEN.
* You must install to C:\Games\ENLIVEN (or possibly other path without
  spaces, as long as you don't move the launcher) in order for ENLIVEN
  to run.

### Server

For Linux servers, place the "ENLIVEN" directory from "Releases" into
your "games" directory in minetest if you have a run-in-place version.
If not, place it in ~/.minetest/games/. For what Minetest versions are
compatible, see the first part of this document.

#### Customization
* The farming plugin is overwritten with farming redo in the
  minetest_game based install script. Bucket_Game already has something
  good, apparently based on farming redo.
* Before using anything in the `change_world_name_manually_first` and
  its subfolders, change the values of the variables in the folder name
  as noted before using.
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


## Naming conventions
* The filenames without extensions
* The abbreviation "mts" is for minetest server-specific scripts or
  variables
* du-show-big searches your hard drive for big files, in case
  $HOME/.minetest/debug.txt fills your drive, or a log rotate utility
  fails (going into a cumulative copy loop, or not) in regard to
  debug.txt, filling up your drive
* The network folder contains some stuff for networks, which is usually
  only useful for using Minetest on a managed LAN such as a network
  cafe or school.
  - The purpose of minetest_userscript_localENLIVEN_server_only.vbs is
    to make sure the user only uses the hostname localENLIVEN, however
    this only changes the default, and cannot be enforced in any way as
    far as I know without recompiling the client.


## Changes
See [changelog.md](changelog.md).


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


## Sources and License
Authors: poikilos (Jake Gustafson)
ENLIVEN project (aka EnlivenMinetest), including launcher (ENLIVEN
application) and ENLIVEN subgame, is released under the LGPL v2.1
license (see LICENSE), except media which is released under the CC BY-SA
3.0 license (see LICENSE). There are other exceptions to this license
and authorship where specified below and in subfolders.
Source code is available at
[https://github.com/Poikilos/EnlivenMinetest](https://github.com/Poikilos/EnlivenMinetest).

### Additional Media

#### subgame icon
- by erlehmann and Poikilos
- Attribution-ShareAlike 3.0 Unported
  ([CC BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/))
- based on minetest/misc/minetest.svg by erlehmann

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

## Development
For future plans and how you can contribute or build the game (Lua) or package (Lua+engine+conf) see [doc/development.md](doc/development.md) and [issues](https://github.com/Poikilos/EnlivenMinetest/issues).

### Work in Progress
This section is a temporary dev discussion record for the purpose of tracking meta (issues about issues). In other words, this section has version-specific points that clarify reasoning such as prioritization, difficulty, or impact of issues or solutions. It may clarify why some issues are undecided, need feedback, are lowered in priority (such as via "Bucket_Game-future", "non-trivial"), etc.

On 1/14/22 3:13 AM, Robert Kiraly wrote:
(except changed 0 to # so GitHub creates links to issue pages)

> #497 RJK could fix this but he has questions. TBD.
> #498 RJK could fix this but he has questions. TBD.

> #510 Poikilos needs to review next snapshot first
> #511 Poikilos needs to review next snapshot first
> #512 Doable but TBD

> #516 Poikilos needs to review next snapshot first

> #523 Q. Oily Patch: Can you put the patch in the ENI?

[see next e-mail below]

> #530 Q. Is the fix to modify the images or the models?

Modifying the models would be complicated. They were never designed to align with the pixels on different resolutions. This may require lots of model editing or image editing to use mobile-sized textures. The problem is that even if you make some edges right, the pixel, at a low res, may be shared with another face. We could try reverting to the old higher resolution then upscaling instead of downscaling and see if the pixels line up, and if not then hand editing would work since there would be enough pixels that they aren't used twice on more than one polygon. I can try it.


On 1/22/22 3:21 AM, Robert Kiraly wrote:

(except added # so GitHub creates links to issue pages)

>
> * ENI #486 Dye shapes:
>
> So, this is a simple incorrect-images issue. I'd thought that it might be the dingy-colors issue.
>
> Poikilos said: The actual images are in bucket_game/mods/codercore/dye/textures and either aren't all used by the dye mod code or unifieddyes reverts them to its image. The latter is probably the case. It is probably best to revert the images there to the ones in the dye mod in..."
>
> I follow that we can just change the images. However, I'm not certain of what "there" refers to. I assume that you mean "unifieddyes". Are you able to provide a patch?

`<Poikilos>` there: bucket_game/mods/codercore/dye/textures

`<Poikilos>` I'll provide a patch. A good compromise would be to to some resizing and editing to make a better dye pile rather than reverting the nice bowls to the 16x16 MTG dye piles. The patch would also have to cover unifieddyes since that seems to override some of them since they aren't uniform. In any case, dye and unifieddyes images should be uniform anyway.

> * ENI #487 Revert a change:
>
> Are you able to provide a patch relative to the latest snapshot that does the revert?

`<Poikilos>` Ok can do.




Issues where discussion was requested by RJK:
- #500

Issues where discussion was requested by Poikilos:
- #517 (see discussion below):

On 1/10/22 6:31 PM, Jake Gustafson wrote:
> > `<OldCoder>` 0517 Animal Materials: Should we just factor the mod out?
>
> Factoring it out would be like factoring out default or basic_materials. Factoring it out would make several mods much more complex to maintain. Such mods exist for good reasons: See my comments at the two links ...

1. #517
2. [readme.md](https://github.com/Poikilos/animalmaterials/blob/master/readme.md) in https://github.com/Poikilos/animalmaterials.git

Issues deferred pending a previous issue but ready to address:

On 1/10/22 6:31 PM, Jake Gustafson wrote:
>> `<OldCoder>` 0510 Animal materials
>> `<OldCoder>` 0511 Meat
>> `<OldCoder>` 0516 Meat
> `<Poikilos>` 510-511 & 516: I'm waiting on incremental change so I don't desync from you (same reasons as under 0508 above, including my suggestion to add animalmaterials).


Issues deferred pending a current issue:
- #508 (requires a decision on #517)

See also:
- [Planning](doc/development.md#planning) in doc/development.md.

#### copypasta
(This section provides out-of-context copypasta lines that have no meaning relevant to this document except to prevent retyping them over and over)
```
This is resolved in bucket_game snapshot 220114.
```
