-- Snail. Descended from Skandarella version.

-- ===================================================================

local lcname     = "snail"
local ucname     = "Snail"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =     -1       ,
    spawn_chance =  40000       ,

    day_mode     = true         ,
    min_light    =      0       ,
    max_light    =     20       ,
    min_height   =      2       ,
    max_height   =    200       ,

    spawn_type   = "animal"     ,

    spawn_nodes  = {
        "default:dirt_with_dry_grass"   ,
        "ethereal:mushroom_dirt"        ,
    } ,

    spawn_by = {
        "group:grass"                   ,
        "flowers:mushroom_brown"        ,
        "farming:cucumber"              ,
        "flowers:dandelion_yellow"      ,
    } ,

    add_egg   = true                    ,
    egg_image = "egg_snail.png"         ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type ,
    makes_footstep_sound = true  ,

    armor         = 100          ,
    attack_npcs   = false        ,
    attack_type   = "dogfight"   ,
    damage        =   0          ,
    fear_height   =   3          ,
    floats        =   0          ,
    group_attack  = true         ,
    hp_max        =  20          ,
    hp_min        =  10          ,
    stepheight    =   3          ,
    jump          = false        ,
    jump_height   =   3          ,
    owner_loyal   = true         ,
    passive       = true         ,
    pushable      = true         ,
    reach         =   2          ,
    run_velocity  =   0.4        ,
    runaway       = false        ,
    type          = "animal"     ,
    view_range    =   5          ,
    walk_velocity =   0.2        ,

    lava_damage   =   5          ,
    light_damage  =   0          ,
    water_damage  =   1          ,

    collisionbox  = { -0.20, -0.01, -0.20, 0.20, 0.30, 0.20 } ,
    mesh          = msname .. ".b3d"                          ,
    textures      = {{ msname .. ".png" }}                    ,
    visual        = "mesh"                                    ,

    animation     = {
        speed_normal =  25   ,
        stand_start  =   0   ,
        stand_end    = 100   ,
        walk_start   = 100   ,
        walk_end     = 200   ,
        die_start    =   1   ,
        die_end      =   2   ,
        die_speed    =   1   ,
        die_loop     = false ,
        die_rotate   = true  ,
    } ,

    sounds        = {
    } ,

    follow        = {
        "default:apple"                   ,
        "default:dry_dirt_with_dry_grass" ,
        "farming:seed_wheat"              ,
        "default:junglegrass"             ,
        "farming:seed_oat"                ,
        "default:kelp"                    ,
        "seaweed"                         ,
        "xocean:kelp"                     ,
        "default:grass"                   ,
        "farming:cucumber"                ,
        "farming:cabbage"                 ,
        "xocean:seagrass"                 ,
        "farming:lettuce"                 ,
        "default:junglegrass"
    } ,

    drops = {
        {
            name   = "codermobs:snail" ,
            chance = 3                 ,
            min    = 1                 ,
            max    = 1                 ,
        } ,
    } ,

    on_rightclick = function (self, clicker)
        if mobs:feed_tame (self, clicker, 8, true, true) then
            return
        end
        if mobs:protect (self, clicker) then return end

        if mobs:capture_mob (self, clicker,
30, 50, 80, false, nil) then
            return
        end
    end ,
}

-- ===================================================================

minetest.register_craftitem (":codermobs:escargot", {
    description     = ("Escargot")                      ,
    inventory_image = "codermobs_escargot.png"          ,
    on_use          = minetest.item_eat (2)             ,
    groups          = { food_meat_raw=1, flammable=2 }  ,
})

minetest.register_craft ({
    output = "codermobs:escargot" ,
    type   = "shapeless"          ,
    recipe =  {
        "codermobs:snail"         ,
        "group:food_garlic_clove" ,
        "group:food_butter"       ,
        "farming:bread"           ,
    } ,
})

-- ===================================================================

codermobs.setup_mob()
codermobs.log_done()

-- ===================================================================
-- End of file.
