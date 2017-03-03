minetest.override_item("dryplants:reedmace_sapling", {
	drop = {
		max_items = 1,
		items = {
			{items = {'farming:seed_cotton'}, rarity = 8},
			{items = {'dryplants:reedmace_sapling'}},
		}
	},
})

-- formerly only possible using default:junglegrass
minetest.register_craft({
	output = "moreblocks:sweeper 4",
	recipe = {
		{"dryplants:reedmace_sapling"},
		{"default:stick"},
	}
})

-- formerly only possible using default:junglegrass
-- reedmace_height_2, reedmace_sapling, reedmace_height_3_spikes, etc all become reedmace_sapling when mined
minetest.register_craft({
	output = "moreblocks:rope 3",
	recipe = {
		{"dryplants:reedmace_sapling"},
		{"dryplants:reedmace_sapling"},
		{"dryplants:reedmace_sapling"},
	}
})

-- formerly only possible using group:vines
-- if minetest.get_modpath("vines") ~= nil then
minetest.register_craft({
	output = 'vines:rope_block',
	recipe = {
		{'', 'default:wood', ''},
		{'', 'farming:string', ''},
		{'', 'farming:string', ''}
	}
})
-- end