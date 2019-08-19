--if minetest.get_modpath("anvil") ~= nil then
if not minetest.registered_nodes["cottages:hammer"] then
    if minetest.registered_nodes["anvil:hammer"] then
	minetest.register_alias("cottages:hammer", "anvil:hammer")
    end
end

if not minetest.registered_nodes["cottages:anvil"] then
    if minetest.registered_nodes["anvil:anvil"] then
	minetest.register_alias("cottages:anvil", "anvil:anvil")
    end
end
