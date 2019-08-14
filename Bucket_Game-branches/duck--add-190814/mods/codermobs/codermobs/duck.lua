-- Duck. Descended from Sapier Ostrich.

-- ===================================================================
-- Media license. Applies to model and associated texture.
--
-- You may  copy,  use,  modify or do nearly anything  but remove this
-- copyright notice. Of course,  you're not allowed to pretend  you've
-- created or written the Sapier, Poikilos, or OldCoder pieces.
--
-- CC-BY-SA 3.0. Attribution: Sapier, Poikilos, and OldCoder.

-- ===================================================================

local lcname     = "duck"
local ucname     = "Duck"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =    2         ,
    day_mode     = true         ,
    min_light    =   14         ,
    max_light    =   20         ,
    min_height   =    0         ,
    max_height   =  200         ,
    spawn_chance = 50000        ,
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

-- Chicken-based  images  stand in for  ostrich-based  images  in some
-- cases.

local mcname                = "codermobs_duck"

local msname_cooked         = mcname           .. "_cooked"
local msname_raw            = mcname           .. "_raw"

local msname_img            = mcname           .. ".png"
local msname_cooked_img     = msname_cooked    .. ".png"
local msname_raw_img        = msname_raw       .. ".png"

local msname_egg            = mcname           .. "_egg"
local msname_egg_fried      = msname_egg       .. "_fried"
local msname_egg_fried_img  = msname_egg_fried .. ".png"
local msname_egg_img        = msname_egg       .. ".png"

local obj_name_cooked       = obj_name         .. "_cooked"
local obj_name_raw          = obj_name         .. "_raw"

local obj_name_egg          = obj_name         .. "_egg"
local obj_name_egg_entity   = obj_name_egg     .. "_entity"
local obj_name_egg_fried    = obj_name_egg     .. "_fried"

-- ===================================================================

mobs_param.core_param = {
    type = mobs_param.spawn_type ,
    makes_footstep_sound = true  ,

    armor         = 200          ,
    attack_npcs   = false        ,
    attack_type   = "dogfight"   ,
    damage        =   2          ,
    fear_height   =   3          ,
    floats        =   0          ,
    group_attack  = true         ,
    hp_max        =  15          ,
    hp_min        =   5          ,
    jump_height   =   6          ,
    jump          = true         ,
    owner_loyal   = true         ,
    passive       = false        ,
    pushable      = true         ,
    reach         =   2          ,
    runaway       = true         ,
    stepheight    =   0.6        ,
    type          = "animal"     ,
    view_range    =  10          ,

    lava_damage   =   5          ,
    light_damage  =   0          ,
    water_damage  =   1          ,

    collisionbox  = { -0.22, 0.0, -0.22, 0.22, 0.48, 0.22 } ,
    mesh          = "codermobs_duck-hd.b3d"                   ,
    rotate        = 0                                       ,
    textures      = { "codermobs_duck_mallard_male.png" } ,
    child_texture = { "codermobs_duck_mallard_male.png" } ,
    visual        = "mesh"                                    ,

    sounds        = {
    } ,

    follow        = { "farming:seed_wheat", "farming:seed_cotton" } ,

    drops         = {
        {
            name   = "animal_materials:meat" ,
            chance = 1 , min = 1, max = 3 ,
        } ,
    } ,

    walk_velocity =   0.444 ,
    run_velocity  =   1.778 ,

    animation     = {
        stand_start  = 0 ,
        stand_end    = 2 ,
        speed_normal = 8 ,
        walk_start   = 3 ,
        walk_end     = 11 ,
		speed_run    = 32,
        run_start    = 3 ,
        run_end      = 11 ,
    },

    on_rightclick = function (self, clicker)
        if mobs:feed_tame(self, clicker, 8, true, true) then return end
        if mobs:protect(self, clicker) then return end

        if mobs:capture_mob(self, clicker, 0, 5, 50, false, nil) then
            return
        end
    end,
}

-- ===================================================================

codermobs.setup_mob()

-- ===================================================================
-- Egg.

--minetest.register_node (obj_name_egg, {
    --description = ucname .. " Egg",
    --inventory_image  = msname_egg_img ,
    --wield_image = msname_egg_img ,
    --paramtype = "light",
    --walkable = false,
    --is_ground_content = true,
    --sunlight_propagates = true,

    --drawtype      = "mesh"                                  ,
    --mesh          = "animal-materials-egg.b3d"              ,
    --tiles         = { "animal_materials_egg_ent_mesh.png" } ,
    --visual_scale  = 0.24                                    ,

    --selection_box = {
        --type = "fixed" ,
        --fixed = { -0.25, -0.25, -0.25, 0.25, 0.25, 0.24 } ,
    --} ,

    --groups = {snappy = 2, dig_immediate = 3},
    --after_place_node = function(pos, placer, itemstack)
        --if placer:is_player() then
            --minetest.set_node(pos, {name = obj_name_egg, param2 = 1})
        --end
    --end,
--})

