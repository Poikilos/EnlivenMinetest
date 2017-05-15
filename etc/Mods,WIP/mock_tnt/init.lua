-- nondestructive replacement for tnt
-- uses some code from minetest\games\default\mods\tnt\init.lua
mock_tnt = {}
-- Default to enabled when in singleplayer
local enable_tnt = minetest.setting_getbool("enable_tnt")
if enable_tnt == nil then
	enable_tnt = minetest.is_singleplayer()
end

local function notify(name, retcode)
	if(retcode == false) then
		minetest.chat_send_player(name, "You did not suffer any ill effects.")
	-- else
	--  NOTE: tostring(retcode) is just a number, and debuff countdowns are automatically shown on right anyway
	-- 	minetest.chat_send_player(name, "You temporarily suffer from "..tostring(retcode))
	end
end

if (minetest.global_exists("playereffects")) then
	dofile(minetest.get_modpath(minetest.get_current_modname()).."/playereffects.lua")
end

local function apply_flashbang_debuffs(player)
	if (minetest.global_exists("playereffects")) then
		-- see also /usr/local/share/minetest/games/ENLIVEN/mods/playereffects/examples.lua
		local ret = playereffects.apply_effect_type("blind", 10, player)
		notify(player:get_player_name(), ret)
		local ret = playereffects.apply_effect_type("low_speed", 12, player)
		notify(player:get_player_name(), ret)
	end
end

local tnt_radius = tonumber(minetest.setting_get("tnt_radius") or 3)

local function rand_pos(center, pos, radius)
	local def
	local reg_nodes = minetest.registered_nodes
	local i = 0
	repeat
		-- Give up and use the center if this takes too long
		if i > 4 then
			pos.x, pos.z = center.x, center.z
			break
		end
		pos.x = center.x + math.random(-radius, radius)
		pos.z = center.z + math.random(-radius, radius)
		def = reg_nodes[minetest.get_node(pos).name]
		i = i + 1
	until def and not def.walkable
end


-- minetest.register_node( "mock_tnt:mock_tnt", {
-- 	description = "Unknown Explosive",
-- 	tiles = { "mock_tnt_top.png", "mock_tnt_sides.png", "mock_tnt_sides.png", "mock_tnt_sides.png", "mock_tnt_sides.png", "mock_tnt_sides.png" },
-- 	is_ground_content = true,
-- 	groups = {cracky = 1, level = 2},
-- 	sounds = default.node_sound_sand_defaults(),
-- })


-- Only when "not" to not overlap tnt mod:
if not enable_tnt then
	minetest.register_alias("tnt:tnt", "mock_tnt:mock_tnt")
	minetest.register_craft({
		output = "mock_tnt:mock_tnt",
		recipe = {
			{"group:wood",    "tnt:gunpowder", "group:wood"},
			{"tnt:gunpowder", "tnt:gunpowder", "tnt:gunpowder"},
			{"group:wood",    "tnt:gunpowder", "group:wood"}
		}
	})

	minetest.register_abm({
		label = "mock_tnt ignition",
		nodenames = {"group:tnt", "tnt:gunpowder"},
		neighbors = {"fire:basic_flame", "default:lava_source", "default:lava_flowing", "default:torch", "fire:permanent_flame"},
		interval = 4,
		chance = 1,
		action = function(pos, node)
			mock_tnt.burn(pos, node.name)
		end,
	})
end


