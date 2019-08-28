-- ===================================================================

local function is_empty (s)
    if (s == nil) or (s == '') then return true end
    return false
end

-- ===================================================================

local disable_multispawn =
    minetest.setting_getbool ("disable_multispawn" )

local enable_bucket_city =
    minetest.setting_getbool ("enable_bucket_city" )

local enable_edgylos     =
    minetest.setting_getbool ("enable_edgylos"     )

local enable_moontest    =
    minetest.setting_getbool ("enable_moon"        ) or
    minetest.setting_getbool ("enable_moontest"    )

-- ===================================================================

minetest.register_privilege ("spawn",
    { description = "Enables shortcut teleport commands" })

local teleport_to_spawn

-- ===================================================================

local function CloneTable (original)
    local copy = {}
    for k, v in pairs (original) do
        if type (v) == 'table' then
            v = CloneTable (v)
        end
        copy [k] = v
    end
    return copy
end

-- ===================================================================

local function setwarp (warpname, fullname)

    local s_point  = "static_" .. warpname .. "_point"
    local s_pos    = minetest.setting_get_pos (s_point)
    if s_pos == nil or s_pos == "" then return end

    minetest.register_chatcommand (warpname, {
        description = "Teleport to " .. warpname ,
        params      = ""                         ,
        privs       = { interact=true }          ,

        func = function (name, params)
            local key    = warpname
            local player = minetest.env:get_player_by_name (name)
            local point  = "static_" .. key .. "_point"
            local pos    = minetest.setting_get_pos (point)

            if pos then
                minetest.chat_send_player (name,
                    "Teleporting to " .. fullname)
                player:setpos (pos)
                codersky.update_skybox (player)
                return true
            else
                minetest.chat_send_player (name,
                    "ERROR: " .. key .. " point isn't set on this server")
                return false
            end
        end
    })
end

-- ===================================================================

minetest.register_globalstep (function (dtime)
    if collectgarbage ("count") > 307200 then collectgarbage() end
end)

-- ===================================================================

if enable_moontest then
    setwarp ("earth" , "Earth"   )
    setwarp ("moon"  , "Moon"    )
else
    setwarp ("earth" , "Earth 2" )
end

setwarp ("bron"       , "BRON Realm"        )
setwarp ("tron"       , "BRON Realm"        )
setwarp ("planetoid"  , "Planetoids Realm"  )
setwarp ("planetoids" , "Planetoids Realm"  )
setwarp ("asteroid"   , "Asteroids Realm"   )
setwarp ("asteroids"  , "Asteroids Realm"   )

-- Nyan RedIce World
setwarp ("atlantis"             , "Atlantis"            )
setwarp ("corner"               , "Corner of World"     )
setwarp ("lulu"                 , "lulululu offices"    )
setwarp ("oddsymbol"            , "Odd Symbol"          )
setwarp ("palmcove"             , "Palm Cove"           )
setwarp ("pierre"               , "Pierre's Mines"      )
setwarp ("ramor"                , "Ramor's Room"        )
setwarp ("skybase"              , "Sky Base"            )
setwarp ("walle"                , "Big Robot"           )
setwarp ("wallee"               , "Big Robot"           )

setwarp ("mauvebic"             , "Mauvebic City"       )
setwarp ("russharbor"           , "Russian Harbor"      )
setwarp ("russian"              , "Russian Harbor"      )

setwarp ("bremen"               , "Bremen"              )
setwarp ("bucket"               , "Bucket City"         )
setwarp ("bucketcity"           , "Bucket City"         )
setwarp ("hometown"             , "HomeTown"            )
setwarp ("karsthafen"           , "Karsthafen"          )
setwarp ("leyadel"              , "Leyadel"             )
setwarp ("liberty"              , "Statue of Liberty"   )
setwarp ("shadow"               , "Shadow City"         )
setwarp ("shadowcity"           , "Shadow City"         )
setwarp ("shadownet"            , "ShadowNet Central"   )
setwarp ("sonos"                , "SONOS Capitol"       )
setwarp ("stadium"              , "Veritas Stadium"     )
setwarp ("nyc"                  , "NYC Times Square"    )
setwarp ("timesquare"           , "NYC Times Square"    )
setwarp ("timessquare"          , "NYC Times Square"    )
setwarp ("ussent"               , "NYC USS Enterprise"  )

-- ===================================================================
-- Bucket City points of interest.

setwarp ("angkor"       , "Angkor Wat"                  )
setwarp ("angkorwat"    , "Angkor Wat"                  )
setwarp ("angkorcross"  , "Angkor Wat at Cross"         )
setwarp ("angkorhigh"   , "Angkor Wat High Plaza"       )

setwarp ("apartment"    , "Apartment Block"             )
setwarp ("babylon"      , "Hanging Gardens of Babylon"  )
setwarp ("bighouse"     , "Big Manor House"             )
setwarp ("building"     , "Strange Unfinished Building" )
setwarp ("challenge"    , "Community Challenge"         )
setwarp ("citadel"      , "The Citadel"                 )

