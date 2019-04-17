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

local msname_img            = msname           .. ".png"
local msname_cooked_img     = msname_cooked    .. ".png"
local msname_raw_img        = msname_raw       .. ".png"

local msname_egg_img        = msname_egg       .. ".png"
local msname_egg_fried_img  = msname_egg_fried .. ".png"


local obj_name_egg          = obj_name         .. "_egg"
local obj_name_egg_entity   = obj_name_egg     .. "_entity"
local obj_name_egg_fried    = obj_name_egg     .. "_fried"

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type    ,
    makes_footstep_sound = true     ,

    armor       = 200               ,
    passive     = true              ,
    fall_damage =  0                ,
    fall_speed  = -8                ,
    jump_height =  0                ,
    fear_height =  1                ,
    hp_max      = 10                ,
    hp_min      =  5                ,

    water_damage = 1,
    lava_damage = 5,
    light_damage = 0,

    collisionbox  = { -0.1, 0, -0.1, 0.1, 0.22, 0.1 }   ,
    visual_size   = { x=1.0, y=1.0 }                        ,
    visual        = "mesh"                                  ,
    mesh          = msname .. ".b3d"                        ,
    textures      = {{ msname_img }}                        ,
    child_texture = {{ msname_img }}                        ,

    sounds = {
        random = msname ,
    },

    walk_velocity = 3.2,
    run_velocity = 6.4,
    runaway = true,
    jump = true,

    drops = {
        { name = obj_name_raw, chance = 1, min = 2, max = 2 } ,
    },

    animation = {
        speed_normal = 14,
        stand_start = 0,
        stand_end = 69,
        walk_start = 70,
        walk_end = 85,
        speed_run = 28,
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
