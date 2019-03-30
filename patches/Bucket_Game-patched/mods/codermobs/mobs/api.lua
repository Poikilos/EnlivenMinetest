-- Mobs Api

-- Changes:
-- Merge in some RJK sections
-- detab
-- Remove a few superfluous blank lines to improve readability

mobs = {}
mobs.mod = "redo"
mobs.version = "20171112"

-- Intllib
local MP = minetest.get_modpath(minetest.get_current_modname())
local S, NS = dofile(MP .. "/intllib.lua")
mobs.intllib = S

local table_append = function (t1, t2)
    for _, v in ipairs (t2) do
        table.insert (t1, v)
    end
--  return t1
end

-- CMI support check
local use_cmi = minetest.global_exists("cmi")

-- Invisibility mod check
mobs.invis = {}
if minetest.global_exists("invisibility") then
	mobs.invis = invisibility
end


-- creative check
local creative_mode_cache = minetest.settings:get_bool("creative_mode")
function mobs.is_creative(name)
	return creative_mode_cache or minetest.check_player_privs(name, {creative = true})
end

local cmdebug = false


-- localize math functions
local pi = math.pi
local square = math.sqrt
local sin = math.sin
local cos = math.cos
local abs = math.abs
local min = math.min
local max = math.max
local atann = math.atan
local random = math.random
local floor = math.floor
local atan = function(x)
	if not x or x ~= x then
		--error("atan bassed NaN")
		return 0
	else
		return atann(x)
	end
end

-- ===================================================================

local function StartsWith (String, Start)
    return string.sub (String, 1,
        string.len (Start)) == Start
end

-- ===================================================================

local codermobs_disable_wild           =
      minetest.setting_getbool ("codermobs_disable_wild"           )
local codermobs_disable_mobs           =
      minetest.setting_getbool ("codermobs_disable_mobs"           )
local codermobs_disable_monsters       =
      minetest.setting_getbool ("codermobs_disable_monsters"       )
local codermobs_disable_npc            =
      minetest.setting_getbool ("codermobs_disable_npc"            )
local codermobs_peaceful               =
      minetest.setting_getbool ("codermobs_peaceful"               )
local codermobs_creative_eggs          =
      minetest.setting_getbool ("codermobs_creative_eggs"          )

local codermobs_talk_french            =
      minetest.setting_getbool ("codermobs_talk_french"            )
local codermobs_talk_spanish           =
      minetest.setting_getbool ("codermobs_talk_spanish"           )

-- ===================================================================
-- Mixed 10+1 and RJK section.

-- Load settings
local damage_enabled = minetest.settings:get_bool("enable_damage")
local peaceful_only = minetest.settings:get_bool("only_peaceful_mobs")
local disable_blood = minetest.settings:get_bool("mobs_disable_blood")
local creative = minetest.settings:get_bool("creative_mode")
local spawn_protected = minetest.settings:get_bool("mobs_spawn_protected") ~= false
local remove_far = minetest.settings:get_bool("remove_far_mobs")
local difficulty = tonumber(minetest.settings:get("mob_difficulty")) or 1.0
local show_health = minetest.settings:get_bool("mob_show_health") ~= false
local max_per_block = tonumber(minetest.settings:get("max_objects_per_block") or 99)
local codermobs_density = tonumber(minetest.settings:get("codermobs_density") or 12)

if codermobs_disable_monsters then
    peaceful_only = true
end

mobs.defaultaoc = tonumber (minetest.setting_get("codermobs_aoc_default")) or 6
mobs.protected  = true
mobs.remove     = minetest.setting_getbool ("remove_far_mobs")

codermobs_spawn_protected = minetest.setting_getbool ("codermobs_spawn_protected")

--if minetest.setting_getbool ("codermobs_spawn_protected" ) or
--   minetest.setting_getbool ("mobs_spawn_protected"     ) then
--    mobs.protected = true
--end

-- ===================================================================
-- RJK section.

local extra_english

local BeeRemarks =
{
    "my favorite rock-star is Sting"                ,
    "my favorite sport is Rug-Bee"                  ,
    "bee all that you can bee"                      ,
    "buzzzz"                                        ,
    "buzzy buzz buzz"                               ,
    "honey is money"                                ,
    "you and me, one two bee"                       ,
    "i feel buzzy, oh so buzzy, I feel buzzy today"     ,
    "i ride the school-buzz"                            ,
    "a wasp is just a wanna-bee"                        ,
    "A, B, C It's as easy as 1, 2, bee"                 ,
    "honey, i'm home"                                   ,
    "vitamin bee is good for you"                       ,
    "to bee or not to bee is the question"              ,
}

extra_english = true

if codermobs_talk_french then
    extra_english = false
    table_append (BeeRemarks, {
        "les fleurs sont belles"                            ,
        "J'aime les fleurs"                                 ,
        "l'abeille occupee n'a pas le temps de tristesse"   ,
        "abeille hum parce que nous oublions les mots"      ,
        "travailler dur"                                    ,
        "la reine a toujours raison"                        ,
    })
end

if codermobs_talk_spanish then
    extra_english = false
    table_append (BeeRemarks, {
        "las flores son bonitas"                            ,
        "me gustan las flores"                              ,
        "la abeja ocupada no tiene tiempo para la tristeza" ,
        "zumban las abejas porque olvidamos las palabras"   ,
        "trabaja duro"                                      ,
        "la abeja reina siempre tiene la raz"               ,
    })
end

if extra_english then
    table_append (BeeRemarks, {
        "flowers are nice"                                  ,
        "i like flowers"                                    ,
        "the busy bee has no time for sorrow"               ,
        "bees hum because we forget the words"              ,
        "work hard"                                         ,
        "the queen is always right"                         ,
    })
end

local LastBeeTalkTime =   0
local BeeTalkDelay    = 600

-- ===================================================================
-- RJK section.

local KittenRemarks =
{
    "mice r gud"                        ,
    "mew"                               ,
    "moar rats"                         ,
}

extra_english = true

-- The remarks in each section here should match
--
if codermobs_talk_french then
    extra_english = false
    table_append (KittenRemarks, {
        "nourris moi"                   ,
    })
end

if codermobs_talk_spanish then
    extra_english = false
    table_append (KittenRemarks, {
        "alimentame"                    ,
    })
end

if extra_english then
    table_append (KittenRemarks, {
        "feed me"                       ,
    })
end

local LastKittenTalkTime =   0
local KittenTalkDelay    = 750

-- ===================================================================
-- RJK section.

local WolfRemarks =
{
    "a man's best friend is his dogma"                              ,
    "a man's horizons are bounded by his vision"                    ,
    "a man who knows that he is a fool is not a great fool"         ,
    "even a hawk is an eagle among crows"                           ,
    "even the boldest zebra fears the hungry lion"                  ,
    "freedom's just another word for nothing left to lose"          ,
    "God made the integers; all else is the work of Man"            ,
    "he is winding the watch of his wit; by and by it will strike"  ,
    "he who laughs, lasts"                                          ,
    "howl do you do?"                                               ,
    "if tin whistles are made of tin, what are foghorns made of?"   ,
    "it's almost cosmic"                                            ,
    "I was born in truth's own city, Veritas"                       ,
    "just because things are obvious doesn't mean they're true"     ,
    "like winter snow on summer lawn, time past is time gone"       ,
    "opportunities multiply as they are seized"                     ,
    "prepare and prevent, instead of repair and repent"             ,
    "speak the truth, but leave immediately after"                  ,
    "the bogosity meter just pegged"                                ,
    "this era too is almost at an end"                              ,
    "thrift is a wonderful virtue; especially in ancestors"         ,
    "to err is human; to moo, bovine"                               ,
    "well-done is better than well-said"                            ,
    "trifles make perfection, but perfection is no trifle"          ,
    "where ignorance is bliss, it is folly to be wise"              ,
    "why do humans always look to the sky?"                         ,
}

extra_english = true

if codermobs_talk_french then
    extra_english = false
    table_append (WolfRemarks, {
"ce que l'homme a fait, l'homme peut aspirer a faire"                 ,
"le vent froid de l'espoir souffle eternel"                           ,
"la meilleure facon de predire l'avenir est de l'inventer"            ,
"profiter du present"                                                 ,
"seul le phoenix vole et ne descend pas"                              ,
"l'argent est un bon serviteur, mais un mauvais maitre"               ,
"ecoute bien les paroles de ton ame"                                  ,
"la vie est un voyage et non une destination"                         ,
"si tu es heureux, tu as du succes"                                   ,
"si cela arrive, cela doit etre possible"                             ,
"celui qui monte le tigre ne peut pas demonter"                       ,
"meme la plus petite bougie brule plus brillamment dans l'obscurite"  ,
"un marin qualifie n'a jamais ete cree sur une mer calme"             ,
"une promesse faite est une dette impayee"                            ,
"un honnete homme est le plus noble travail de Dieu"                  ,
"un chat en verre n'attrape pas de souris"                            ,
"un imbecile ne voit pas le meme arbre qu'un homme sage voit"         ,
"un coeur gentil a peu de valeur sur l'echiquier"                     ,
"si vous en avez assez, vous avez une montagne"                       ,
"c'est un oiseau sage qui construit son nid dans un arbre"            ,
"les mots doivent etre peses, non comptes"                            ,
"de quelle couleur est un cameleon sur un miroir?"                    ,
"L'horloge et la maree n'attendent personne"                          ,
"le temps est la riviere ou je pecherai"                              ,
"meme un chou peut regarder un roi"                                   ,
"tous les chats sont gris dans le noir"                               ,
"l'histoire sera gentille avec moi, car j'ai l'intention de l'ecrire" ,
"vous devez nourrir les chevaux, si vous voulez le wagon tire"        ,
"les humains sont croquants"                                          ,
"Je ne consens pas a l'Univers"                                       ,
"la force du loup est la tribu des loups"                             ,
    })
end

if codermobs_talk_spanish then
    extra_english = false
    table_append (WolfRemarks, {
"lo que el hombre ha hecho, el hombre puede aspirar a hacer"    ,
"el viento frio de la esperanza sopla eterno"                   ,
"la mejor manera de predecir el futuro es inventarlo"           ,
"aprovecha el dia"                                              ,
"solo el fix surge y no desciende"                              ,
"el dinero es un buen servidor, pero un mal maestro"            ,
"escucha bien las palabras de tu alma"                          ,
"la vida es un viaje no un destino"                             ,
"me gusta la carne"                                             ,
"si eres feliz, tienes ito"                                     ,
"si sucede, debe ser posible"                                   ,
"el que monta el tigre no puede dejarlo"                        ,
"incluso la vela m peque arde m brillante en la oscuridad"      ,
"un marinero hil nunca fue hecho en un mar en calma"            ,
"una promesa hecha es una deuda impaga"                         ,
"el hombre honesto es la m noble obra de Dios"                  ,
"un gato de cristal no atrapa ratones"                          ,
"un tonto no ve el mismo arbol que ve un hombre sabio"          ,
"un coraz bueno tiene poco valor en el ajedrez"                 ,
"lo suficiente es tan bueno como una fiesta"                    ,
"es un ave sabia que construye su nido en un arbol"             ,
"las palabras se deben medir por peso, no por numero"           ,
"de que color es un camaleon en un espejo?"                     ,
"el paso del tiempo y la marea no esperan a nadie"              ,
"el rio del tiempo es donde prefiero ir a pescar"               ,
"incluso un repollo puede mirar a un rey"                       ,
"todos los gatos son grises en la oscuridad"                    ,
"el ma nunca es inocente en el juzgado de los pollos"           ,
"ten cuidado con los tiburones que beben whisky"                ,
"la historia sera amable conmigo, porque la escribire"          ,
"el que dice la verdad es expulsado de nueve pueblos"           ,
"si desea tirar del carro, debe alimentar a los caballos"       ,
"los humanos son crujientes y deliciosos"                       ,
"no doy mi consentimiento al Universo"                          ,
"el mayor defecto es no estar al tanto de ningun defecto"       ,
"la fuerza del Lobo es el Pack"                                 ,
    })
end

