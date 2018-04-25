-- Copyright 2017 poikilos
-- Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
-- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-- NOTE: register_alias is not needed for mobs, since alias_mob calls that
-- minetest.register_alias(name, convert_to)
-- "This means that if the engine finds nodes with the name name in the world the node with the name convert_to is used instead. "
-- <https://dev.minetest.net/minetest.register_alias>
-- minetest.register_alias("creatures:chicken", "mobs_animal:chicken")
-- minetest.register_alias("creatures:sheep", "mobs_animal:sheep_white")
-- minetest.register_alias("mobs_animal:sheep", "mobs_animal:sheep_white")  -- this is to fix an earlier bug in this mod
-- minetest.register_alias("creatures:ghost", "mobs_monster:spider")
-- minetest.register_alias("creatures:mummy", "spawners_mobs:mummy")
-- minetest.register_alias("creatures:mummy", "mobs_monster:stone_monster")
-- minetest.register_alias("creatures:oerrki", "mobs_monster:oerrki")
-- minetest.register_alias("creatures:zombie", "mobs_monster:stone_monster")

mobs:alias_mob("creatures:chicken", "mobs_animal:chicken")
mobs:alias_mob("creatures:sheep", "mobs_animal:sheep_white")
mobs:alias_mob("mobs_animal:sheep", "mobs_animal:sheep_white")  -- this is to fix an earlier bug in this mod
mobs:alias_mob("creatures:ghost", "mobs_monster:spider")
mobs:alias_mob("creatures:mummy", "spawners_mobs:mummy")
-- minetest.register_alias("creatures:mummy", "mobs_monster:stone_monster")
mobs:alias_mob("creatures:oerrki", "mobs_monster:oerrki")
mobs:alias_mob("creatures:zombie", "mobs_monster:stone_monster")

minetest.register_alias("creatures:chicken_spawner", "spawners_mobs:mobs_chicken_spawner")
minetest.register_alias("creatures:ghost_spawner", "spawners_env:mobs_spider_spawner")
minetest.register_alias("creatures:mummy_spawner", "spawners_mobs:spawners_mobs_mummy_spawner")
minetest.register_alias("creatures:oerrki_spawner", "spawners_mobs:mobs_oerkki_spawner")
minetest.register_alias("creatures:sheep_spawner", "spawners_mobs:mobs_sheep_white_spawner")
minetest.register_alias("creatures:zombie_spawner", "spawners_mobs:mobs_stone_monster_spawner")

-- meat:
minetest.register_alias("creatures:chicken_flesh", "mobs:chicken_raw")
minetest.register_alias("creatures:chicken_meat", "mobs:chicken_cooked")
minetest.register_alias("creatures:rotten_flesh", "")
minetest.register_alias("creatures:grilled_rotten_flesh", "")
minetest.register_alias("creatures:flesh", "mobs:meat_raw")
minetest.register_alias("creatures:meat", "mobs:meat")

-- non-meat food:
minetest.register_alias("creatures:egg", "mobs:egg")
minetest.register_alias("creatures:fried_egg", "mobs:chicken_egg_fried")

-- materials:
minetest.register_alias("creatures:feather", "farming:string")

-- tools:
minetest.register_alias("creatures:shears", "mobs:shears")

-- eggs (there is no true chicken spawner egg item (at least in egg texture) in spawners or mobs, so using regular chicken which works the same (could also use mobs:egg for partial effectiveness) instead):
minetest.register_alias("creatures:chicken_spawn_egg", "mobs_animal:chicken")
minetest.register_alias("creatures:ghost_spawn_egg", "mobs_monster:spider")
minetest.register_alias("creatures:mummy_spawn_egg", "spawners_mobs:mummy")
minetest.register_alias("creatures:oerrki_spawn_egg", "mobs_monster:oerkki")
minetest.register_alias("creatures:sheep_spawn_egg", "mobs:sheep_white")
minetest.register_alias("creatures:zombie_spawn_egg", "mobs_monster:stone_monster")
