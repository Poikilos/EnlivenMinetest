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

-- BELOW is copied from spawners but pyramids is changed to tsm_pyramids
--
-- backwards compatibility
--
-- spawner mummy
minetest.register_alias("tsm_pyramids:spawner_mummy", "spawners:spawners_mummy_spawner_env")
-- minetest.register_alias("tsm_pyramids:mummy_spawner", "spawners:spawners_mummy_spawner_env")
-- spawn egg
minetest.register_alias("tsm_pyramids:spawn_egg", "spawners:mummy")
-- mummy entity
minetest.register_alias("tsm_pyramids:mummy", "spawners:mummy")
-- deco stone 1
minetest.register_alias("tsm_pyramids:deco_stone1", "spawners:deco_stone1")
-- deco stone 2
minetest.register_alias("tsm_pyramids:deco_stone2", "spawners:deco_stone2")
-- deco stone 3
minetest.register_alias("tsm_pyramids:deco_stone3", "spawners:deco_stone3")
-- deco trap
minetest.register_alias("tsm_pyramids:trap", "spawners:trap")
-- deco trap 2
minetest.register_alias("tsm_pyramids:trap_2", "spawners:trap_2")