setwarp ("bigtemple"    , "Huge Temple"                 )
setwarp ("hugetemple"   , "Huge Temple"                 )
setwarp ("templecat"    , "Temple of the Cat"           )
setwarp ("templelight"  , "Temple of Light and Dark"    )
setwarp ("templewell"   , "Temple of the Sacred Well"   )

setwarp ("empty"        , "Empty Town Garden"           )
setwarp ("emptygarden"  , "Empty Town Garden"           )
setwarp ("farm"         , "Farm of No Harm"             )
setwarp ("forum"        , "The Minetest Forum"          )
setwarp ("gardencastle" , "Garden Castle"               )

setwarp ("house1"       , "House of Mysteries"          )
setwarp ("house2"       , "House of Secrets"            )
setwarp ("house3"       , "House of Lazy Sunday"        )
setwarp ("house01"      , "House of Mysteries"          )
setwarp ("house02"      , "House of Secrets"            )
setwarp ("house03"      , "House of Lazy Sunday"        )

setwarp ("kiosk"        , "The Kiosk"                   )
setwarp ("nother"       , "Nother Castle"               )
setwarp ("palace"       , "Buckinghuge Castle"          )
setwarp ("picnic"       , "Public Picnic Grounds"       )
setwarp ("ranger"       , "Ranger's Outpost"            )
setwarp ("tavern"       , "Terry's Tavern"              )
setwarp ("tinyfort"     , "Tiny Fort"                   )

setwarp ("townhall"     , "Town Hall"                   )
setwarp ("village"      , "The Village"                 )
setwarp ("beata"        , "Villa Beata"                 )
setwarp ("villa"        , "Villa Beata"                 )

setwarp ("bluecottage"  , "Blue Cottage"                )
setwarp ("clubhouse"    , "Clubhouse"                   )
setwarp ("decotower"    , "Deco Tower"                  )
setwarp ("desertmotel"  , "Desert Motel"                )
setwarp ("diagonal"     , "Diagonal Development"        )
setwarp ("dyersguild"   , "Dyer's Guild"                )

setwarp ("grandhall"    , "Grand Hall"                  )
setwarp ("poshdining"   , "Posh Restaurant"             )
setwarp ("romanfort"    , "Roman Fort"                  )
setwarp ("stardome"     , "The Stardome"                )
setwarp ("wizardskeep"  , "Wizard's Keep"               )

-- Possibly temporary aliases:
--
setwarp ("cottage"      , "Blue Cottage"                )
setwarp ("dyers"        , "Dyer's Guild"                )
setwarp ("fort"         , "Roman Fort"                  )
setwarp ("motel"        , "Desert Motel"                )

-- ===================================================================
-- Legends of Survival.

if enable_edgylos then
    setwarp ("adam"       , "Adam's Place"     )
    setwarp ("bremen"     , "Bremen"           )
    setwarp ("newspawn"   , "New Spawn"        )
    setwarp ("robocop"    , "Robo LEO"         )
    setwarp ("ruslan1"    , "Ruslan1's House"  )
    setwarp ("tinytrain"  , "Tiny Train"       )
    setwarp ("village"    , "Village"          )
    setwarp ("zulfikar"   , "Zulfikar's Place" )

    setwarp ("armenia"    , "Armenia"          )
    setwarp ("bogdan"     , "Bogdan 0575"      )
    setwarp ("bogdan0575" , "Bogdan 0575"      )
    setwarp ("zetg"       , "zetg place"       )
end

-- ===================================================================

local                       static_spawn_point  =
    minetest.settings:get ("static_spawn_point" )

local                       static_spawnpoint   =
    minetest.settings:get ("static_spawnpoint"  )

if is_empty (static_spawn_point) then
             static_spawn_point = static_spawnpoint
end

if not is_empty (static_spawn_point) then
    disable_multispawn = true
end

-- ===================================================================

if disable_multispawn then
    teleport_to_spawn = function (name)
        if is_empty (static_spawn_point) then
            return false
        end
        local pos = minetest.string_to_pos (static_spawn_point)

        if pos ~= nil then
            local player = minetest.env:get_player_by_name (name)
            player:setpos (pos)
            codersky.update_skybox (player)
            return true
        end

        return false
    end

    minetest.register_chatcommand ("spawn", {
        description = "Teleport to spawnpoint" ,
        privs = {} ,
        func  = function (name)
            teleport_to_spawn (name)
        end
    })
end

-- ===================================================================

if not disable_multispawn then
spawnpoints = {}

spawnpoints.list = {
    cid = 1 ,
}

-- ===================================================================

local function load_spawns()
    local  f = io.open (minetest.get_worldpath() .. "/spawnpoints", "r")
    if not f then
        minetest.log ("action",
            "[coderwarp] Missing spawn data [1]")
        return
    end

    spawnpoints.list = minetest.deserialize (f:read ("*a"))
    f:close()
end

-- ===================================================================