if extra_english then
    table_append (WolfRemarks, {
"what man has done, man can aspire to do"                       ,
"the cold wind of hope blows eternal"                           ,
"the best way to predict the future is to invent it"            ,
"seize the day"                                                 ,
"only the phoenix arises and does not descend"                  ,
"money is a good servant, but a bad master"                     ,
"listen well to the words of your soul"                         ,
"life is a journey, not a destination"                          ,
"i like meat"                                                   ,
"if you're happy, you're successful"                            ,
"if it happens, it must be possible"                            ,
"he who rides the tiger cannot dismount"                        ,
"even the smallest candle burns brighter in the dark"           ,
"a skillful sailor was never made on a calm sea"                ,
"a promise made is a debt unpaid"                               ,
"an honest man's the noblest work of God"                       ,
"a glass cat catches no mice"                                   ,
"a fool sees not the same tree that a wise man sees"            ,
"a kind heart is of little value in chess"                      ,
"enough is as good as a feast"                                  ,
"it's a wise bird who builds his nest in a tree"                ,
"words must be weighed, not counted"                            ,
"what color is a chameleon on a mirror?"                        ,
"time and tide wait for no man"                                 ,
"time is the stream that I go fishing in"                       ,
"even a cabbage may look at a king"                             ,
"all cats are gray in the dark"                                 ,
"the corn is never found innocent in the court of the chickens" ,
"a shark with whiskey is mighty risky"                          ,
"history will be kind to me, for I intend to write it"          ,
"he who tells the truth is chased out of nine villages"         ,
"you've got to feed the horses, if you want the wagon pulled"   ,
"humans r crunchy"                                              ,
"I do not consent to the Universe"                              ,
"the greatest of faults is to be conscious of none"             ,
"the strength of the Wolf is the Pack"                          ,
    })
end

local LastWolfTalkTime =   0
local WolfTalkDelay    = 300

-- ===================================================================


-- Peaceful mode message so players will know there are no monsters
if peaceful_only then
	minetest.register_on_joinplayer(function(player)
		minetest.chat_send_player(player:get_player_name(),
			S("** Peaceful Mode Active - No Monsters Will Spawn"))
	end)
end

-- calculate aoc range for mob count
local aosrb = tonumber(minetest.settings:get("active_object_send_range_blocks"))
local abr = tonumber(minetest.settings:get("active_block_range"))
local aoc_range = max(aosrb, abr) * 16

-- pathfinding settings
local enable_pathfinding = true
local stuck_timeout = 3 -- how long before mob gets stuck in place and starts searching
local stuck_path_timeout = 10 -- how long will mob follow path before giving up

-- default nodes
local node_fire = "fire:basic_flame"
local node_permanent_flame = "fire:permanent_flame"
local node_ice = "default:ice"
local node_snowblock = "default:snowblock"
local node_snow = "default:snow"
mobs.fallback_node = minetest.registered_aliases["mapgen_dirt"] or "default:dirt"


-- play sound
local mob_sound = function(self, sound)

	if sound then
		minetest.sound_play(sound, {
			object = self.object,
			gain = 1.0,
			max_hear_distance = self.sounds.distance
		})
	end
end


-- attack player/mob
local do_attack = function(self, player)

	if self.state == "attack" then
		return
	end

	self.attack = player
	self.state = "attack"

	if random(0, 100) < 90 then
		mob_sound (self, self.sounds.war_cry)
	end
end


-- move mob in facing direction
local set_velocity = function(self, v)

	local yaw = (self.object:get_yaw() or 0) + self.rotate

	self.object:setvelocity({
		x = sin(yaw) * -v,
		y = self.object:getvelocity().y,
		z = cos(yaw) * v
	})
end


-- calculate mob velocity
local get_velocity = function(self)

	local v = self.object:getvelocity()

	return (v.x * v.x + v.z * v.z) ^ 0.5
end


-- set and return valid yaw
local set_yaw = function(self, yaw)

	if not yaw or yaw ~= yaw then
		yaw = 0
	end

	self:setyaw(yaw)

	return yaw
end


-- set defined animation
local set_animation = function(self, anim)

	if not self.animation
	or not anim then return end

	self.animation.current = self.animation.current or ""

	if anim == self.animation.current
	or not self.animation[anim .. "_start"]
	or not self.animation[anim .. "_end"] then
		return
	end

	self.animation.current = anim

	self.object:set_animation({
		x = self.animation[anim .. "_start"],
		y = self.animation[anim .. "_end"]},
		self.animation[anim .. "_speed"] or self.animation.speed_normal or 15,
		0, self.animation[anim .. "_loop"] ~= false)
end


-- above function exported for mount.lua
function mobs:set_animation(self, anim)
	set_animation(self, anim)
end


-- compatibility function for old entities to new modpack entities
function mobs:alias_mob(old_name, new_name)

	-- spawn egg
	minetest.register_alias(old_name, new_name)

	-- entity
	minetest.register_entity(":" .. old_name, {

		physical = false,

		on_activate = function(self)

			if minetest.registered_entities[new_name] then
				minetest.add_entity(self.object:get_pos(), new_name)
			end

			self.object:remove()
		end
	})
end


-- calculate distance
local get_distance = function(a, b)

	local x, y, z = a.x - b.x, a.y - b.y, a.z - b.z

	return square(x * x + y * y + z * z)
end


-- check line of sight (BrunoMine)
local line_of_sight = function(self, pos1, pos2, stepsize)

	stepsize = stepsize or 1

	local s, pos = minetest.line_of_sight(pos1, pos2, stepsize)

	-- normal walking and flying mobs can see you through air
	if s == true then
		return true
	end

	-- New pos1 to be analyzed
	local npos1 = {x = pos1.x, y = pos1.y, z = pos1.z}

	local r, pos = minetest.line_of_sight(npos1, pos2, stepsize)

	-- Checks the return
	if r == true then return true end

	-- Nodename found
	local nn = minetest.get_node(pos).name

	-- Target Distance (td) to travel
	local td = get_distance(pos1, pos2)

	-- Actual Distance (ad) traveled
	local ad = 0

	-- It continues to advance in the line of sight in search of a real
	-- obstruction which counts as 'normal' nodebox.
	while minetest.registered_nodes[nn]
	and (minetest.registered_nodes[nn].walkable == false
	or minetest.registered_nodes[nn].drawtype == "nodebox") do

		-- Check if you can still move forward
		if td < ad + stepsize then
			return true -- Reached the target
		end

		-- Moves the analyzed pos
		local d = get_distance(pos1, pos2)

		npos1.x = ((pos2.x - pos1.x) / d * stepsize) + pos1.x
		npos1.y = ((pos2.y - pos1.y) / d * stepsize) + pos1.y
		npos1.z = ((pos2.z - pos1.z) / d * stepsize) + pos1.z

		-- NaN checks
		if d == 0
		or npos1.x ~= npos1.x
		or npos1.y ~= npos1.y
		or npos1.z ~= npos1.z then
			return false
		end

		ad = ad + stepsize

		-- scan again
		r, pos = minetest.line_of_sight(npos1, pos2, stepsize)

		if r == true then return true end

		-- New Nodename found
		nn = minetest.get_node(pos).name

	end

	return false
end


-- are we flying in what we are suppose to? (taikedz)
local flight_check = function(self, pos_w)

	local nod = self.standing_in
	local def = minetest.registered_nodes[nod]

	if not def then return false end -- nil check

	if type(self.fly_in) == "string"
	and nod == self.fly_in then

		return true

	elseif type(self.fly_in) == "table" then

		for _,fly_in in pairs(self.fly_in) do

			if nod == fly_in then

				return true
			end
		end
	end

	-- stops mobs getting stuck inside stairs and plantlike nodes
	if def.drawtype ~= "airlike"
	and def.drawtype ~= "liquid"
	and def.drawtype ~= "flowingliquid" then
		return true
	end

	return false
end


-- custom particle effects
local effect = function(pos, amount, texture, min_size, max_size, radius, gravity, glow)

	radius = radius or 2
	min_size = min_size or 0.5
	max_size = max_size or 1
	gravity = gravity or -10
	glow = glow or 0

	minetest.add_particlespawner({
		amount = amount,
		time = 0.25,
		minpos = pos,
		maxpos = pos,
		minvel = {x = -radius, y = -radius, z = -radius},
		maxvel = {x = radius, y = radius, z = radius},
		minacc = {x = 0, y = gravity, z = 0},
		maxacc = {x = 0, y = gravity, z = 0},
		minexptime = 0.1,
		maxexptime = 1,
		minsize = min_size,
		maxsize = max_size,
		texture = texture,
		glow = glow,
	})
end


-- update nametag colour
local update_tag = function(self)

	local col = "#00FF00"
	local qua = self.hp_max / 4

	if self.health <= floor(qua * 3) then
		col = "#FFFF00"
	end
	if self.health <= floor(qua * 2) then
		col = "#FF6600"
	end
	if self.health <= floor(qua) then
		col = "#FF0000"
	end

	self.object:set_properties({
		nametag = self.nametag,
		nametag_color = col
	})

end


-- drop items
local item_drop = function(self, cooked)

	-- no drops for child mobs
	if self.child then return end

	local obj, item, num
	local pos = self.object:get_pos()

	self.drops = self.drops or {} -- nil check

	for n = 1, #self.drops do

		if random(1, self.drops[n].chance) == 1 then

			num = random(self.drops[n].min, self.drops[n].max)
			item = self.drops[n].name

			-- cook items when true
			if cooked then

				local output = minetest.get_craft_result({
					method = "cooking", width = 1, items = {item}})

				if output and output.item and not output.item:is_empty() then
					item = output.item:get_name()
				end
			end

			-- add item if it exists
			obj = minetest.add_item(pos, ItemStack(item .. " " .. num))

			if obj and obj:get_luaentity() then

				obj:setvelocity({
					x = random(-10, 10) / 9,
					y = 6,
					z = random(-10, 10) / 9,
				})
			elseif obj then
				obj:remove() -- item does not exist
			end
		end
	end

	self.drops = {}
end


-- check if mob is dead or only hurt
local check_for_death = function(self, cause, cmi_cause)

	-- has health actually changed?
	if self.health == self.old_health and self.health > 0 then
		return
	end

	self.old_health = self.health

	-- still got some health? play hurt sound
	if self.health > 0 then

		mob_sound(self, self.sounds.damage)

		-- make sure health isn't higher than max
		if self.health > self.hp_max then
			self.health = self.hp_max
		end

		-- backup nametag so we can show health stats
		if not self.nametag2 then
			self.nametag2 = self.nametag or ""
		end

		if show_health then

			self.htimer = 2
			self.nametag = "♥ " .. self.health .. " / " .. self.hp_max

			update_tag(self)
		end

		return false
	end

	-- dropped cooked item if mob died in lava
	if cause == "lava" then
		item_drop(self, true)
	else
		item_drop(self, nil)
	end

	mob_sound(self, self.sounds.death)

	local pos = self.object:get_pos()

	-- execute custom death function
	if self.on_die then

		self.on_die(self, pos)

		if use_cmi then
			cmi.notify_die(self.object, cmi_cause)
		end

		self.object:remove()

		return true
	end

	-- default death function and die animation (if defined)
	if self.animation
	and self.animation.die_start
	and self.animation.die_end then

		local frames = self.animation.die_end - self.animation.die_start
		local speed = self.animation.die_speed or 15
		local length = max(frames / speed, 0)

		self.attack = nil
		self.v_start = false
		self.timer = 0
		self.blinktimer = 0
		self.passive = true
		self.state = "die"
		set_velocity(self, 0)
		set_animation(self, "die")

		minetest.after(length, function(self)

			if use_cmi then
				cmi.notify_die(self.object, cmi_cause)
			end

			self.object:remove()
		end, self)
	else

		if use_cmi then
			cmi.notify_die(self.object, cmi_cause)
		end

		self.object:remove()
	end

	effect(pos, 20, "tnt_smoke.png")

	return true
end


-- check if within physical map limits (-30911 to 30927)
local within_limits = function(pos, radius)

	if  (pos.x - radius) > -30913
	and (pos.x + radius) <  30928
	and (pos.y - radius) > -30913
	and (pos.y + radius) <  30928
	and (pos.z - radius) > -30913
	and (pos.z + radius) <  30928 then
		return true -- within limits
	end

	return false -- beyond limits
end


-- is mob facing a cliff
local is_at_cliff = function(self)

	if self.fear_height == 0 then -- 0 for no falling protection!
		return false
	end

--  RJK: Bug fix for old mobs
--  local yaw = self.object:get_yaw()
	local yaw = (self.object:get_yaw() or 0) + self.rotate
	minetest.log ("action", "yawful " .. yaw) -- @@@

	local dir_x = -sin(yaw) * (self.collisionbox[4] + 0.5)
	local dir_z =  cos(yaw) * (self.collisionbox[4] + 0.5)
	local pos = self.object:get_pos()
	local ypos = pos.y + self.collisionbox[2] -- just above floor

	if minetest.line_of_sight(
		{x = pos.x + dir_x, y = ypos, z = pos.z + dir_z},
		{x = pos.x + dir_x, y = ypos - self.fear_height, z = pos.z + dir_z}
	, 1) then
		return true
	end

	dir_x = sin(yaw) * 2
	dir_z = cos(yaw) * 2

    if self.fear_height > 2 then
        if minetest.line_of_sight (
            {x = pos.x + dir_x, y = pos.y                    , z = pos.z + dir_z} ,
            {x = pos.x + dir_x, y = pos.y - self.fear_height , z = pos.z + dir_z} ,
1) then
            return true
        end
    end

	return false
