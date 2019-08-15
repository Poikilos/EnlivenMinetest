-- Oerkki.

-- ===================================================================

local lcname     = "oerkki"
local ucname     = "Oerkki"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =      1       ,
    day_mode     = true         ,
    min_light    =      0       ,
    max_light    =      7       ,
    min_height   = -31000       ,
    max_height   =    -10       ,
    spawn_chance =  25000       ,
    spawn_type   = "monster"    ,

    spawn_nodes  = {
        "default:stone"                 ,
    } ,

    add_egg   = true                    ,
    egg_image = "default_obsidian.png"  ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type ,

    armor          = 100         ,
    attack_type    = "dogfight"  ,
    damage         =   4         ,
    attack_animals = true           ,
    fear_height    =   4         ,
    hp_max         =  34         ,
    hp_min         =   8         ,
    stepheight     = 1.2         ,
    jump_height    =   0         ,
    jump           = false       ,
    passive        = false       ,
    pathfinding    = true        ,
    reach          =   2         ,
    run_velocity   =   3         ,
    view_range     =  10         ,
    walk_velocity  =   1         ,
    floats         =   0         ,
    runaway        = true        ,

    lava_damage    =   4         ,
    light_damage   =   1         ,
    water_damage   =   2         ,

    -- This mob eats torches
    replace_offset =  -1                    ,
    replace_rate   =   5                    ,
    replace_what   = { "default:torch" }    ,
    replace_with   = "air"                  ,

    makes_footstep_sound = false ,

    drops = {
        { name = "default:obsidian" ,
          chance = 3, min = 1, max = 2 } ,
    },

    immune_to = {
        { "default:sword_wood" ,   0 } , -- No damage
        { "default:gold_lump"  , -10 } , -- Heals by 10 points
    },

    sounds = {
        random = "codermobs_oerkki" ,
    },

    animation = {
        stand_start  =  0 ,
        stand_end    = 23 ,
        walk_start   = 24 ,
        walk_end     = 36 ,
        run_start    = 37 ,
        run_end      = 49 ,
        punch_start  = 37 ,
        punch_end    = 49 ,
        speed_normal = 15 ,
        speed_run    = 15 ,
    },

    textures = {
        { "codermobs_oerkki1.png" } ,
        { "codermobs_oerkki2.png" } ,
    },

    collisionbox = { -0.4, -1, -0.4, 0.4, 0.9, 0.4 }    ,
    mesh         = "codermobs_oerkki.b3d"               ,
    visual       = "mesh"                               ,
}

-- ===================================================================

codermobs.setup_mob()

mobs:alias_mob ("mobs_monster:oerkki" , obj_name)

codermobs.log_done()

-- ===================================================================
-- End of file.
