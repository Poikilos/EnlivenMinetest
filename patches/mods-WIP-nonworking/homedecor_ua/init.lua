local modpath = minetest.get_modpath("homedecor_ua")
homedecor_ua = {}
dofile(modpath.."/handlers/init.lua")

local S = homedecor_i18n.gettext
local wine_cbox = homedecor.nodebox.slab_z(-0.75)
minetest.clear_craft({
	output = "homedecor:wine_rack",
})
minetest.clear_craft({
	output = "homedecor:beer_tap",
})


-- minetest.register_alias("homedecor:beer_tap", "homedecor:coffee_maker")
-- minetest.register_alias("homedecor:wine_rack", "homedecor:coffee_maker")
-- NOTE: tap transforms vessels:drinking_glass into item below (on right-click):
-- minetest.register_alias("homedecor:beer_mug", "vessels:drinking_glass")
homedecor_ua.register("drink_rack", {
	description = S("Drink rack"),
	mesh = "homedecor_wine_rack.obj",
	tiles = {
		"homedecor_generic_wood_red.png",
		"homedecor_bottle_brown.png",
		"homedecor_bottle_brown2.png",
		"homedecor_bottle_brown3.png",
		"homedecor_bottle_brown4.png"
	},
	inventory_image = "homedecor_wine_rack_inv.png",
	groups = {choppy=2},
	selection_box = wine_cbox,
	collision_box = wine_cbox,
	sounds = default.node_sound_defaults(),
})
minetest.register_alias("homedecor:wine_rack", "homedecor_ua:drink_rack")

homedecor_ua.register("drink_tap", {
	description = S("drink tap"),
	mesh = "homedecor_beer_taps.obj",
	tiles = {
		"homedecor_generic_metal_bright.png",
		{ name = "homedecor_generic_metal.png", color = homedecor.color_black }
	},
	inventory_image = "homedecor_beertap_inv.png",
	groups = { snappy=3 },
	walkable = false,
	selection_box = {
		type = "fixed",
		fixed = { -0.25, -0.5, -0.4375, 0.25, 0.235, 0 }
	},
	on_rightclick = function(pos, node, clicker, itemstack, pointed_thing)
		local inv = clicker:get_inventory()

		local wieldname = itemstack:get_name()
		if wieldname == "vessels:drinking_glass" then
			if inv:room_for_item("main", "homedecor:drink_mug 1") then
				itemstack:take_item()
				clicker:set_wielded_item(itemstack)
				inv:add_item("main", "homedecor:drink_mug 1")
				minetest.chat_send_player(clicker:get_player_name(),
						S("Ahh, a nice cold drink - look in your inventory for it!"))
			else
				minetest.chat_send_player(clicker:get_player_name(),
						S("No room in your inventory to add a drink mug!"))
			end
		end
	end
})
minetest.register_alias("homedecor:beer_tap", "homedecor_ua:drink_tap")


homedecor_ua.register("drink_mug", {
	description = S("Drink mug"),
	drawtype = "mesh",
	mesh = "homedecor_beer_mug.obj",
	tiles = { "homedecor_ua_drink_mug.png" },
	inventory_image = "homedecor_ua_drink_mug_inv.png",
	groups = { snappy=3, oddly_breakable_by_hand=3 },
	walkable = false,
	sounds = default.node_sound_glass_defaults(),
	selection_box = beer_cbox,
	on_use = function(itemstack, user, pointed_thing)
		local inv = user:get_inventory()
		if not creative.is_enabled_for(user:get_player_name()) then
			if inv:room_for_item("main", "vessels:drinking_glass 1") then
				inv:add_item("main", "vessels:drinking_glass 1")
			else
				local pos = user:get_pos()
				local dir = user:get_look_dir()
				local fdir = minetest.dir_to_facedir(dir)
				local pos_fwd = {	x = pos.x + homedecor.fdir_to_fwd[fdir+1][1],
									y = pos.y + 1,
									z = pos.z + homedecor.fdir_to_fwd[fdir+1][2] }
				minetest.add_item(pos_fwd, "vessels:drinking_glass 1")
			end
			minetest.do_item_eat(2, nil, itemstack, user, pointed_thing)
			return itemstack
		end
	end
})
minetest.register_alias("homedecor:beer_mug", "homedecor_ua:drink_mug")

--[[minetest.register_craft({
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