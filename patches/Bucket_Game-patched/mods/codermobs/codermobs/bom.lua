-- BOM. Descended from Sapier Creeper.

-- ===================================================================
-- codermobs_bom_random, codermobs_bom_death
--   CC0
--   based on fuse by Seidolon
-- codermobs_bom_explode, codermobs_damage_hollow_metal
--   CC0
--   based on Explosion 1 by Deganoth
--
-- Other media (model and textures):
-- You may  copy,  use,  modify or do nearly anything  but remove this
-- copyright notice. Of course,  you're not allowed to pretend  you've
-- created or written the Poikilos and OldCoder pieces.
-- CC-BY-SA 3.0. Attribution: Poikilos and OldCoder.

-- ===================================================================

local lcname     = "bom"
local ucname     = "BOM"
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
        random  = "codermobs_bom_random"         ,
        explode = "codermobs_bom_explode"        ,
        damage = "codermobs_damage_hollow_metal" ,
        death   = "codermobs_bom_death"          ,
    } ,

    textures = {
        { "codermobs_bom_mesh.png" } ,
    },
    
    animation     = {
        -- speed_normal = 10 ,
        speed_normal = 5 ,
        stand_start  =  1 ,
        stand_end    = 29 ,
        walk_start   = 31 ,
        walk_end     = 50 ,
        -- speed_run    = 20 ,
        speed_run    = 10 ,
        run_start    = 31 ,
        run_end      = 50 ,
    },
    
    collisionbox  = { -0.65, 0, -0.65, 0.65, 1.75, 0.65 } ,
    visual_size   = { x=0.9, y=0.9 }                    ,
    -- visual_scale = 1                                    ,
    visual_scale  = 2                                   ,
    mesh          = "codermobs_bom.b3d"                 ,
    visual        = "mesh"                              ,
}

-- ===================================================================

codermobs.setup_mob()
codermobs.log_done()

-- ===================================================================
-- End of file.
