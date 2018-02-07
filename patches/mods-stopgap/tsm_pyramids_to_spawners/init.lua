-- Copyright 2017 expertmm
-- Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
-- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-- minetest.register_alias("name", "convert_to")
-- "This means that if the engine finds nodes with the name name in the world the node with the name convert_to is used instead."
-- from https://dev.minetest.net/minetest.register_alias

-- BELOW is based on all instances of tsm_pyramids: from tsm_pyramids:
-- minetest.register_alias("tsm_pyramids:spawner_mummy", "pyramids:spawner_mummy")
-- minetest.register_alias("tsm_pyramids:spawn_egg", "pyramids:spawn_egg")
-- minetest.register_alias("tsm_pyramids:mummy", "pyramids:mummy")
-- minetest.register_alias("tsm_pyramids:mummy_spawner", "pyramids:mummy_spawner")
-- minetest.register_alias("tsm_pyramids:trap", "pyramids:trap")
-- minetest.register_alias("tsm_pyramids:trap_2", "pyramids:trap_2")
-- minetest.register_alias("tsm_pyramids:deco_stone1", "pyramids:deco_stone1")
-- minetest.register_alias("tsm_pyramids:deco_stone2", "pyramids:deco_stone2")
-- minetest.register_alias("tsm_pyramids:deco_stone3", "pyramids:deco_stone3")
-- minetest.register_alias("tsm_pyramids:spawner_mummy", "pyramids:spawner_mummy")

-- BELOW is found from instances of pyramids: in spawners:
-- minetest.register_alias("pyramids:spawn_egg", "tsm_pyramids:spawn_egg")
-- minetest.register_alias("pyramids:deco_stone1", "tsm_pyramids:deco_stone1")
-- minetest.register_alias("pyramids:deco_stone2", "tsm_pyramids:deco_stone2")
-- minetest.register_alias("pyramids:deco_stone3", "tsm_pyramids:deco_stone3")
-- minetest.register_alias("pyramids:trap", "tsm_pyramids:trap")
-- minetest.register_alias("pyramids:trap_2", "tsm_pyramids:trap_2")

-- BELOW uses the backwards compatibility from spawners but pyramids is changed to tsm_pyramids
--
-- backwards compatibility
--
-- spawner mummy
minetest.register_alias("tsm_pyramids:spawner_mummy", "spawners_mobs:spawners_mobs_mummy_spawner")
-- minetest.register_alias("tsm_pyramids:mummy_spawner", "spawners:spawners_mummy_spawner_env")
-- spawn egg
minetest.register_alias("tsm_pyramids:spawn_egg", "spawners_mobs:mummy")
-- mummy entity
minetest.register_alias("tsm_pyramids:mummy", "spawners_mobs:mummy")
-- deco stone 1
minetest.register_alias("tsm_pyramids:deco_stone1", "spawners_mobs:deco_stone_bird")
-- deco stone 2
minetest.register_alias("tsm_pyramids:deco_stone2", "spawners_mobs:deco_stone_eye")
-- deco stone 3
minetest.register_alias("tsm_pyramids:deco_stone3", "spawners_mobs:deco_stone_men")
-- deco trap
minetest.register_alias("tsm_pyramids:trap", "moreblocks:trap_sandstone")
-- deco trap 2
minetest.register_alias("tsm_pyramids:trap_2", "moreblocks:trap_desert_stone")
