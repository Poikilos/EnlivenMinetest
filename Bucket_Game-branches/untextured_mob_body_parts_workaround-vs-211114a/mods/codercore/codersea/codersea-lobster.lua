-- Lobster. Descended from Skandarella version.

local spawnchance = codersea_chance_lobster
if    spawnchance < 300 then
      spawnchance = 300 end

local mobname = "codersea:lobster"

mobs:register_mob (mobname, {
    type          = "animal"    ,
    armor         = 100         ,
    attack_npcs   = false       ,
    attack_type   = "dogfight"  ,
    damage        =   5         ,
    fear_height   =   2         ,
    floats        =   0         ,
    group_attack  = true        ,
    hp_max        =  70         ,
    hp_min        =  25         ,
    jump          = false       ,
    jump_height   =   3         ,
    owner_loyal   = true        ,
    passive       = false       ,
    pushable      = true        ,
    reach         =   2         ,
    run_velocity  =   1.0       ,
    runaway       = true        ,
    stepheight    =   1         ,
    view_range    =  10         ,
    walk_velocity =   0.5       ,

    air_damage    =   1         ,
    lava_damage   =   5         ,
    light_damage  =   0         ,
    water_damage  =   0         ,

    sounds        = {}          ,

    collisionbox = { -0.6, -0.01, -0.6, 0.6, 0.5, 0.6 } ,
    visual       = "mesh"                       ,
    mesh         =    "codersea_lobster.b3d"    ,
    textures     = codersea.multiply_texture("codersea_lobster.png", 27),

    makes_footstep_sound = true,

    animation = {
        speed_normal = 50,
        stand_start = 0,
        stand_end = 100,
        walk_start = 100,
        walk_end = 200,
        punch_start = 200,
        punch_end = 300,

        die_start = 1, -- we dont have a specific death animation so we will
        die_end = 2, --   re-use 2 standing frames at a speed of 1 fps and
        die_speed = 1, -- have mob rotate when dying.
        die_loop = false,
        die_rotate = true,
    } ,

    runaway_from = {
        "animalworld:bear"               ,
        "animalworld:crocodile"          ,
        "animalworld:tiger"              ,
        "animalworld:spider"             ,
        "animalworld:spidermale"         ,
        "animalworld:shark"              ,
        "animalworld:hyena"              ,
        "animalworld:kobra"              ,
        "animalworld:monitor"            ,
        "animalworld:snowleopard"        ,
        "animalworld:volverine"          ,
        "livingfloatlands:deinotherium"  ,
        "livingfloatlands:carnotaurus"   ,
        "livingfloatlands:lycaenops"     ,
        "livingfloatlands:smilodon"      ,
        "livingfloatlands:tyrannosaurus" ,
        "livingfloatlands:velociraptor"  ,
        "animalworld:divingbeetle"       ,
        "animalworld:scorpion"           ,
        "animalworld:polarbear"          ,
        "animalworld:leopardseal"        ,
        "animalworld:stellerseagle"      ,
        "player"
    } ,

    follow = {
        "animalworld:rawfish"    ,
        "mobs_fish:tropical"     ,
        "mobs:clownfish_raw"     ,
        "mobs:bluefish_raw"      ,
        "fishing:bait_worm"      ,
        "fishing:clownfish_raw"  ,
        "fishing:bluewhite_raw"  ,
        "fishing:exoticfish_raw" ,
        "fishing:fish_raw"       ,
        "fishing:carp_raw"       ,
        "fishing:perch_raw"      ,
        "water_life:meat_raw"    ,
        "fishing:shark_raw"      ,
        "fishing:pike_raw"       ,
    } ,

    drops = {
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

    on_rightclick = function (self, clicker)
        if mobs:feed_tame    (self, clicker, 8, true, true) then
            return
        end
        if mobs:protect      (self, clicker) then return end
        if mobs:capture_mob  (self, clicker,
            0, 5, 50, false, nil) then
            return
        end
    end ,
})

-- ===================================================================

mobs:spawn_specific (mobname     ,
    codersea.default_spawn_nodes ,
    codersea.default_spawn_near  ,
     0, 30, 30, spawnchance, codersea_aoc_lobster, -31000, 0)

mobs:register_egg   (mobname     ,
    "Lobster", "egg_lobster.png", 0)

-- ===================================================================
-- End of file.
