-- Baby Chick. Original mob w/media by Poikilos.

-- ===================================================================
-- Code license. Applies to this module only.
--
-- CC-BY-NC-SA 3.0.  (c) 2019 and attribution:  OldCoder  (Robert Kir-
-- aly).

-- ===================================================================
-- Media license. Applies to model and associated texture.
--
-- You may  copy,  use,  modify or do nearly anything  but remove this
-- copyright notice. Of course,  you're not allowed to pretend  you've
-- created or written the Poikilos pieces.
--
-- CC-BY-SA 3.0. (c) 2019 and attribution: Poikilos.

-- ===================================================================

local lcname     = "baby_chick"
local ucname     = "Baby Chick"
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
    aoc          = -1           ,

    obr          =  1           ,
    day_mode     = true         ,
    min_light    =  3           ,
    max_light    = 20           ,
    min_height   = -31000       ,
    max_height   =  31000       ,
    spawn_chance =  60000       ,
    spawn_type   = "animal"     ,

    spawn_nodes  = {
        "never:nosuchnode" ,
    } ,

    add_egg   = true                    ,
    egg_image = "wool_brown.png"        ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type    ,
    makes_footstep_sound = false    ,

    armor         = 20              ,
    passive       = true            ,
    fall_damage   =  0              ,
    fall_speed    = -8              ,
    hp_max        = 10              ,
    hp_min        =  5              ,
    runaway       = true            ,
    jump          = false           ,
    view_range    =  5              ,

    jump_height   =  0              ,
    fear_height   =  1              ,
    stepheight    =  1.2            ,
    -- at 14 fps, the feet move at .32 meters/sec:
    walk_velocity =  .32            ,
    run_velocity  =  .64            ,

    water_damage  = 1               ,
    floats = 0,
    runaway = true,
    lava_damage   = 5               ,
    light_damage  = 0               ,

    collisionbox  = { -0.3, 0, -0.3, 0.3, 0.8, 0.3 } ,
    visual_scale  = 1.0                              ,
    visual        = "mesh"                           ,
    mesh          = msname .. ".b3d"                 ,
    textures      = {{ msname .. "_mesh.png" }}      ,

    animation     = {
        speed_normal = 14 ,
        stand_start  =  0 ,
        stand_end    = 69 ,
        walk_start   = 70 ,
        walk_end     = 85 ,
        speed_run    = 28 ,
        run_start    = 70 ,
        run_end      = 85 ,
    },

    sounds = {
        random = msname ,
    },

    drops = {
    },

    follow = { "farming:seed_wheat", "farming:seed_cotton" } ,

    on_rightclick = function (self, clicker)
        mobs:protect (self, clicker)
        mobs:capture_mob (self, clicker, 30, 50, 80, false, nil)
    end,

    do_custom = function (self)
        if math.random (1, 4000) > 1 then return end
        local pos = self.object:getpos()
        self.object:remove()
        minetest.add_entity (pos, "codermobs:chicken")
    end ,
}

-- ===================================================================

codermobs.setup_mob()

mobs:alias_mob ("codermobs:chick" , obj_name)

codermobs.log_done()

-- ===================================================================
-- End of file.
