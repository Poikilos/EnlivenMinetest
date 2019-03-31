-- ===================================================================
-- Light.

minetest.register_node("nftools:light", {
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

minetest.register_tool("nftools:pick_mese", {
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

minetest.register_craft({
    output = 'nftools:pick_mese',
    recipe = {
        {'default:torch'},
        {'default:pick_mese'},
    }
})

-- ===================================================================
-- Stool.

minetest.register_node("nftools:stool",{
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

minetest.register_node("nftools:quartz_crystals", {
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

minetest.register_ore({
    ore_type       = "scatter",
    ore            = "nftools:stone_with_bismuth",
    wherein        = "default:stone",
		clust_scarcity = 24*24*24,
		clust_num_ores = 4,
		clust_size     = 3,
    y_max          = -64,
    y_min          = -31000,
    flags          = "absheight",
})

-- ===================================================================

minetest.register_ore({
    ore_type       = "scatter",
    ore            = "nftools:stone_with_amber",
    wherein        = "default:stone",
    clust_scarcity = 48*48*48,
    clust_num_ores = 1,
    clust_size     = 2,
    y_max          = -8,
    y_min          = -64,
    flags          = "absheight",
})

-- ===================================================================

minetest.register_ore({
    ore_type       = "scatter",
    ore            = "nftools:stone_with_blackopal",
    wherein        = "default:stone",
    clust_scarcity = 48*48*48,
    clust_num_ores = 1,
    clust_size     = 2,
    y_max          = -128,
    y_min          = -256,
})

-- ===================================================================

minetest.register_ore({
    ore_type       = "scatter",
    ore            = "nftools:stone_with_turquoise",
    wherein        = "default:stone",
    clust_scarcity = 24*24*24,
    clust_num_ores = 3,
    clust_size     = 3,
    y_max          = -8,
    y_min          = -64,
    flags          = "absheight",
})

-- ===================================================================
-- Bismuth (formerly Alexandrite)

minetest.register_alias("nftools:alexandrite_ore", "nftools:stone_with_bismuth")
minetest.register_alias("nftools:alexandrite", "nftools:bismuth")

minetest.register_craftitem("nftools:bismuth", {
    description = "Bismuth",
    inventory_image = "nftools_bismuth.png",
})

minetest.register_node("nftools:stone_with_bismuth", {
    description = "Raw Bismuth",
    tiles = {"default_stone.png^nftools_mineral_bismuth.png"},
    is_ground_content = true,
    groups = {cracky=1},
    drop = "nftools:stone_with_bismuth",
})


-- ===================================================================
-- Smelting (only metals)

minetest.register_craft ({
    type = "cooking",
    output = "nftools:bismuth",
    recipe = "nftools:stone_with_bismuth",
})

-- ===================================================================
-- Amber

minetest.register_alias("nftools:amber", "nftools:stone_with_amber")
-- (formerly called amber but dropped chip; use conventions instead)

minetest.register_node("nftools:stone_with_amber", {
    description = "Rough Amber",
    tiles = {"default_stone.png^nftools_mineral_amber.png"},
    is_ground_content = true,
    groups = {cracky=1},
    drop = "nftools:amber_chip",
})

minetest.register_craftitem("nftools:amber_chip", {
    description = "Amber",
    inventory_image = "nftools_amberchip.png",
})

-- ===================================================================
-- Turquoise (formerly Aquamarine)

minetest.register_alias("nftools:aquamarine_ore", "nftools:stone_with_turquoise")
minetest.register_alias("nftools:aquamarine", "nftools:turquoise")

minetest.register_node("nftools:stone_with_turquoise", {
    description = "Rough Turquoise",
    tiles = {"default_stone.png^nftools_mineral_turquoise.png"},
    is_ground_content = true,
    groups = {cracky=1},
    drop = "nftools:turquoise",
})

minetest.register_craftitem("nftools:turquoise", {
    description = "Turquoise",
    inventory_image = "nftools_turquoise.png",
})

-- ===================================================================
-- Black Opal (formerly Amethyst)

minetest.register_alias("nftools:amethyst_ore", "nftools:stone_with_blackopal")
minetest.register_alias("nftools:amethyst", "nftools:blackopal")

minetest.register_craftitem("nftools:blackopal", {
    description = "Black Opal",
    inventory_image = "nftools_blackopal.png",
})

minetest.register_node("nftools:stone_with_blackopal", {
    description = "Rough Black Opal",
    tiles = {"default_stone.png^nftools_mineral_blackopal.png"},
    is_ground_content = true,
    groups = {cracky=1},
    drop = "nftools:blackopal",
})

-- ===================================================================
-- Sunflower.

minetest.register_node("nftools:sunflower", {
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
-- Blocks


minetest.register_node("nftools:amberblock", {
    description = "Amber Block",
    alpha = 170,
    sunlight_propagates = true,
    tiles = {"nftools_amber_block.png"},
    is_ground_content = true,
    groups = {cracky=1},
    drop = "nftools:amberblock",
})

local function registerblockrecipe(name, blockname)
    minetest.register_craft({
        output = blockname,
        recipe = {{name, name, name},
          {name, name, name},
          {name, name, name}
        }
    })
    minetest.register_craft({
        output = name..' 9',
        recipe = {
          {blockname},
        }
    })
end

registerblockrecipe('nftools:amber_chip', 'nftools:amberblock')

if minetest.get_modpath("quartz") ~= nil then
  minetest.register_craft({
    output = "nftools:quartz_crystals",
    recipe = {
      {'', '', ''},
      {'', 'quartz:quartz_crystal', ''},
      {'quartz:quartz_crystal', 'nftools:amberblock', 'quartz:quartz_crystal'}
    }
  
  })

  minetest.register_craft({
    output = "quartz:quartz_crystal"..' 3',
    recipe = {
      {"nftools:quartz_crystals"},
    }
  })
end

-- ===================================================================
-- Scythe

minetest.register_tool("nftools:scythe", {
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

minetest.register_craft({
    output = 'nftools:scythe',
    recipe = {
        {'default:steel_ingot', 'default:steel_ingot', 'default:steel_ingot'},
        {'', '', 'default:stick'},
        {'', '', 'default:stick'},
    }
})

-- ===================================================================
-- Mace

minetest.register_tool("nftools:mace", {
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

minetest.register_craft({
    output = 'nftools:mace',
    recipe = {
        {'default:obsidian_shard', 'default:steel_ingot', 'default:obsidian_shard'},
        {'', 'default:stick', ''},
        {'', 'default:stick', ''},
    }
})

-- ===================================================================
-- Battle-axe

minetest.register_tool("nftools:battleaxe", {
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

minetest.register_craft({
    output = 'nftools:battleaxe',
    recipe = {
        {'default:cobble', 'default:cobble', 'default:cobble'},
        {'', 'default:cobble', ''},
        {'', 'default:stick', ''},
    }
})
