local modname = minetest.get_current_modname()
local modpath = minetest.get_modpath (modname)

local enable_wonder = minetest.setting_getbool ("enable_wonder")
unified_hunger = {}

-- HUD statbar values
unified_hunger.hunger = {}
unified_hunger.hunger_out = {}

-- HUD item ids
local hunger_hud = {}

if minetest.setting_getbool ("enable_damage") then
    unified_hunger.enable_damage = true
else
    unified_hunger.enable_damage = false
end

HUNGER_HUD_TICK = 0.5 -- 0.1

--Some hunger settings
unified_hunger.exhaustion = {} -- Exhaustion is experimental!

-- time in seconds after that 1 hunger point is taken

local HUNGER_TICK_DEFAULT = 180
if enable_wonder then
      HUNGER_TICK_DEFAULT =  90
end

   HUNGER_HUNGER_TICK = tonumber (minetest.setting_get ("hunger_tick")) or HUNGER_TICK_DEFAULT
if HUNGER_HUNGER_TICK < 10 then HUNGER_HUNGER_TICK = 10 end

HUNGER_EXHAUST_DIG = 1.5  -- exhaustion increased this value after digged node
HUNGER_EXHAUST_PLACE = 1 -- exhaustion increased this value after placed
HUNGER_EXHAUST_MOVE = 0.3 -- exhaustion increased this value if player movement detected
HUNGER_EXHAUST_LVL = 160 -- at what exhaustion player satiation gets lowerd


--[[load custom settings
local set = io.open(minetest.get_modpath("unified_hunger").."/unified_hunger.conf", "r")
if set then
    dofile(minetest.get_modpath("unified_hunger").."/unified_hunger.conf")
    set:close()
end--]]

local function custom_hud(player)
    hb.init_hudbar(player, "satiation", unified_hunger.get_hunger(player))
end

-- Keep these for backwards compatibility

function unified_hunger.save_hunger(player)
    unified_hunger.set_hunger(player)
end

function unified_hunger.load_hunger(player)
    unified_hunger.get_hunger(player)
end

-- Poison player
local function poisenp(tick, time, time_left, player)
    time_left = time_left + tick
    if time_left < time then
        minetest.after(tick, poisenp, tick, time, time_left, player)
    else
        --reset hud image
    end
    if player:get_hp()-1 > 0 then
        player:set_hp(player:get_hp()-1)
    end

end

