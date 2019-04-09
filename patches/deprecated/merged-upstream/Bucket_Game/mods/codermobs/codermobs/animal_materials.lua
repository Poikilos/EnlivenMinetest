-- ===================================================================
-- License for this mod.
--
-- You may  copy,  use,  modify or do nearly anything  but remove this
-- copyright notice. Of course,  you're not allowed to pretend  you've
-- created or written the Sapier-specific pieces.
--
-- CC-BY-SA 3.0. Attribution: sapier.

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

core.log("action","MOD: animal_materials loading ...")
local version = "0.1.3"

animal_materialsdata = {}

-- ===================================================================
-- Node definitions

-- ===================================================================
-- Item definitions

-- ===================================================================
-- deamondeath sword
--

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
--

minetest.register_craftitem(":animal_materials:lasso", {
    description = S("Lasso"),
    image = "animal_materials_lasso.png",
    stack_max=10,
})

-- ===================================================================
-- net
--

minetest.register_craftitem(":animal_materials:net", {
    description = S("Net"),
    image = "animal_materials_net.png",
    stack_max=10,
})

-- ===================================================================
-- saddle
--

minetest.register_craftitem(":animal_materials:saddle", {
    description = S("Saddle"),
    image = "animal_materials_saddle.png",
    stack_max=1
})

-- ===================================================================
-- contract
--

minetest.register_craftitem(":animal_materials:contract", {
    description = S("Contract"),
    image = "animal_materials_contract.png",
    stack_max=10,
})

-- ===================================================================
-- meat
--

minetest.register_craftitem(":animal_materials:meat_raw", {
    description = S("Raw meat"),
    image = "animal_materials_meat_raw.png",
    on_use = minetest.item_eat(1),
    groups = { meat=1, eatable=1 },
    stack_max=25
})

minetest.register_craftitem(":animal_materials:meat_pork", {
    description = S("Pork (raw)"),
    image = "animal_materials_meat_raw.png",
    on_use = minetest.item_eat(1),
    groups = { meat=1, eatable=1 },
    stack_max=25
})

minetest.register_craftitem(":animal_materials:meat_beef", {
    description = S("Beef (raw)"),
    image = "animal_materials_meat_raw.png",
    on_use = minetest.item_eat(1),
    groups = { meat=1, eatable=1 },
    stack_max=25
})

minetest.register_craftitem(":animal_materials:meat_chicken", {
    description = S("Chicken (raw)"),
    image = "animal_materials_meat_raw.png",
    on_use = minetest.item_eat(1),
    groups = { meat=1, eatable=1 },
    stack_max=25
})

minetest.register_craftitem(":animal_materials:meat_lamb", {
    description = S("Lamb (raw)"),
    image = "animal_materials_meat_raw.png",
    on_use = minetest.item_eat(1),
    groups = { meat=1, eatable=1 },
    stack_max=25
})

minetest.register_craftitem(":animal_materials:meat_venison", {
    description = S("Venison (raw)"),
    image = "animal_materials_meat_raw.png",
    on_use = minetest.item_eat(1),
    groups = { meat=1, eatable=1 },
    stack_max=25
})

minetest.register_craftitem(":animal_materials:meat_undead", {
    description = S("Meat (not quite dead)"),
    image = "animal_materials_meat_undead_raw.png",
    on_use = minetest.item_eat(-2),
    groups = { meat=1, eatable=1 },
    stack_max=5
})

minetest.register_craftitem(":animal_materials:meat_toxic", {
    description = S("Toxic Meat"),
    image = "animal_materials_meat_toxic_raw.png",
    on_use = minetest.item_eat(-5),
    groups = { meat=1, eatable=1 },
    stack_max=5
})

minetest.register_craftitem(":animal_materials:meat_ostrich", {
    description = S("Ostrich Meat"),
    image = "animal_materials_meat_raw.png",
    on_use = minetest.item_eat(3),
    groups = { meat=1, eatable=1 },
    stack_max=5
})

minetest.register_craftitem(":animal_materials:pork_raw", {
    description = S("Pork"),
    image = "animal_materials_pork_raw.png",
    on_use = minetest.item_eat(4),
    groups = { meat=1, eatable=1 },
    stack_max=5
})

minetest.register_craftitem(":animal_materials:fish_bluewhite", {
    description = S("Fish (bluewhite)"),
    image = "animal_materials_meat_raw.png",
    on_use = minetest.item_eat(1),
    groups = { meat=1, eatable=1 },
    stack_max=25
})

minetest.register_craftitem(":animal_materials:fish_clownfish", {
    description = S("Fish (clownfish)"),
    image = "animal_materials_meat_raw.png",
    on_use = minetest.item_eat(1),
    groups = { meat=1, eatable=1 },
    stack_max=25
})

-- ===================================================================
-- feather
--

minetest.register_craftitem(":animal_materials:feather", {
    description = S("Feather"),
    image = "animal_materials_feather.png",
    stack_max=25
})

-- ===================================================================
-- milk
--

minetest.register_craftitem(":animal_materials:milk", {
    description = S("Milk"),
    image = "animal_materials_milk.png",
    on_use = minetest.item_eat(1),
    groups = { eatable=1 },
    stack_max=10
})

-- ===================================================================
-- egg
--

minetest.register_craftitem(":animal_materials:egg", {
    description = S("Egg"),
    image = "animal_materials_egg.png",
    stack_max=10
})

minetest.register_craftitem(":animal_materials:egg_big", {
    description = S("Egg (big)"),
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
--

minetest.register_craftitem(":animal_materials:bone", {
    description = S("Bone"),
    image = "animal_materials_bone.png",
    stack_max=25
})

-- ===================================================================
-- furs
--

-- ===================================================================

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
--

minetest.register_craftitem(":animal_materials:antlers", {
    description = S("Antlers"),
    image = "animal_materials_antlers.png",
    stack_max=20
})
minetest.register_alias("animal_materials:deer_horns", "animal_materials:antlers")

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
