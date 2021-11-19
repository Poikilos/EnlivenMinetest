-- ===================================================================
-- Code and media license.
--
-- You may  copy,  use,  modify or do nearly anything  but remove this
-- copyright notice. Of course,  you're not allowed to pretend  you've
-- created or written the Sapier or Poikilos pieces.
--
-- CC-BY-SA 3.0. Attribution: Sapier and Poikilos.

-- ===================================================================

-- Boilerplate to support localized strings if intllib mod is install-
-- ed.

local S
if (minetest.get_modpath("intllib")) then
  dofile(minetest.get_modpath("intllib").."/intllib.lua")
  S = intllib.Getter(minetest.get_current_modname())
else
  S = function ( s ) return s end
end

core.log("action","MOD: codermobs integrated animal_materials loading ...")
local version = "0.1.3"

animal_materialsdata = {}

-- ===================================================================
-- Node definitions

-- ===================================================================
-- Item definitions

-- ===================================================================
-- deamondeath sword

minetest.register_tool(":animal_materials:sword_deamondeath", {
    description = S("Sword (Deamondeath)"),
    inventory_image = "default_tool_steelsword.png",
    tool_capabilities = {
        full_punch_interval = 0.50,
        max_drop_level=1,
        groupcaps={
            fleshy={times={[1]=2.00, [2]=0.80, [3]=0.40}, uses=10, maxlevel=1},
            snappy={times={[2]=0.70, [3]=0.30}, uses=40, maxlevel=1},
            choppy={times={[3]=0.70}, uses=40, maxlevel=0},
            deamon={times={[1]=0.25, [2]=0.10, [3]=0.05}, uses=20, maxlevel=3},
        }
    }
    })

-- ===================================================================
-- scissors
--

minetest.register_tool(":animal_materials:scissors", {
    description = S("Scissors"),
    inventory_image = "animal_materials_scissors.png",
    tool_capabilities = {
        max_drop_level=0,
        groupcaps={
            wool  = {uses=40,maxlevel=1}
        }
    },
})

-- ===================================================================
-- lasso

minetest.register_craftitem(":animal_materials:lasso", {
    description = S("Lasso"),
    image = "animal_materials_lasso.png",
    stack_max=10,
})

-- ===================================================================
-- net

minetest.register_craftitem(":animal_materials:net", {
    description = S("Net"),
    image = "animal_materials_net.png",
    stack_max=10,
})

-- ===================================================================
-- saddle

minetest.register_craftitem(":animal_materials:saddle", {
    description = S("Saddle"),
    image = "animal_materials_saddle.png",
    stack_max=1
})

-- ===================================================================
-- contract

minetest.register_craftitem(":animal_materials:contract", {
    description = S("Contract"),
    image = "animal_materials_contract.png",
    stack_max=10,
})

-- ===================================================================
-- meat

local dep_meat_raw = nil
if minetest.registered_items["mobs:meat"] then
    dep_meat_raw = "mobs:meat"
elseif minetest.registered_items["animalmaterials:meat"] then
    dep_meat_raw = "animalmaterials:meat"
end

if not dep_meat_raw then
    minetest.register_craftitem(":animal_materials:meat_raw", {
        description = S("Raw Meat"),
        image = "animal_materials_meat_raw.png",
        on_use = minetest.item_eat(1),
        groups = { meat=1, eatable=1 },
        stack_max=25
    })
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
    minetest.register_craftitem(":animal_materials:meat_pork", {
        description = S("Raw Pork"),
        image = "codermobs_pork_raw.png",
        on_use = minetest.item_eat(1),
        groups = { meat=1, eatable=1 },
        stack_max=25
    })

    minetest.register_alias("animal_materials:pork_raw", "animal_materials:meat_pork")
else
    minetest.register_alias("animal_materials:pork_raw", dep_pork_raw)
    minetest.register_alias("animal_materials:meat_pork", dep_pork_raw)
end

local dep_beef_raw = nil
if minetest.registered_items["animalmaterials:meat_beef"] then
    dep_beef_raw = "animalmaterials:meat_beef"
end
if not dep_beef_raw then
    minetest.register_craftitem(":animal_materials:meat_beef", {
        description = S("Raw Beef"),
        image = "codermobs_beef_raw.png",
        on_use = minetest.item_eat(1),
        groups = { meat=1, eatable=1 },
        stack_max=25
    })
else
    minetest.register_alias("animal_materials:meat_beef", dep_beef_raw)
