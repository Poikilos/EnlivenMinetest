-- Hen. Descended from "Farlands" version.

-- ===================================================================
-- License information for Sapier's 3D-egg media.
--
-- You may  copy,  use,  modify or do nearly anything  but remove this
-- copyright notice. Of course,  you're not allowed to pretend  you've
-- created or written the Sapier pieces.
--
-- CC-BY-SA 3.0. Attribution: Sapier.

-- ===================================================================

local numset = codermobs.numset_if_any

local        codermobs_egg_time_delay   =
    numset ("codermobs_egg_time_delay"   ) or 120
if           codermobs_egg_time_delay   < 3 then
             codermobs_egg_time_delay   = 3
end

local        codermobs_egg_hatch_chance =
    numset ("codermobs_egg_hatch_chance" ) or   3

local EGG_UNFERTILIZED = 1
local EGG_FERTILIZED   = 2

-- ===================================================================

local lcname     = "chicken"
local ucname     = "Chicken"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- This mob is a special case
local obj_hen    = "codermobs:hen"

-- ===================================================================

mobs_param = {
    lcname       = "hen"           ,
    ucname       = "Hen"           ,
    obj_name     = "codermobs:hen" ,

    aoc          =      4       ,
    spawn_chance =  20000       ,

    day_mode     = true         ,
    min_light    =      5       ,
    max_light    =     30       ,
    min_height   = -31000       ,
    max_height   =  31000       ,

    spawn_type   = "animal"     ,

    spawn_nodes  = {
        "default:dirt_with_dry_grass"   ,
        "default:dirt_with_grass"       ,
        "earthgen:dirt_with_dry_grass"  ,
        "ethereal:bamboo_dirt"          ,
        "ethereal:green_dirt"           ,
        "ethereal:green_dirt_top"       ,
        "ethereal:grove_dirt"           ,
        "mg:dirt_with_dry_grass"        ,
        "noisegrid:grass"               ,
    } ,

    add_egg   = true                    ,
    egg_image = "wool_brown.png"        ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

local msname_cooked         = msname           .. "_cooked"
local msname_raw            = msname           .. "_raw"

local msname_img            = msname           .. ".png"
local msname_cooked_img     = msname_cooked    .. ".png"
local msname_raw_img        = msname_raw       .. ".png"

local msname_egg            = msname           .. "_egg"
local msname_egg_fried      = msname_egg       .. "_fried"
local msname_egg_img        = msname_egg       .. ".png"
local msname_egg_fried_img  = msname_egg_fried .. ".png"

local obj_name_cooked       = obj_name         .. "_cooked"
local obj_name_raw          = obj_name         .. "_raw"

local obj_name_egg          = obj_name         .. "_egg"
local obj_name_egg_entity   = obj_name_egg     .. "_entity"
local obj_name_egg_fried    = obj_name_egg     .. "_fried"

-- ===================================================================

local do_breed = function (self)
    local pos        = self.object:getpos()
    local objs       = minetest.get_objects_inside_radius (pos, 12)
    local egg_status = EGG_UNFERTILIZED

    for n = 1, #objs do
        if not objs [n]:is_player() then
            local obj = objs [n]:get_luaentity()
            if obj and obj.name == "codermobs:rooster" then
                egg_status = EGG_FERTILIZED
            end
        end
    end

    minetest.set_node (pos,
        { name = obj_name_egg, param2 = egg_status })

    minetest.sound_play ("chicken_lay_egg", {
        pos  = pos, gain = 1.0, max_hear_distance = 5,
    })
end

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type ,
    makes_footstep_sound = true  ,

    -- Most behavior/sight/battle
    armor          = 200         ,
    attack_type    = "dogfight"  ,
    damage         =   1         ,
    hp_max         =  10         ,
    hp_min         =   5         ,
    passive        = false       ,
    reach          =   1         ,
    runaway        = true        ,
    view_range     =   5         ,

    -- Velocities
    run_velocity   =   3         ,
    walk_velocity  =   1         ,

    -- Step/jump/fall parameters
    fall_damage    =   0         ,
    fall_speed     =  -8         ,
    fear_height    =   5         ,
    jump           = false       ,
    jump_height    =   0         ,
    stepheight     =   1.2       ,

    -- Environment damage
    lava_damage    =   5         ,
    light_damage   =   0         ,
    water_damage   =   1         ,

    -- Misc. parameters
    floats         =   0         ,

--  Too small:
--  collisionbox = {-0.2, 0, -0.2, 0.2, 0.45, 0.2},

--  Too large:
--  collisionbox = {-0.4, 0, -0.4, 0.4, 0.90, 0.4},
--  visual_size = { x=2, y=2 },

    collisionbox     = { -0.30, -0.01 , -0.30, 0.30, 0.66, 0.30 } ,
    mesh             = msname .. ".b3d"                         ,
    textures         = {{ "codermobs_hen_mesh.png" }}           ,
    visual           = "mesh"                                   ,
    visual_size      = { x=1.5, y=1.5 }                         ,

    animation        = {
        stand_start  =  0 ,
        stand_end    = 20 ,
        walk_start   = 25 ,
        walk_end     = 45 ,
        speed_normal = 15 ,
    } ,

    drops            = {
        { name=obj_name_raw, chance=1, min=2, max=2 } ,
    } ,

    follow           = {
        "farming:seed_wheat", "farming:seed_cotton"
    } ,

    sounds           = { random = msname } ,

    specific_attack  = codermobs.make_mob_list ({
        "bug", "beetle"
    }) ,

    on_rightclick = function (self, clicker)
        if mobs:feed_tame (self, clicker, 8, true, true) then
            return
        end
        mobs:protect (self, clicker)
        mobs:capture_mob (self, clicker, 30, 50, 80, false, nil)
    end,

    do_custom = function (self)
        if self.child or math.random (1, 4000) > 1 then return end
        do_breed (self)
    end ,

-- Poikilos June 2019:  false here  prevents  the creation  of a mini-
-- chicken based on the adult mesh.

    on_breed = function (self, ent)
        do_breed (self)
        return false
    end ,
}

