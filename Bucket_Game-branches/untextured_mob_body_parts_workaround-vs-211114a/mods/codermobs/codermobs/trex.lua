-- T-Rex. Descended from Skandarella version.

-- ===================================================================

local lcname     = "trex"
local ucname     = "T-Rex"
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
    max_height   =  500         ,

    spawn_type   = "monster"    ,

    spawn_nodes  = {
        "ethereal:prairie_dirt"               ,
        "ethereal:dry_dirt"                   ,
        "default:dry_dirt_with_dry_grass"     ,
        "default:dirt_with_rainforest_litter" ,
        "default:sand"                        ,
    } ,

    add_egg   = true           ,
    egg_image = "egg_trex.png" ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

local dup_texture_count = 30
local multimesh_textures = {}
for multimesh_texture_i = 1,dup_texture_count,1
do
    multimesh_textures[multimesh_texture_i] = msname .. ".png"
end


mobs_param.core_param = {
    type = mobs_param.spawn_type  ,
    makes_footstep_sound = true   ,

    armor          =  100         ,
    attack_animals = true         ,
    attack_npcs    = true         ,
    attack_type    = "dogfight"   ,
    damage         =   30         ,
    fear_height    =    3         ,
    group_attack   = true         ,
    hp_max         =  550         ,
    hp_min         =  300         ,
    owner_loyal    = false        ,
    passive        = false        ,
    pathfinding    = true         ,
    pushable       = false        ,
    reach          =    6         ,
    runaway        = false        ,
    view_range     =   10         ,

    floats         =    0         ,
    jump           = false        ,
    jump_height    =    6         ,
    run_velocity   =    3         ,
    stepheight     =    1         ,
    walk_chance    =   20         ,
    walk_velocity  =    3         ,

    air_damage     =    0         ,
    lava_damage    =    4         ,
    light_damage   =    0         ,
    water_damage   =    0         ,

	collisionbox   = { -1.20, -0.01, -1.00, 1.20, 1.50, 1.00 } ,
    mesh           =    msname .. ".b3d"    ,
    textures       = multimesh_textures     ,
    visual         = "mesh"                 ,

	animation      = {
		speed_normal = 30,
		stand_start = 250,
		stand_end = 350,
		walk_speed = 75,
		walk_start = 0,
		walk_end = 100,
		punch_speed = 100,
		punch_start = 100,
		punch_end = 200,
		-- 50-70 is slide/water idle
	} ,

    drops = {
        { name="mobs:meat_raw", chance=1, min=1, max=1 } ,
    } ,

    follow         = {
    } ,

	follow         = {
		"ethereal:fish_raw"       ,
		"animalworld:rawfish"     ,
		"mobs_fish:tropical"      ,
		"mobs:meat_raw"           ,
		"animalworld:rabbit_raw"  ,
		"animalworld:pork_raw"    ,
		"water_life:meat_raw"     ,
		"animalworld:chicken_raw" ,
	} ,

    sounds         = {
		random   = "codermobs_trex1" ,
		attack   = "codermobs_trex2" ,
        distance = 20 ,
    } ,

    on_rightclick  = function (self, clicker)
        if mobs:feed_tame     (self, clicker, 4, true, true) then
            return
        end
        if mobs:protect       (self, clicker) then return end

        if mobs:capture_mob   (self, clicker,
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
