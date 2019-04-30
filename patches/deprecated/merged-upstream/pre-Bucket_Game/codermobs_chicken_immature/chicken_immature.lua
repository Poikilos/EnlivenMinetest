-- Chick. Code descended from "Farlands" chicken.

-- ===================================================================
--
-- You may  copy,  use,  modify or do nearly anything  but remove this
-- copyright notice. Of course,  you're not allowed to pretend  you've
-- created or written the Sapier pieces.
--
-- ===================================================================

local lcname     = "chicken_immature"
local ucname     = "Chick"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,
    aoc          =  2           ,
    obr          =  1           ,
    day_mode     = true         ,
    add_egg   = true                    ,
    egg_image = "wool_brown.png"        ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

local msname_img            = msname           .. "_mesh.png"
-- local msname_cooked_img     = msname_cooked    .. ".png"
-- local msname_raw_img        = msname_raw       .. ".png"

-- local msname_egg_img        = msname_egg       .. ".png"
-- local msname_egg_fried_img  = msname_egg_fried .. ".png"


-- local obj_name_egg          = obj_name         .. "_egg"
-- local obj_name_egg_entity   = obj_name_egg     .. "_entity"
-- local obj_name_egg_fried    = obj_name_egg     .. "_fried"

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type    ,
    makes_footstep_sound = false    ,

    armor       = 200               ,
    passive     = true              ,
    fall_damage =  0                ,
    fall_speed  = -8                ,
    jump_height =  0                ,
    fear_height =  1                ,
    hp_max      =  1                ,
    hp_min      =  1                ,

    water_damage = 1,
    lava_damage = 5,
    light_damage = 0,
    collisionbox  = { -0.21, 0, -0.21, 0.21, 0.42, 0.21 }   ,
    -- The chick, at size x10, is .53 m tall. Therefore, ratio of
    -- adult to immature is .63:.53. Maybe change it to two thirds:
    -- .63:.42 therefore scale by .79 (.42/.53):    
    visual_size   = { x=7.9, y=7.9 }                        ,
    visual        = "mesh"                                  ,
    mesh          = msname .. ".b3d"                        ,
    textures      = {{ msname_img }}             ,
    child_texture = {{ msname_img }}                        ,

    sounds = {
        random = msname ,
    },

    walk_velocity = 1.264,
    run_velocity = 1.264,
    runaway = true,
    jump = true,

    animation = {
        speed_normal = 5.53,  -- speed_run / 2 = 5.53
        stand_start = 0,
        stand_end = 69,
        walk_start = 70,
        walk_end = 85,
        speed_run = 11.06, -- 14 fps * visual_size = 11.06
        run_start = 70,
        run_end = 85,
    },

    follow = { "farming:seed_wheat", "farming:seed_cotton" } ,
    view_range = 5,

    on_rightclick = function (self, clicker)
        mobs:protect (self, clicker)
        mobs:capture_mob (self, clicker, 30, 50, 80, false, nil)
    end,

}

-- ===================================================================

codermobs.setup_mob()

-- ===================================================================

codermobs.log_done()

-- ===================================================================
-- End of file.
