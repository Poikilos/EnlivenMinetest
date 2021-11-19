-- Warthog. Descended from KrupnoPavel version.

-- ===================================================================

local lcname     = "warthog"
local ucname     = "Warthog"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =     -1       ,
    spawn_chance =  80000       ,

    day_mode     = true         ,
    min_light    =     14       ,
    max_light    =     20       ,
    min_height   =      0       ,
    max_height   =    200       ,

    spawn_type   = "animal"     ,

    spawn_nodes  = {
        "default:dirt_with_dry_grass"   ,
        "ethereal:mushroom_dirt"        ,
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

mobs_param.core_param = {
    type = mobs_param.spawn_type ,
    makes_footstep_sound = true  ,

    armor         = 200          ,
    attack_npcs   = false        ,
    attack_type   = "dogfight"   ,
    damage        =   2          ,
    fear_height   =   2          ,
    floats        =   0          ,
    group_attack  = true         ,
    hp_max        =  15          ,
    hp_min        =   5          ,
    stepheight    = 1.2          ,
    jump_height   =   0          ,
    jump          = false        ,
    owner_loyal   = true         ,
    passive       = false        ,
    pushable      = true         ,
    reach         =   2          ,
    run_velocity  =   3          ,
    runaway       = true         ,
    type          = "animal"     ,
    view_range    =  10          ,
    walk_velocity =   2          ,

    lava_damage   =   5          ,
    light_damage  =   0          ,
    water_damage  =   1          ,

    collisionbox  = { -0.40, -0.01, -0.40, 0.40, 0.95, 0.40 } ,
    mesh          = msname .. ".x"                            ,
    textures      = {{ msname .. ".png" }}                    ,
    visual        = "mesh"                                    ,

    animation     = {
        stand_start  =  25 ,
        stand_end    =  55 ,
        punch_start  =  70 ,
        punch_end    = 100 ,
        walk_start   =  70 ,
        walk_end     = 100 ,
        speed_normal =  15 ,
    } ,

    sounds        = {
        random = "mobs_pig",
        attack = "mobs_pig_angry",
    } ,

    follow        = { "default:apple", "farming:potato" } ,

    drops         = {
        { name="mobs:pork_raw", chance=1, min=1, max=3 } ,
    } ,

    specific_attack = codermobs.make_mob_list ({
        "rat" , "rat_better", "chicken",
    }) ,

    on_rightclick = function (self, clicker)
        if mobs:feed_tame(self, clicker, 8, true, true) then return end
        if mobs:protect(self, clicker) then return end

        if mobs:capture_mob(self, clicker, 0, 5, 50, false, nil) then
            return
        end
    end,
}

-- ===================================================================

-- raw porkchop
local dep_pork_raw = nil
if minetest.registered_items["animal_materials:meat_pork"] then
    dep_pork_raw = "animal_materials:meat_pork"
elseif minetest.registered_items["animalmaterials:meat_pork"] then
    dep_pork_raw = "animalmaterials:meat_pork"
end
if not dep_pork_raw then
    minetest.register_craftitem(":mobs:pork_raw", {
        description = "Raw Porkchop" ,
        inventory_image = "codermobs_pork_raw.png",
        on_use = minetest.item_eat(4),
        groups = {food_meat_raw = 1, food_pork_raw = 1, flammable = 2},
    })
else
    minetest.register_alias("mobs:pork_raw", dep_pork_raw)
end

-- cooked porkchop
minetest.register_craftitem(":mobs:pork_cooked", {
    description = "Cooked Porkchop" ,
    inventory_image = "codermobs_pork_cooked.png",

    on_use = minetest.item_eat(8),
    groups = {food_meat = 1, food_pork = 1, flammable = 2},
})

minetest.register_craft({
    type = "cooking",
    output = "mobs:pork_cooked",
    recipe = "mobs:pork_raw",
    cooktime = 5,
})

-- ===================================================================

codermobs.setup_mob()
mobs:alias_mob ("mobs:pumba"        , obj_name)
mobs:alias_mob ("mobs:warthog"      , obj_name)
mobs:alias_mob ("mobs_animal:pumba" , obj_name)
codermobs.log_done()

-- ===================================================================
-- End of file.