end


-- get node but use fallback for nil or unknown
local node_ok = function(pos, fallback)

	fallback = fallback or mobs.fallback_node

	local node = minetest.get_node_or_nil(pos)

	if node and minetest.registered_nodes[node.name] then
		return node
	end

	return minetest.registered_nodes[fallback] -- {name = fallback}
end


-- environmental damage (water, lava, fire, light etc.)
local do_env_damage = function(self)

	-- feed/tame text timer (so mob 'full' messages dont spam chat)
	if self.htimer > 0 then
		self.htimer = self.htimer - 1
	end

	-- reset nametag after showing health stats
	if self.htimer < 1 and self.nametag2 then

		self.nametag = self.nametag2
		self.nametag2 = nil

		update_tag(self)
	end

	local pos = self.object:get_pos()

	self.time_of_day = minetest.get_timeofday()

	-- remove mob if beyond map limits
	if not within_limits(pos, 0) then
		self.object:remove()
		return
	end

	-- bright light harms mob
	if self.light_damage ~= 0
--	and pos.y > 0
--	and self.time_of_day > 0.2
--	and self.time_of_day < 0.8
	and (minetest.get_node_light(pos) or 0) > 12 then

		self.health = self.health - self.light_damage

		effect(pos, 5, "tnt_smoke.png")

		if check_for_death(self, "light", {type = "light"}) then return end
	end

	local y_level = self.collisionbox[2]

	if self.child then
		y_level = self.collisionbox[2] * 0.5
	end

	-- what is mob standing in?
	pos.y = pos.y + y_level + 0.25 -- foot level
	self.standing_in = node_ok(pos, "air").name
--	print ("standing in " .. self.standing_in)

	-- don't fall when on ignore, just stand still
	if self.standing_in == "ignore" then
		self.object:setvelocity({x = 0, y = 0, z = 0})
	end

	local nodef = minetest.registered_nodes[self.standing_in]

	pos.y = pos.y + 1 -- for particle effect position

	-- water
	if self.water_damage
	and nodef.groups.water then

		if self.water_damage ~= 0 then

			self.health = self.health - self.water_damage

			effect(pos, 5, "bubble.png", nil, nil, 1, nil)

			if check_for_death(self, "water", {type = "environment",
					pos = pos, node = self.standing_in}) then return end
		end

	-- lava or fire
	elseif self.lava_damage
	and (nodef.groups.lava
	or self.standing_in == node_fire
	or self.standing_in == node_permanent_flame) then

		if self.lava_damage ~= 0 then

			self.health = self.health - self.lava_damage

			effect(pos, 5, "fire_basic_flame.png", nil, nil, 1, nil)

			if check_for_death(self, "lava", {type = "environment",
					pos = pos, node = self.standing_in}) then return end
		end

	-- damage_per_second node check
	elseif nodef.damage_per_second ~= 0 then

		self.health = self.health - nodef.damage_per_second

		effect(pos, 5, "tnt_smoke.png")

		if check_for_death(self, "dps", {type = "environment",
				pos = pos, node = self.standing_in}) then return end
	end
--[[
	--- suffocation inside solid node
	if self.suffocation ~= 0
	and nodef.walkable == true
	and nodef.groups.disable_suffocation ~= 1
	and nodef.drawtype == "normal" then

		self.health = self.health - self.suffocation

		if check_for_death(self, "suffocation", {type = "environment",
				pos = pos, node = self.standing_in}) then return end
	end
]]
	check_for_death(self, "", {type = "unknown"})
end


-- jump if facing a solid node (not fences or gates)
local do_jump = function(self)

	if not self.jump
	or self.jump_height == 0
	or self.fly
	or self.child then
		return false
	end

	self.facing_fence = false

	-- something stopping us while moving?
	if self.state ~= "stand"
	and get_velocity(self) > 0.5
	and self.object:getvelocity().y ~= 0 then
		return false
	end

	local pos = self.object:get_pos()
	local yaw = self.object:get_yaw()

	-- what is mob standing on?
	pos.y = pos.y + self.collisionbox[2] - 0.2

	local nod = node_ok(pos)

--print ("standing on:", nod.name, pos.y)

	if minetest.registered_nodes[nod.name].walkable == false then
		return false
	end

	-- where is front
	local dir_x = -sin(yaw) * (self.collisionbox[4] + 0.5)
	local dir_z = cos(yaw) * (self.collisionbox[4] + 0.5)

	-- what is in front of mob?
	local nod = node_ok({
		x = pos.x + dir_x,
		y = pos.y + 0.5,
		z = pos.z + dir_z
	})

	-- thin blocks that do not need to be jumped
	if nod.name == node_snow then
		return false
	end

--print ("in front:", nod.name, pos.y + 0.5)

	if self.walk_chance == 0
	or minetest.registered_items[nod.name].walkable then

		if not nod.name:find("fence")
		and not nod.name:find("gate") then

			local v = self.object:getvelocity()

			v.y = self.jump_height

			set_animation(self, "jump") -- only when defined

			self.object:setvelocity(v)

			mob_sound(self, self.sounds.jump)
		else
			self.facing_fence = true
		end

		return true
	end

	return false
end


-- blast damage to entities nearby (modified from TNT mod)
local entity_physics = function(pos, radius)

	radius = radius * 2

	local objs = minetest.get_objects_inside_radius(pos, radius)
	local obj_pos, dist

	for n = 1, #objs do

		obj_pos = objs[n]:get_pos()

		dist = get_distance(pos, obj_pos)
		if dist < 1 then dist = 1 end

		local damage = floor((4 / dist) * radius)
		local ent = objs[n]:get_luaentity()

		-- punches work on entities AND players
		objs[n]:punch(objs[n], 1.0, {
			full_punch_interval = 1.0,
			damage_groups = {fleshy = damage},
		}, pos)
	end
end


-- should mob follow what I'm holding ?
local follow_holding = function(self, clicker)

	if mobs.invis[clicker:get_player_name()] then
		return false
	end

	local item = clicker:get_wielded_item()
	local t = type(self.follow)

	-- single item
	if t == "string"
	and item:get_name() == self.follow then
		return true

	-- multiple items
	elseif t == "table" then

		for no = 1, #self.follow do

			if self.follow[no] == item:get_name() then
				return true
			end
		end
	end

	return false
end


-- find two animals of same type and breed if nearby and horny
local breed = function(self)

	-- child takes 240 seconds before growing into adult
	if self.child == true then

		self.hornytimer = self.hornytimer + 1

		if self.hornytimer > 240 then
			self.child = false
			self.hornytimer = 0

			self.object:set_properties({
				textures = self.base_texture,
				mesh = self.base_mesh,
				visual_size  = self.base_size   ,
				collisionbox = self.base_colbox ,
			})

			-- custom function when child grows up
			if self.on_grown then
				self.on_grown(self)
			else
				-- jump when fully grown so as not to fall into ground
				self.object:setvelocity({
					x = 0,
					y = self.jump_height,
					z = 0
				})
			end
		end

		return
	end

	-- horny animal can mate for 40 seconds,
	-- afterwards horny animal cannot mate again for 200 seconds
	if self.horny == true
	and self.hornytimer < 240 then

		self.hornytimer = self.hornytimer + 1

		if self.hornytimer >= 240 then
			self.hornytimer = 0
			self.horny = false
		end
	end

	-- find another same animal who is also horny and mate if nearby
	if self.horny == true
	and self.hornytimer <= 40 then

		local pos = self.object:get_pos()

		effect({x = pos.x, y = pos.y + 1, z = pos.z}, 8, "heart.png", 3, 4, 1, 0.1)

		local objs = minetest.get_objects_inside_radius(pos, 3)
		local num = 0
		local ent = nil

		for n = 1, #objs do

			ent = objs[n]:get_luaentity()

			-- check for same animal with different colour
			local canmate = false

			if ent then

				if ent.name == self.name then
					canmate = true
				else
					local entname = string.split(ent.name,":")
					local selfname = string.split(self.name,":")

					if entname[1] == selfname[1] then
						entname = string.split(entname[2],"_")
						selfname = string.split(selfname[2],"_")

						if entname[1] == selfname[1] then
							canmate = true
						end
					end
				end
			end

			if ent
			and canmate == true
			and ent.horny == true
			and ent.hornytimer <= 40 then
				num = num + 1
			end

			-- found your mate? then have a baby
			if num > 1 then

				self.hornytimer = 41
				ent.hornytimer = 41

				-- spawn baby
				minetest.after(5, function()

					-- custom breed function
					if self.on_breed then

						-- when false skip going any further
						if self.on_breed(self, ent) == false then
								return
						end
					else
						effect(pos, 15, "tnt_smoke.png", 1, 2, 2, 15, 5)
					end

					local mob = minetest.add_entity(pos, self.name)
					local ent2 = mob:get_luaentity()
					local textures = self.base_texture

					-- using specific child texture (if found)
					if self.child_texture then
						textures = self.child_texture[1]
					end

					-- and resize to half height
					mob:set_properties({
						textures = textures,
						visual_size = {
							x = self.base_size.x * .5,
							y = self.base_size.y * .5,
						},
						collisionbox = {
							self.base_colbox[1] * .5,
							self.base_colbox[2] * .5,
							self.base_colbox[3] * .5,
							self.base_colbox[4] * .5,
							self.base_colbox[5] * .5,
							self.base_colbox[6] * .5,
						},
					})
					-- tamed and owned by parents' owner
					ent2.child = true
					ent2.tamed = true
					ent2.owner = self.owner
				end)

				num = 0

				break
			end
		end
	end
end


