-- ===================================================================
-- Code and media license.
--
-- You may  copy,  use,  modify or do nearly anything  but remove this
-- copyright notice. Of course,  you're not allowed to pretend  you've
-- created or written the Sapier or Poikilos pieces.
--
-- CC-BY-SA 3.0. Attribution: Sapier and Poikilos.

-- ===================================================================

--   Poikilos' distinguish_meats-vs-211114a patch adds this file and
--   conditionally uses it instead of animal_materials.lua in case a
--   user added the animalmaterials mod. This file will add aliases
--   in that case.
--
--   These aliases are only necessary for worlds that had been running
--   older versions of bucket_game. Newer worlds don't need them as
--   long as all code in new versions of bucket_game always use the
--   animalmaterial namespace in all cases (To see if that is done,
--   see [issue #517](https://github.com/poikilos/EnlivenMinetest/issues/517)  )
--
--   -Poikilos

core.log("action","MOD: codermobs is loading animal_materials aliases (to use detected animalmaterials)...")

minetest.register_alias("animal_materials:sword_deamondeath", "animalmaterials:sword_deamondeath")
minetest.register_alias("animal_materials:scissors", "animalmaterials:scissors")
minetest.register_alias("animal_materials:lasso", "animalmaterials:lasso")
minetest.register_alias("animal_materials:net", "animalmaterials:net")
minetest.register_alias("animal_materials:saddle", "animalmaterials:saddle")
minetest.register_alias("animal_materials:contract", "animalmaterials:contract")

local dep_meat_raw = nil
if minetest.registered_items["mobs:meat"] then
    dep_meat_raw = "mobs:meat"
elseif minetest.registered_items["animalmaterials:meat_raw"] then
    dep_meat_raw = "animalmaterials:meat_raw"
end
if not dep_meat_raw then
    minetest.register_alias("animal_materials:meat_raw", "animalmaterials:meat_raw")
else
    minetest.register_alias("animal_materials:meat_raw", dep_meat_raw)
end

local dep_pork_raw = nil
if minetest.registered_items["mobs:pork_raw"] then
    dep_pork_raw = "mobs:pork_raw"
elseif minetest.registered_items["animalmaterials:meat_pork"] then
    dep_pork_raw = "animalmaterials:meat_pork"
end
if not dep_pork_raw then
    minetest.register_alias("animal_materials:pork_raw", "animalmaterials:meat_pork")
    minetest.register_alias("animal_materials:meat_pork", "animalmaterials:meat_pork")
else
    minetest.register_alias("animal_materials:pork_raw", dep_pork_raw)
    minetest.register_alias("animal_materials:meat_pork", dep_pork_raw)
end

minetest.register_alias("animal_materials:meat_beef", "animalmaterials:meat_beef")
minetest.register_alias("animalmaterials:meat_chicken", "animalmaterials:meat_chicken")
minetest.register_alias("animal_materials:meat_lamb", "animalmaterials:meat_lamb")
minetest.register_alias("animal_materials:meat_venison", "animalmaterials:meat_venison")
minetest.register_alias("animal_materials:meat_undead", "animalmaterials:meat_undead")
minetest.register_alias("animal_materials:meat_toxic", "animalmaterials:meat_toxic")
minetest.register_alias("animal_materials:meat_ostrich", "animalmaterials:meat_ostrich")
minetest.register_alias("animal_materials:fish_bluewhite", "animalmaterials:fish_bluewhite")
minetest.register_alias("animal_materials:fish_clownfish", "animalmaterials:fish_clownfish")

minetest.register_alias("animal_materials:feather", "animalmaterials:feather")
minetest.register_alias("animal_materials:milk", "animalmaterials:milk")
minetest.register_alias("animal_materials:egg", "animalmaterials:egg")
minetest.register_alias("animal_materials:egg_big", "animalmaterials:egg_big")
minetest.register_alias("animal_materials:bone", "animalmaterials:")
minetest.register_alias("animal_materials:fur", "animalmaterials:")
minetest.register_alias("animal_materials:fur_deer", "animalmaterials:")
minetest.register_alias("animal_materials:coat_cattle", "animalmaterials:")
minetest.register_alias("animal_materials:antlers", "animalmaterials:deer_horns")
minetest.register_alias("animal_materials:ivory", "animalmaterials:ivory")
minetest.register_alias("animal_materials:scale_golden", "animalmaterials:scale_golden")
minetest.register_alias("animal_materials:scale_white", "animalmaterials:scale_white")
minetest.register_alias("animal_materials:scale_gray", "animalmaterials:scale_gray")
minetest.register_alias("animal_materials:scale_blue", "animalmaterials:scale_blue")

