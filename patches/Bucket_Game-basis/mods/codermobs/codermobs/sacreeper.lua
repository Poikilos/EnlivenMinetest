-- Sapier Creeper. Descended from Sapier version.

-- ===================================================================
-- Media license. Applies to model but not associated texture.
--
-- You may  copy,  use,  modify or do nearly anything  but remove this
-- copyright notice. Of course,  you're not allowed to pretend  you've
-- created or written the Sapier pieces.
--
-- CC-BY-SA 3.0. Attribution: Sapier.

-- ===================================================================

local lcname     = "sacreeper"
local ucname     = "Sapier Creeper"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =     1        ,
    obr          =     1        ,
    day_mode     = false        ,
    min_light    =     0        ,
    max_light    =     7        ,
    min_height   =     1        ,
    max_height   =   200        ,
    spawn_chance = 50000        ,
    spawn_type   = "monster"    ,

    spawn_nodes  = {
        "default:desert_sand"   ,
        "default:silver_sand"   ,
    } ,

    add_egg   = true                ,
    egg_image = "default_brick.png" ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type    ,
    makes_footstep_sound = true     ,

    armor            = 100          ,
    attack_animals   = false        ,
    attack_type      = "explode"    ,
    damage           =   3          ,
    explosion_radius =   3          ,
    fall_damage      =   0          ,
    hp_min           =   7          ,
    hp_max           =  33          ,
    jump             = true         ,
    lava_damage      =   0          ,
    light_damage     =   2          ,
    passive          = false        ,
    reach            =   2          ,
    run_velocity     =   2          ,
    view_range       =   4          ,
    walk_velocity    =   1          ,
    water_damage     =   0          ,
    floats = 0,

    drops = {
        { name = "default:apple"          ,
          chance = 2, min = 1, max = 3 }  ,
    },

    sounds = {
        random  = "codermobs_sacreeper_random"  ,
        explode = "codermobs_sacreeper_explode" ,
    } ,

    textures = {
        { "codermobs_sacreeper_mesh.png" } ,
    },

    collisionbox  = { -0.9, -0.9, -0.9, 0.9, 0.9, 0.9 } ,
    visual_size   = { x=0.9, y=0.9 }                    ,
    mesh          = "codermobs_sacreeper.b3d"           ,
    visual        = "mesh"                              ,
}

-- ===================================================================

codermobs.setup_mob()
codermobs.log_done()

-- ===================================================================
-- End of file.