end

local dep_chicken_raw = nil
if minetest.registered_items["animalmaterials:meat_chicken"] then
    dep_chicken_raw = "animalmaterials:meat_chicken"
end

if not dep_chicken_raw then
    minetest.register_craftitem(":animal_materials:meat_chicken", {
        description = S("Raw Chicken"),
        image = "codermobs_chicken_raw.png",
        on_use = minetest.item_eat(1),
        groups = { meat=1, eatable=1 },
        stack_max=25
    })
else
    minetest.register_alias("animalmaterials:meat_chicken", dep_chicken_raw)
    -- ^ The alias is only necessary for older versions of bucket_game--
    --   as long as new ones always use the latter craftitem everywhere else,
    --   they don't need the alias for any other reason.
end

local dep_lamb_raw = nil
if minetest.registered_items["animalmaterials:meat_lamb"] then
    dep_lamb_raw = "animalmaterials:meat_lamb"
end

if not dep_lamb_raw then
    minetest.register_craftitem(":animal_materials:meat_lamb", {
        description = S("Raw Lamb"),
        image = "codermobs_lamb_raw.png",
        on_use = minetest.item_eat(1),
        groups = { meat=1, eatable=1 },
        stack_max=25
    })
else
    minetest.register_alias("animal_materials:meat_lamb", dep_lamb_raw)
end

local dep_venison_raw = nil
if minetest.registered_items["animalmaterials:meat_venison"] then
    dep_venison_raw = "animalmaterials:meat_venison"
end

if not dep_venison_raw then
    minetest.register_craftitem(":animal_materials:meat_venison", {
        description = S("Raw Venison"),
        image = "codermobs_venison_raw.png",
        on_use = minetest.item_eat(1),
        groups = { meat=1, eatable=1 },
        stack_max=25
    })
else
    minetest.register_alias("animal_materials:meat_venison", dep_venison_raw)
end

local dep_undead_raw = nil
if minetest.registered_items["animalmaterials:meat_undead"] then
    dep_undead_raw = "animalmaterials:meat_undead"
end

if not dep_undead_raw then
    minetest.register_craftitem(":animal_materials:meat_undead", {
        description = S("Meat (not quite dead)"),
        image = "animal_materials_meat_undead_raw.png",
        on_use = minetest.item_eat(-2),
        groups = { meat=1, eatable=1 },
        stack_max=5
    })
else
    minetest.register_alias("animal_materials:meat_undead", dep_undead_raw)
end


local dep_toxic_raw = nil
if minetest.registered_items["animalmaterials:meat_toxic"] then
    dep_toxic_raw = "animalmaterials:meat_toxic"
end

if not dep_toxic_raw then
    minetest.register_craftitem(":animal_materials:meat_toxic", {
        description = S("Toxic Meat"),
        image = "animal_materials_meat_toxic_raw.png",
        on_use = minetest.item_eat(-5),
        groups = { meat=1, eatable=1 },
        stack_max=5
    })
else
    minetest.register_alias("animal_materials:meat_toxic", dep_toxic_raw)
end

local dep_ostrich_raw = nil
if minetest.registered_items["animalmaterials:meat_ostrich"] then
    dep_ostrich_raw = "animalmaterials:meat_ostrich"
end

if not dep_ostrich_raw then
  minetest.register_craftitem(":animal_materials:meat_ostrich", {
      description = S("Raw Ostrich"),
      image = "animal_materials_ostrich_meat_raw.png",
      on_use = minetest.item_eat(3),
      groups = { food_meat_raw = 1, meat=1, eatable=1 },
      stack_max=5
  })
else
    minetest.register_alias("animal_materials:meat_ostrich", dep_ostrich_raw)
end


local dep_bluewhite_raw = nil
if minetest.registered_items["animalmaterials:fish_bluewhite"] then
    dep_bluewhite_raw = "animalmaterials:fish_bluewhite"
end

if not dep_bluewhite_raw then
    minetest.register_craftitem(":animal_materials:fish_bluewhite", {
        description = S("Raw Fish (cichlid)"),
        image = "animal_materials_bluewhite_raw.png",
        on_use = minetest.item_eat(1),
        groups = { meat=1, eatable=1 },
        stack_max=25
    })
else
    minetest.register_alias("animal_materials:fish_bluewhite", dep_bluewhite_raw)
end