local function add_effects(pos, radius, drops)
	minetest.add_particle({
		pos = pos,
		velocity = vector.new(),
		acceleration = vector.new(),
		expirationtime = 0.4,
		size = radius * 10,
		collisiondetection = false,
		vertical = false,
		texture = "mock_tnt_boom.png",
	})
	minetest.add_particlespawner({
		amount = 64,
		time = 0.5,
		minpos = vector.subtract(pos, radius / 2),
		maxpos = vector.add(pos, radius / 2),
		minvel = {x = -10, y = -10, z = -10},
		maxvel = {x = 10, y = 10, z = 10},
		minacc = vector.new(),
		maxacc = vector.new(),
		minexptime = 1,
		maxexptime = 2.5,
		minsize = radius * 3,
		maxsize = radius * 5,
		texture = "mock_tnt_smoke.png",
	})

	-- we just dropped some items. Look at the items entities and pick
	-- one of them to use as texture
	local texture = "mock_tnt_blast.png" --fallback texture
	if drops ~= nil then
		local most = 0
		for name, stack in pairs(drops) do
			local count = stack:get_count()
			if count > most then
				most = count
				local def = minetest.registered_nodes[name]
				if def and def.tiles and def.tiles[1] then
					texture = def.tiles[1]
				end
			end
		end
	end
	minetest.add_particlespawner({
		amount = 64,
		time = 0.1,
		minpos = vector.subtract(pos, radius / 2),
		maxpos = vector.add(pos, radius / 2),
		minvel = {x = -3, y = 0, z = -3},
		maxvel = {x = 3, y = 5,  z = 3},
		minacc = {x = 0, y = -10, z = 0},
		maxacc = {x = 0, y = -10, z = 0},
		minexptime = 0.8,
		maxexptime = 2.0,
		minsize = radius * 0.66,
		maxsize = radius * 2,
		texture = texture,
		collisiondetection = true,
	})
end

function mock_tnt.burn(pos, nodename)
	local name = nodename or minetest.get_node(pos).name
	local group = minetest.get_item_group(name, "mock_tnt")
	if group > 0 then
		minetest.sound_play("tnt_ignite", {pos = pos})
		minetest.set_node(pos, {name = name .. "_burning"})
		minetest.get_node_timer(pos):start(1)
	elseif name == "tnt:gunpowder" then
		minetest.set_node(pos, {name = "tnt:gunpowder_burning"})
	end
end

local function UNUSED_mock_tnt_explode(pos, radius, ignore_protection, ignore_on_blast)
	-- NOTE: register_tnt def param and register_tnt itself leave ignore_protection undefined
	-- which translates to false below.
	pos = vector.round(pos)
	-- scan for adjacent TNT nodes first, and enlarge the explosion
	local vm1 = VoxelManip()
	local p1 = vector.subtract(pos, 2)
	local p2 = vector.add(pos, 2)
	local minp, maxp = vm1:read_from_map(p1, p2)
	local a = VoxelArea:new({MinEdge = minp, MaxEdge = maxp})
	local data = vm1:get_data()
	local count = 0
	local c_tnt = minetest.get_content_id("mock_tnt:mock_tnt")
	local c_tnt_burning = minetest.get_content_id("mock_tnt:mock_tnt_burning")
	local c_tnt_boom = minetest.get_content_id("mock_tnt:boom")
	local c_air = minetest.get_content_id("air")

	for z = pos.z - 2, pos.z + 2 do
	for y = pos.y - 2, pos.y + 2 do
		local vi = a:index(pos.x - 2, y, z)
		for x = pos.x - 2, pos.x + 2 do
			local cid = data[vi]
			if cid == c_tnt or cid == c_tnt_boom or cid == c_tnt_burning then
				count = count + 1
				data[vi] = c_air
			end
			vi = vi + 1
		end
	end
	end

	vm1:set_data(data)
	vm1:write_to_map()

	-- recalculate new radius
	radius = math.floor(radius * math.pow(count, 1/3))

	-- perform the explosion
	local vm = VoxelManip()
	local pr = PseudoRandom(os.time())
	p1 = vector.subtract(pos, radius)
	p2 = vector.add(pos, radius)
	minp, maxp = vm:read_from_map(p1, p2)
	a = VoxelArea:new({MinEdge = minp, MaxEdge = maxp})
	data = vm:get_data()

	local drops = {}
	local on_blast_queue = {}

	local c_fire = minetest.get_content_id("fire:basic_flame")
	-- for z = -radius, radius do
	-- for y = -radius, radius do
	-- local vi = a:index(pos.x + (-radius), pos.y + y, pos.z + z)
	-- for x = -radius, radius do
	-- 	local r = vector.length(vector.new(x, y, z))
	-- 	if (radius * radius) / (r * r) >= (pr:next(80, 125) / 100) then
	-- 		local cid = data[vi]
	-- 		local p = {x = pos.x + x, y = pos.y + y, z = pos.z + z}
	-- 		if cid ~= c_air then
	-- 			data[vi] = destroy(drops, p, cid, c_air, c_fire,
	-- 				on_blast_queue, ignore_protection,
	-- 				ignore_on_blast)
	-- 		end
	-- 	end
	-- 	vi = vi + 1
	-- end
	-- end
	-- end

	-- vm:set_data(data)
	-- vm:write_to_map()
	-- vm:update_map()
	-- vm:update_liquids()

	-- call check_single_for_falling for everything within 1.5x blast radius
	for y = -radius * 1.5, radius * 1.5 do
	for z = -radius * 1.5, radius * 1.5 do
	for x = -radius * 1.5, radius * 1.5 do
		local rad = {x = x, y = y, z = z}
		local s = vector.add(pos, rad)
		local r = vector.length(rad)
		if r / radius < 1.4 then
			minetest.check_single_for_falling(s)
		end
	end
	end
	end

	for _, queued_data in pairs(on_blast_queue) do
		local dist = math.max(1, vector.distance(queued_data.pos, pos))
		local intensity = (radius * radius) / (dist * dist)
		local node_drops = queued_data.on_blast(queued_data.pos, intensity)
		if node_drops then
			for _, item in pairs(node_drops) do
				add_drop(drops, item)
			end
		end
	end

	return drops, radius
