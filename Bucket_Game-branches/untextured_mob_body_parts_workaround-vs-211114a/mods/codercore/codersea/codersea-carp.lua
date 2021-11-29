-- Carp. Descended from Skandarella version.

local spawnchance = codersea_chance_fish
if    spawnchance < 300 then
      spawnchance = 300 end

local mobname = "codersea:carp"

mobs:register_mob (mobname, {
    stepheight     = 0.0        ,
    type           = "animal"   ,
    passive        = true       ,
    attack_type    = "dogfight" ,
    attack_animals = false      ,
    reach          =   1        ,
    damage         =   1        ,
    hp_min         =   5        ,
    hp_max         =  25        ,
    armor          = 100        ,
    visual         = "mesh"     ,
    sounds         = {}         ,
    walk_velocity  =   2        ,
    run_velocity   =   3        ,
    fly            = true       ,
    fall_speed     =   0        ,
    runaway        = true       ,
    jump           = false      ,
    stepheight     = 0.0        ,
    fear_height    =   2        ,
    floats         =   0        ,
    view_range     =  10        ,

    air_damage     =   1        ,
    lava_damage    =   4        ,
    light_damage   =   0        ,
    water_damage   =   0        ,

    mesh           = "codersea_carp.b3d"       ,
    visual_size    = { x=1.0, y=1.0 }          ,
    textures       = codersea.multiply_texture("codersea_carp.png", 13),

    collisionbox = { -0.40, -0.01, -0.40, 0.40, 0.50, 0.40 } ,
    makes_footstep_sound = false ,

    animation = {
        speed_normal = 100,
        stand_start = 0,
        stand_end = 100,
        walk_start = 150,
        walk_end = 250,
        fly_start = 150, -- swim animation
        fly_end = 250,
        punch_start = 100,
        punch_end = 200,
        -- 50-70 is slide/water idle
    },

    drops = {
        { name = "codersea:sushi",
          chance = 1, min = 1, max = 1 } ,
    } ,

    fly_in = {
        "codersea:water_flowing"      ,
        "codersea:water_source"       ,
        "default:water_flowing"       ,
        "default:water_source"        ,
        "default:water_gel"           ,
        "default:river_water_source"  ,
        "default:river_water_flowing" ,
    } ,

    follow = {
        "ethereal:worm", "seaweed", "fishing:bait_worm",
        "default:grass", "farming:cucumber",
        "farming:cabbage", "animalworld:ant",
        "animalworld:termite", "animalworld:fishfood"
    },

    runaway_from = {
        "animalworld:bear", "animalworld:crocodile",
        "animalworld:tiger", "animalworld:spider",
        "animalworld:spidermale", "animalworld:shark",
        "animalworld:hyena", "animalworld:kobra",
        "animalworld:monitor", "animalworld:snowleopard",
        "animalworld:volverine",
        "livingfloatlands:deinotherium",
        "livingfloatlands:carnotaurus",
        "livingfloatlands:lycaenops",
        "livingfloatlands:smilodon",
        "livingfloatlands:tyrannosaurus",
        "livingfloatlands:velociraptor",
        "animalworld:divingbeetle",
        "animalworld:divingbeetle",
        "animalworld:scorpion",
        "animalworld:polarbear",
        "animalworld:leopardseal",
        "animalworld:stellerseagle", "player"
    } ,

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
    "Carp", "egg_carp.png", 0)

-- ===================================================================
-- End of file.
