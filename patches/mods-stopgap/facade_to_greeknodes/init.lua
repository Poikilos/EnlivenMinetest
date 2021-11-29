-- NOTE: register_alias is not needed for mobs, since alias_mob calls that
-- minetest.register_alias(name, convert_to)
-- "This means that if the engine finds nodes with the name name in the world the node with the name convert_to is used instead. "
-- <https://dev.minetest.net/minetest.register_alias>
minetest.register_alias("facade:block_column", "greeknodes:pillar")

-- TODO: finish this.