end

local function eject_drops(drops, pos, radius)
	local drop_pos = vector.new(pos)
	for _, item in pairs(drops) do
		local count = math.min(item:get_count(), item:get_stack_max())
		while count > 0 do
			local take = math.max(1,math.min(radius * radius,
					count,
					item:get_stack_max()))
			rand_pos(pos, drop_pos, radius)
			local dropitem = ItemStack(item)
			dropitem:set_count(take)
			local obj = minetest.add_item(drop_pos, dropitem)
			if obj then
				obj:get_luaentity().collect = true
				obj:setacceleration({x = 0, y = -10, z = 0})
				obj:setvelocity({x = math.random(-3, 3),
						y = math.random(0, 10),
						z = math.random(-3, 3)})
			end
			count = count - take
		end
	end
end

local function entity_physics(pos, radius, drops)
	local objs = minetest.get_objects_inside_radius(pos, radius)
	for _, obj in pairs(objs) do
		local obj_pos = obj:getpos()
		local dist = math.max(1, vector.distance(pos, obj_pos))

		local damage = (4 / dist) * radius
		if obj:is_player() then
			-- currently the engine has no method to set
			-- player velocity. See #2960
			-- instead, we knock the player back 1.0 node, and slightly upwards
			local dir = vector.normalize(vector.subtract(obj_pos, pos))
			local moveoff = vector.multiply(dir, dist + 1.0)
			local newpos = vector.add(pos, moveoff)
			newpos = vector.add(newpos, {x = 0, y = 0.2, z = 0})
			obj:setpos(newpos)

			obj:set_hp(obj:get_hp() - damage)
		else
			local do_damage = true
			local do_knockback = true
			local entity_drops = {}
			local luaobj = obj:get_luaentity()
			local objdef = minetest.registered_entities[luaobj.name]

			if objdef and objdef.on_blast then
				do_damage, do_knockback, entity_drops = objdef.on_blast(luaobj, damage)
			end

			if do_knockback then
				local obj_vel = obj:getvelocity()
				obj:setvelocity(calc_velocity(pos, obj_pos,
						obj_vel, radius * 10))
			end
			if do_damage then
				if not obj:get_armor_groups().immortal then
					obj:punch(obj, 1.0, {
						full_punch_interval = 1.0,
						damage_groups = {fleshy = damage},
					}, nil)
				end
			end
			for _, item in pairs(entity_drops) do
				add_drop(drops, item)
			end
		end
	end
end