-- ===================================================================

codermobs.setup_mob()

mobs:alias_mob ("codermobs:chicken"   , obj_hen)
mobs:alias_mob ("codermobs:chook"     , obj_hen)
mobs:alias_mob ("mobs:chicken"        , obj_hen)
mobs:alias_mob ("mobs_animal:chicken" , obj_hen)

-- ===================================================================
-- Egg throwing item

local egg_GRAVITY = 9
local egg_VELOCITY = 19

-- shoot egg
local mobs_shoot_egg = function (item, player, pointed_thing)

    local playerpos = player:getpos()

    minetest.sound_play("default_place_node_hard", {
        pos = playerpos,
        gain = 1.0,
        max_hear_distance = 5,
    })

    local obj = minetest.add_entity({
        x = playerpos.x,
        y = playerpos.y +1.5,
        z = playerpos.z
    }, obj_name_egg_entity)

    local ent = obj:get_luaentity()
    local dir = player:get_look_dir()

    ent.velocity = egg_VELOCITY -- needed for api internal timing
    ent.switch = 1 -- needed so that egg doesn't despawn straight away

    obj:setvelocity({
        x = dir.x * egg_VELOCITY,
        y = dir.y * egg_VELOCITY,
        z = dir.z * egg_VELOCITY
    })

    obj:setacceleration({
        x = dir.x * -3,
        y = -egg_GRAVITY,
        z = dir.z * -3
    })

    -- pass player name to egg for chick ownership
    local ent2 = obj:get_luaentity()
    ent2.playername = player:get_player_name()
    item:take_item()
    return item
end

-- ===================================================================
-- Egg.

minetest.register_node (obj_name_egg, {
    description = ucname .. " Egg",
    inventory_image  = msname_egg_img ,
    wield_image = msname_egg_img ,
    paramtype = "light",
    walkable = false,
    is_ground_content = true,
    sunlight_propagates = true,

--  This draws the new 3D chicken egg:
--
    drawtype      = "mesh"                                  ,
    mesh          = "codermobs_chicken_egg.b3d"             ,
    tiles         = { "animal_materials_egg_ent_mesh.png" } ,
    selection_box = {
        type = "fixed"                                      ,
        fixed = { -0.12,-0.425,-0.12,0.12,-0.175,0.12 }     ,
    } ,
    visual_scale  = 0.12                                    ,

    groups = {snappy = 2, dig_immediate = 3},

    after_place_node = function(pos, placer, itemstack)
        if placer:is_player() then
            minetest.set_node(pos,
                { name = obj_name_egg, param2 = EGG_UNFERTILIZED })
        end
    end,

    on_construct = function (pos)
        minetest.get_node_timer (pos):start (codermobs_egg_time_delay)
    end ,

    on_use = mobs_shoot_egg ,

    on_timer = function (pos, elapsed)
        local self = minetest.get_node (pos)
        local sp2  = self.param2

        minetest.remove_node (pos)

        if sp2 ~= nil and sp2 == EGG_FERTILIZED then
            local num = math.random (1, codermobs_egg_hatch_chance)
            if    num == 1 then
                minetest.add_entity (pos, "codermobs:baby_chick")
            end
        end
    end ,
})

minetest.register_alias ("codermobs:egg" , obj_name_egg)
minetest.register_alias ("mobs:egg"      , obj_name_egg)
minetest.register_alias ("egg"           , obj_name_egg)

