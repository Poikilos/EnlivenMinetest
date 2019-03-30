-- Deer. Descended from Sapier version.

-- ===================================================================
-- Mob Framework Mod by Sapier
--
-- You may copy, use, modify or do nearly anything except removing this
-- copyright  notice. Of course,  you are NOT allow to pretend you have
-- written it.
-- CC-BY-SA 3.0. Attribution: sapier.
--
--! @file init.lua
--! @brief deer implementation
--! @copyright Sapier
--! @author Sapier
--! @date 2013-01-27

-- ===================================================================

local lcname     = "elk"
local ucname     = "Elk"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =    2         ,
    obr          =    1         ,
    day_mode     = true         ,
    min_light    =   14         ,
    max_light    =   20         ,
    min_height   =    0         ,
    max_height   =  200         ,
    spawn_chance = 8000         ,
    spawn_type   = "animal"     ,

    spawn_nodes  = {
        "default:dirt_with_grass"       ,
        "ethereal:green_dirt"           ,
        "ethereal:green_dirt_top"       ,
        "ethereal:grove_dirt"           ,
        "mg:dirt_with_dry_grass"        ,
    } ,

    spawn_by = {
        "group:grass"                   ,
        "flowers:mushroom_brown"        ,
    } ,

    add_egg   = true                    ,
    egg_image = "wool_pink.png"         ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type ,
    makes_footstep_sound = true  ,

    armor         = 200          ,
    attack_npcs   = false        ,
    attack_type   = "dogfight"   ,
    damage        =   2          ,
    fear_height   =   3          ,
    group_attack  = true         ,
    hp_max        =  15          ,
    hp_min        =   5          ,
    jump_height   =   6          ,
    jump          = true         ,
    owner_loyal   = true         ,
    passive       = false        ,
    pushable      = true         ,
    reach         =   2          ,
    rotate        = 270          ,
    run_velocity  =   3          ,
    stepheight    =   0.6        ,
    type          = "animal"     ,
    view_range    =  10          ,
    walk_velocity =   2          ,

    lava_damage   =   5          ,
    light_damage  =   0          ,
    water_damage  =   0          ,

    collisionbox  = { -0.70, -1.10, -0.70, 0.70, 0.80, 0.70 } ,
    mesh          = msname .. ".b3d"                     ,
    textures      = {{ msname .. "_male.png" }}               ,
    visual        = "mesh"                                    ,

    sounds        = {
    },

    follow        = { "default:apple", "farming:potato" } ,

    drops         = {
        {
            name   = "animal_materials:meat_venison" ,
            chance = 1, min = 1, max = 1             ,
        } ,
        {
            name   = "animal_materials:antlers"   ,
            chance = 1, min = 1, max = 1             ,
        } ,
        {
            name   = "animal_materials:fur_elk"     ,
            chance = 4, min = 1, max = 1             ,
        } ,
        {
            name   = "animal_materials:bone"         ,
            chance = 4, min = 1, max = 1             ,
        } ,
    } ,

    animation     = {
        walk_start   =   0 ,
        walk_end     =  60 ,
        stand_start  =  61 ,
        stand_end    = 120 ,
        speed_normal =  15 ,
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

-- codermobs:alias_mob("codermobs:deer", "codermobs:elk")
-- minetest.register_alias("codermobs:deer", "codermobs:elk")

codermobs.log_done()

-- ===================================================================
-- End of file.
