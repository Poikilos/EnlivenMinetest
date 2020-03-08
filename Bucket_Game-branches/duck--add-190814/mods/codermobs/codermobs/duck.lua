-- Duck Walking. Original by Poikilos.

-- ===================================================================
-- Media license. Applies to model and associated texture.
--
-- You may  copy,  use,  modify or do nearly anything  but remove this
-- copyright notice. Of course,  you're not allowed to pretend  you've
-- created or written the Sapier, Poikilos, or OldCoder pieces.
--
-- CC-BY-SA 3.0. Attribution: Poikilos.

-- ===================================================================

local lcname     = "duck_walking"
local ucname     = "Duck Walking"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =     -1       ,
    spawn_chance =  30000       ,

    day_mode     = true         ,
    min_light    =     14       ,
    max_light    =     20       ,
    min_height   =      0       ,
    max_height   =    200       ,

    spawn_type   = "animal"     ,

    spawn_nodes  = {
        "default:dirt_with_dry_grass"   ,
        "ethereal:mushroom_dirt"        ,
        "noisegrid:grass"               ,
    } ,

    spawn_by = {
        "group:dry_grass"               ,
        "group:grass"                   ,
        "flowers:mushroom_brown"        ,
    } ,

    add_egg   = true                    ,
    egg_image = "wool_pink.png"         ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

-- Chicken-based  images  stand in for  ostrich-based  images  in some
-- cases.

local mcname                = "codermobs_duck_walking"

local msname_cooked         = mcname           .. "_cooked"
local msname_raw            = mcname           .. "_raw"

local msname_img            = mcname           .. ".png"
local msname_cooked_img     = msname_cooked    .. ".png"
local msname_raw_img        = msname_raw       .. ".png"

local msname_egg            = mcname           .. "_egg"
local msname_egg_fried      = msname_egg       .. "_fried"
local msname_egg_fried_img  = msname_egg_fried .. ".png"
local msname_egg_img        = msname_egg       .. ".png"

local obj_name_cooked       = obj_name         .. "_cooked"
local obj_name_raw          = obj_name         .. "_raw"

local obj_name_egg          = obj_name         .. "_egg"
local obj_name_egg_entity   = obj_name_egg     .. "_entity"
local obj_name_egg_fried    = obj_name_egg     .. "_fried"

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type ,
    makes_footstep_sound = true  ,

    armor         = 200          ,
    attack_npcs   = false        ,
    attack_type   = "dogfight"   ,
    damage        =   2          ,
    fear_height   =   3          ,
    floats        =   0          ,
    group_attack  = true         ,
    hp_max        =  15          ,
    hp_min        =   5          ,
    jump_height   =   6          ,
    jump          = true         ,
    owner_loyal   = true         ,
    passive       = false        ,
    pushable      = true         ,
    reach         =   2          ,
    runaway       = true         ,
    stepheight    =   0.6        ,
    type          = "animal"     ,
    view_range    =  10          ,

    lava_damage   =   5          ,
    light_damage  =   0          ,
    water_damage  =   1          ,

    collisionbox  = { -0.22, 0.0, -0.22, 0.22, 0.48, 0.22 } ,
    mesh          = "codermobs_duck_walking.b3d"            ,
    rotate        = 0                                       ,
    scale         = 2                                       ,

    textures      = {
        { msname .. "_male_mesh.png"   } ,
        { msname .. "_female_mesh.png" } ,
    },

    visual        = "mesh"                                  ,

    sounds        = {
    } ,

    follow        = { "farming:seed_wheat", "farming:seed_cotton" } ,

    drops         = {
        {
            name   = "animal_materials:meat" ,
            chance = 1 , min = 1, max = 3 ,
        } ,
    } ,

    walk_velocity =   0.444 ,
    run_velocity  =   1.778 ,

    animation     = {
        stand_start  =  0 ,
        stand_end    =  2 ,
        speed_normal =  8 ,
        walk_start   =  3 ,
        walk_end     = 11 ,
        speed_run    = 32,
        run_start    =  3 ,
        run_end      = 11 ,
    },

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
