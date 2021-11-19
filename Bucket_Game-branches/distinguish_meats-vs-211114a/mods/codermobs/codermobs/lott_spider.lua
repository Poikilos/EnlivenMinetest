-- Giant Spider. Descended from LOTT version.

-- ===================================================================

local lcname     = "lott_spider"
local ucname     = "LOTT Spider"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =     -1       ,
    spawn_chance = 120000       ,

    day_mode     = true         ,
    min_light    =      0       ,
    max_light    =     30       ,
    min_height   = -31000       ,
    max_height   =  31000       ,

    spawn_type   = "npc"        ,

    spawn_nodes  = {
        "default:junglegrass"           ,
        "default:jungleleaves"          ,
        "default:jungletree"            ,
    } ,

    add_egg   = true                    ,
    egg_image = "default_stone.png"     ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

minetest.register_craftitem (obj_name .. "_meat", {
    description = "Cooked Spider",
    inventory_image = msname .. "_meat.png",
    on_use = minetest.item_eat (4),
})

minetest.register_craftitem (obj_name .. "_meat_raw", {
    description = "Raw Spider",
    inventory_image = msname .. "_meat_raw.png",
})

minetest.register_craft ({
    type = "cooking",
    output = obj_name .. "_meat",
    recipe = obj_name .. "_meat_raw",
})

mobs_param.core_param = {
    type = mobs_param.spawn_type ,
    passive = false,
    attacks_monsters = true,
    hp_min = 15,
    hp_max = 30,
    collisionbox = {-0.9, -0.01, -0.7, 0.7, 0.6, 0.7},
    textures = { msname .. ".png"} ,
    visual_size = {x=7,y=7},
    visual = "mesh",
    mesh = msname .. ".x",
    makes_footstep_sound = true,
    view_range = 15,
    walk_velocity = 1,
    run_velocity = 3,
    armor = 200,
    damage = 3,
    stepheight    = 1.2         ,
    jump_height   =   0         ,
    jump          = false       ,

    drops = {
        { name   = "farming:string"         ,
          chance = 2, min = 1, max = 3 }    ,
        { name   = obj_name .. "_meat_raw"  ,
          chance = 4, min = 1, max = 2 }    ,
    } ,

    light_resistant = true,
    drawtype = "front",
    water_damage = 5,
    floats = 0,
    runaway = true,
    lava_damage = 5,
    light_damage = 0,
    on_rightclick = nil,
    attack_type = "dogfight",

    animation = {
        speed_normal = 15,
        speed_run = 15,
        stand_start = 1,
        stand_end = 1,
        walk_start = 20,
        walk_end = 40,
        run_start = 20,
        run_end = 40,
        punch_start = 50,
        punch_end = 90,
    },
    blood_texture = msname .. "_blood.png",

    sounds = {
        war_cry = "codermobs_eerie"                    ,
        damage  = "codermobs_damage_giant_exoskeleton" ,
        death   = "codermobs_death_giant_bug"          ,
        attack  = "codermobs_use_giant_exoskeleton"    ,
    },
}

-- ===================================================================

codermobs.setup_mob()
mobs:alias_mob ("mobs_monster:spider" , obj_name)
codermobs.log_done()

-- ===================================================================
-- End of file.
