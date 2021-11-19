
--   Poikilos' distinguish_meats-vs-211114a patch adds this file.
--   The purpose of this file is to add recipes that are not in
--   the cooking mod in the animalmaterials modpack, nor probably.
--   anywhere else.
--   Any meats without a specific cooked version (craftitem) can
--   go here, but only use register_mystery_meat if the item would
--   look like a leg roast after cooked.
--   If the cooking mod is not present, more such cooking recipes
--   are added as well.

local register_mystery_meat = function (meat_name)
  -- This function ensures that the item can be cooked to
  -- a generic meat that looks like a leg roast.
  -- Therefore, only call this for raw craftitems that look
  -- like that visually and don't have a specifically
  -- related cooked meat craftitem.
  -- This function only works when there is a cooking recipe
  -- to produced generic cooked meat from group:food_meat_raw
  -- (The recipe is already present in bucket_game 211114a
  -- or earlier).
  minetest.override_item(meat_name, {
      groups = { meat=1, eatable=1, food_meat_raw = 1 },
  })
  return true
end

local am_namespace = "animal_materials"

if minetest.get_modpath("animalmaterials") then
    am_namespace = "animalmaterials"
end

register_mystery_meat(am_namespace..":meat_lamb")

-- register_mystery_meat(am_namespace..":meat_ostrich")
-- ^ commented since ostrich.lua registers a specific
--   meat & recipe

-- if not minetest.get_modpath("cooking") then
-- ^ commented for reason below:
-- Add the groups even if cooking is present, because
-- bucket_game uses the food_meat_raw group for more
-- recipes other than cooking recipes:
register_mystery_meat(am_namespace..":meat_beef")
register_mystery_meat(am_namespace..":meat_venison")
-- end

-- Note that the following recipes not in animalmaterials:cooking are
-- also not done in this file (reason in parenthesis):
-- - egg, egg_big
--   (since recipes for them have to be registered in
--   the mod that defines the fried eggs--or in a mod that
--   depends on that mod--and there is no large fried egg though
--   distinguish_meats-vs-211114a adds a texture for it (a
--   different texture file than the patch's cooked ostrich egg)).
-- - fish_clownfish, fish_bluewhite
--   (since recipes for them have to be registered in the mod that
--   defines codersea:cookedfish--or in a mod that depends on that
--   mod)
