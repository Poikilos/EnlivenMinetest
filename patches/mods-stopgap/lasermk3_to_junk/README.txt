Minetest mod: lasermk3_to_junk
==========================================
This Minetest mod was created due to protector_drop item duplication being exploited, especially using technic:laser_mk3 since it has instant firing.
You must also remove the line:
	{"3", 21, 650000, 3000},
from near the beginning of technic/tools/mining_laser.lua

Instead of using this mod, one could take all technic:laser_mk3 (and mk2 and mk1 if they duplicated that on your server) then give a chest to everyone who has one or more with ingredients for it:
/give x technic:laser_mk3
/give x technic:blue_energy_crystal
/give x technic:laser_mk2
/give x technic:carbon_steel_ingot 2
/give x default:diamond
/give x default:copper_ingot



Code: LGPLv2.1, assets: CC BY-SA 3.0 Unported

Mod dependencies: slimenodes, technic

Authors of source code
----------------------
poikilos (github.com/poikilos)

Authors of media (textures)
---------------------------
(no media)