function unified_hunger.item_eat (hunger_change,
    replace_with_item, poisen, heal, msg)

    return function (itemstack, user, pointed_thing)
        if itemstack:take_item() ~= nil and user ~= nil then
            local name = user:get_player_name()
            local h = tonumber(unified_hunger.hunger[name])
            local hp = user:get_hp()
            minetest.sound_play("unified_hunger_eat_generic", {
                object = user,
                max_hear_distance = 10,
                gain = 1.0
            })

            -- Saturation
            if h < 30 and hunger_change then
                h = h + hunger_change
                if h > 30 then h = 30 end
                unified_hunger.hunger[name] = h
                unified_hunger.set_hunger(user)
            end
            -- Healing
            if hp < 20 and heal then
                hp = hp + heal
                if hp > 20 then hp = 20 end
                user:set_hp(hp)
            end
            -- Poison
            if poisen then
                --set hud-img
                poisenp(1.0, poisen, 0, user)
            end

            if replace_with_item then
                if itemstack:is_empty() then
                    itemstack:add_item(replace_with_item)
                else
                    local inv = user:get_inventory()
                    if inv:room_for_item("main", {name = replace_with_item}) then
                        inv:add_item("main", replace_with_item)
                    else
                        local pos = user:getpos()
                        pos.y = math.floor(pos.y + 0.5)
                        core.add_item(pos, replace_with_item)
                    end
                end
            end

            if msg ~= nil then
                local mt   = type (msg)
                local send = nil

                if     mt == "string" then
                    send = msg
                elseif mt == "table"  then
                    send = msg [math.random (#msg)]
                end

                minetest.chat_send_player (name, send)
            end
        end
        return itemstack
    end
end

unified_hunger.overwrite = function (name, satiate, heal, poison,
    replace, msg)

    if not unified_hunger.enable_damage then
        poison = nil
    end
    name = minetest.registered_aliases [name] or name

    if minetest.registered_items [name] ~= nil then
        minetest.override_item (name, {
            on_use = unified_hunger.item_eat (satiate,
                replace, poison, heal, msg)
        })
    end
end

local overwrite = unified_hunger.overwrite

-- ===================================================================

-- player-action based hunger changes
function unified_hunger.handle_node_actions(pos, oldnode, player, ext)
    if not player or not player:is_player() then
        return
    end
    local name = player:get_player_name()
    local exhaus = unified_hunger.exhaustion[name]
    if exhaus == nil then return end
    local new = HUNGER_EXHAUST_PLACE
    -- placenode event
    if not ext then
        new = HUNGER_EXHAUST_DIG
    end
    -- assume its send by main timer when movement detected
    if not pos and not oldnode then
        new = HUNGER_EXHAUST_MOVE
    end
    exhaus = exhaus + new
    if exhaus > HUNGER_EXHAUST_LVL then
        exhaus = 0
        local h = tonumber(unified_hunger.hunger[name])
        h = h - 1
        if h < 0 then h = 0 end
        unified_hunger.hunger[name] = h
        unified_hunger.set_hunger(player)
    end
    unified_hunger.exhaustion[name] = exhaus
end

--minetest.register_on_placenode(unified_hunger.handle_node_actions)
minetest.register_on_dignode(unified_hunger.handle_node_actions)

-- register satiation hudbar
hb.register_hudbar(
    "satiation", 0xFFFFFF, "Satiation",
    {
        icon = "unified_hunger_icon.png",
        bgicon = "unified_hunger_bgicon.png",
        bar = "unified_hunger_bar.png"
    },
    20, 30, false
)

-- update hud elemtents if value has changed
local function update_hud(player)
    local name = player:get_player_name()
    local h_out = tonumber(unified_hunger.hunger_out[name])
    local h = tonumber(unified_hunger.hunger[name])
    if h_out ~= h then
        unified_hunger.hunger_out[name] = h
        hb.change_hudbar(player, "satiation", h)
    end
end

unified_hunger.get_hunger = function(player)
    local inv = player:get_inventory()
    if not inv then return nil end
    local hgp = inv:get_stack("hunger", 1):get_count()
    if hgp == 0 then
        hgp = 21
        inv:set_stack("hunger", 1, ItemStack({name = ":", count = hgp}))
    else
        hgp = hgp
    end
    return hgp - 1
end

unified_hunger.set_hunger = function(player)
    local inv = player:get_inventory()
    local name = player:get_player_name()
    local value = unified_hunger.hunger[name]
    if not inv  or not value then return nil end
    if value > 30 then value = 30 end
    if value < 0 then value = 0 end
    inv:set_stack("hunger", 1, ItemStack({name = ":", count = value + 1}))
    return true
end

minetest.register_on_joinplayer(function(player)
    local name = player:get_player_name()
    local inv = player:get_inventory()
    inv:set_size("hunger", 1)
    unified_hunger.hunger[name] = unified_hunger.get_hunger(player)
    unified_hunger.hunger_out[name] = unified_hunger.hunger[name]
    unified_hunger.exhaustion[name] = 0
    custom_hud(player)
    unified_hunger.set_hunger(player)
end)

minetest.register_on_respawnplayer(function(player)
    -- reset hunger (and save)
    local name = player:get_player_name()
    unified_hunger.hunger[name] = 20
    unified_hunger.set_hunger(player)
    unified_hunger.exhaustion[name] = 0
end)

-- ===================================================================

local param_starve = {
    description = "Be hungry" ,
    params      = ""          ,
    privs       = {}          ,

    func = function (plname, params)
        local player = minetest.env:get_player_by_name (plname)
        unified_hunger.hunger [plname] = 5
        unified_hunger.set_hunger (player)
        minetest.chat_send_player (plname, "O.K. you're hungry")

    end
}

minetest.register_chatcommand ("starve", param_starve)

-- ===================================================================

minetest.register_privilege ("satiate", {
    description          = "satiate administration" ,
    give_to_singleplayer = false                    ,
})

local param_satiate = {
    description = "Be satiated"    ,
    params      = ""               ,
    privs       = { satiate=true } ,

    func = function (plname, params)
        local player = minetest.env:get_player_by_name (plname)
        unified_hunger.hunger [plname] = 20
        unified_hunger.set_hunger (player)
        minetest.chat_send_player (plname, "O.K. you're satiated")

    end
}

minetest.register_chatcommand ("satiate", param_satiate)

-- ===================================================================

if unified_hunger.enable_damage then
local main_timer = 0
local timer = 0
local timer2 = 0

minetest.register_globalstep(function(dtime)
    main_timer = main_timer + dtime
    timer = timer + dtime
    timer2 = timer2 + dtime

    if main_timer > HUNGER_HUD_TICK
    or timer > 4
    or timer2 > HUNGER_HUNGER_TICK then

        if  main_timer > HUNGER_HUD_TICK then
            main_timer = 0
        end

        for _,player in pairs(minetest.get_connected_players()) do

            local name = player:get_player_name()
            local h = tonumber(unified_hunger.hunger[name])
            local hp = player:get_hp()

            if timer > 4 then

                -- heal player by 1 hp if not dead and satiation is > 15
                if h > 15
                and hp > 0
                and player:get_breath() > 0 then
                    player:set_hp(hp + 1)
                -- or damage player by 1 hp if satiation is < 2
                elseif h <= 1 then
                    if hp - 1 >= 0 then
                        player:set_hp(hp - 1)
                    end
                end
            end

            -- lower satiation by 1 point after xx seconds
            if timer2 > HUNGER_HUNGER_TICK then
                    if h > 0 then
                    h = h - 1
                    unified_hunger.hunger[name] = h
                    unified_hunger.set_hunger(player)
                end
            end

            -- update hud elements
            update_hud(player)

            -- Determine if player is walking
            local controls = player:get_player_control()
            if controls.up
            or controls.down
            or controls.left
            or controls.right then
                unified_hunger.handle_node_actions(nil, nil, player)
            end

        end
    end

    if timer > 4 then
        timer = 0
    end

    if timer2 > HUNGER_HUNGER_TICK then
        timer2 = 0
    end
end)
end -- end if damage enabled
