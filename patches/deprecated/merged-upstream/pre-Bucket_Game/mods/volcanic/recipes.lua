local glue_fullname = nil

if mesecons_materials then
	glue_fullname = "mesecons_materials:glue"
elseif technic then
	glue_fullname = "technic:glue"
end
if glue_fullname then
	minetest.register_craft({
		type = "shapeless",
		output = "volcanic:bucket_crusted_lava",
		recipe = {"bucket:bucket_lava", glue_fullname},
	})
end
