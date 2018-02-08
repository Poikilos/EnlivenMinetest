-- Copyright 2017 expertmm
-- Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
-- The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
-- THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

-- NOTE: register_alias is not needed for mobs, since alias_mob calls that
-- minetest.register_alias(name, convert_to)
-- "This means that if the engine finds nodes with the name name in the world the node with the name convert_to is used instead. "
-- <https://dev.minetest.net/minetest.register_alias>

mobs:alias_mob("spawners:mummy", "spawners_mobs:mummy")
mobs:alias_mob("spawners:bunny_evil", "spawners_mobs:bunny_evil")
mobs:alias_mob("spawners:uruk_hai", "spawners_mobs:uruk_hai")
minetest.register_alias("spawners:spawners_mummy_spawner_env", "spawners_mobs:spawners_mobs_mummy_spawner")
-- matched 1,2,3 with eye,men,sun by looking at old non-modpack version:
minetest.register_alias("spawners:deco_stone1", "spawners_mobs:deco_stone_eye")
minetest.register_alias("spawners:deco_stone2", "spawners_mobs:deco_stone_men")
minetest.register_alias("spawners:deco_stone3", "spawners_mobs:deco_stone_sun")
minetest.register_alias("spawners:trap", "moreblocks:trap_sandstone")
minetest.register_alias("spawners:trap_2", "moreblocks:trap_sandstone")

