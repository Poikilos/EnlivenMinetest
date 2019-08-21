-- mdoege skeleton.

-- Mesh by Morn76
-- Animation by Pavel_S

-- ===================================================================

local lcname     = "mdskeleton"
local ucname     = "Mdoege Skeleton"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =     1        ,
    day_mode     = false        ,
    min_light    =     0        ,
    max_light    =     3        ,
    min_height   = -1000        ,
    max_height   =   500        ,
    spawn_chance =    36        ,
    spawn_type   = "monster"    ,

    spawn_nodes  = {
        "default:cobble"           ,
        "default:mossycobble"      ,
        "default:desert_stone"     ,
        "default:sandstonebrick"   ,
        "ethereal:gray_dirt"       ,
    } ,

    add_egg   = true               ,
    egg_image = "default_dirt.png" ,
    backface_culling = false,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type    ,
    passive        = false          ,
    attack_animals = true           ,
    attack_type    = "dogfight"     ,
    damage         =   2            ,
    view_range     =  15            ,
    reach          =   2            ,

    hp_min         =   7            ,
    hp_max         =  33            ,
    armor          = 100            ,
    fall_damage    =   0            ,
    lava_damage    =   0            ,
    light_damage   =   2            ,
    water_damage   =   0            ,
    drops          = {
        { name="default:apple", chance=2, min=1, max=3 } ,
    } ,

    collisionbox   = { -0.40, -0.01, -0.40, 0.40, 1.80, 0.40 } ,
    visual         = "mesh"                                    ,
    -- drawtype       = "front"                                   ,
    -- backface_culling = false,
    mesh           = msname .. ".x"                            ,
    textures       = { msname .. "_mesh.png" }                 ,
    stepheight     = 1.2            ,
    jump_height    =   0            ,
    jump           = false          ,
    floats         =   0            ,
    walk_velocity  =   1            ,
    run_velocity   =   3            ,
    animation      = {
        stand_start  =   0 ,
        stand_end    =  23 ,
        walk_start   =  24 ,
        walk_end     =  49 ,
        run_start    =  24 ,
        run_end      =  49 ,
        shoot_start  =  50 ,
        shoot_end    =  82 ,
        hurt_start   =  85 ,
        hurt_end     = 115 ,
        death_start  = 117 ,
        death_end    = 145 ,
        speed_normal =  30 ,
        speed_run    =  60 ,
    } ,

    sounds         = {
        death  = msname .. "_death"  ,
        hurt   = msname .. "_hurt"   ,
        random = msname .. "_random" ,
        war_cry = msname .. "_war_cry",
        attack = msname .. "_attack",
        jump = msname .. "_jump",
    } ,
    makes_footstep_sound = true     ,
}

-- ===================================================================

codermobs.setup_mob()
codermobs.log_done()

-- ===================================================================
-- End of file.
