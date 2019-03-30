-- ===================================================================
-- Light.

minetest.register_node ("nftools:light", {
    drawtype          = "glasslike"              ,
    tiles             = { "nftools_debug.png" }  ,
    is_ground_content = true                     ,
    paramtype         = "light"                  ,
    light_source      = default.LIGHT_MAX - 1    ,

    groups            = {
        cracky = 3, oddly_breakable_by_hand=2,
    } ,

    sounds = default.node_sound_stone_defaults() ,
})

-- ===================================================================
-- Mese Pickaxe.

minetest.register_tool ("nftools:pick_mese", {
    description = "Mese Pickaxe with light",
    inventory_image = "nftools_mesepick.png",
    wield_image = "nftools_mesepick_wield.png",
    tool_capabilities = {
        full_punch_interval = 1.0,
        max_drop_level=3,
        groupcaps={
            cracky={times={[1]=2.0, [2]=1.0, [3]=0.5}, uses=20, maxlevel=3},
            crumbly={times={[1]=2.0, [2]=1.0, [3]=0.5}, uses=20, maxlevel=3},
            snappy={times={[1]=2.0, [2]=1.0, [3]=0.5}, uses=20, maxlevel=3}
        }
    },
})

minetest.register_craft ({
    output = 'nftools:pick_mese',
    recipe = {
        {'default:torch'},
        {'default:pick_mese'},
    }
})

-- ===================================================================
-- Stool.

minetest.register_node ("nftools:stool",{
    description = "Wooden Stool",
    tiles = {"nftools_stool.png"},
    drop = 'nftools:stool',
    groups = {choppy=2,oddly_breakable_by_hand=2,flammable=3,wood=1},
    sounds = default.node_sound_wood_defaults(),
    drawtype="nodebox",
    paramtype = "light",
    node_box = {
        type = "fixed",
        fixed = {
            {0.412500,-0.500000,-0.500000,0.500000,0.000000,-0.437500}, --NodeBox 1
            {-0.500000,-0.500000,-0.500000,-0.437500,0.000000,-0.437500}, --NodeBox 2
            {0.412500,-0.500000,0.437504,0.500000,0.000000,0.500000}, --NodeBox 3
            {-0.500000,-0.500000,0.462500,-0.437500,0.000000,0.500000}, --NodeBox 4
            {-0.500000,0.000000,-0.500000,0.500000,0.062500,0.500000}, --NodeBox 5
        }
    }
})

-- ===================================================================
-- Quartz crystals.

minetest.register_node ("nftools:quartz_crystals", {
    description = "Quartz Crystals",
    tiles = {"nftools_quartz_crystal.png"},
    is_ground_content = true,
    groups = {cracky=1,level=2},
    sounds = default.node_sound_stone_defaults(),
    drawtype="nodebox",
    paramtype = "light",
    paramtype2="facedir",
    sunlight_propagates = true,
    node_box = {
        type = "fixed",
        fixed = {
            {-0.437500,-0.500000,-0.437500,0.425000,-0.250000,0.425004}, 
            {-0.375000,-0.250000,0.187500,-0.250000,0.500000,0.312500}, 
            {0.062500,-0.250000,-0.187500,0.312500,0.375000,0.125000}, 
            {-0.312500,-0.500000,-0.250000,-0.125000,0.125000,0.000000}, 
            {-0.187500,-0.250000,-0.437500,0.125000,0.500000,-0.250000}, 
            {0.000000,-0.312500,0.187500,0.250000,0.312500,0.375000}, 
            {-0.125000,-0.187500,-0.250000,0.062500,0.312500,0.000000}, 
            {0.125000,-0.250000,-0.375000,0.375000,0.375000,-0.187500}, 
            {-0.250000,-0.250000,0.062500,0.000000,0.125000,0.375000}, 
        }
    }
})

-- ===================================================================
-- Ore.

minetest.register_ore ({
    ore_type       = "scatter",
    ore            = "nftools:alexandrite_ore",
    wherein        = "default:stone",
    clust_scarcity = 24*24*24,
    clust_num_ores = 27,
    clust_size     = 6,
    y_max          =    -64,
    y_min          = -31000,
    flags          = "absheight",
})

-- ===================================================================

minetest.register_ore ({
    ore_type       = "scatter",
    ore            = "nftools:amber",
    wherein        = "default:stone",
    clust_scarcity = 24*24*24,
    clust_num_ores = 27,
    clust_size     = 6,
    y_max          =    -64,
    y_min          = -31000,
    flags          = "absheight",
})

-- ===================================================================

minetest.register_ore ({
    ore_type       = "scatter",
    ore            = "nftools:amethyst_ore",
    wherein        = "default:stone",
    clust_scarcity = 24*24*24,
    clust_num_ores = 27,
    clust_size     = 6,
    y_max          =    -64,
    y_min          = -31000,
    flags          = "absheight",
})

-- ===================================================================

minetest.register_ore ({
    ore_type       = "scatter",
    ore            = "nftools:aquamarine_ore",
    wherein        = "default:stone",
    clust_scarcity = 13*13*13,
    clust_num_ores = 5,
    clust_size     = 3,
    y_max          =  -5,
    y_min          = -40,
    flags          = "absheight",
})

