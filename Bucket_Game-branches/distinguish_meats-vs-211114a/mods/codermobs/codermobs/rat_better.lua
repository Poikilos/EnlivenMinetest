-- Better Rat. Descended from Melkor version.

-- Note: Should be loaded *after* regular rat.

-- ===================================================================

local lcname     = "rat_better"
local ucname     = "Better Rat"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =      2       ,
    spawn_chance = 150000       ,

    day_mode     = true         ,
    min_light    =     10       ,
    max_light    =     20       ,
    min_height   = -31000       ,
    max_height   =  31000       ,

    scale        = 1.5          ,
    spawn_type   = "animal"     ,

    spawn_nodes  = {
        "darkage:silt"                  ,
        "default:desert_sand"           ,
        "default:dirt_with_dry_grass"   ,
        "default:dirt_with_grass"       ,
        "default:silver_sand"           ,
        "default:stone"                 ,
        "earthgen:dirt_with_dry_grass"  ,
        "ethereal:green_dirt"           ,
        "ethereal:green_dirt_top"       ,
        "ethereal:grove_dirt"           ,
        "ethereal:mushroom_dirt"        ,
        "loud_walking:polluted_dirt"    ,
        "mg:dirt_with_dry_grass"        ,
        "noisegrid:grass"               ,
    } ,

    add_egg   = false                   ,
    egg_image = msname .. "_inv.png"    ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

mobs_param.core_param = {
    type   = mobs_param.spawn_type    ,
    visual = "mesh" ,
    mesh   = msname .. ".b3d" ,
    rotate = 180,

    textures = {
        { msname .. "_black.png" } ,
        { msname .. "_brown.png" } ,
        { msname .. "_gray.png"  } ,
        { msname .. "_white.png" } ,
    },

    collisionbox = {-0.2, -0.01, -0.2, 0.2, 0.2, 0.2},
    hp_min= 2,
    hp_max = 5,
    armor = 80,
    knock_back = 2,
    blood_amount = 1,
    stepheight    = 1.2         ,
    jump_height   =   0         ,
    jump          = false       ,
    water_damage = 1,
    floats = 0,
    runaway = true,
    lava_damage = 5,
    fall_damage = 0,
    damage = 1,
    attack_type = "dogfight",
    group_attack = true,

    drops = {
        { name="mobs:cheese", chance=1, min=1, max=2 } ,
    } ,

    follow = { "mobs:cheese" , } ,
    replace_rate = 50,
    replace_what = { "mobs:cheese" , "mobs:cheeseblock" , } ,
    replace_with = "air",
    view_range = 8,

    on_rightclick = function (self, clicker)
        mobs:capture_mob (self, clicker, 25, 80, 0, true, nil)
    end ,
}

-- cooked rat, yummy!
minetest.register_craft ({
    type     = "cooking"                       ,
    output   = "codermobs:rat_standard_cooked" ,
    recipe   = obj_name                        ,
    cooktime = 5,
})

-- ===================================================================

codermobs.setup_mob()
codermobs.log_done()

-- ===================================================================
-- End of file.
