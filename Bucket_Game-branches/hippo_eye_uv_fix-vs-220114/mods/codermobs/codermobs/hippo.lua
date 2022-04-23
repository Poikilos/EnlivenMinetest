-- Hippo. Descended from "22i-amcaw" mobset.

-- ===================================================================
-- Media license. Applies to model and associated textures.

-- GNU GENERAL PUBLIC LICENSE
-- Version 3, 29 June 2007

-- ===================================================================

local lcname     = "hippo"
local ucname     = "Hippo"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

local dup_texture_count = 16
local multimesh_textures = {}
for multimesh_texture_i = 1,dup_texture_count,1
do
    multimesh_textures[multimesh_texture_i] = msname .. "_mesh.png"
end

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =     -1       ,
    spawn_chance =  50000       ,

    day_mode     = true         ,
    min_light    =     14       ,
    max_light    =     20       ,
    min_height   =      0       ,
    max_height   =    200       ,

    spawn_type   = "animal"     ,

    spawn_nodes  = {
        "default:dirt_with_grass"       ,
        "ethereal:green_dirt"           ,
        "ethereal:green_dirt_top"       ,
        "ethereal:grove_dirt"           ,
        "mg:dirt_with_dry_grass"        ,
        "noisegrid:grass"               ,
    } ,

    add_egg   = true                    ,
    egg_image = "wool_pink.png"         ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

mobs_param.core_param = {

-- ===================================================================
-- Basic parameters.

    type = mobs_param.spawn_type ,
    makes_footstep_sound = true  ,

    -- Behavior/sight/battle
    armor         = 150          ,
    attack_npcs   = false        ,
    attack_type   = "dogfight"   ,
    damage        =   3          ,
    group_attack  = true         ,
    hp_max        =  35          ,
    hp_min        =  12          ,
    owner_loyal   = true         ,
    passive       = false        ,
    pushable      = true         ,
    reach         =   2.5        ,
    runaway       = true         ,
    view_range    =  10          ,

    -- Velocities
    run_velocity  =   1.5        ,
    walk_velocity =   1.0        ,

    -- Step/jump/fall parameters
    fall_damage   =   1          ,
    fear_height   =   5          ,
    jump          = true         ,
    jump_height   =   2          ,
    stepheight    =   1.2        ,

    -- Environment damage
    lava_damage   =   2          ,
    light_damage  =   0          ,
    water_damage  =   0          ,

    -- Misc. parameters
    floats        =   1          ,

-- ===================================================================
-- Model.

--                    x1     y1     z1     x2    y2    z2
    collisionbox  = { -0.21,  0.00, -0.21, 0.21, 0.24, 0.21 } ,
    mesh          = msname .. ".b3d"                          ,
    rotate        = 180                                       ,
    scale         = 8                                         ,
    visual        = "mesh"                                    ,
    textures      = multimesh_textures                        ,

    animation     = {
        stand_start  = 40 ,
        stand_end    = 80 ,
        walk_start   =  0 ,
        walk_end     = 40 ,
        run_start    =  0 ,
        run_end      = 40 ,
        speed_normal = 25 ,
        speed_run    = 30 ,
    } ,

-- ===================================================================
-- Other.

    sounds        = {
    },

    follow        = { "default:apple", "farming:potato" }     ,

    drops = {
        { name="mobs:meat_raw", chance=1, min=1, max=1 } ,
    } ,

    on_rightclick = function (self, clicker)
        if mobs:feed_tame(self, clicker, 8, true, true) then return end
        if mobs:protect(self, clicker) then return end

        if mobs:capture_mob(self, clicker, 0, 5, 50, false, nil) then
            return
        end
    end,
}

-- ===================================================================

codermobs.setup_mob()
codermobs.log_done()

-- ===================================================================
-- End of file.
