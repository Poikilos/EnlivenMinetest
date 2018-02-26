minetest.clear_craft({
	output = "homedecor:wine_rack",
})
minetest.clear_craft({
	output = "homedecor:beer_tap",
})

minetest.register_alias("homedecor:beer_tap", "homedecor:coffee_maker")
minetest.register_alias("homedecor:wine_rack", "homedecor:coffee_maker")
-- NOTE: tap transforms vessels:drinking_glass into item below:
minetest.register_alias("homedecor:beer_mug", "vessels:drinking_glass")
--[[
minetest.register_craft({
	output = "homedecor:drink_rack",
	recipe = {
		{ "homedecor:4_bottles_brown", "group:wood", "homedecor:4_bottles_brown" },
		{ "homedecor:4_bottles_brown", "group:wood", "homedecor:4_bottles_brown" },
		{ "homedecor:4_bottles_brown", "group:wood", "homedecor:4_bottles_brown" },
	},
})
minetest.register_alias("homedecor:wine_rack", "homedecor:drink_rack")


minetest.register_craft({
	output = "homedecor:drink_tap",
	recipe = {
		{ "group:stick","default:steel_ingot","group:stick" },
		{ "homedecor:kitchen_faucet","default:steel_ingot","homedecor:kitchen_faucet" },
		{ "default:steel_ingot","default:steel_ingot","default:steel_ingot" }
	},
})
minetest.register_alias("homedecor:beer_tap", "homedecor:drink_tap")
]]--