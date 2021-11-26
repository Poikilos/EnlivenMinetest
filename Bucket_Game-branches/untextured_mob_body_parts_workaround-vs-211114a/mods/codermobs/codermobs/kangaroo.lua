-- Kangaroo. Descended from Skandarella version.

-- ===================================================================

local lcname     = "kangaroo"
local ucname     = "Kangaroo"
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
    max_light    =   30         ,
    min_height   =    1         ,
    max_height   =  150         ,

    spawn_type   = "animal"     ,

    spawn_nodes  = {
        "default:desert_sand"             ,
        "default:dry_dirt_with_dry_grass" ,
        "ethereal:dry_dirt"               ,
        "ethereal:grass_grove"            ,
    } ,

    add_egg   = true               ,
    egg_image = "egg_kangaroo.png" ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

local dup_texture_count = 18
local multimesh_textures = {}
for multimesh_texture_i = 1,dup_texture_count,1
do
    multimesh_textures[multimesh_texture_i] = msname .. ".png"
end

mobs_param.core_param = {
    type = mobs_param.spawn_type ,
    makes_footstep_sound = true  ,

    armor         =  100         ,
    attack_npcs   = false        ,
    attack_type   = "dogfight"   ,
    damage        =    2         ,
    fear_height   =    4         ,
    floats        =    0         ,
    group_attack  = true         ,
    hp_max        =   55         ,
    hp_min        =   25         ,
    jump          = true         ,
    jump_height   =    8         ,
    owner_loyal   = true         ,
    passive       = false        ,
    pushable      = true         ,
    reach         =    2         ,
    run_velocity  =    5         ,
    runaway       = true         ,
    stepheight    =    2         ,
    view_range    =   10         ,
    walk_velocity =    5         ,

    air_damage    =    0         ,
    lava_damage   =    5         ,
    light_damage  =    0         ,
    water_damage  =    0         ,

    collisionbox  = { -0.50, -0.01, -0.50, 0.50, 0.95, 0.50 } ,
    mesh          =    msname .. ".b3d"    ,
    textures      = multimesh_textures     ,
    visual        = "mesh"                 ,

    animation = {
        speed_normal = 100   ,
        stand_start  =   0   ,
        stand_end    = 100   ,
        walk_start   = 100   ,
        walk_end     = 200   ,
        punch_start  = 200   ,
        punch_end    = 300   ,

        die_start    =   1   ,
        die_end      =   2   ,
        die_speed    =   1   ,
        die_loop     = false ,
        die_rotate   = true  ,
    } ,

    drops = {
        { name="mobs:meat_raw", chance=1, min=1, max=1 } ,
    } ,

    follow        = {
        "default:grass_3"         ,
        "default:dry_grass_3"     ,
        "ethereal:dry_shrub"      ,
        "farming:lettuce"         ,
        "farming:seed_wheat"      ,
        "default:junglegrass"     ,
    } ,

    runaway_from  = {
        "animalworld:bear"        ,
        "animalworld:crocodile"   ,
        "animalworld:tiger"       ,
        "animalworld:spider"      ,
        "animalworld:spidermale"  ,
        "animalworld:shark"       ,
        "animalworld:hyena"       ,
        "animalworld:kobra"       ,
        "animalworld:monitor"     ,
        "animalworld:snowleopard" ,
        "animalworld:volverine"   ,
        "player"
    } ,

    sounds        = {
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
}

-- ===================================================================

codermobs.setup_mob()
codermobs.log_done()

-- ===================================================================
-- End of file.
