-- NOTE: register_alias is not needed for mobs, since alias_mob calls that
-- minetest.register_alias(name, convert_to)
-- "This means that if the engine finds nodes with the name name in the world the node with the name convert_to is used instead. "
-- <https://dev.minetest.net/minetest.register_alias>

minetest.register_alias("nftools:alexandrite_ore", "nftools:stone_with_bismuth")
minetest.register_alias("nftools:alexandrite", "nftools:bismuth")

minetest.register_alias("nftools:amber", "nftools:stone_with_amber")
-- (formerly called amber but dropped chip; use conventions instead)

minetest.register_alias("nftools:aquamarine_ore", "nftools:stone_with_turquoise")
minetest.register_alias("nftools:aquamarine", "nftools:turquoise")


-- minetest.register_alias("nftools:amethyst_ore", "nftools:stone_with_blackopal")  -- merged with Bucket_Game
minetest.register_alias("nftools:amethyst", "nftools:blackopal")
