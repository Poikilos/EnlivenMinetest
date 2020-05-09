# "Map Generation" Test Documentation
This documentation covers all testing in the category of "mapgen," and
is is based on
[general.md](https://github.com/poikilos/EnlivenMinetest/blob/master/procedures/testing/general.md).

_NOTICE: I originally created the original version of this document (and
the original document that led to creating the article [Minetest's
Scope Issue](https://poikilos.org/minetest-scope-issue), and the
initial version of general.md) for my Software Development II class. I
didn't do it here nor elsewhere before that nor plagiarize._

## Test Design Guide
Setting up an efficient map generation test environment requires
finding a seed that provides a biome providing edible plants near where
grass and water are touching. The tsm_pyramids location must be far
away enough from the starting location and farming locations that
loading the pyramid cannot crash the game during other tests. The
tsm_pyramids test must always come last.


## Test Environment Creation
1. Add "enable_marble_generation = true" to minetest.conf to test
   technic_worldgen fully. Set the gamma to 2.0 to ensure that the
   testers can see in the dark so that ore generation tests proceed
   quickly and hopefully without the need to place torches.
2. Before entering the world, backup the minetest.conf file.
3. Enter as singleplayer and grant singleplayer the noclip, fly, and
   teleport privileges.
4. Add the following to singleplayer’s inventory: 1 stone hoe, 64
   torches.
5. Determine the following locations and provide 3D coordinates for the
   tester: farming ("farming redo"), moreores, tsm_pyramids,
   technic_ores.


## Instructions for Testers
This section is intended to be the only test document that the tester
needs for this or other test categories.

### General instructions:
Proceed to the tests section, use the inputs as the tests describe,
then record the results.

### Inputs:
[Instead of "...", the test documentation must provide coordinates of
each test location.]
- farming: ...
- moreores: ...
- technic_ores: ...
- tsm_pyramids: ...

### Tests:
1. Teleport to the farming location. Ensure that edible plants are there
   and that harvesting them yields produce or seeds.
   - Results: <textarea name="mapgenTest1Result" form="usrform"></textarea>
2. Teleport to the moreores location. Ensure that
   "moreores:mineral_silver" appears within sight range and that
   harvesting it yields ore (not stone with silver)
   (Minetest-mods/moreores, 2020).
   - Results: <textarea name="mapgenTest2Result" form="usrform"></textarea>
3. Teleport to the technic_ores location. Ensure that
   "technic:mineral_lead" appears within site range and that harvesting
   it yields ore (not stone with lead) (Minetest-mods/technic, 2019).
   - Results: <textarea name="mapgenTest3Result" form="usrform"></textarea>
4. Teleport to the tsm_pyramids location. Wait 5 seconds. Ensure that
   the game does not crash. Enter the pyramid. Wait 5 more seconds.
   Ensure that the game does not crash.
  - Results: <textarea name="mapgenTest4Result" form="usrform"></textarea>