local function save_spawns()
    local  f = io.open (minetest.get_worldpath() .. "/spawnpoints", "w")
    if not f then return end
    f:write (minetest.serialize (spawnpoints.list))
    f:close()
end

-- ===================================================================

teleport_to_spawn = function (pname, id)
    if #spawnpoints.list == 0 then
        minetest.chat_send_player (pname,
            "Sorry, there are no spawns set")
        minetest.log ("action",
            "[coderwarp] Missing spawn data [2]")
        return
    end

    local spawn = nil

    if id ~= nil then
        for _, spwn in ipairs (spawnpoints.list) do
            if spwn.id == id then
                spawn = spwn
                break
            end
        end
    else
        id = math.floor (math.random() * #spawnpoints.list) + 1
        minetest.chat_send_player (pname,
            "Teleporting to spawn #" .. id)
        spawn    = spawnpoints.list [id]
    end

    if not spawn then
        minetest.chat_send_player (pname,
            "Sorry, spawn #" .. id .. " doesn't exist")
        minetest.log ("action",
            "[coderwarp] Missing spawn data [3]")
        return
    end

    local player = minetest.get_player_by_name(pname)
    player:setpos (spawn)
    codersky.update_skybox (player)
end

-- ===================================================================

minetest.register_chatcommand ("spawn", {
    params = "[id]",
    description = "Teleport to spawnpoint",
    privs = {},
    func = function(name, param)
        local id = tonumber(param)

        if id == nil then
            teleport_to_spawn (name)
        else
            teleport_to_spawn (name, id)
        end
    end,
})

-- ===================================================================

local tb_addspawn = {
    params = "<x> <y> <z>",
    description = "Add a spawnpoint",
    privs = {basic_privs=true},
    func = function(name, param)
        local x, y, z = param:match ('(.-) (.-) (.*)')
        x = tonumber (x)
        y = tonumber (y)
        z = tonumber (z)

        if not x or not y or not z then
            x, y, z = param:match ('(.-) *, *(.-) *, *(.*)')
            x = tonumber (x)
            y = tonumber (y)
            z = tonumber (z)

            if not x or not y or not z then
                minetest.chat_send_player (name,
                    "Invalid coordinates")
                return
            end
        end

        spawnpoints.list [#spawnpoints.list + 1] = {
            x=x, y=y, z=z, id=spawnpoints.list.cid
        }

        local id = spawnpoints.list.cid
        spawnpoints.list.cid = spawnpoints.list.cid + 1
        minetest.chat_send_player (name, "Created new spawnpoint. ID: " .. id)
        save_spawns()
    end ,
}

minetest.register_chatcommand ("add_spawn" , tb_addspawn)
minetest.register_chatcommand ("addspawn"  , tb_addspawn)

-- ===================================================================

local tb_delspawn = {
    params = "<id>",
    description = "Delete a spawnpoint",
    privs = { basic_privs=true } ,

    func = function (name, param)
        local id = tonumber (param)
        if not id then
            minetest.chat_send_player (name, "Invalid ID")
            return
        end
        local del     = false
        local newlist = {}

        for i, sp in ipairs (spawnpoints.list) do
            if sp.id == id then
                del = true
            else
                newlist [#newlist + 1] =
                    CloneTable (spawnpoints.list [i])
            end
        end
        newlist.cid      = spawnpoints.list.cid
        spawnpoints.list = newlist

        if del then
            minetest.chat_send_player (name,
                "Deleted spawnpoint #" .. id)
            save_spawns()
        else
            minetest.chat_send_player(name,
                "There was no spawnpoint #" .. id)
        end
    end ,
}

minetest.register_chatcommand ("del_spawn"    , tb_delspawn)
minetest.register_chatcommand ("delspawn"     , tb_delspawn)
minetest.register_chatcommand ("delete_spawn" , tb_delspawn)
minetest.register_chatcommand ("deletespawn"  , tb_delspawn)
minetest.register_chatcommand ("rm_spawn"     , tb_delspawn)
minetest.register_chatcommand ("rmspawn"      , tb_delspawn)

-- ===================================================================

local tb_listspawns = {
    params = "",
    description = "List spawnpoints" ,
    privs = {},
    func = function (name, param)
        for _, sp in ipairs (spawnpoints.list) do
            local str = minetest.pos_to_string (sp) .. " #" .. sp.id
            minetest.chat_send_player (name, str)
        end
    end ,
}

minetest.register_chatcommand ("list_spawn"  , tb_listspawns)
minetest.register_chatcommand ("listspawn"   , tb_listspawns)
minetest.register_chatcommand ("list_spawns" , tb_listspawns)
minetest.register_chatcommand ("listspawns"  , tb_listspawns)

-- ===================================================================

load_spawns()
end

-- ===================================================================

minetest.register_on_newplayer (function (player)
    teleport_to_spawn (player:get_player_name())
    return true
end)

minetest.register_on_respawnplayer (function (player)
    teleport_to_spawn (player:get_player_name())
    return true
end)

minetest.log ("action", "Loaded coderwarp")
