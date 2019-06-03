-- exactly the same as lava_source and lava_flowing code from default, except:
-- * names are changed
-- * added liquid_range = 0
-- * changed liquid_alternative_* params
-- * removed igniter from groups
minetest.register_node("volcanic:crusted_lava_source", {
    description = "Crusted Lava Source",
    drawtype = "liquid",
    tiles = {
        {
            name = "volcanic_crusted_lava_source_animated.png",
            animation = {
                type = "vertical_frames",
                aspect_w = 16,
                aspect_h = 16,
                length = 3.0,
            },
        },
    },
    special_tiles = {
        -- New-style lava source material (mostly unused)
        {
            name = "volcanic_crusted_lava_source_animated.png",
            animation = {
                type = "vertical_frames",
                aspect_w = 16,
                aspect_h = 16,
                length = 3.0,
            },
            backface_culling = false,
        },
    },
    paramtype = "light",
    light_source = default.LIGHT_MAX - 1,
    walkable = true,
    pointable = false,
    diggable = false,
    buildable_to = true,
    is_ground_content = false,
    drop = "",
    drowning = 1,
    liquidtype = "source",
    liquid_alternative_flowing = "volcanic:crusted_lava_flowing",
    liquid_alternative_source = "volcanic:crusted_lava_source",
    liquid_range = 0,
    liquid_viscosity = 7,
    liquid_renewable = false,
    damage_per_second = 2,  -- formerly 4 * 2
    post_effect_color = {a = 191, r = 255, g = 64, b = 0},
    groups = {lava = 3, liquid = 2, hot = 3},
})
minetest.register_node("volcanic:crusted_lava_flowing", {
    description = "Flowing Crusted Lava",
    drawtype = "flowingliquid",
    tiles = {"volcanic_crusted_lava.png"},
    special_tiles = {
        {
            name = "volcanic_crusted_lava_source_animated.png",  -- intentionally use source animation
            backface_culling = false,
            animation = {
                type = "vertical_frames",
                aspect_w = 16,
                aspect_h = 16,
                length = 3.3,
            },
        },
        {
            name = "volcanic_crusted_lava_source_animated.png",  -- intentionally use source animation
            backface_culling = true,
            animation = {
                type = "vertical_frames",
                aspect_w = 16,
                aspect_h = 16,
                length = 3.3,
            },
        },
    },
    paramtype = "light",
    paramtype2 = "flowingliquid",
    light_source = default.LIGHT_MAX - 1,
    walkable = true,
    pointable = true,
    diggable = true,
    buildable_to = true,
    is_ground_content = false,
    drop = 'default:cobble',
    drowning = 1,
    liquidtype = "none",
    liquid_alternative_flowing = "volcanic:crusted_lava_flowing",
    liquid_alternative_source = "volcanic:crusted_lava_source",
    liquid_range = 0,
    liquid_viscosity = 7,
    liquid_renewable = false,
    damage_per_second = 2,  -- formerly 4 * 2
    post_effect_color = {a = 191, r = 255, g = 64, b = 0},
    groups = {lava = 3, hot = 3,
        not_in_creative_inventory = 1, crumbly = 3, cracky = 3},
})