-- ===================================================================
-- Egg entity

mobs:register_arrow (obj_name_egg_entity, {
    visual = "sprite",
    visual_size = {x=.5, y=.5},
    textures = { msname_egg_img } ,
    velocity = 6,

    hit_player = function(self, player)
        player:punch(self.object, 1.0, {
            full_punch_interval = 1.0,
            damage_groups = {fleshy = 1},
        }, nil)
    end,

    hit_mob = function(self, player)
        player:punch(self.object, 1.0, {
            full_punch_interval = 1.0,
            damage_groups = {fleshy = 1},
        }, nil)
    end,

    hit_node = function(self, pos, node)
        local num = math.random(1, 10)

-- RJK 191223: This code is  disabled for now because  it'll presently
-- crash if it's used.

        if false and num == 1 then
            pos.y = pos.y + 1
            local nod = minetest.get_node_or_nil(pos)

            if not nod
            or not minetest.registered_nodes[nod.name]
            or minetest.registered_nodes[nod.name].walkable == true then
                return
            end

            local mob = minetest.add_entity (pos, obj_name)
            local ent2 = mob:get_luaentity()

            mob:set_properties({
                textures = ent2.child_texture[1],
                visual_size = {
                    x = ent2.base_size.x / 2,
                    y = ent2.base_size.y / 2
                },
                collisionbox = {
                    ent2.base_colbox[1] / 2,
                    ent2.base_colbox[2] / 2,
                    ent2.base_colbox[3] / 2,
                    ent2.base_colbox[4] / 2,
                    ent2.base_colbox[5] / 2,
                    ent2.base_colbox[6] / 2
                },
            })

            ent2.child = true
            ent2.tamed = true
            ent2.owner = self.playername
        end
    end
})

-- ===================================================================
-- Fried egg.

minetest.register_craftitem (obj_name_egg_fried, {
    description     = "Fried " .. ucname .. " Egg" ,
    inventory_image = msname_egg_fried_img         ,
    on_use          = minetest.item_eat (2)        ,
})

minetest.register_alias ("mobs:chicken_egg_fried",
                         obj_name_egg_fried)

minetest.register_craft ({
    type   = "cooking"              ,
    recipe = obj_name_egg           ,
    output = obj_name_egg_fried     ,
})

-- ===================================================================
-- Raw bird.
local dep_chicken_raw = nil
if minetest.registered_items["animal_materials:meat_chicken"] then
    dep_chicken_raw = "animal_materials:meat_chicken"
elseif minetest.registered_items["animalmaterials:meat_chicken"] then
    dep_chicken_raw = "animalmaterials:meat_chicken"
end
if not dep_chicken_raw then
    minetest.register_craftitem (obj_name_raw, {
        description = "Raw " .. ucname   ,
        inventory_image = msname_raw_img ,

        on_use = function (itemstack, player, pointed_thing)
            local name = player:get_player_name()
            local msg  = name .. " ate raw " .. ucname .. ". Salmonella!"
            minetest.chat_send_all (msg)
            player:set_hp (player:get_hp() - 2)
        end ,
    })

    minetest.register_alias ("mobs:chicken_raw", obj_name_raw)
else
    minetest.register_alias ("mobs:chicken_raw", dep_chicken_raw)
    minetest.register_alias (obj_name_raw, dep_chicken_raw)
end

-- ===================================================================
-- Cooked bird.

local dep_chicken_cooked = nil
if minetest.registered_items["cooking:meat_chicken_cooked"] then
    dep_chicken_cooked = "cooking:meat_chicken_cooked"
end

if not dep_chicken_cooked then
    minetest.register_craftitem (obj_name_cooked, {
        description     = "Cooked " .. ucname ,
        inventory_image = msname_cooked_img   ,
        on_use = minetest.item_eat (6)        ,
    })

    minetest.register_alias ("mobs:chicken_cooked",
                             obj_name_cooked)
else
    minetest.register_alias ("mobs:chicken_cooked", dep_chicken_cooked)
    minetest.register_alias (obj_name_cooked, dep_chicken_cooked)
end

minetest.register_craft ({
    type   = "cooking"          ,
    recipe = obj_name_raw       ,
    output = obj_name_cooked    ,
})

-- ===================================================================
-- Chicken feather.

minetest.register_craftitem ("codermobs:chicken_feather", {
    description     = "Feather"                       ,
    inventory_image = "codermobs_chicken_feather.png" ,
})

minetest.register_alias ("mobs:chicken_feather",
                         "codermobs:chicken_feather")

-- ===================================================================

codermobs.log_done()

-- ===================================================================
-- End of file.
