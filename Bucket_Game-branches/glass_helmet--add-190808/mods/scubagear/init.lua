
-- if rawget(_G, "armor") and armor.register_liquid then

armor:register_armor("3d_armor:helmet_glass_scuba", {
	description = S("Glass Scuba Helmet"),
	inventory_image = "3d_armor_inv_helmet_wood.png",
	groups = {armor_head=1, armor_water=1, armor_use=2000},
	armor_groups = {fleshy=5},
	damage_groups = {cracky=3, snappy=2, choppy=3, crumbly=2, level=1},
})