-- find and replace what mob is looking for (grass, wheat etc.)
local replace = function(self, pos)

	if not self.replace_rate
	or not self.replace_what
	or self.child == true
	or self.object:getvelocity().y ~= 0
	or random(1, self.replace_rate) > 1 then
		return
	end

	local what, with, y_offset

	if type(self.replace_what[1]) == "table" then

		local num = random(#self.replace_what)

		what = self.replace_what[num][1] or ""
		with = self.replace_what[num][2] or ""
		y_offset = self.replace_what[num][3] or 0
	else
		what = self.replace_what
		with = self.replace_with or ""
		y_offset = self.replace_offset or 0
	end

	pos.y = pos.y + y_offset

	if #minetest.find_nodes_in_area(pos, pos, what) > 0 then

-- print ("replace node = ".. minetest.get_node(pos).name, pos.y)

		local oldnode = {name = what}
		local newnode = {name = with}
		local on_replace_return

		if self.on_replace then
			on_replace_return = self.on_replace(self, pos, oldnode, newnode)
		end

		if on_replace_return ~= false then

			minetest.set_node(pos, {name = with})

			-- when cow/sheep eats grass, replace wool and milk
			if self.gotten == true then
				self.gotten = false
				self.object:set_properties(self)
			end
		end
	end
end


-- check if daytime and also if mob is docile during daylight hours
local day_docile = function(self)

	if self.docile_by_day == false then

		return false

	elseif self.docile_by_day == true
	and self.time_of_day > 0.2
	and self.time_of_day < 0.8 then

		return true
	end
end


-- path finding and smart mob routine by rnd
local smart_mobs = function(self, s, p, dist, dtime)

	local s1 = self.path.lastpos

	-- is it becoming stuck?
	if abs(s1.x - s.x) + abs(s1.z - s.z) < 1.5 then
		self.path.stuck_timer = self.path.stuck_timer + dtime
	else
		self.path.stuck_timer = 0
	end

	self.path.lastpos = {x = s.x, y = s.y, z = s.z}

	-- im stuck, search for path
	if (self.path.stuck_timer > stuck_timeout and not self.path.following)
	or (self.path.stuck_timer > stuck_path_timeout and self.path.following) then

		self.path.stuck_timer = 0

		-- lets try find a path, first take care of positions
		-- since pathfinder is very sensitive
		local sheight = self.collisionbox[5] - self.collisionbox[2]

		-- round position to center of node to avoid stuck in walls
		-- also adjust height for player models!
		s.x = floor(s.x + 0.5)
--		s.y = floor(s.y + 0.5) - sheight
		s.z = floor(s.z + 0.5)

		local ssight, sground = minetest.line_of_sight(s, {
			x = s.x, y = s.y - 4, z = s.z}, 1)

		-- determine node above ground
		if not ssight then
			s.y = sground.y + 1
		end

		local p1 = self.attack:get_pos()

		p1.x = floor(p1.x + 0.5)
		p1.y = floor(p1.y + 0.5)
		p1.z = floor(p1.z + 0.5)

		local dropheight = 6
		if self.fear_height ~= 0 then dropheight = self.fear_height end

--		self.path.way = minetest.find_path(s, p1, 16, 2, 6, "Dijkstra")
		self.path.way = minetest.find_path(s, p1, 16, self.stepheight, dropheight, "A*_noprefetch")

		-- attempt to unstick mob that is "daydreaming"
		self.object:setpos({
			x = s.x + 0.1 * (random() * 2 - 1),
			y = s.y + 1,
			z = s.z + 0.1 * (random() * 2 - 1)
		})

		self.state = ""
		do_attack(self, self.attack)

		-- no path found, try something else
		if not self.path.way then

			self.path.following = false

			 -- lets make way by digging/building if not accessible
			if self.pathfinding == 2 then

				-- is player higher than mob?
				if s.y < p1.y then

					-- build upwards
					if not minetest.is_protected(s, "") then

						local ndef1 = minetest.registered_nodes[self.standing_in]

						if ndef1 and (ndef1.buildable_to or ndef1.groups.liquid) then

								minetest.set_node(s, {name = mobs.fallback_node})
						end
					end

					local sheight = math.ceil(self.collisionbox[5]) + 1

					-- assume mob is 2 blocks high so it digs above its head
					s.y = s.y + sheight

					-- remove one block above to make room to jump
					if not minetest.is_protected(s, "") then

						local node1 = node_ok(s, "air").name
						local ndef1 = minetest.registered_nodes[node1]

						if node1 ~= "air"
						and node1 ~= "ignore"
						and ndef1
						and not ndef1.groups.level
						and not ndef1.groups.unbreakable
						and not ndef1.groups.liquid then

							minetest.set_node(s, {name = "air"})
							minetest.add_item(s, ItemStack(node1))

						end
					end

					s.y = s.y - sheight
					self.object:setpos({x = s.x, y = s.y + 2, z = s.z})

				else -- dig 2 blocks to make door toward player direction

					local yaw1 = self.object:get_yaw() + pi / 2
					local p1 = {
						x = s.x + cos(yaw1),
						y = s.y,
						z = s.z + sin(yaw1)
					}

					if not minetest.is_protected(p1, "") then

						local node1 = node_ok(p1, "air").name
						local ndef1 = minetest.registered_nodes[node1]

						if node1 ~= "air"
						and node1 ~= "ignore"
						and ndef1
						and not ndef1.groups.level
						and not ndef1.groups.unbreakable
						and not ndef1.groups.liquid then

							minetest.add_item(p1, ItemStack(node1))
							minetest.set_node(p1, {name = "air"})
						end

						p1.y = p1.y + 1
						node1 = node_ok(p1, "air").name
						ndef1 = minetest.registered_nodes[node1]

						if node1 ~= "air"
						and node1 ~= "ignore"
						and ndef1
						and not ndef1.groups.level
						and not ndef1.groups.unbreakable
						and not ndef1.groups.liquid then

							minetest.add_item(p1, ItemStack(node1))
							minetest.set_node(p1, {name = "air"})
						end

					end
				end
			end

			-- will try again in 2 second
			self.path.stuck_timer = stuck_timeout - 2

			-- frustration! cant find the damn path :(
			mob_sound(self, self.sounds.random)
		else
			-- yay i found path
			mob_sound(self, self.sounds.attack)

			set_velocity(self, self.walk_velocity)

			-- follow path now that it has it
			self.path.following = true
		end
	end
end


-- specific attacks
local specific_attack = function(list, what)

	-- no list so attack default (player, animals etc.)
	if list == nil then
		return true
	end

	-- found entity on list to attack?
	for no = 1, #list do

		if list[no] == what then
			return true
		end
	end

	return false
end


-- monster find someone to attack
local monster_attack = function(self)

	if self.type ~= "monster"
	or not damage_enabled
	or creative
	or self.state == "attack"
	or day_docile(self) then
		return
	end

	local s = self.object:get_pos()
	local p, sp, dist
	local player, obj, min_player
	local type, name = "", ""
	local min_dist = self.view_range + 1
	local objs = minetest.get_objects_inside_radius(s, self.view_range)

	for n = 1, #objs do

		if objs[n]:is_player() then

			if mobs.invis[ objs[n]:get_player_name() ] then

				type = ""
			else
				player = objs[n]
				type = "player"
				name = "player"
			end
		else
			obj = objs[n]:get_luaentity()

			if obj then
				player = obj.object
				type = obj.type
				name = obj.name or ""
			end
		end

		-- find specific mob to attack, failing that attack player/npc/animal
		if specific_attack(self.specific_attack, name)
		and (type == "player" or type == "npc"
			or (type == "animal" and self.attack_animals == true)) then

			s = self.object:get_pos()
			p = player:get_pos()
			sp = s

			-- aim higher to make looking up hills more realistic
			p.y = p.y + 1
			sp.y = sp.y + 1

			dist = get_distance(p, s)

			if dist < self.view_range then
			-- field of view check goes here

				-- choose closest player to attack
				if line_of_sight(self, sp, p, 2) == true
				and dist < min_dist then
					min_dist = dist
					min_player = player
				end
			end
		end
	end

	-- attack player
	if min_player then
		do_attack(self, min_player)
	end
end

-- npc, find closest monster to attack
local npc_attack = function (self)

    if false then
    	if self.type ~= "npc"
    	or not self.attacks_monsters
    	or self.state == "attack" then
    		return
    	end
    end

    if  self.type  == "monster" or
        self.state == "attack"  then return end

    local may_attack = false
    if self.attacks_monsters    or
       self.attacks_set ~= nil then may_attack = true end
    if not may_attack then return end

	local p, sp, obj, min_player
	local s = self.object:get_pos()
	local min_dist = self.view_range + 1
	local objs = minetest.get_objects_inside_radius (s, self.view_range)

	for n = 1, #objs do
		obj = objs [n]:get_luaentity()
		local attack_it = false

		if self.attacks_monsters and
		   obj and obj.type == "monster" then
		    attack_it = true
		end

		if  self.attacks_set ~= nil and obj and obj.name and
            self.attacks_set [obj.name] then
		    attack_it = true
		end

		if attack_it then
			p = obj.object:get_pos()
			local dist = get_distance (p, s)

			if dist < min_dist then
				min_dist   = dist
				min_player = obj.object
			end
		end
	end

	if min_player then
		do_attack (self, min_player)
	end
end


-- follow player if owner or holding item, if fish outta water then flop
local follow_flop = function(self)

	-- find player to follow
	if (self.follow ~= ""
	or self.order == "follow")
	and not self.following
	and self.state ~= "attack"
	and self.state ~= "runaway" then

		local s = self.object:get_pos()
		local players = minetest.get_connected_players()

		for n = 1, #players do

			if get_distance(players[n]:get_pos(), s) < self.view_range
			and not mobs.invis[ players[n]:get_player_name() ] then

				self.following = players[n]

				break
			end
		end
	end

	if self.type == "npc"
	and self.order == "follow"
	and self.state ~= "attack"
	and self.owner ~= "" then

		-- npc stop following player if not owner
		if self.following
		and self.owner
		and self.owner ~= self.following:get_player_name() then
			self.following = nil
		end
	else
		-- stop following player if not holding specific item
		if self.following
		and self.following:is_player()
		and follow_holding(self, self.following) == false then
			self.following = nil
		end

	end

	-- follow that thing
	if self.following then

		local s = self.object:get_pos()
		local p

		if self.following:is_player() then

			p = self.following:get_pos()

		elseif self.following.object then

			p = self.following.object:get_pos()
		end

		if p then

			local dist = get_distance(p, s)

			-- dont follow if out of range
			if dist > self.view_range then
				self.following = nil
			else
				local vec = {
					x = p.x - s.x,
					z = p.z - s.z
				}

				local yaw = (atan(vec.z / vec.x) + pi / 2) - self.rotate

				if p.x > s.x then yaw = yaw + pi end

				yaw = set_yaw(self.object, yaw)

				-- anyone but standing npc's can move along
				if dist > self.reach
				and self.order ~= "stand" then

					set_velocity(self, self.walk_velocity)

					if self.walk_chance ~= 0 then
						set_animation(self, "walk")
					end
				else
					set_velocity(self, 0)
					set_animation(self, "stand")
				end

				return
			end
		end
	end

	-- swimmers flop when out of their element, and swim again when back in
	if self.fly then
		local s = self.object:get_pos()
		if not flight_check(self, s) then

			self.state = "flop"
			self.object:setvelocity({x = 0, y = -5, z = 0})

			set_animation(self, "stand")

			return
		elseif self.state == "flop" then
			self.state = "stand"
		end
	end
end


-- dogshoot attack switch and counter function
local dogswitch = function(self, dtime)

	-- switch mode not activated
	if not self.dogshoot_switch
	or not dtime then
		return 0
	end

	self.dogshoot_count = self.dogshoot_count + dtime

	if (self.dogshoot_switch == 1
	and self.dogshoot_count > self.dogshoot_count_max)
	or (self.dogshoot_switch == 2
	and self.dogshoot_count > self.dogshoot_count2_max) then

		self.dogshoot_count = 0

		if self.dogshoot_switch == 1 then
			self.dogshoot_switch = 2
		else
			self.dogshoot_switch = 1
		end
	end

	return self.dogshoot_switch
end


-- execute current state (stand, walk, run, attacks)
local do_states = function(self, dtime)

	local yaw = self.object:get_yaw() or 0

	if self.state == "stand" then

		if random(1, 4) == 1 then

			local lp = nil
			local s = self.object:get_pos()
			local objs = minetest.get_objects_inside_radius(s, 3)

			for n = 1, #objs do

				if objs[n]:is_player() then
					lp = objs[n]:get_pos()
					break
				end
			end

			-- look at any players nearby, otherwise turn randomly
			if lp then

				local vec = {
					x = lp.x - s.x,
					z = lp.z - s.z
				}

				yaw = (atan(vec.z / vec.x) + pi / 2) - self.rotate

				if lp.x > s.x then yaw = yaw + pi end
			else
				yaw = yaw + random(-0.5, 0.5)
			end

			yaw = set_yaw(self.object, yaw)
		end

		set_velocity(self, 0)
		set_animation(self, "stand")

		-- npc's ordered to stand stay standing
		if self.type ~= "npc"
		or self.order ~= "stand" then

			if self.walk_chance ~= 0
			and self.facing_fence ~= true
			and random(1, 100) <= self.walk_chance
			and is_at_cliff(self) == false then

				set_velocity(self, self.walk_velocity)
				self.state = "walk"
				set_animation(self, "walk")

				-- fly up/down randomly for flying mobs
				if self.fly and random(1, 100) <= self.walk_chance then

					local v = self.object:getvelocity()
					local ud = random(-1, 2) / 9

					self.object:setvelocity({x = v.x, y = ud, z = v.z})
				end
			end
		end

	elseif self.state == "walk" then

		local s = self.object:get_pos()
		local lp = nil

		-- is there something I need to avoid?
		if self.water_damage > 0
		and self.lava_damage > 0 then

			lp = minetest.find_node_near(s, 1, {"group:water", "group:lava"})

		elseif self.water_damage > 0 then

			lp = minetest.find_node_near(s, 1, {"group:water"})

		elseif self.lava_damage > 0 then

			lp = minetest.find_node_near(s, 1, {"group:lava"})
		end

		if lp then

			-- if mob in water or lava then look for land
			if (self.lava_damage
				and minetest.registered_nodes[self.standing_in].groups.lava)
			or (self.water_damage
				and minetest.registered_nodes[self.standing_in].groups.water) then

				lp = minetest.find_node_near(s, 5, {"group:soil", "group:stone",
					"group:sand", node_ice, node_snowblock})

				-- did we find land?
				if lp then

					local vec = {
						x = lp.x - s.x,
						z = lp.z - s.z
					}

					yaw = (atan(vec.z / vec.x) + pi / 2) - self.rotate

					if lp.x > s.x then yaw = yaw + pi end

					-- look towards land and jump/move in that direction
					yaw = set_yaw(self.object, yaw)
					do_jump(self)
					set_velocity(self, self.walk_velocity)
				else
					yaw = yaw + random(-0.5, 0.5)
				end

			else

				local vec = {
					x = lp.x - s.x,
					z = lp.z - s.z
				}

				yaw = (atan(vec.z / vec.x) + pi / 2) - self.rotate

				if lp.x > s.x then yaw = yaw + pi end
			end

			yaw = set_yaw(self.object, yaw)

		-- otherwise randomly turn
		elseif random(1, 100) <= 30 then

			yaw = yaw + random(-0.5, 0.5)

			yaw = set_yaw(self.object, yaw)
		end

		-- stand for great fall in front
		local temp_is_cliff = is_at_cliff(self)

		if self.facing_fence == true
		or temp_is_cliff
		or random(1, 100) <= 30 then

			set_velocity(self, 0)
			self.state = "stand"
			set_animation(self, "stand")
		else
			set_velocity(self, self.walk_velocity)

			if flight_check(self)
			and self.animation
			and self.animation.fly_start
			and self.animation.fly_end then
				set_animation(self, "fly")
			else
				set_animation(self, "walk")
			end
		end

	-- runaway when punched
	elseif self.state == "runaway" then

		self.runaway_timer = self.runaway_timer + 1

		-- stop after 5 seconds or when at cliff
		if self.runaway_timer > 5
		or is_at_cliff(self) then
			self.runaway_timer = 0
			set_velocity(self, 0)
			self.state = "stand"
			set_animation(self, "stand")
		else
			set_velocity(self, self.run_velocity)
			set_animation(self, "walk")
		end

	-- attack routines (explode, dogfight, shoot, dogshoot)
	elseif self.state == "attack" then

		-- calculate distance from mob and enemy
		local s = self.object:get_pos()
		local p = self.attack:get_pos() or s
		local dist = get_distance(p, s)

		-- stop attacking if player or out of range
		if dist > self.view_range
		or not self.attack
		or not self.attack:get_pos()
		or self.attack:get_hp() <= 0
		or (self.attack:is_player() and mobs.invis[ self.attack:get_player_name() ]) then

--			print(" ** stop attacking **", dist, self.view_range)
			self.state = "stand"
			set_velocity(self, 0)
			set_animation(self, "stand")
			self.attack = nil
			self.v_start = false
			self.timer = 0
			self.blinktimer = 0

			return
		end

		if self.attack_type == "explode" then

			local vec = {
				x = p.x - s.x,
				z = p.z - s.z
			}

			yaw = (atan(vec.z / vec.x) + pi / 2) - self.rotate

			if p.x > s.x then yaw = yaw + pi end

			yaw = set_yaw(self.object, yaw)

			-- start timer when inside reach
			if dist < self.reach and not self.v_start then
				self.v_start = true
				self.timer = 0
				self.blinktimer = 0
--				print ("=== explosion timer started", self.explosion_timer)
			end

			-- walk right up to player when timer active
			if dist < 1.5 and self.v_start then
				set_velocity(self, 0)
			else
				set_velocity(self, self.run_velocity)
			end

			if self.animation and self.animation.run_start then
				set_animation(self, "run")
			else
				set_animation(self, "walk")
			end

			if self.v_start then

				self.timer = self.timer + dtime
				self.blinktimer = (self.blinktimer or 0) + dtime

				if self.blinktimer > 0.2 then

					self.blinktimer = 0

					if self.blinkstatus then
						self.object:settexturemod("")
					else
						self.object:settexturemod("^[brighten")
					end

					self.blinkstatus = not self.blinkstatus
				end

--				print ("=== explosion timer", self.timer)

				if self.timer > self.explosion_timer then

					local pos = self.object:get_pos()
					local radius = self.explosion_radius or 1
					local damage_radius = radius

					-- dont damage anything if area protected or next to water
					if minetest.find_node_near(pos, 1, {"group:water"})
					or minetest.is_protected(pos, "") then

						damage_radius = 0
					end

					self.object:remove()

					if minetest.get_modpath("tnt") and tnt and tnt.boom
					and not minetest.is_protected(pos, "") then

						tnt.boom(pos, {
							radius = radius,
							damage_radius = damage_radius,
							sound = self.sounds.explode,
						})
					else

						minetest.sound_play(self.sounds.explode, {
							pos = pos,
							gain = 1.0,
							max_hear_distance = self.sounds.distance or 32
						})

						entity_physics(pos, damage_radius)
						effect(pos, 32, "tnt_smoke.png", radius * 3, radius * 5, radius, 1, 0)
					end

					return
				end
			end

		elseif self.attack_type == "dogfight"
		or (self.attack_type == "dogshoot" and dogswitch(self, dtime) == 2)
		or (self.attack_type == "dogshoot" and dist <= self.reach and dogswitch(self) == 0) then

			if self.fly
			and dist > self.reach then

				local p1 = s
				local me_y = floor(p1.y)
				local p2 = p
				local p_y = floor(p2.y + 1)
				local v = self.object:getvelocity()

				if flight_check(self, s) then

					if me_y < p_y then

						self.object:setvelocity({
							x = v.x,
							y = 1 * self.walk_velocity,
							z = v.z
						})

					elseif me_y > p_y then

						self.object:setvelocity({
							x = v.x,
							y = -1 * self.walk_velocity,
							z = v.z
						})
					end
				else
					if me_y < p_y then

						self.object:setvelocity({
							x = v.x,
							y = 0.01,
							z = v.z
						})

					elseif me_y > p_y then

						self.object:setvelocity({
							x = v.x,
							y = -0.01,
							z = v.z
						})
					end
				end

			end

			-- rnd: new movement direction
			if self.path.following
			and self.path.way
			and self.attack_type ~= "dogshoot" then

				-- no paths longer than 50
				if #self.path.way > 50
				or dist < self.reach then
					self.path.following = false
					return
				end

				local p1 = self.path.way[1]

				if not p1 then
					self.path.following = false
					return
				end

				if abs(p1.x-s.x) + abs(p1.z - s.z) < 0.6 then
					-- reached waypoint, remove it from queue
					table.remove(self.path.way, 1)
				end

				-- set new temporary target
				p = {x = p1.x, y = p1.y, z = p1.z}
			end

			local vec = {
				x = p.x - s.x,
				z = p.z - s.z
			}

			yaw = (atan(vec.z / vec.x) + pi / 2) - self.rotate

			if p.x > s.x then yaw = yaw + pi end

			yaw = set_yaw(self.object, yaw)

			-- move towards enemy if beyond mob reach
			if dist > self.reach then

				-- path finding by rnd
				if self.pathfinding -- only if mob has pathfinding enabled
				and enable_pathfinding then

					smart_mobs(self, s, p, dist, dtime)
				end

				if is_at_cliff(self) then

					set_velocity(self, 0)
					set_animation(self, "stand")
				else

					if self.path.stuck then
						set_velocity(self, self.walk_velocity)
					else
						set_velocity(self, self.run_velocity)
					end

					if self.animation and self.animation.run_start then
						set_animation(self, "run")
					else
						set_animation(self, "walk")
					end
				end

			else -- rnd: if inside reach range

				self.path.stuck = false
				self.path.stuck_timer = 0
				self.path.following = false -- not stuck anymore

				set_velocity(self, 0)

				if not self.custom_attack then

					if self.timer > 1 then

						self.timer = 0

						if self.double_melee_attack
						and random(1, 2) == 1 then
							set_animation(self, "punch2")
						else
							set_animation(self, "punch")
						end

						local p2 = p
						local s2 = s

						p2.y = p2.y + .5
						s2.y = s2.y + .5

						if line_of_sight(self, p2, s2) == true then

							-- play attack sound
							mob_sound(self, self.sounds.attack)

							-- punch player (or what player is attached to)
							local attached = self.attack:get_attach()
							if attached then
								self.attack = attached
							end
							self.attack:punch(self.object, 1.0, {
								full_punch_interval = 1.0,
								damage_groups = {fleshy = self.damage}
							}, nil)
						end
					end
				else	-- call custom attack every second
					if self.custom_attack
					and self.timer > 1 then

						self.timer = 0

						self.custom_attack(self, p)
					end
				end
			end

		elseif self.attack_type == "shoot"
		or (self.attack_type == "dogshoot" and dogswitch(self, dtime) == 1)
		or (self.attack_type == "dogshoot" and dist > self.reach and dogswitch(self) == 0) then

			p.y = p.y - .5
			s.y = s.y + .5

			local dist = get_distance(p, s)
			local vec = {
				x = p.x - s.x,
				y = p.y - s.y,
				z = p.z - s.z
			}

			yaw = (atan(vec.z / vec.x) + pi / 2) - self.rotate

			if p.x > s.x then yaw = yaw + pi end

			yaw = set_yaw(self.object, yaw)

			set_velocity(self, 0)

			if self.shoot_interval
			and self.timer > self.shoot_interval
			and random(1, 100) <= 60 then

				self.timer = 0
				set_animation(self, "shoot")

				-- play shoot attack sound
				mob_sound(self, self.sounds.shoot_attack)

				local p = self.object:get_pos()

				p.y = p.y + (self.collisionbox[2] + self.collisionbox[5]) / 2

				if minetest.registered_entities[self.arrow] then

					local obj = minetest.add_entity(p, self.arrow)
					local ent = obj:get_luaentity()
					local amount = (vec.x * vec.x + vec.y * vec.y + vec.z * vec.z) ^ 0.5
					local v = ent.velocity or 1 -- or set to default

					ent.switch = 1
					ent.owner_id = tostring(self.object) -- add unique owner id to arrow

					 -- offset makes shoot aim accurate
					vec.y = vec.y + self.shoot_offset
					vec.x = vec.x * (v / amount)
					vec.y = vec.y * (v / amount)
					vec.z = vec.z * (v / amount)

					obj:setvelocity(vec)
				end
			end
		end
	end
end


-- falling and fall damage
local falling = function(self, pos)

	if self.fly then
		return
	end

	-- floating in water (or falling)
	local v = self.object:getvelocity()

	if v.y > 0 then

		-- apply gravity when moving up
		self.object:setacceleration({
			x = 0,
			y = -10,
			z = 0
		})

	elseif v.y <= 0 and v.y > self.fall_speed then

		-- fall downwards at set speed
		self.object:setacceleration({
			x = 0,
			y = self.fall_speed,
			z = 0
		})
	else
		-- stop accelerating once max fall speed hit
		self.object:setacceleration({x = 0, y = 0, z = 0})
	end

	-- in water then float up
--	if minetest.registered_nodes[node_ok(pos).name].groups.liquid then
	if minetest.registered_nodes[node_ok(pos).name].groups.water then

		if self.floats == 1 then

			self.object:setacceleration({
				x = 0,
				y = -self.fall_speed / (max(1, v.y) ^ 2),
				z = 0
			})
		end
	else

		-- fall damage onto solid ground
		if self.fall_damage == 1
		and self.object:getvelocity().y == 0 then

			local d = (self.old_y or 0) - self.object:get_pos().y

			if d > 5 then

				self.health = self.health - floor(d - 5)

				effect(pos, 5, "tnt_smoke.png", 1, 2, 2, nil)

				if check_for_death(self, "fall", {type = "fall"}) then
					return
				end
			end

			self.old_y = self.object:get_pos().y
		end
	end
end


-- deal damage and effects when mob punched
local mob_punch = function(self, hitter, tflp, tool_capabilities, dir)

	-- custom punch function
	if self.do_punch then

		-- when false skip going any further
		if self.do_punch(self, hitter, tflp, tool_caps, dir) == false then
			return
		end
	end

	-- mob health check
--	if self.health <= 0 then
--		return
--	end

	-- error checking when mod profiling is enabled
	if not tool_capabilities then
		minetest.log("warning", "[mobs] Mod profiling enabled, damage not enabled")
		return
	end

	-- is mob protected?
	if self.protected and hitter:is_player()
	and minetest.is_protected(self.object:get_pos(), hitter:get_player_name()) then
		minetest.chat_send_player(hitter:get_player_name(), S("Mob has been protected!"))
		return
	end


	-- weapon wear
	local weapon = hitter:get_wielded_item()
	local punch_interval = 1.4

	-- calculate mob damage
	local damage = 0
	local armor = self.object:get_armor_groups() or {}
	local tmp

	-- quick error check incase it ends up 0 (serialize.h check test)
	if tflp == 0 then
		tflp = 0.2
	end

	if use_cmi then
		damage = cmi.calculate_damage(self.object, hitter, tflp, tool_capabilities, dir)
	else

		for group,_ in pairs( (tool_capabilities.damage_groups or {}) ) do

			tmp = tflp / (tool_capabilities.full_punch_interval or 1.4)

			if tmp < 0 then
				tmp = 0.0
			elseif tmp > 1 then
				tmp = 1.0
			end

			damage = damage + (tool_capabilities.damage_groups[group] or 0)
				* tmp * ((armor[group] or 0) / 100.0)
		end
	end

	-- check for tool immunity or special damage
	for n = 1, #self.immune_to do

		if self.immune_to[n][1] == weapon:get_name() then

			damage = self.immune_to[n][2] or 0
			break
		end
	end

	-- healing
	if damage <= -1 then
		self.health = self.health - floor(damage)
		return
	end

--	print ("Mob Damage is", damage)

	if use_cmi then

		local cancel =  cmi.notify_punch(self.object, hitter, tflp, tool_capabilities, dir, damage)

		if cancel then return end
	end

	-- add weapon wear
	if tool_capabilities then
		punch_interval = tool_capabilities.full_punch_interval or 1.4
	end

	if weapon:get_definition()
	and weapon:get_definition().tool_capabilities then

		weapon:add_wear(floor((punch_interval / 75) * 9000))
		hitter:set_wielded_item(weapon)
	end

	-- only play hit sound and show blood effects if damage is 1 or over
	if damage >= 1 then

		-- weapon sounds
		if weapon:get_definition().sounds ~= nil then

			local s = random(0, #weapon:get_definition().sounds)

			minetest.sound_play(weapon:get_definition().sounds[s], {
				object = self.object, --hitter,
				max_hear_distance = 8
			})
		else
			minetest.sound_play("default_punch", {
				object = self.object, --hitter,
				max_hear_distance = 5
			})
		end

		-- blood_particles
		if self.blood_amount > 0
		and not disable_blood then

			local pos = self.object:get_pos()

			pos.y = pos.y + (-self.collisionbox[2] + self.collisionbox[5]) * .5

			effect(pos, self.blood_amount, self.blood_texture, nil, nil, 1, nil)
		end

		-- do damage
		self.health = self.health - floor(damage)

		-- exit here if dead, special item check
		if weapon:get_name() == "mobs:pick_lava" then
			if check_for_death(self, "lava", {type = "punch",
					puncher = hitter}) then
				return
			end
		else
			if check_for_death(self, "hit", {type = "punch",
					puncher = hitter}) then
				return
			end
		end

		--[[ add healthy afterglow when hit (can cause hit lag with larger textures)
		core.after(0.1, function()
			self.object:settexturemod("^[colorize:#c9900070")

			core.after(0.3, function()
				self.object:settexturemod("")
			end)
		end) ]]

		-- knock back effect (only on full punch)
		if self.knock_back > 0
		and tflp >= punch_interval then

			local v = self.object:getvelocity()
			local r = 1.4 - min(punch_interval, 1.4)
			local kb = r * 5
			local up = 2

			-- if already in air then dont go up anymore when hit
			if v.y > 0
			or self.fly then
				up = 0
			end

			-- direction error check
			dir = dir or {x = 0, y = 0, z = 0}

			-- check if tool already has specific knockback value
			if tool_capabilities.damage_groups["knockback"] then
				kb = tool_capabilities.damage_groups["knockback"]
			else
				kb = kb * 1.5
			end

			self.object:setvelocity({
				x = dir.x * kb,
				y = up,
				z = dir.z * kb
			})

			self.pause_timer = 0.25
		end
	end -- END if damage

	-- if skittish then run away
	if self.runaway == true then

		local lp = hitter:get_pos()
		local s = self.object:get_pos()
		local vec = {
			x = lp.x - s.x,
			y = lp.y - s.y,
			z = lp.z - s.z
		}

		local yaw = (atan(vec.z / vec.x) + 3 * pi / 2) - self.rotate

		if lp.x > s.x then
			yaw = yaw + pi
		end

		yaw = set_yaw(self.object, yaw)
		self.state = "runaway"
		self.runaway_timer = 0
		self.following = nil
	end

	local name = hitter:get_player_name() or ""

	-- attack puncher and call other mobs for help
	if self.passive == false
	and self.state ~= "flop"
	and self.child == false
	and hitter:get_player_name() ~= self.owner
	and not mobs.invis[ name ] then

		-- attack whoever punched mob
		self.state = ""
		do_attack(self, hitter)

		-- alert others to the attack
		local objs = minetest.get_objects_inside_radius(hitter:get_pos(), self.view_range)
		local obj = nil

		for n = 1, #objs do

			obj = objs[n]:get_luaentity()

			if obj then

				-- only alert members of same mob
				if obj.group_attack == true
				and obj.state ~= "attack"
				and obj.owner ~= name
				and obj.name == self.name then
					do_attack(obj, hitter)
				end

				-- have owned mobs attack player threat
				if obj.owner == name and obj.owner_loyal then
					do_attack(obj, self.object)
				end
			end
		end
	end
end


-- get entity staticdata
local mob_staticdata = function(self)

	-- remove mob when out of range unless tamed
	if remove_far
	and self.remove_ok
	and not self.tamed
	and self.lifetimer < 20000 then
        -- RJK code
        if codermobs_disable_wild then self.lifetimer = 0 end

		--print ("REMOVED " .. self.name)

		self.object:remove()

		return ""-- nil
	end

	self.remove_ok = true
	self.attack = nil
	self.following = nil
	self.state = "stand"

	-- used to rotate older mobs
	if self.drawtype
	and self.drawtype == "side" then
		self.rotate = math.rad(90)
	end

	if use_cmi then
		self.serialized_cmi_components = cmi.serialize_components(self._cmi_components)
	end

	local tmp = {}

	for _,stat in pairs(self) do

		local t = type(stat)

		if  t ~= "function"
		and t ~= "nil"
		and t ~= "userdata"
		and _ ~= "_cmi_components" then
			tmp[_] = self[_]
		end
	end

	--print('===== '..self.name..'\n'.. dump(tmp)..'\n=====\n')
	return minetest.serialize(tmp)
end


-- activate mob and reload settings
local mob_activate = function(self, staticdata, def, dtime)

	-- remove monsters in peaceful mode
	if self.type == "monster"
	and peaceful_only then

		self.object:remove()

		return
	end

	-- load entity variables
	local tmp = minetest.deserialize(staticdata)

	if tmp then
		for _,stat in pairs(tmp) do
			self[_] = stat
		end
	end

	-- select random texture, set model and size
	if not self.base_texture then

		-- compatiblity with old simple mobs textures
		if type(def.textures[1]) == "string" then
			def.textures = {def.textures}
		end

		self.base_texture = def.textures[random(1, #def.textures)]
		self.base_mesh = def.mesh
		self.base_size = self.visual_size
		self.base_colbox = self.collisionbox
	end

	-- set texture, model and size
	local textures = self.base_texture
	local mesh = self.base_mesh
	local vis_size = self.base_size
	local colbox = self.base_colbox

	-- specific texture if gotten
	if self.gotten == true
	and def.gotten_texture then
		textures = def.gotten_texture
	end

	-- specific mesh if gotten
	if self.gotten == true
	and def.gotten_mesh then
		mesh = def.gotten_mesh
	end

	-- set child objects to half size
	if self.child == true then

		vis_size = {
			x = self.base_size.x * .5,
			y = self.base_size.y * .5,
		}

		if def.child_texture then
			textures = def.child_texture[1]
		end

		colbox = {
			self.base_colbox[1] * .5,
			self.base_colbox[2] * .5,
			self.base_colbox[3] * .5,
			self.base_colbox[4] * .5,
			self.base_colbox[5] * .5,
			self.base_colbox[6] * .5
		}
	end

	if self.health == 0 then
		self.health = random (self.hp_min, self.hp_max)
	end

	-- pathfinding init
	self.path = {}
	self.path.way = {} -- path to follow, table of positions
	self.path.lastpos = {x = 0, y = 0, z = 0}
	self.path.stuck = false
	self.path.following = false -- currently following path?
	self.path.stuck_timer = 0 -- if stuck for too long search for path

	-- mob defaults
	self.object:set_armor_groups({immortal = 1, fleshy = self.armor})
	self.old_y = self.object:get_pos().y
	self.old_health = self.health
	self.sounds.distance = self.sounds.distance or 10
	self.textures = textures
	self.mesh = mesh
	self.collisionbox = colbox
	self.visual_size = vis_size
	self.standing_in = ""

	-- check existing nametag
	if not self.nametag then
		self.nametag = def.nametag
	end

	-- set anything changed above
	self.object:set_properties(self)
	set_yaw(self.object, (random(0, 360) - 180) / 180 * pi)
	update_tag(self)
	set_animation(self, "stand")

	-- run on_spawn function if found
	if self.on_spawn and not self.on_spawn_run then
		if self.on_spawn(self) then
			self.on_spawn_run = true --  if true, set flag to run once only
		end
	end

	-- run after_activate
	if def.after_activate then
		def.after_activate(self, staticdata, def, dtime)
	end

	if use_cmi then
		self._cmi_components = cmi.activate_components(self.serialized_cmi_components)
		cmi.notify_activate(self.object, dtime)
	end
end


-- main mob function
local mob_step = function(self, dtime)

	if use_cmi then
		cmi.notify_step(self.object, dtime)
	end

	local pos = self.object:get_pos()
	local yaw = 0

    -- RJK code
    if (self.type == "monster" and peaceful_only         ) or
       (self.type == "npc"     and codermobs_disable_npc  ) or
       (not self.tamed         and codermobs_disable_wild ) or
       codermobs_disable_mobs then
        self.object:remove()
        return
    end

	-- when lifetimer expires remove mob (except npc and tamed)
	if self.type ~= "npc"
	and not self.tamed
	and self.state ~= "attack"
	and remove_far ~= true
	and self.lifetimer < 20000 then

		self.lifetimer = self.lifetimer - dtime

		if self.lifetimer <= 0 then

			-- only despawn away from player
			local objs = minetest.get_objects_inside_radius(pos, 15)

			for n = 1, #objs do

				if objs[n]:is_player() then

					self.lifetimer = 20

					return
				end
			end

--			minetest.log("action",
--				S("lifetimer expired, removed @1", self.name))

			effect(pos, 15, "tnt_smoke.png", 2, 4, 2, 0)

			self.object:remove()

			return
		end
	end

-- RJK: Start of simple mob talk code.
--
    if self.name == nil then
        self.name = "__oink__"
    end
    if self.name == "codermobs:bee"
        and not self.tamed and math.random (2) == 1 then
        local ttime = os.time()
        if (ttime - LastBeeTalkTime) > BeeTalkDelay then
        local mm = math.random (#BeeRemarks)
        local ss = BeeRemarks [mm]
        minetest.chat_send_all ("<bee> " .. ss)
        LastBeeTalkTime = ttime
        end
    end
    if self.name == "codermobs:kitten"
        and not self.tamed and math.random (2) == 1 then
        local ttime = os.time()
        if (ttime - LastKittenTalkTime) > KittenTalkDelay then
            local mm = math.random (#KittenRemarks)
            local ss = KittenRemarks [mm]
            minetest.chat_send_all ("<kitten> " .. ss)
            LastKittenTalkTime = ttime
        end
    end
    if self.name == "codermobs:wolf"
        and not self.tamed and math.random (2) == 1 then
        local ttime = os.time()
        if (ttime - LastWolfTalkTime) > WolfTalkDelay then
            local mm = math.random (#WolfRemarks)
            local ss = WolfRemarks [mm]
            minetest.chat_send_all ("<wolf> " .. ss)
            LastWolfTalkTime = ttime
        end
    end
--
-- RJK: End of simple mob talk code.

	falling(self, pos)

	-- knockback timer
	if self.pause_timer > 0 then

		self.pause_timer = self.pause_timer - dtime

		return
	end

	-- run custom function (defined in mob lua file)
	if self.do_custom then

		-- when false skip going any further
		if self.do_custom(self, dtime) == false then
			return
		end
	end

	-- attack timer
	self.timer = self.timer + dtime

	if self.state ~= "attack" then
		if self.timer < 1 then
			return
		end
		self.timer = 0
	end

	-- never go over 100
	if self.timer > 100 then
		self.timer = 1
	end

	-- node replace check (cow eats grass etc.)
	replace(self, pos)

	-- mob plays random sound at times
	if random(1, 100) == 1 then
		mob_sound(self, self.sounds.random)
	end

	-- environmental damage timer (every 1 second)
	self.env_damage_timer = self.env_damage_timer + dtime

	if (self.state == "attack" and self.env_damage_timer > 1)
	or self.state ~= "attack" then

		self.env_damage_timer = 0

		do_env_damage(self)
	end

	monster_attack(self)
	npc_attack(self)
	breed(self)
	follow_flop(self)
	do_states(self, dtime)
	do_jump(self)
end


-- default function when mobs are blown up with TNT
local do_tnt = function(obj, damage)

	--print ("----- Damage", damage)

	obj.object:punch(obj.object, 1.0, {
		full_punch_interval = 1.0,
		damage_groups = {fleshy = damage},
	}, nil)

	return false, true, {}
end


mobs.spawning_mobs = {}

-- register mob entity
function mobs:register_mob (name, def)

	mobs.spawning_mobs[name] = true

minetest.register_entity(name, {

	stepheight = def.stepheight or 1.1, -- was 0.6
	name = name,
	type = def.type,
	attack_type = def.attack_type,
	fly = def.fly,
	fly_in = def.fly_in or "air",
	owner = def.owner or "",
	order = def.order or "",
	on_die = def.on_die,
	do_custom = def.do_custom,
	jump_height = def.jump_height or 4, -- was 6
	drawtype = def.drawtype, -- DEPRECATED, use rotate instead
	rotate = math.rad(def.rotate or 0), --  0=front, 90=side, 180=back, 270=side2
	lifetimer = def.lifetimer or 180, -- 3 minutes
	hp_min = max(1, (def.hp_min or 5) * difficulty),
	hp_max = max(1, (def.hp_max or 10) * difficulty),
	physical = true,
	collisionbox = def.collisionbox,
	visual = def.visual,
	visual_size = def.visual_size or {x = 1, y = 1},
	mesh = def.mesh,
	makes_footstep_sound = def.makes_footstep_sound or false,
	view_range = def.view_range or 5,
	walk_velocity = def.walk_velocity or 1,
	run_velocity = def.run_velocity or 2,
	damage = max(0, (def.damage or 0) * difficulty),
	light_damage = def.light_damage or 0,
	water_damage = def.water_damage or 0,
	lava_damage = def.lava_damage or 0,
	suffocation = def.suffocation or 2,
	fall_damage = def.fall_damage or 1,
	fall_speed = def.fall_speed or -10, -- must be lower than -2 (default: -10)
	drops = def.drops or {},
	armor = def.armor or 100,
	on_rightclick = def.on_rightclick,
	arrow = def.arrow,
	shoot_interval = def.shoot_interval,
	sounds = def.sounds or {},
	animation = def.animation,
	follow = def.follow,
	jump = def.jump ~= false,
	walk_chance = def.walk_chance or 50,
	attacks_monsters = def.attacks_monsters or false,

    -- RJK:
	attacks_set = def.attacks_set,

	group_attack = def.group_attack or false,
	passive = def.passive or false,
	knock_back = def.knock_back or 3,
	blood_amount = def.blood_amount or 5,
	blood_texture = def.blood_texture or "mobs_blood.png",
	shoot_offset = def.shoot_offset or 0,
	floats = def.floats or 1, -- floats in water by default
	replace_rate = def.replace_rate,
	replace_what = def.replace_what,
	replace_with = def.replace_with,
	replace_offset = def.replace_offset or 0,
	on_replace = def.on_replace,
	timer = 0,
	env_damage_timer = 0, -- only used when state = "attack"
	tamed = false,
	pause_timer = 0,
	horny = false,
	hornytimer = 0,
	child = false,
	gotten = false,
	health = 0,
	reach = def.reach or 3,
	htimer = 0,
	texture_list = def.textures,
	child_texture = def.child_texture,
	docile_by_day = def.docile_by_day or false,
	time_of_day = 0.5,
	fear_height = def.fear_height or 0,
	runaway = def.runaway,
	runaway_timer = 0,
	pathfinding = def.pathfinding,
	immune_to = def.immune_to or {},
	explosion_radius = def.explosion_radius,
	explosion_timer = def.explosion_timer or 3,
	custom_attack = def.custom_attack,
	double_melee_attack = def.double_melee_attack,
	dogshoot_switch = def.dogshoot_switch,
	dogshoot_count = 0,
	dogshoot_count_max = def.dogshoot_count_max or 5,
	dogshoot_count2_max = def.dogshoot_count2_max or (def.dogshoot_count_max or 5),
	attack_animals = def.attack_animals or false,
	specific_attack = def.specific_attack,
	owner_loyal = def.owner_loyal,
	facing_fence = false,
	_cmi_is_mob = true,

	on_spawn = def.on_spawn,

	on_blast = def.on_blast or do_tnt,

	on_step = mob_step,

	do_punch = def.do_punch,

	on_punch = mob_punch,

	on_breed = def.on_breed,

	on_grown = def.on_grown,

	on_activate = function(self, staticdata, dtime)
		return mob_activate(self, staticdata, def, dtime)
	end,

	get_staticdata = function(self)
		return mob_staticdata(self)
	end,

})

end -- END mobs:register_mob function

local function StartsWithAnyOf (String, StartList)
    for _, str in ipairs (StartList) do
        if string.sub (String, 1, string.len (str)) == str then
            return true
        end
    end
    return false
end

local mob_prefixes = {
    "critters_", "codermobs:", "petores:", "codersea:"
}

local count_mobs = function (pos, type, mbrange)
	local num_type  = 0
	local num_total = 0

    mbrange = mbrange * 16
	local objs = minetest.get_objects_inside_radius (pos, mbrange)

	for n = 1, #objs do
		if not objs [n]:is_player() then
			local obj = objs [n]:get_luaentity()

			if obj and obj.name and
			    StartsWithAnyOf (obj.name, mob_prefixes) then
                num_total = num_total + 1

                if obj.name == type then
                    num_type  = num_type + 1
                end
			end
		end
	end

	return num_type, num_total
end

-- global functions

function mobs:spawn_specific (name, nodes, neighbors, min_light, max_light,
	interval, chance, aoc, min_height, max_height, day_toggle, on_spawn)

    if cmdebug then
print ("cmdebug spawn_specific"
    .. " name:"           .. name
    .. " min_light:"      .. min_light
    .. " max_light:"      .. max_light
    .. " min_height:"     .. min_height
    .. " max_height:"     .. max_height
       )
    end

    local mbrange = mobs.mbrange
    mobs.mbrange = nil

    -- RJK: Set a default active_object_count
    if (not aoc) or (aoc < 1) then
        aoc = mobs.defaultaoc
    end

	-- chance/spawn number override in minetest.conf for registered mob
	local numbers = minetest.settings:get(name)

	if numbers then
		numbers = numbers:split(",")
		chance = tonumber(numbers[1]) or chance
		aoc = tonumber(numbers[2]) or aoc

		if chance == 0 then
			minetest.log("warning", string.format("[mobs] %s has spawning disabled", name))
			return
		end

		minetest.log("action",
			string.format("[mobs] Chance setting for %s changed to %s (total: %s)", name, chance, aoc))

	end

	minetest.register_abm ({
		label = name .. " spawning",
		nodenames = nodes,
		neighbors = neighbors,
		interval = interval,
		chance   = chance ,
		catch_up = false,

		action = function (pos, node, active_object_count, active_object_count_wider)

            if cmdebug then
print ("cmdebug chance:"..chance.." name:"..name.." pos:"
..pos.x..","..pos.y..","..pos.z)
            end

			-- is mob actually registered?
			if not mobs.spawning_mobs[name] then
				return
			end

--			if active_object_count_wider >= max_per_block then
--				return
--			end

            if mbrange == nil or mbrange == 0 then mbrange = 1 end
            if mbrange > 3 then mbrange = 3 end
            local m3  = mbrange * mbrange * mbrange
            local cde = codermobs_density * m3

            local not_ghost = true
            if (name == "codermobs:ghost") then not_ghost = false end

            local a1, a2 = count_mobs (pos, name, mbrange)
			if  (a1 >= aoc) or
			    (not_ghost and (a1 > 0) and (a2 >= cde/2)) or
			    (not_ghost and (a2 >= cde)) then
			    if cmdebug then
print ("cmdebug too many entities: ", name, a1, aoc, a2, codermobs_density)
                end
				return
			end

			-- if toggle set to nil then ignore day/night check
			if day_toggle ~= nil then
				local tod = (minetest.get_timeofday() or 0) * 24000

				if tod > 4500 and tod < 19500 then
					-- daylight, but mob wants night
					if day_toggle == false then
						return
					end
				else
					-- night time but mob wants day
					if day_toggle == true then
						return
					end
				end
			end

			-- spawn above node
			pos.y = pos.y + 1

			-- only spawn away from player
			local objs = minetest.get_objects_inside_radius(pos, 6)

			for n = 1, #objs do
				if objs[n]:is_player() then
					return
				end
			end

			-- mobs cannot spawn in protected areas when enabled
			if not codermobs_spawn_protected
			and minetest.is_protected(pos, "") then
				return
			end

			-- are we spawning within height limits?
			if pos.y > max_height
			or pos.y < min_height then
				return
			end

			-- are light levels ok?
			local light = minetest.get_node_light(pos)
			if not light
			or light > max_light
			or light < min_light then
				return
			end

			-- are we spawning inside solid nodes?
			if minetest.registered_nodes[node_ok(pos).name].walkable == true then
				return
			end

			pos.y = pos.y + 1

			if minetest.registered_nodes[node_ok(pos).name].walkable == true then
				return
			end

			-- spawn mob half block higher than ground
			pos.y = pos.y - 0.5

			if minetest.registered_entities[name] then
				local mob = minetest.add_entity(pos, name)
--[[
				print ("[mobs] Spawned " .. name .. " at "
				.. minetest.pos_to_string(pos) .. " on "
				.. node.name .. " near " .. neighbors[1])
]]
				if on_spawn then

					local ent = mob:get_luaentity()

					on_spawn(ent, pos)
				end
			else
				minetest.log("warning", string.format("[mobs] %s failed to spawn at %s",
					name, minetest.pos_to_string(pos)))
			end
		end
	})
end

-- RJK: Support for spawning amphibious mobs

-- compatibility with older mob registration
function mobs:register_spawn (name, nodes, max_light, min_light,
chance, active_object_count, max_height, day_toggle)

    if cmdebug then
        print ("cmdebug register_spawn"
.. " name:"           .. name
.. " min_light:"      .. min_light
.. " max_light:"      .. max_light
.. " max_height:"     .. max_height
        )
    end

    local spawn_in = { "air" }

    -- RJK
    if name == "codermobs:mooncow" then
        spawn_in = { "moontest:vacuum" }
    end

    local amphibious = mobs.amphibious
    mobs.amphibious = nil

    if (amphibious ~= nil) and amphibious then
        spawn_in = {
            "default:water_source"  ,
            "default:water_flowing" ,
            "air"                   ,
        }
    end

    if mobs.spawn_by ~= nil then spawn_in = mobs.spawn_by end
    mobs.spawn_by = nil

	mobs:spawn_specific (name, nodes, spawn_in, min_light, max_light, 30,
		chance, active_object_count, -31000, max_height, day_toggle)
end


-- MarkBu's spawn function
function mobs:spawn(def)

	local name = def.name
	local nodes = def.nodes or {"group:soil", "group:stone"}
	local neighbors = def.neighbors or {"air"}
	local min_light = def.min_light or 0
	local max_light = def.max_light or 15
	local interval = def.interval or 30
	local chance = def.chance or 5000
	local active_object_count = def.active_object_count or 1
	local min_height = def.min_height or -31000
	local max_height = def.max_height or 31000
	local day_toggle = def.day_toggle
	local on_spawn = def.on_spawn

	mobs:spawn_specific(name, nodes, neighbors, min_light, max_light, interval,
		chance, active_object_count, min_height, max_height, day_toggle, on_spawn)
end


-- register arrow for shoot attack
function mobs:register_arrow(name, def)

	if not name or not def then return end -- errorcheck

	minetest.register_entity(name, {

		physical = false,
		visual = def.visual,
		visual_size = def.visual_size,
		textures = def.textures,
		velocity = def.velocity,
		hit_player = def.hit_player,
		hit_node = def.hit_node,
		hit_mob = def.hit_mob,
		drop = def.drop or false, -- drops arrow as registered item when true
		collisionbox = {0, 0, 0, 0, 0, 0}, -- remove box around arrows
		timer = 0,
		switch = 0,
		owner_id = def.owner_id,
		rotate = def.rotate,
		automatic_face_movement_dir = def.rotate
			and (def.rotate - (pi / 180)) or false,

		on_activate = def.on_activate,

		on_step = def.on_step or function(self, dtime)

			self.timer = self.timer + 1

			local pos = self.object:get_pos()

			if self.switch == 0
			or self.timer > 150
			or not within_limits(pos, 0) then

				self.object:remove() ; -- print ("removed arrow")

				return
			end

			-- does arrow have a tail (fireball)
			if def.tail
			and def.tail == 1
			and def.tail_texture then

				minetest.add_particle({
					pos = pos,
					velocity = {x = 0, y = 0, z = 0},
					acceleration = {x = 0, y = 0, z = 0},
					expirationtime = def.expire or 0.25,
					collisiondetection = false,
					texture = def.tail_texture,
					size = def.tail_size or 5,
					glow = def.glow or 0,
				})
			end

			if self.hit_node then

				local node = node_ok(pos).name

				if minetest.registered_nodes[node].walkable then

					self.hit_node(self, pos, node)

					if self.drop == true then

						pos.y = pos.y + 1

						self.lastpos = (self.lastpos or pos)

						minetest.add_item(self.lastpos, self.object:get_luaentity().name)
					end

					self.object:remove() ; -- print ("hit node")

					return
				end
			end

			if self.hit_player or self.hit_mob then

				for _,player in pairs(minetest.get_objects_inside_radius(pos, 1.0)) do

					if self.hit_player
					and player:is_player() then

						self.hit_player(self, player)
						self.object:remove() ; -- print ("hit player")
						return
					end

					local entity = player:get_luaentity()

					if entity
					and self.hit_mob
					and entity._cmi_is_mob == true
					and tostring(player) ~= self.owner_id
					and entity.name ~= self.object:get_luaentity().name then

						self.hit_mob(self, player)

						self.object:remove() ;  --print ("hit mob")

						return
					end
				end
			end

			self.lastpos = pos
		end
	})
end


-- compatibility function
function mobs:explosion(pos, radius)
	local self = {sounds = {}}
	self.sounds.explode = "tnt_explode"
	mobs:boom(self, pos, radius)
end


-- make explosion with protection and tnt mod check
function mobs:boom(self, pos, radius)

	if minetest.get_modpath("tnt") and tnt and tnt.boom
	and not minetest.is_protected(pos, "") then

		tnt.boom(pos, {
			radius = radius,
			damage_radius = radius,
			sound = self.sounds.explode,
			explode_center = true,
		})
	else
		minetest.sound_play(self.sounds.explode, {
			pos = pos,
			gain = 1.0,
			max_hear_distance = self.sounds.distance or 32
		})

		entity_physics(pos, radius)
		effect(pos, 32, "tnt_smoke.png", radius * 3, radius * 5, radius, 1, 0)
	end
end


-- Register spawn eggs

-- Note: This also introduces the “spawn_egg” group:
-- * spawn_egg=1: Spawn egg (generic mob, no metadata)
-- * spawn_egg=2: Spawn egg (captured/tamed mob, metadata)
function mobs:register_egg(mob, desc, background, addegg, no_creative)

	local grp = {spawn_egg = 1}

    -- RJK code: 
    if codermobs_creative_eggs == false then
         no_creative = true
    end

	-- do NOT add this egg to creative inventory (e.g. dungeon master)
	if creative and no_creative == true then
		grp.not_in_creative_inventory = 1
	end

	local invimg = background

	if addegg == 1 then
		invimg = "mobs_chicken_egg.png^(" .. invimg ..
			"^[mask:mobs_chicken_egg_overlay.png)"
	end

	-- register new spawn egg containing mob information
	minetest.register_craftitem(mob .. "_set", {

		description = S("@1 (Tamed)", desc),
		inventory_image = invimg,
		groups = {spawn_egg = 2, not_in_creative_inventory = 1},
		stack_max = 1,

		on_place = function(itemstack, placer, pointed_thing)

			local pos = pointed_thing.above

			-- am I clicking on something with existing on_rightclick function?
			local under = minetest.get_node(pointed_thing.under)
			local def = minetest.registered_nodes[under.name]
			if def and def.on_rightclick then
				return def.on_rightclick(pointed_thing.under, under, placer, itemstack)
			end

			if pos
			and within_limits(pos, 0)
			and not minetest.is_protected(pos, placer:get_player_name()) then

				if not minetest.registered_entities[mob] then
					return
				end

				pos.y = pos.y + 1

				local data = itemstack:get_metadata()
				local mob = minetest.add_entity(pos, mob, data)
				local ent = mob:get_luaentity()

				-- set owner if not a monster
				if ent.type ~= "monster" then
					ent.owner = placer:get_player_name()
					ent.tamed = true
				end

				-- since mob is unique we remove egg once spawned
				itemstack:take_item()
			end

			return itemstack
		end,
	})


	-- register old stackable mob egg
	minetest.register_craftitem(mob, {

		description = desc,
		inventory_image = invimg,
		groups = grp,

		on_place = function(itemstack, placer, pointed_thing)

			local pos = pointed_thing.above

			-- am I clicking on something with existing on_rightclick function?
			local under = minetest.get_node(pointed_thing.under)
			local def = minetest.registered_nodes[under.name]
			if def and def.on_rightclick then
				return def.on_rightclick(pointed_thing.under, under, placer, itemstack)
			end

			if pos
			and within_limits(pos, 0)
			and not minetest.is_protected(pos, placer:get_player_name()) then

				if not minetest.registered_entities[mob] then
					return
				end

				pos.y = pos.y + 1

				local mob = minetest.add_entity(pos, mob)
				local ent = mob:get_luaentity()

				-- don't set owner if monster or sneak pressed
				if ent.type ~= "monster"
				and not placer:get_player_control().sneak then
					ent.owner = placer:get_player_name()
					ent.tamed = true
				end

				-- if not in creative then take item
				if not mobs.is_creative(placer:get_player_name()) then
					itemstack:take_item()
				end
			end

			return itemstack
		end,
	})

end


-- capture critter (thanks to blert2112 for idea)
function mobs:capture_mob(self, clicker, chance_hand, chance_net, chance_lasso, force_take, replacewith)

	if self.child
	or not clicker:is_player()
	or not clicker:get_inventory() then
		return false
	end

	-- get name of clicked mob
	local mobname = self.name

	-- if not nil change what will be added to inventory
	if replacewith then
		mobname = replacewith
	end

	local name = clicker:get_player_name()
	local tool = clicker:get_wielded_item()

	-- are we using hand, net or lasso to pick up mob?
	if tool:get_name() ~= ""
	and tool:get_name() ~= "mobs:net"
	and tool:get_name() ~= "mobs:lasso" then
		return false
	end

	-- is mob tamed?
	if self.tamed == false
	and force_take == false then

		minetest.chat_send_player(name, S("Not tamed!"))

		return true -- false
	end

	-- cannot pick up if not owner
	if self.owner ~= name
	and force_take == false then

		minetest.chat_send_player(name, S("@1 is owner!", self.owner))

		return true -- false
	end

	if clicker:get_inventory():room_for_item("main", mobname) then

		-- was mob clicked with hand, net, or lasso?
		local chance = 0

		if tool:get_name() == "" then
			chance = chance_hand

		elseif tool:get_name() == "mobs:net" then

			chance = chance_net

			tool:add_wear(4000) -- 17 uses

			clicker:set_wielded_item(tool)

		elseif tool:get_name() == "mobs:lasso" then

			chance = chance_lasso

			tool:add_wear(650) -- 100 uses

			clicker:set_wielded_item(tool)

		end

		-- calculate chance.. add to inventory if successful?
		if chance > 0 and random(1, 100) <= chance then

			-- default mob egg
			local new_stack = ItemStack(mobname)

			-- add special mob egg with all mob information
			-- unless 'replacewith' contains new item to use
			if not replacewith then

				new_stack = ItemStack(mobname .. "_set")

				local tmp = {}

				for _,stat in pairs(self) do
					local t = type(stat)
					if  t ~= "function"
					and t ~= "nil"
					and t ~= "userdata" then
						tmp[_] = self[_]
					end
				end

				local data_str = minetest.serialize(tmp)

				new_stack:set_metadata(data_str)
			end

			local inv = clicker:get_inventory()

			if inv:room_for_item("main", new_stack) then
				inv:add_item("main", new_stack)
			else
				minetest.add_item(clicker:get_pos(), new_stack)
			end

			self.object:remove()

			mob_sound(self, "default_place_node_hard")


		else
			minetest.chat_send_player(name, S("Missed!"))

			mob_sound(self, "mobs_swing")
		end
	end

	return true
end


-- protect tamed mob with rune item
function mobs:protect(self, clicker)

	local name = clicker:get_player_name()
	local tool = clicker:get_wielded_item()

	if tool:get_name() ~= "mobs:protector" then
		return false
	end

	if self.tamed == false then
		minetest.chat_send_player(name, S("Not tamed!"))
		return true -- false
	end

	if self.protected == true then
		minetest.chat_send_player(name, S("Already protected!"))
		return true -- false
	end

	if not mobs.is_creative(clicker:get_player_name()) then
		tool:take_item() -- take 1 protection rune
		clicker:set_wielded_item(tool)
	end

	self.protected = true

	local pos = self.object:get_pos()
	pos.y = pos.y + self.collisionbox[2] + 0.5

	effect(self.object:get_pos(), 25, "mobs_protect_particle.png", 0.5, 4, 2, 15)

	mob_sound(self, "mobs_spell")

	return true
end


local mob_obj = {}
local mob_sta = {}

-- feeding, taming and breeding (thanks blert2112)
function mobs:feed_tame(self, clicker, feed_count, breed, tame)

	if not self.follow then
		return false
	end

	-- can eat/tame with item in hand
	if follow_holding(self, clicker) then

		-- if not in creative then take item
		if not mobs.is_creative(clicker:get_player_name()) then

			local item = clicker:get_wielded_item()

			item:take_item()

			clicker:set_wielded_item(item)
		end

		-- increase health
		self.health = self.health + 4

		if self.health >= self.hp_max then

			self.health = self.hp_max

			if self.htimer < 1 then

				minetest.chat_send_player(clicker:get_player_name(),
					S("@1 at full health (@2)",
					self.name:split(":")[2], tostring(self.health)))

				self.htimer = 5
			end
		end

		self.object:set_hp(self.health)

		update_tag(self)

		-- make children grow quicker
		if self.child == true then

			self.hornytimer = self.hornytimer + 20

			return true
		end

		-- feed and tame
		self.food = (self.food or 0) + 1
		if self.food >= feed_count then

			self.food = 0

			if breed and self.hornytimer == 0 then
				self.horny = true
			end

			self.gotten = false

			if tame then

				if self.tamed == false then
					minetest.chat_send_player(clicker:get_player_name(),
						S("@1 has been tamed!",
						self.name:split(":")[2]))
				end

				self.tamed = true

				if not self.owner or self.owner == "" then
					self.owner = clicker:get_player_name()
				end
			end

			-- make sound when fed so many times
			mob_sound(self, self.sounds.random)
		end

		return true
	end

	local item = clicker:get_wielded_item()

	-- if mob has been tamed you can name it with a nametag
	if item:get_name() == "mobs:nametag"
	and clicker:get_player_name() == self.owner then

		local name = clicker:get_player_name()

		-- store mob and nametag stack in external variables
		mob_obj[name] = self
		mob_sta[name] = item

		local tag = self.nametag or ""

		minetest.show_formspec(name, "mobs_nametag", "size[8,4]"
			.. default.gui_bg
			.. default.gui_bg_img
			.. "field[0.5,1;7.5,0;name;" .. minetest.formspec_escape(S("Enter name:")) .. ";" .. tag .. "]"
			.. "button_exit[2.5,3.5;3,1;mob_rename;" .. minetest.formspec_escape(S("Rename")) .. "]")

	end

	return false

end


-- inspired by blockmen's nametag mod
minetest.register_on_player_receive_fields(function(player, formname, fields)

	-- right-clicked with nametag and name entered?
	if formname == "mobs_nametag"
	and fields.name
	and fields.name ~= "" then

		local name = player:get_player_name()

		if not mob_obj[name]
		or not mob_obj[name].object then
			return
		end

		-- limit name entered to 64 characters long
		if string.len(fields.name) > 64 then
			fields.name = string.sub(fields.name, 1, 64)
		end

		-- update nametag
		mob_obj[name].nametag = fields.name

		update_tag(mob_obj[name])

		-- if not in creative then take item
		if not mobs.is_creative(name) then

			mob_sta[name]:take_item()

			player:set_wielded_item(mob_sta[name])
		end

		-- reset external variables
		mob_obj[name] = nil
		mob_sta[name] = nil

	end
end)


-- compatibility function for old entities to new modpack entities
function mobs:alias_mob(old_name, new_name)

	-- spawn egg
	minetest.register_alias(old_name, new_name)

	-- entity
	minetest.register_entity(":" .. old_name, {

		physical = false,

		on_step = function(self)

			local pos = self.object:get_pos()

			if minetest.registered_entities[new_name] then
				minetest.add_entity(pos, new_name)
			end

			self.object:remove()
		end
	})
end

-- ===================================================================
-- RJK code.

minetest.register_on_chat_message(function(name, message)
    local n
    n = string.find (message, "bee"     )
    if n ~= nil then LastBeeTalkTime  = 0 end
    n = string.find (message, "Bee"     )
    if n ~= nil then LastBeeTalkTime  = 0 end

    n = string.find (message, "kitten"  )
    if n ~= nil then LastKittenTalkTime  = 0 end
    n = string.find (message, "Kitten"  )
    if n ~= nil then LastKittenTalkTime  = 0 end

    n = string.find (message, "cat"     )
    if n ~= nil then LastKittenTalkTime  = 0 end
    n = string.find (message, "Cat"     )
    if n ~= nil then LastKittenTalkTime  = 0 end

    n = string.find (message, "wolf"    )
    if n ~= nil then LastWolfTalkTime = 0 end
    n = string.find (message, "Wolf"    )
    if n ~= nil then LastWolfTalkTime = 0 end
end)