-- ===================================================================
-- Egg entity.

--mobs:register_arrow (obj_name_egg_entity, {
    --visual = "sprite",
    --visual_size = {x=.5, y=.5},
    --textures = { msname_egg_img } ,
    --velocity = 6,

    --hit_player = function(self, player)
        --player:punch(self.object, 1.0, {
            --full_punch_interval = 1.0,
            --damage_groups = {fleshy = 1},
        --}, nil)
    --end,

    --hit_mob = function(self, player)
        --player:punch(self.object, 1.0, {
            --full_punch_interval = 1.0,
            --damage_groups = {fleshy = 1},
        --}, nil)
    --end,

    --hit_node = function(self, pos, node)
        --local num = math.random(1, 10)

        --if num == 1 then
            --pos.y = pos.y + 1
            --local nod = minetest.get_node_or_nil(pos)

            --if not nod
            --or not minetest.registered_nodes[nod.name]
            --or minetest.registered_nodes[nod.name].walkable == true then
                --return
            --end

            --local mob = minetest.add_entity (pos, obj_name)
            --local ent2 = mob:get_luaentity()

            --mob:set_properties({
                --textures = ent2.child_texture[1],
                --visual_size = {
                    --x = ent2.base_size.x / 2,
                    --y = ent2.base_size.y / 2
                --},
                --collisionbox = {
                    --ent2.base_colbox[1] / 2,
                    --ent2.base_colbox[2] / 2,
                    --ent2.base_colbox[3] / 2,
                    --ent2.base_colbox[4] / 2,
                    --ent2.base_colbox[5] / 2,
                    --ent2.base_colbox[6] / 2
                --},
            --})

            --ent2.child = true
            --ent2.tamed = true
            --ent2.owner = self.playername
        --end
    --end
--})

-- Egg-throwing item

--local egg_GRAVITY = 9
--local egg_VELOCITY = 19

-- Shoot egg
--local mobs_shoot_egg = function (item, player, pointed_thing)

    --local playerpos = player:getpos()

    --minetest.sound_play ("default_place_node_hard", {
        --pos = playerpos,
        --gain = 1.0,
        --max_hear_distance = 5,
    --})

    --local obj = minetest.add_entity({
        --x = playerpos.x,
        --y = playerpos.y +1.5,
        --z = playerpos.z
    --}, obj_name_egg_entity)

    --local ent = obj:get_luaentity()
    --local dir = player:get_look_dir()

    --ent.velocity = egg_VELOCITY -- needed for api internal timing
    --ent.switch = 1 -- needed so that egg doesn't despawn straight away

    --obj:setvelocity({
        --x = dir.x * egg_VELOCITY,
        --y = dir.y * egg_VELOCITY,
        --z = dir.z * egg_VELOCITY
    --})

    --obj:setacceleration({
        --x = dir.x * -3,
        --y = -egg_GRAVITY,
        --z = dir.z * -3
    --})

    ---- pass player name to egg for chick ownership
    --local ent2 = obj:get_luaentity()
    --ent2.playername = player:get_player_name()
    --item:take_item()
    --return item
--end

-- ===================================================================
-- Fried egg.

--minetest.register_craftitem (obj_name_egg_fried, {
    --description     = "Fried " .. ucname .. " Egg" ,
    --inventory_image = msname_egg_fried_img         ,
    --on_use          = minetest.item_eat (3)        ,
--})

--minetest.register_craft ({
    --type   = "cooking"          ,
    --recipe = obj_name_egg       ,
    --output = obj_name_egg_fried ,
--})

-- ===================================================================
-- Raw bird.

minetest.register_craftitem (obj_name_raw, {
    description     = "Raw " .. ucname ,
    inventory_image = msname_raw_img   ,

    on_use = function (itemstack, player, pointed_thing)
        local name = player:get_player_name()
        local msg  = name .. " ate raw " .. ucname .. ". Salmonella!"
        minetest.chat_send_all (msg)
        player:set_hp (player:get_hp() - 2)
    end ,
})

-- ===================================================================
-- Cooked bird.

minetest.register_craftitem (obj_name_cooked, {
    description     = "Cooked " .. ucname ,
    inventory_image = msname_cooked_img   ,
    on_use = minetest.item_eat (6)        ,
})

minetest.register_craft ({
    type   = "cooking"          ,
    recipe = obj_name_raw       ,
    output = obj_name_cooked    ,
})

-- ===================================================================

codermobs.log_done()

-- ===================================================================
-- End of file.
