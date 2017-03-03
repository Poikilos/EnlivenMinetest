
-- formerly getting cotton seeds only possible 1/8 chance harvesting default:junglegrass
minetest.register_craft({
	output = "moreblocks:sweeper 4",
	recipe = {
		{"default:grass"},
		{"default:stick"},
	}
})

minetest.register_craft({
	output = "farming:seed_cotton",
	type = "shapeless",
	recipe = {
		{"farming:cotton"},
		{"farming:cotton"},
		{"farming:cotton"},
		{"farming:cotton"},
		{"farming:cotton"},
		{"farming:cotton"},
		{"farming:cotton"},
		{"farming:cotton"},
	}
})



-- formerly only possible using default:junglegrass
-- reedmace_height_2, reedmace_sapling, reedmace_height_3_spikes, etc all become reedmace_sapling when mined
minetest.register_craft({
	output = "moreblocks:rope 3",
	recipe = {
		{"default:grass"},
		{"default:grass"},
		{"default:grass"},
	}
})

