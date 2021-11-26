-- Tiger. Descended from Skandarella version.

-- ===================================================================

local lcname     = "tiger"
local ucname     = "Tiger"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =   -1         ,
    spawn_chance = 8000         ,

    day_mode     = true         ,
    min_light    =    0         ,
    max_light    =   20         ,
    min_height   =    1         ,
    max_height   =   50         ,

    spawn_type   = "monster"    ,

    spawn_nodes  = {
        "default:dirt_with_rainforest_litter" ,
        "ethereal:green_dirt"                 ,
        "ethereal:grass_grove"                ,
    } ,

    add_egg   = true            ,
    egg_image = "egg_tiger.png" ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type ,
    makes_footstep_sound = true  ,

    armor          =  100         ,
    attack_animals = true         ,
    attack_npcs    = true         ,
    attack_type    = "dogfight"   ,
    damage         =   13         ,
    fear_height    =    4         ,
    group_attack   = true         ,
    hp_max         =   75         ,
    hp_min         =   45         ,
    owner_loyal    = false        ,
    passive        = false        ,
    pushable       = false        ,
    reach          =    2         ,
    runaway        = false        ,
    view_range     =   15         ,

    floats         =    0         ,
    jump           = true         ,
    jump_height    =    6         ,
    run_velocity   =    4         ,
    stepheight     =    2         ,
    walk_velocity  =    2         ,

    air_damage     =    0         ,
    lava_damage    =    4         ,
    light_damage   =    0         ,
    water_damage   =    0         ,

    collisionbox  = { -0.50, -0.01, -0.50, 0.50, 0.95, 0.50 } ,
    mesh          =    msname .. ".b3d"    ,
    textures      = {{ msname .. ".png" }} ,
    visual        = "mesh"                 ,

    animation = {
        speed_normal = 100 ,
        stand_start  =   0 ,
        stand_end    = 100 ,
        walk_start   = 100 ,
        walk_end     = 200 ,
        punch_start  = 200 ,
        punch_end    = 300 ,
        -- 50-70 is slide/water idle
    } ,

    drops = {
        { name="mobs:meat_raw", chance=1, min=1, max=1 } ,
    } ,

    follow = {
        "ethereal:fish_raw"         ,
        "animalworld:rawfish"       ,
        "mobs_fish:tropical"        ,
        "mobs:meat_raw"             ,
        "animalworld:rabbit_raw"    ,
        "animalworld:pork_raw"      ,
        "water_life:meat_raw"       ,
        "animalworld:chicken_raw"   ,
    } ,

    sounds        = {
        random = "codermobs_tiger" ,
        attack = "codermobs_tiger" ,
    } ,

    on_rightclick = function (self, clicker)
        if mobs:feed_tame    (self, clicker, 4, true, true) then
            return
        end
        if mobs:protect      (self, clicker) then return end

        if mobs:capture_mob  (self, clicker,
5, 50, 80, false, nil) then
            return
        end
    end ,
}

-- ===================================================================

codermobs.setup_mob()
codermobs.log_done()

-- ===================================================================
-- End of file.
