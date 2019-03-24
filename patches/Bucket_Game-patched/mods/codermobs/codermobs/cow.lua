-- Cow. Descended from Krupnovpavel-JurajVajda version.

-- ===================================================================

local lcname     = "cow"
local ucname     = "Cow"
local msname     = "codermobs_" .. lcname
local obj_name   = "codermobs:" .. lcname

-- ===================================================================

mobs_param = {
    lcname       = lcname       ,
    ucname       = ucname       ,
    obj_name     = obj_name     ,

    aoc          =  2           ,
    obr          =  1           ,
    day_mode     = true         ,
    min_light    = 10           ,
    max_light    = 20           ,
    min_height   = -31000       ,
    max_height   =  31000       ,
    scale        = 1.25         ,
    spawn_chance =  40000       ,
    spawn_type   = "animal"     ,

    spawn_nodes  = {
        "default:dirt_with_dry_grass"   ,
        "default:dirt_with_grass"       ,
        "earthgen:dirt_with_dry_grass"  ,
        "ethereal:green_dirt"           ,
        "ethereal:green_dirt_top"       ,
        "ethereal:grove_dirt"           ,
        "mg:dirt_with_dry_grass"        ,
    } ,

    add_egg   = true                    ,
    egg_image = "default_grass.png"     ,
}

-- ===================================================================

codermobs.adjust_param()

-- ===================================================================

mobs_param.core_param = {
    type         = mobs_param.spawn_type    ,

    passive = false,
    attack_type = "dogfight",
    reach = 2,
    damage = 4,
    hp_min = 5,
    hp_max = 20,
    armor = 200,
    collisionbox = {-0.4, -0.01, -0.4, 0.4, 1, 0.4},
    visual = "mesh",
    mesh = msname .. ".x" ,
    textures = {
        { msname .. "_01.png" } ,
        { msname .. "_02.png" } ,
    },
    makes_footstep_sound = true,
    sounds = {
        random = msname ,
    },
    walk_velocity = 1,
    run_velocity = 2,
    jump = true,
    drops = {
        { name = "mobs:meat_raw", chance = 1, min = 1, max = 3},
        { name = "mobs:leather", chance = 1, min = 1, max = 2},
    },
    water_damage = 1,
    lava_damage = 5,
    light_damage = 0,
    animation = {
        speed_normal = 15,
        speed_run = 15,
        stand_start = 0,
        stand_end = 30,
        walk_start = 35,
        walk_end = 65,
        run_start = 105,
        run_end = 135,
        punch_start = 70,
        punch_end = 100,
    },
    follow = "farming:wheat",
    view_range = 8,
    replace_rate = 10,
--  replace_what = {"default:grass_3", "default:grass_4", "default:grass_5", "farming:wheat_8"},
    replace_what = {
        {"group:grass", "air", 0},
        {"default:dirt_with_grass", "default:dirt", -1}
    },
    replace_with = "air",
    fear_height = 2,
    on_rightclick = function(self, clicker)

        -- feed or tame
        if mobs:feed_tame(self, clicker, 8, true, true) then return end
        if mobs:protect(self, clicker) then return end
        if mobs:capture_mob(self, clicker, 0, 5, 60, false, nil) then return end

        local tool = clicker:get_wielded_item()
        local name = clicker:get_player_name()

        -- milk cow with empty bucket
        if tool:get_name() == "bucket:bucket_empty" then

            --if self.gotten == true
            if self.child == true then
                return
            end

            if self.gotten == true then
                minetest.chat_send_player(name,
                    "Cow already milked!")
                return
            end

            local inv = clicker:get_inventory()

            inv:remove_item("main", "bucket:bucket_empty")

            if inv:room_for_item("main", {name = "mobs:bucket_milk"}) then
                clicker:get_inventory():add_item("main", "mobs:bucket_milk")
            else
                local pos = self.object:get_pos()
                pos.y = pos.y + 0.5
                minetest.add_item(pos, {name = "mobs:bucket_milk"})
            end

            self.gotten = true -- milked

            return
        end
        -- milk cow with empty glass
        if tool:get_name() == "vessels:drinking_glass" then

            --if self.gotten == true
            if self.child == true then
                return
            end

            if self.gotten == true then
                minetest.chat_send_player(name,
                    "Cow already milked!")
                return
            end

            local inv = clicker:get_inventory()

            inv:remove_item("main", "vessels:drinking_glass")

            if inv:room_for_item("main", {name = "food:milk"}) then
                clicker:get_inventory():add_item("main", "food:milk")
            else
                local pos = self.object:get_pos()
                pos.y = pos.y + 0.5
                minetest.add_item(pos, {name = "food:milk"})
            end

            self.gotten = true -- milked

            return
        end
    end,
}

-- bucket of milk
minetest.register_craftitem(":mobs:bucket_milk", {
    description = "Bucket of Milk",
    inventory_image = "codermobs_bucket_milk.png",
    stack_max = 1,
    on_use = minetest.item_eat(8, 'bucket:bucket_empty'),
})

-- cheese wedge
minetest.register_craftitem(":mobs:cheese", {
    description = "Cheese",
    inventory_image = "codermobs_cheese.png",
    on_use = minetest.item_eat (4) ,
})

minetest.register_craft ({
    type = "cooking",
    output = "mobs:cheese",
    recipe = "mobs:bucket_milk",
    cooktime = 5,
    replacements = {{ "mobs:bucket_milk", "bucket:bucket_empty"}}
})

-- cheese block
minetest.register_node(":mobs:cheeseblock", {
    description = "Cheese Block",
    tiles = { "codermobs_cheeseblock.png" } ,
    is_ground_content = false,
    groups = {crumbly = 3},
    sounds = default.node_sound_dirt_defaults()
})

minetest.register_craft ({
    output = "mobs:cheeseblock" ,
    recipe = {
        {'mobs:cheese', 'mobs:cheese', 'mobs:cheese'},
        {'mobs:cheese', 'mobs:cheese', 'mobs:cheese'},
        {'mobs:cheese', 'mobs:cheese', 'mobs:cheese'},
    }
})

minetest.register_craft({
    output = "mobs:cheese 9",
    recipe = {
        {'mobs:cheeseblock'},
    }
})

-- ===================================================================

codermobs.setup_mob()
codermobs.log_done()

-- ===================================================================
-- End of file.