function mock_tnt.boom(pos, def)
	minetest.sound_play("tnt_explode", {pos = pos, gain = 1.5, max_hear_distance = 2*64})
	minetest.set_node(pos, {name = "mock_tnt:boom"})
	--  local drops, radius = mock_tnt_explode(pos, def.radius, def.ignore_protection,
	-- 		def.ignore_on_blast)
	-- append entity drops
	-- local damage_radius = (radius / def.radius) * def.damage_radius
	local drops = {}
	local radius = def.damage_radius
	local damage_radius = def.damage_radius
	entity_physics(pos, damage_radius, drops)

	local objs = minetest.get_objects_inside_radius(pos, radius)
	for _, obj in pairs(objs) do
		local obj_pos = obj:getpos()
		local dist = math.max(1, vector.distance(pos, obj_pos))

		local damage = (4 / dist) * radius
		if obj:is_player() then
			apply_flashbang_debuffs(obj)
		end
	end

	if not def.disable_drops then
		eject_drops(drops, pos, radius)
	end
	add_effects(pos, radius, drops)
	-- add_effects_nodrops(pos, damage_radius)
end

minetest.register_node("mock_tnt:boom", {
	drawtype = "airlike",
	light_source = default.LIGHT_MAX,
	walkable = false,
	drop = "",
	groups = {dig_immediate = 3},
	on_construct = function(pos)
		minetest.get_node_timer(pos):start(0.4)
	end,
	on_timer = function(pos, elapsed)
		minetest.remove_node(pos)
	end,
	-- unaffected by explosions
	on_blast = function() end,
})

function mock_tnt.register_tnt(def)
	local name
	if not def.name:find(':') then
		name = "mock_tnt:" .. def.name
	else
		name = def.name
		def.name = def.name:match(":([%w_]+)")
	end
	if not def.tiles then def.tiles = {} end
	local tnt_top = def.tiles.top or def.name .. "_top.png"
	local tnt_bottom = def.tiles.bottom or def.name .. "_bottom.png"
	local tnt_side = def.tiles.side or def.name .. "_side.png"
	local tnt_burning = def.tiles.burning or def.name .. "_top_burning_animated.png"
	if not def.damage_radius then def.damage_radius = def.radius * 2 end

	-- if "not" since only make fake if real does not exist:
	
	-- if not enable_tnt then
	minetest.register_node(":" .. name, {
		description = def.description,
		tiles = { tnt_top, tnt_bottom, tnt_side },
		is_ground_content = false,
		groups = {dig_immediate = 2, mesecon = 2, tnt = 1, flammable = 5},
		sounds = default.node_sound_sand_defaults(),
		on_punch = function(pos, node, puncher)
			if puncher:get_wielded_item():get_name() == "default:torch" then
				minetest.set_node(pos, {name = name .. "_burning"})
			end
		end,
		on_blast = function(pos, intensity)
			minetest.after(0.1, function()
				mock_tnt.boom(pos, def)
			end)
		end,
		mesecons = {effector =
			{action_on =
				function(pos)
					mock_tnt.boom(pos, def)
				end
			}
		},
		on_burn = function(pos)
			minetest.set_node(pos, {name = name .. "_burning"})
		end,
		on_ignite = function(pos, igniter)
			minetest.set_node(pos, {name = name .. "_burning"})
		end,
	})
	-- end

	minetest.register_node(":" .. name .. "_burning", {
		tiles = {
			{
				name = tnt_burning,
				animation = {
					type = "vertical_frames",
					aspect_w = 16,
					aspect_h = 16,
					length = 1,
				}
			},
			tnt_bottom, tnt_side
			},
		light_source = 5,
		drop = "",
		sounds = default.node_sound_sand_defaults(),
		groups = {falling_node = 1},
		on_timer = function(pos, elapsed)
			mock_tnt.boom(pos, def)
		end,
		-- unaffected by explosions
		on_blast = function() end,
		on_construct = function(pos)
			minetest.sound_play("tnt_ignite", {pos = pos})
			minetest.get_node_timer(pos):start(4)
			minetest.check_for_falling(pos)
		end,
	})
end

mock_tnt.register_tnt({
	name = "mock_tnt:mock_tnt",
	description = "Unknown Explosive",
	radius = tnt_radius,
})



-- ALREADY DONE by minetest_game tnt mod even if tnt_enable is false:

