-- Butterfly. Descended from AspireMint-blert2112 version.

-- ===================================================================

local lcname     = "butterfly"
local ucname     = "Butterfly"
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
    egg_image = "default_cloud.png"     ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

local mob_skins = {
    { "(" ..
      msname .. "_01.png^" ..
      msname .. "_02.png^" ..
      msname .. "_03.png^" ..
      msname .. "_04.png^" ..
      msname .. "_05.png)" } ,

    { "(" ..
      msname .. "_01.png^[colorize:orange)^("       ..
      msname .. "_02.png^[colorize:violet)^("       ..
      msname .. "_03.png^[colorize:yellow)^("       ..
      msname .. "_04.png^[colorize:cyan)^("         ..
      msname .. "_05.png^[colorize:black)"          } ,

    { "(" ..
      msname .. "_01.png^[colorize:magenta)^("      ..
      msname .. "_02.png^[colorize:green)^("        ..
      msname .. "_03.png^[colorize:red)^("          ..
      msname .. "_04.png^[colorize:blue)^("         ..
      msname .. "_05.png^[colorize:white)"          } ,

    { "(" ..
      msname .. "_01.png^[colorize:yellow)^("       ..
      msname .. "_02.png^[colorize:cyan)^("         ..
      msname .. "_03.png^[colorize:green)^("        ..
      msname .. "_04.png^[colorize:violet)^("       ..
      msname .. "_05.png^[colorize:darkgray)"       } ,

    { "(" ..
      msname .. "_01.png^[colorize:pink)^("         ..
      msname .. "_02.png^[colorize:white)^("        ..
      msname .. "_03.png^[colorize:blue)^("         ..
      msname .. "_04.png^[colorize:orange)^("       ..
      msname .. "_05.png^[colorize:gray)"           } ,

    { "(" ..
      msname .. "_01.png^[colorize:darkgreen)^("    ..
      msname .. "_02.png^[colorize:brown)^("        ..
      msname .. "_03.png^[colorize:black)^("        ..
      msname .. "_04.png^[colorize:darkgray)^("     ..
      msname .. "_05.png^[colorize:red)"            } ,
}

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type ,
    passive = true,
    hp_min = 1,
    hp_max = 2,
    armor = 100,
    collisionbox = {-1, -0.3, -1, 1, 0.3, 1},
    visual = "mesh",
    mesh = msname .. ".x" ,
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

    animation = {
        speed_normal = 15,  speed_run = 30,
        stand_start = 0,    stand_end = 90,
        walk_start = 0,     walk_end = 90,
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