local dep_clownfish_raw = nil
if minetest.registered_items["animalmaterials:fish_clownfish"] then
    dep_clownfish_raw = "animalmaterials:fish_clownfish"
end

if not dep_clownfish_raw then
    minetest.register_craftitem(":animal_materials:fish_clownfish", {
        description = S("Raw Fish (clownfish)"),
        image = "animal_materials_clownfish_raw.png",
        on_use = minetest.item_eat(1),
        groups = { meat=1, eatable=1 },
        stack_max=25
    })
else
    minetest.register_alias("animal_materials:fish_clownfish", dep_clownfish_raw)
end

-- ===================================================================
-- feather

minetest.register_craftitem(":animal_materials:feather", {
    description = S("Feather"),
    image = "animal_materials_feather.png",
    stack_max=25
})

-- ===================================================================
-- milk

minetest.register_craftitem(":animal_materials:milk", {
    description = S("Milk"),
    image = "animal_materials_milk.png",
    on_use = minetest.item_eat(1),
    groups = { eatable=1 },
    stack_max=10
})

-- ===================================================================
-- egg

minetest.register_craftitem(":animal_materials:egg", {
    description = S("Egg"),
    image = "animal_materials_egg.png",
    stack_max=10
})

minetest.register_craftitem(":animal_materials:egg_big", {
    description = S("Big Egg"),
    image = "animal_materials_egg_big.png",
    stack_max=5
})

animal_materialsdata["animal_materials_egg"] = {
            graphics_3d = {
                visual = "mesh",
                mesh   = "animal_materials_egg_ent.b3d",
                textures = { "animal_materials_egg_ent_mesh.png" },
                collisionbox = { -0.12,-0.125,-0.12,0.12,0.125,0.12 },
                visual_size     = {x=1,y=1,z=1},
                }
    }

animal_materialsdata["animal_materials_egg_big"] = {
            graphics_3d = {
                visual = "mesh",
                mesh   = "animal_materials_egg_ent.b3d",
                textures = { "animal_materials_egg_ent_mesh.png" },
                collisionbox = { -0.24,-0.25,-0.24,0.24,0.25,0.24 },
                visual_size     = {x=2,y=2,z=2},
                }
    }

-- ===================================================================
-- bone

minetest.register_craftitem(":animal_materials:bone", {
    description = S("Bone"),
    image = "animal_materials_bone.png",
    stack_max=25
})

-- ===================================================================
-- furs

minetest.register_craftitem(":animal_materials:fur", {
    description = S("Fur"),
    image = "animal_materials_fur.png",
    stack_max=25
})

minetest.register_craftitem(":animal_materials:fur_deer", {
    description = S("Deer fur"),
    image = "animal_materials_deer_fur.png",
    stack_max=10
})

minetest.register_craftitem(":animal_materials:coat_cattle", {
    description = S("Cattle coat"),
    image = "animal_materials_cattle_coat.png",
    stack_max=10
})

-- ===================================================================
-- horns

minetest.register_craftitem(":animal_materials:antlers", {
    description = S("Antlers"),
    image = "animal_materials_antlers.png",
    stack_max=20
})

minetest.register_craftitem(":animal_materials:ivory", {
    description = S("Ivory"),
    image = "animal_materials_ivory.png",
    stack_max=20
})

-- ===================================================================
-- scale

minetest.register_craftitem(":animal_materials:scale_golden", {
    description = S("Scale (golden)"),
    image = "animal_materials_scale_golden.png",
    stack_max=25
})

minetest.register_craftitem(":animal_materials:scale_white", {
    description = S("Scale (white)"),
    image = "animal_materials_scale_white.png",
    stack_max=25
})

minetest.register_craftitem(":animal_materials:scale_grey", {
    description = S("Scale (grey)"),
    image = "animal_materials_scale_grey.png",
    stack_max=25
})

minetest.register_craftitem(":animal_materials:scale_blue", {
    description = S("Scale (blue)"),
    image = "animal_materials_scale_blue.png",
    stack_max=25
})

-- ===================================================================
-- recipes

minetest.register_craft({
    output = "wool:white",
    recipe = {
        {"animal_materials:feather","animal_materials:feather","animal_materials:feather"},
        {"animal_materials:feather", "animal_materials:feather","animal_materials:feather"},
        {"animal_materials:feather","animal_materials:feather","animal_materials:feather"},
    }
})

minetest.register_craft({
    output = "animal_materials:contract",
    recipe = {
        {"default:paper"},
        {"default:paper"},
    }
})