-- minetest.register_node("tnt:gunpowder_burning", {
-- 	drawtype = "raillike",
-- 	paramtype = "light",
-- 	sunlight_propagates = true,
-- 	walkable = false,
-- 	light_source = 5,
-- 	tiles = {{
-- 		name = "mock_tnt_gunpowder_burning_straight_animated.png",
-- 		animation = {
-- 			type = "vertical_frames",
-- 			aspect_w = 16,
-- 			aspect_h = 16,
-- 			length = 1,
-- 		}
-- 	},
-- 	{
-- 		name = "mock_tnt_gunpowder_burning_curved_animated.png",
-- 		animation = {
-- 			type = "vertical_frames",
-- 			aspect_w = 16,
-- 			aspect_h = 16,
-- 			length = 1,
-- 		}
-- 	},
-- 	{
-- 		name = "mock_tnt_gunpowder_burning_t_junction_animated.png",
-- 		animation = {
-- 			type = "vertical_frames",
-- 			aspect_w = 16,
-- 			aspect_h = 16,
-- 			length = 1,
-- 		}
-- 	},
-- 	{
-- 		name = "mock_tnt_gunpowder_burning_crossing_animated.png",
-- 		animation = {
-- 			type = "vertical_frames",
-- 			aspect_w = 16,
-- 			aspect_h = 16,
-- 			length = 1,
-- 		}
-- 	}},
-- 	selection_box = {
-- 		type = "fixed",
-- 		fixed = {-1/2, -1/2, -1/2, 1/2, -1/2+1/16, 1/2},
-- 	},
-- 	drop = "",
-- 	groups = {dig_immediate = 2, attached_node = 1, connect_to_raillike = minetest.raillike_group("gunpowder")},
-- 	sounds = default.node_sound_leaves_defaults(),
-- 	on_timer = function(pos, elapsed)
-- 		for dx = -1, 1 do
-- 		for dz = -1, 1 do
-- 		for dy = -1, 1 do
-- 			if not (dx == 0 and dz == 0) then
-- 				mock_tnt.burn({
-- 					x = pos.x + dx,
-- 					y = pos.y + dy,
-- 					z = pos.z + dz,
-- 				})
-- 			end
-- 		end
-- 		end
-- 		end
-- 		minetest.remove_node(pos)
-- 	end,
-- 	-- unaffected by explosions
-- 	on_blast = function() end,
-- 	on_construct = function(pos)
-- 		minetest.sound_play("mock_tnt_gunpowder_burning", {pos = pos, gain = 2})
-- 		minetest.get_node_timer(pos):start(1)
-- 	end,
-- })
-- 
-- minetest.register_craft({
-- 	output = "tnt:gunpowder 5",
-- 	type = "shapeless",
-- 	recipe = {"default:coal_lump", "default:gravel"}
-- })

-- minetest.register_node("tnt:gunpowder", {
-- 	description = "Gun Powder",
-- 	drawtype = "raillike",
-- 	paramtype = "light",
-- 	is_ground_content = false,
-- 	sunlight_propagates = true,
-- 	walkable = false,
-- 	tiles = {"mock_tnt_gunpowder_straight.png", "mock_tnt_gunpowder_curved.png", "mock_tnt_gunpowder_t_junction.png", "mock_tnt_gunpowder_crossing.png"},
-- 	inventory_image = "mock_tnt_gunpowder_inventory.png",
-- 	wield_image = "mock_tnt_gunpowder_inventory.png",
-- 	selection_box = {
-- 		type = "fixed",
-- 		fixed = {-1/2, -1/2, -1/2, 1/2, -1/2+1/16, 1/2},
-- 	},
-- 	groups = {dig_immediate = 2, attached_node = 1, flammable = 5,
-- 		connect_to_raillike = minetest.raillike_group("gunpowder")},
-- 	sounds = default.node_sound_leaves_defaults(),
-- 
-- 	on_punch = function(pos, node, puncher)
-- 		if puncher:get_wielded_item():get_name() == "default:torch" then
-- 			minetest.set_node(pos, {name = "tnt:gunpowder_burning"})
-- 		end
-- 	end,
-- 	on_blast = function(pos, intensity)
-- 		minetest.set_node(pos, {name = "tnt:gunpowder_burning"})
-- 	end,
-- 	on_burn = function(pos)
-- 		minetest.set_node(pos, {name = "tnt:gunpowder_burning"})
-- 	end,
-- 	on_ignite = function(pos, igniter)
-- 		minetest.set_node(pos, {name = "tnt:gunpowder_burning"})
-- 	end,
-- })