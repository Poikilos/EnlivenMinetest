# Mock TNT
Mod for Minetest

## Usage
* Place in mods folder such as in your subgame
* "Unknown Explosive" (mock_tnt:mock_tnt) can coexist with TNT if TNT is enabled, but gunpowder and mock_tnt work even if enable_tnt is false.

## Differences from regular TNT
* Does not harm any block or entity

## Known Issues
* also ignite gunpowder with "default:torch", "fire:permanent_flame" (minetest_game only ignites via "fire:basic_flame", "default:lava_source", "default:lava_flowing") -- for some reason torch works already but permanent_flame does not
* Make gunpowder ignite via "building_blocks:Fireplace"
* Make TNT ignite via neighbors "throwing:arrow_fireworks_blue", "throwing:arrow_fireworks_red"
* Make "fire:flint_and_steel" item ignite TNT and gunpowder