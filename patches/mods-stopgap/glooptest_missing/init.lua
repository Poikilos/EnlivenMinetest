-- mossy stone etc (not cobblestone):
-- if minetest.get_modpath("gloopblocks") == nil then
if not minetest.registered_nodes["gloopblocks:stone_mossy"] then
    minetest.register_alias("gloopblocks:stone_mossy", "default:stone")
    minetest.register_alias("gloopblocks:stone_brick_mossy", "default:stonebrick")
    if minetest.get_modpath("moreblocks") ~= nil then
	minetest.register_alias("gloopblocks:stair_stone_brick_mossy", "moreblocks:stair_stonebrick")
    end
end