-- ===================================================================
-- Alexandrite

minetest.register_node ("nftools:alexandrite_ore", {
    description = "Alexandrite Ore",
    tiles = {"nftools_alexandriteore.png"},
    is_ground_content = true,
    groups = {cracky=1},
    drop = "nftools:alexandrite",
})

minetest.register_craftitem ("nftools:alexandrite", {
    description = "Alexandrite",
    inventory_image = "nftools_alexandrite.png",
})

-- ===================================================================
-- Amber

minetest.register_node ("nftools:amber", {
    description = "Amber",
    tiles = {"nftools_amber.png"},
    is_ground_content = true,
    groups = {cracky=1},
    drop = "nftools:amber_chip",
})

minetest.register_craftitem ("nftools:amber_chip", {
    description = "Amber Chip",
    inventory_image = "nftools_amberchip.png",
})

-- ===================================================================
-- Aquamarine

minetest.register_node ("nftools:aquamarine_ore", {
    description = "Aquamarine Ore",
    tiles = {"nftools_aquamarineore.png"},
    is_ground_content = true,
    groups = {cracky=1},
    drop = "nftools:aquamarine_ore",
})

minetest.register_craftitem ("nftools:aquamarine", {
    description = "Aquamarine",
    inventory_image = "nftools_aquamarine.png",
})

-- ===================================================================
-- Smelting

minetest.register_craft ({
    type = "cooking",
    output = "nftools:aquamarine",
    recipe = "nftools:aquamarine_ore",
})

minetest.register_craft ({
    type = "cooking",
    output = "nftools:alexandrite",
    recipe = "nftools:alexandrite_ore",
})

minetest.register_craft ({
    type = "cooking",
    output = "nftools:amethyst",
    recipe = "nftools:amethyst_ore",
})

-- ===================================================================
-- Amethyst

minetest.register_node ("nftools:amethyst_ore", {
    description = "Amethyst Ore",
    tiles = {"nftools_amethystore.png"},
    is_ground_content = true,
    groups = {cracky=1},
    drop = "nftools:amethyst",
})

minetest.register_craftitem ("nftools:amethyst", {
    description = "Amethyst",
    inventory_image = "nftools_amethyst.png",
})

-- ===================================================================
-- Sunflower.

minetest.register_node ("nftools:sunflower", {
    description = "Sunflower",
    drawtype = "plantlike",
    visual_scale = 1.5,
    tiles = {"nftools_sunflower.png"},
    inventory_image = "nftools_sunflower.png",
    wield_image = "nftools_sunflower.png",
    paramtype = "light",
    walkable = false,
    buildable_to = true,
    is_ground_content = true,
    groups = {snappy=3,flammable=2,flora=1,attached_node=1},
    selection_box = {
        type = "fixed",
        fixed = {-0.5, -0.5, -0.5, 0.5, -5/16, 0.5},
    },
})

-- ===================================================================
-- Scythe

minetest.register_tool ("nftools:scythe", {
    description = "Scythe",
    inventory_image = "nftools_tool_scythe.png",
    tool_capabilities = {
        full_punch_interval = 0.8,
        max_drop_level=1,
        groupcaps={
            snappy={times={[1]=2.5, [2]=1.20, [3]=0.35}, uses=100, maxlevel=2},
        },
        damage_groups = {fleshy=6},
    }
})

minetest.register_craft ({
    output = 'nftools:scythe',
    recipe = {
        {'default:steel_ingot', 'default:steel_ingot', 'default:steel_ingot'},
        {'', '', 'default:stick'},
        {'', '', 'default:stick'},
    }
})

-- ===================================================================
-- Mace

minetest.register_tool ("nftools:mace", {
    description = "Mace",
    inventory_image = "nftools_tool_mace.png",
    tool_capabilities = {
        full_punch_interval = 1.5,
        max_drop_level=1,
        groupcaps={
            snappy={times={[1]=2.5, [2]=1.20, [3]=0.35}, uses=70, maxlevel=2},
        },
        damage_groups = {fleshy=5},
    }
})

minetest.register_craft ({
    output = 'nftools:mace',
    recipe = {
        {'default:obsidian_shard', 'default:steel_ingot', 'default:obsidian_shard'},
        {'', 'default:stick', ''},
        {'', 'default:stick', ''},
    }
})

-- ===================================================================
-- Battle-axe

minetest.register_tool ("nftools:battleaxe", {
    description = "Battle Axe",
    inventory_image = "nftools_tool_battleaxe.png",
    tool_capabilities = {
        full_punch_interval = 0.8,
        max_drop_level=1,
        groupcaps={
            snappy={times={[1]=2.5, [2]=1.20, [3]=0.35}, uses=40, maxlevel=2},
        },
        damage_groups = {fleshy=4},
    }
})

minetest.register_craft ({
    output = 'nftools:battleaxe',
    recipe = {
        {'default:cobble', 'default:cobble', 'default:cobble'},
        {'', 'default:cobble', ''},
        {'', 'default:stick', ''},
    }
})
