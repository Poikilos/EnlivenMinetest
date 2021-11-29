-- Trout. Descended from Skandarella version.

local spawnchance = codersea_chance_fish
if    spawnchance < 300 then
      spawnchance = 300 end

local mobname = "codersea:trout"

mobs:register_mob (mobname, {
    type           = "animal"   ,
    armor          = 100        ,
    attack_type    = "dogfight" ,
    attack_animals = false      ,
    damage         =   1        ,
    hp_max         =  25        ,
    hp_min         =   5        ,
    passive        = true       ,
    reach          =   1        ,
    run_velocity   =   3        ,
    runaway        = true       ,
    view_range     =  10        ,
    walk_velocity  =   2        ,

    stepheight     = 0.0        ,
    fly            = true       ,
    sounds         = {}         ,
    visual         = "mesh"     ,
    fall_speed     =   0        ,
    jump           = false      ,
    fear_height    =   2        ,
    floats         =   0        ,

    air_damage     =   1        ,
    lava_damage    =   4        ,
    light_damage   =   0        ,
    water_damage   =   0        ,

    collisionbox = { -0.4, -0.01, -0.4, 0.4, 0.4, 0.4 } ,
    mesh = "codersea_trout.b3d",
    visual_size = { x=1.0, y=1.0 } ,
    textures = {{ "codersea_trout.png" }} ,
    makes_footstep_sound = false,

    fly_in = {
        "codersea:water_flowing"      ,
        "codersea:water_source"       ,
        "default:water_flowing"       ,
        "default:water_source"        ,
        "default:water_gel"           ,
        "default:river_water_source"  ,
        "default:river_water_flowing" ,
    } ,

    runaway_from = {"codermobs:bear", "codersea:crocodile", "codermobs:tiger", "animalworld:spider", "animalworld:spidermale", "animalworld:shark", "animalworld:hyena", "animalworld:kobra", "animalworld:monitor", "animalworld:snowleopard", "animalworld:volverine", "livingfloatlands:deinotherium", "livingfloatlands:carnotaurus", "livingfloatlands:lycaenops", "livingfloatlands:smilodon", "codermobs:tyrannosaurus", "codermobs:velociraptor", "codermobs:divingbeetle", "codermobs:scorpion", "codermobs:polarbear", "codermobs:leopardseal", "codermobs:stellerseagle", "player"},

    drops = {
        { name = "codersea:sushi", chance = 1, min = 1, max = 1 } ,
    } ,

    animation = {
        speed_normal = 125,
        stand_start = 0,
        stand_end = 100,
        walk_start = 150,
        walk_end = 250,
        fly_start = 150 , -- swim animation
        fly_end = 250,
        punch_start = 100,
        punch_end = 200,
        -- 50-70 is slide/water idle
    },

    fly_in = {
        "default:water_source", "default:river_water_source", "default:water_flowing"
    } ,

    follow = {
        "mobs:meat_raw", "codermobs:ant", "ethereal:worm", "fishing:bait_worm", "water_life:meat_raw", "xocean:fish_edible", "codermobs:fishfood"
    },

    on_rightclick = function (self, clicker)
        if mobs:feed_tame    (self, clicker, 4, false, true) then
            return
        end
        if mobs:protect      (self, clicker) then return end
        if mobs:capture_mob  (self, clicker,
            5, 50, 80, false, nil) then
            return
        end
    end ,
})

-- ===================================================================

mobs:spawn_specific (mobname     ,
    codersea.default_spawn_nodes ,
    codersea.default_spawn_near  ,
     5, 30, 30, spawnchance, codersea_aoc_fish, -31000, 0)

mobs:register_egg   (mobname     ,
    "Trout", "egg_trout.png", 0)

-- ===================================================================
-- End of file.
