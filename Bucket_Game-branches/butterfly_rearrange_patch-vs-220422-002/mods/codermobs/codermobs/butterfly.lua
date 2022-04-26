-- Butterfly. Descended from AspireMint-blert2112 version.

-- ===================================================================

local lcname     = "single_butterfly"
local ucname     = "Single Butterfly"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =     -1       ,
    spawn_chance =  50000       ,

    day_mode     = true         ,
    min_light    =      5       ,
    max_light    =     20       ,
    min_height   =   -500       ,
    max_height   =  31000       ,

    spawn_type   = "animal"     ,

    spawn_nodes  = {
        "default:dirt_with_dry_grass"   ,
        "default:dirt_with_grass"       ,
        "fargen:dirt_with_leafy_grass"  ,
        "noisegrid:grass"               ,
        "group:flower"                  ,
    } ,

    add_egg   = true                    ,
    egg_image = msname .. "_inv.png"     ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

local mob_skins = {
    { msname .. "1.png" },
    { msname .. "2.png" },
    { msname .. "3.png" },
    { msname .. "4.png" },
}

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type ,
    passive = true,
    hp_min = 1,
    hp_max = 2,
    armor = 100,
    collisionbox = {-.25, -0.15, -.25, .25, 0.15, .25},
    visual = "mesh",
    mesh = msname .. ".b3d" ,
    textures = mob_skins,
    walk_velocity = 2,
    fall_speed = 0,
    stepheight = 3,
    fly = true,
    water_damage = 1,
    lava_damage = 1,
    light_damage = 0,
    fall_damage = 0,
    view_range = 10,
    blood_texture = "",

    animation = {
        -- speed_normal = 22,
        --stand_start = 8, stand_end = 19, stand_speed = 60,
        --run_start = 8, run_end = 19, run_speed = 22,
        stand_start = 0, stand_end = 7, stand_speed = 2,
        walk_start = 0, walk_end = 7, walk_speed = 2,
        run_start = 0, run_end = 7, run_speed = 3,
        -- walk_start = 8, walk_end = 19, walk_speed = 22,
        fly_start = 8, fly_end = 19, fly_speed = 22,
        -- TODO (if hover gets added to mobs--see EnlivenMinetest issue #556): hover_start = 8, hover_end = 19, hover_speed = 15,
    },

    on_rightclick = function(self, clicker)
        mobs:capture_mob(self, clicker, 10, 80, 0, true, nil)
    end
}

-- ===================================================================

codermobs.setup_mob()
codermobs.log_done()

-- ===================================================================
-- End of file.
