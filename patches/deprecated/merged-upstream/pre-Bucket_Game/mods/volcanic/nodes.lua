-- exactly the same as lava_source and lava_flowing code from default, except:
-- * names are changed
-- * added liquid_range = 0
-- * changed liquid_alternative_* params
-- * removed igniter from groups

-- ===================================================================

local lcsa = {
    name             = "volcanic_crusted_lava_source_animated.png" ,
    backface_culling = false                            ,

    animation        = {
        type         = "vertical_frames" ,
        aspect_w     = 16                ,
        aspect_h     = 16                ,
        length       =  3.3              ,
    } ,
}

local lava_crust_source_tiles = { lcsa }

-- ===================================================================

minetest.register_node("volcanic:crusted_lava_source", {

    description   = "Crusted Lava Source"     ,
    drawtype      = "liquid"                ,
    tiles         = lava_crust_source_tiles       ,
    special_tiles = lava_crust_source_tiles       ,
    paramtype     = "light"                 ,
    light_source  = default.LIGHT_MAX - 1   ,

    buildable_to      = true  ,
    diggable          = false ,
    pointable         = false ,
    walkable          = true  ,
    is_ground_content = false ,

    damage_per_second = 2,  -- formerly 4 * 2
    drop              = ""    ,
    drowning          = 1     ,
    liquid_range = 0,
    liquidtype                 = "source"                     ,
    liquid_alternative_flowing = "volcanic:crusted_lava_flowing",
    liquid_alternative_source = "volcanic:crusted_lava_source",
    liquid_renewable           = false                        ,
    liquid_viscosity           = 7                            ,

    post_effect_color = { a = 191, r = 255, g = 64, b = 0 } ,
    groups            = { lava = 3, liquid = 2, hot = 3   } ,
})

-- ===================================================================

minetest.register_node("volcanic:crusted_lava_flowing", {
    description = "Crusted Lava Flow",
    drawtype      = "flowingliquid"         ,
                                -- intentionally use source animation
    tiles         = lava_crust_source_tiles ,
    special_tiles = { lcsa, lcsa }          ,

    paramtype     = "light"                 ,
    paramtype2    = "flowingliquid"         ,
    light_source  = default.LIGHT_MAX - 1   ,

    buildable_to      = true  ,
    diggable          = true ,
    pointable         = true ,
    walkable          = true ,
    is_ground_content = false ,

    damage_per_second = 2     ,  -- formerly 4 * 2
    drop              = "default:cobble"    ,
    drowning          = 1     ,

    liquidtype                 = "none"                    ,
    liquid_alternative_flowing = "volcanic:crusted_lava_flowing" ,
    liquid_alternative_source  = "volcanic:crusted_lava_source"  ,
    liquid_range               = 0                            ,
    liquid_renewable           = false                        ,
    liquid_viscosity           = 7                            ,

    post_effect_color = { a = 191, r = 255, g = 64, b = 0 } ,
    groups            = {
        lava = 3, hot = 3,
        not_in_creative_inventory = 1,
        crumbly = 3, cracky = 3,
    } ,
})
