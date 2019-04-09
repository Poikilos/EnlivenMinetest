Minetest mod: teleporter_to_travelnet
==========================================
This Minetest mod provides a transition from "Teleporter Mod" to "travelnet teleporters/bookmarks". If you had a world with any teleporter:teleport_pad (from "Teleporter Mod" by Bad_Command_ https://forum.minetest.net/viewtopic.php?id=2149 ) you can safely remove that mod, then install Sokomine's "travelnet" mod ( https://forum.minetest.net/viewtopic.php?t=4877 ) along with this mod.

However (due to the old metadata and travelnet's ownership scheme), for any teleporter:teleport_pad that existed before this mod (for which purpose this mod was created) users must break it (it will reappear instantly), then they will be allowed to name it and assign a network, then potentially break it again and make the opening face the desired direction.

Multiplayer warning: travelnet does not prevent anyone from changing the owner field and teleporting to someone else's teleporter. Players should be informed of that, so they can have a waiting room with a protected or locked door to the rest of their protected area. This mod has not been tested with locked travelnet, but if it does not, feel free to fork this project on github and try to get it working.

Code: LGPLv2.1, assets: CC BY-SA 3.0 Unported

Mod dependencies: travelnet

Authors of source code
----------------------
poikilos (github.com/poikilos)

Authors of media (textures)
---------------------------
(no media)
