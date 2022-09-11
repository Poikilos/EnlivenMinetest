-- Generic node manipulations
-- @module worldedit.manipulations

require "os"

-- ===================================================================

local                      coderedit_debug            =
    minetest.setting_get ("coderedit_debug"           )

local                      coderedit_disable_verbose  =
    minetest.setting_get ("coderedit_disable_verbose" ) or
    minetest.setting_get ("disable_coderedit_verbose" )

local                      coderedit_noqueue          =
    minetest.setting_get ("coderedit_noqueue"         )

-- ===================================================================

local mh = worldedit.manip_helpers

-- Sets a region to `node_names`
-- @param pos1
-- @param pos2
-- @param node_names Node name or list of node names.
-- @return The number of nodes set.

-- ===================================================================

worldedit.cmd_queue   = {}
worldedit.emerge_busy = 0
worldedit.use_queue   = 1

if coderedit_noqueue then worldedit.use_queue = 0 end

-- ===================================================================

local function idiv (a, b)
    return (a - (a % b)) / b
end

-- ===================================================================

local function sort2num (a, b)
    if a > b then return b, a end
    return a, b
end

-- ===================================================================

local function deblog (str)
    if coderedit_debug then
        ocutil.log ("[we] " .. str)
    end
end

-- ===================================================================

function worldedit.toggle_queue()
    if  worldedit.use_queue == 0 then
        worldedit.use_queue =  1
        minetest.chat_send_all ("CoderEdit commands are queued"     )
    else
        worldedit.use_queue =  0
        minetest.chat_send_all ("CoderEdit commands are not queued" )
    end
end

-- ===================================================================

local function end_of_start_emerge (pos1, pos2, mode)

    if collectgarbage ("count") > 307200 then collectgarbage() end
    deblog ("emerge started")

    if not coderedit_disable_verbose then
        minetest.chat_send_all ("Volume may print immediately," ..
            " but we're not done")
        minetest.chat_send_all ("Wait for DONE message")
        minetest.chat_send_all ("This may take 5 to 45 minutes" ..
            " for large schems")
    end

    return worldedit.volume (pos1, pos2)
end

-- ===================================================================

local function end_of_emerge (mode)

    if collectgarbage ("count") > 307200 then collectgarbage() end
    minetest.chat_send_all ("*** " .. mode .." DONE ***")
    deblog ("emerge done")

    worldedit.emerge_busy = 0
    worldedit.place_base  = nil
    worldedit.place_both  = nil
    worldedit.place_name  = nil
    worldedit.place_path  = nil
    worldedit.place_pos   = nil
end

-- ===================================================================

local function emerge_callback_copy (blockpos, action, numleft, param)

    if collectgarbage ("count") > 307200 then collectgarbage() end
    if numleft ~= 0 then return end

    local pos1     = param.pos1
    local pos2     = param.pos2
    local axis     = param.axis
    local amount   = param.amount
    local overlap  = param.overlap

    local newpos1  = { x=pos1.x, y=pos1.y, z=pos1.z }
    local newpos2  = { x=pos2.x, y=pos2.y, z=pos2.z }

    newpos1 [axis] = newpos1 [axis] + amount
    newpos2 [axis] = newpos2 [axis] + amount

    if overlap then
        if not coderedit_disable_verbose then
            minetest.chat_send_all ("Emerge done, skipping"   ..
                " set air due to overlap")
            minetest.chat_send_all ("Dark areas may result."  ..
                " Starting actual copy.")
        end
    else
        if not coderedit_disable_verbose then
            minetest.chat_send_all ("Emerge done, starting set air")
        end

        deblog ("copy callback: set to air start" )
        worldedit.old_set (newpos1, newpos2, "air")
        deblog ("copy callback: set to air done"  )

        if not coderedit_disable_verbose then
            minetest.chat_send_all ("Set air done, starting"  ..
                " actual copy")
        end
    end

    deblog ("copy callback: actual copy start"  )
    worldedit.old_copy (pos1, pos2, axis, amount)
    deblog ("copy callback: actual copy done"   )

    end_of_emerge ("COPY")
end

-- ===================================================================

local function emerge_callback_move (blockpos, action, numleft, param)

    if collectgarbage ("count") > 307200 then collectgarbage() end
    if numleft ~= 0 then return end

    local pos1     = param.pos1
    local pos2     = param.pos2
    local axis     = param.axis
    local amount   = param.amount
    local overlap  = param.overlap

    local newpos1  = { x=pos1.x, y=pos1.y, z=pos1.z }
    local newpos2  = { x=pos2.x, y=pos2.y, z=pos2.z }

    newpos1 [axis] = newpos1 [axis] + amount
    newpos2 [axis] = newpos2 [axis] + amount

    if overlap then
        if not coderedit_disable_verbose then
            minetest.chat_send_all ("Emerge done, skipping"   ..
                " set air due to overlap")
            minetest.chat_send_all ("Dark areas may result."  ..
                " Starting actual move.")
        end
    else
        if not coderedit_disable_verbose then
            minetest.chat_send_all ("Emerge done, starting set air")
        end

        deblog ("move callback: set to air start" )
        worldedit.old_set (newpos1, newpos2, "air")
        deblog ("move callback: set to air done"  )

        if not coderedit_disable_verbose then
            minetest.chat_send_all ("Set air done, starting"  ..
                " actual move")
        end
    end

    deblog ("move callback: actual move start"  )
    worldedit.old_move (pos1, pos2, axis, amount)
    deblog ("move callback: actual move done"   )

    end_of_emerge ("MOVE")
end

-- ===================================================================

local function emerge_callback_emerge (blockpos, action,
    numleft, param)

    if collectgarbage ("count") > 307200 then collectgarbage() end
    if numleft ~= 0 then return end
    end_of_emerge ("EMERGE")
end

-- ===================================================================

local function emerge_callback_set (blockpos, action, numleft, param)

    if false and (numleft % 8192) == 0 then
        ocutil.log ("emerge left: " .. numleft)
    end
    if numleft ~= 0 then return end

    if not coderedit_disable_verbose then
        minetest.chat_send_all ("Emerge done, starting actual set")
    end

    if  type (param.node_names) ~= "string" or
        param.node_names ~= "default:emerge" then
        worldedit.old_set (param.pos1,
                           param.pos2, param.node_names)
    end

    local pbase = worldedit.place_base
    local pboth = worldedit.place_both
    local pname = worldedit.place_name
    local ppos  = worldedit.place_pos
    local ppath = worldedit.place_path

    if (ppos ~= nil) and (ppath ~= nil) then
        if not coderedit_disable_verbose then
            minetest.chat_send_all ("Set done, starting actual place")
        end

        if minetest.place_schematic (ppos, ppath) == nil then
            minetest.chat_send_all ("Failed to place MTS", false)
        else
            local ps = minetest.pos_to_string (ppos)
            minetest.chat_send_all ("Placed MTS at "    .. ps, false)

            if (pname ~= nil) and (pbase ~= nil) and
               (pboth ~= nil) and pboth then
                worldedit.loadwe (pname, pbase)
                minetest.chat_send_all ("Placed WE at " .. ps, false)
            end
        end
    end

    end_of_emerge ("SET or PLACE")
end

-- ===================================================================

-- Copies a region along `axis` by `amount` nodes.
-- @param pos1
-- @param pos2
-- @param axis Axis ("x", "y", or "z")
-- @param amount
-- @return The number of nodes copied.

function worldedit.old_copy (xpos1, xpos2, axis, amount)

    local pos1, pos2 = worldedit.sort_pos (xpos1, xpos2)
    worldedit.keep_loaded (pos1, pos2)

    local get_node, get_meta, set_node = minetest.get_node,
            minetest.get_meta, minetest.set_node
    -- Copy things backwards when negative to avoid corruption.
    -- FIXME: Lots of code duplication here.

    if amount < 0 then
        local pos = {}
        pos.x = pos1.x

        while pos.x <= pos2.x do
            pos.y = pos1.y

            while pos.y <= pos2.y do
                pos.z = pos1.z

                while pos.z <= pos2.z do

                    -- Obtain current node
                    local node  = get_node (pos)

                    -- Get meta of current node
                    local meta  = get_meta (pos):to_table()

                    -- Store current position
                    local value = pos [axis]

                    -- Move along axis
                    pos[axis]   = value + amount

                    -- Copy node to new position
                    set_node (pos, node)

                    -- Set metadata of new node
                    get_meta (pos):from_table (meta)

                    -- Restore old position
                    pos [axis]  = value

                    pos.z = pos.z + 1
                end

                pos.y = pos.y + 1
            end

            pos.x = pos.x + 1
        end
    else
        local pos = {}
        pos.x = pos2.x

        while pos.x >= pos1.x do
            pos.y = pos2.y

            while pos.y >= pos1.y do
                pos.z = pos2.z

                while pos.z >= pos1.z do

                    -- Obtain current node
                    local node  = get_node (pos)

                    -- Get meta of current node
                    local meta  = get_meta (pos):to_table()

                    -- Store current position
                    local value = pos [axis]

                    -- Move along axis
                    pos[axis]   = value + amount

                    -- Copy node to new position
                    set_node (pos, node)

                    -- Set metadata of new node
                    get_meta (pos):from_table (meta)

                    -- Restore old position
                    pos [axis]  = value

                    pos.z = pos.z - 1
                end

                pos.y = pos.y - 1
            end

            pos.x = pos.x - 1
        end
    end

    return worldedit.volume (pos1, pos2)
end

-- ===================================================================

function worldedit.wait_copy (p)
    worldedit.copy (p.xpos1, p.xpos2, p.axis, p.amount)
    return 0
end

function worldedit.wait_emerge_area (p)
    worldedit.emerge_area (p.xpos1, p.xpos2)
    return 0
end

function worldedit.wait_move (p)
    worldedit.move (p.xpos1, p.xpos2, p.axis, p.amount)
    return 0
end

function worldedit.wait_set (p)
    worldedit.set (p.xpos1, p.xpos2, p.node_names)
    return 0
end

-- ===================================================================

function worldedit.pop_queue()
    if  #worldedit.cmd_queue   == 0 then return 0 end
    if   worldedit.emerge_busy == 1 then
        deblog ("pop_queue: WE is busy, waiting 1 second")
        minetest.after (1, worldedit.pop_queue)
        return 0
    end

    deblog ("pop_queue: WE is free, running next command")
    local qe = table.remove (worldedit.cmd_queue, 1)
    qe.func (qe.param)
    return 0
end

-- ===================================================================

function worldedit.copy (xpos1, xpos2, axis, amount)
    if worldedit.emerge_busy == 1 then
        deblog ("worldedit.copy called but WE is busy")
    else
        deblog ("worldedit.copy called and WE is free")
    end

    local pos1, pos2 = worldedit.sort_pos (xpos1, xpos2)

    if worldedit.volume (pos1, pos2) > 1500000 then
        minetest.chat_send_all ("//copy is limited to 1.5M nodes",
            false)
        return 0
    end

    if worldedit.emerge_busy == 1 then
        if worldedit.use_queue == 0 then
            minetest.chat_send_all ("A previous //operation is busy")
        else
            local qe  = {
                func  = worldedit.wait_copy ,
                param = {
                    xpos1=xpos1, xpos2=xpos2, axis=axis, amount=amount
                }
            }

            deblog ("queuing for later: copy " ..
                ocutil.pos_to_str (xpos1) .. " " ..
                ocutil.pos_to_str (xpos2) .. " " ..
                axis .. " " .. amount)

            qe = ocutil.clone_table (qe)
            table.insert (worldedit.cmd_queue, qe)
            minetest.after (1, worldedit.pop_queue)
        end
        return 0
    else
        deblog ("WE is free, proceeding: copy " ..
            ocutil.pos_to_str (xpos1) .. " " ..
            ocutil.pos_to_str (xpos2) .. " " ..
            axis .. " " .. amount)
    end

-- ===================================================================

    local newpos1  = { x=pos1.x, y=pos1.y, z=pos1.z }
    local newpos2  = { x=pos2.x, y=pos2.y, z=pos2.z }

    newpos1 [axis] = newpos1 [axis] + amount
    newpos2 [axis] = newpos2 [axis] + amount

-- ===================================================================

    local os1      = minetest.pos_to_string (pos1)
    local os2      = minetest.pos_to_string (pos2)

    local ps1      = minetest.pos_to_string (newpos1)
    local ps2      = minetest.pos_to_string (newpos2)

-- ===================================================================

    if not coderedit_disable_verbose then
        minetest.chat_send_all ("//copy " ..
            "Source: " .. os1  .. " " .. os2 .. " " ..
            "Axis: "   .. axis .. " " ..
            "Amount: " .. amount)
        minetest.chat_send_all ("//copy Destin:"  ..
            ps1 .. " " .. ps2)
    end

    deblog ("//copy " ..
        "Source: " .. os1  .. " " .. os2 .. " " ..
        "Axis: "   .. axis .. " " ..
        "Amount: " .. amount)
    deblog ("//copy Destin: " .. ps1 .. " " .. ps2)

-- ===================================================================

    local x1min, x1max = sort2num (pos1.x, pos2.x)
    local y1min, y1max = sort2num (pos1.y, pos2.y)
    local z1min, z1max = sort2num (pos1.z, pos2.z)

    local x2min, x2max = sort2num (newpos1.x, newpos2.x)
    local y2min, y2max = sort2num (newpos1.y, newpos2.y)
    local z2min, z2max = sort2num (newpos1.z, newpos2.z)

    local overlap = true
    if x1max < x2min or x2max < x1min or
       y1max < y2min or y2max < y1min or
       z1max < z2min or z2max < z1min then
        overlap = false
    end

    if overlap then
        minetest.chat_send_all ("Source and dest regions" ..
            " overlap, there may be dark areas")
    end

-- ===================================================================

    worldedit.emerge_busy = 1
    if collectgarbage ("count") > 307200 then collectgarbage() end

    local param = {
        pos1=pos1       , pos2=pos2 , axis=axis , amount=amount ,
        overlap=overlap ,
    }

    minetest.emerge_area (newpos1, newpos2,
        emerge_callback_copy, param)

    return end_of_start_emerge (pos1, pos2, "COPY")
end

-- ===================================================================

function worldedit.emerge_area (xpos1, xpos2)

    if worldedit.emerge_busy == 1 then
        if worldedit.use_queue == 0 then
            minetest.chat_send_all ("A previous //operation is busy")
        else
            local qe  = {
                func  = worldedit.wait_emerge_area   ,
                param = { xpos1=xpos1, xpos2=xpos2 } ,
            }

            qe = ocutil.clone_table (qe)
            table.insert (worldedit.cmd_queue, qe)
            minetest.after (1, worldedit.pop_queue)
        end
        return 0
    end

    worldedit.emerge_busy = 1
    local pos1, pos2 = worldedit.sort_pos (xpos1, xpos2)
    if collectgarbage ("count") > 307200 then collectgarbage() end
    local param = { pos1=pos1, pos2=pos2 }

    minetest.emerge_area (pos1, pos2, emerge_callback_emerge, param)
    return end_of_start_emerge (pos1, pos2, "EMERGE")
end

-- ===================================================================

-- Replaces all instances of "search_node" with "replace_node" in a
-- region. When "inverse" is "true", replaces all instances that are
-- NOT "search_node".
-- @return The number of nodes replaced.

function worldedit.replace (pos1, pos2, search_node,
    replace_node, inverse)

    pos1, pos2 = worldedit.sort_pos (pos1, pos2)
    local manip, area = mh.init (pos1, pos2)
    local data = manip:get_data()

    local search_id  =  ocutil.get_content_id (search_node )
    if    search_id  == nil then
        minetest.chat_send_all ("Error: Unknown node " .. search_node )
        return
    end

    local replace_id =  ocutil.get_content_id (replace_node)
    if    replace_id == nil then
        minetest.chat_send_all ("Error: Unknown node " .. replace_node )
        return
    end

    local count = 0

    --- TODO: This could be shortened by checking `inverse` in the loop,
    -- but that would have a speed penalty.  Is the penalty big enough
    -- to matter?

    if not inverse then
        for i in area:iterp (pos1, pos2) do
            if data [i] == search_id then
                data [i] = replace_id
                count    = count + 1
            end
        end
    else
        for i in area:iterp (pos1, pos2) do
            if data [i] ~= search_id then
                data [i] = replace_id
                count    = count + 1
            end
        end
    end

    mh.finish (manip, data)
    return count
end

-- ===================================================================

-- Sets a region to node_names.
-- @param pos1
-- @param pos2
-- @param node_names Node name or list of node names.
-- @return The number of nodes set.

function worldedit.old_set (xpos1, xpos2, node_names)

    local pos1, pos2
    pos1, pos2 = worldedit.sort_pos (xpos1, xpos2)

    local xdelta  = pos2.x - pos1.x
    local ydelta  = pos2.y - pos1.y
    local zdelta  = pos2.z - pos1.z

    if xdelta >= 30 or xdelta <= -30 then
        local m1   = idiv (xdelta, 2)
        local m2   = xdelta - m1
        local posa = { x=pos1.x+m1, y=pos2.y, z=pos2.z }
        local posb = { x=pos1.x+m2, y=pos1.y, z=pos1.z }
        worldedit.old_set (pos1, posa, node_names)
        worldedit.old_set (posb, pos2, node_names)
        return worldedit.volume (pos1, pos2)
    end

    if ydelta >= 30 or ydelta <= -30 then
        local m1   = idiv (ydelta, 2)
        local m2   = ydelta - m1
        local posa = { x=pos2.x, y=pos1.y+m1, z=pos2.z }
        local posb = { x=pos1.x, y=pos1.y+m2, z=pos1.z }
        worldedit.old_set (pos1, posa, node_names)
        worldedit.old_set (posb, pos2, node_names)
        return worldedit.volume (pos1, pos2)
    end

    if zdelta >= 30 or zdelta <= -30 then
        local m1   = idiv (zdelta, 2)
        local m2   = zdelta - m1
        local posa = { x=pos2.x, y=pos2.y, z=pos1.z+m1 }
        local posb = { x=pos1.x, y=pos1.y, z=pos1.z+m2 }
        worldedit.old_set (pos1, posa, node_names)
        worldedit.old_set (posb, pos2, node_names)
        return worldedit.volume (pos1, pos2)
    end

    local manip, area = mh.init (pos1, pos2)
    manip:update_map()

    local data = mh.get_empty_data (area)
    if collectgarbage ("count") > 307200 then collectgarbage() end

    if type (node_names) == "string" then -- Only one type of node
        if node_names ~= "default:emerge" then
            local id =  ocutil.get_content_id (node_names)
            if    id == nil then
                minetest.chat_send_all ("Error: Unknown node " .. node_names)
                return
            end

            -- Fill area with node
            for i in area:iterp (pos1, pos2) do
                data [i] = id
            end
        end
    else -- Several types of nodes specified
        local node_ids = {}
        for i, v in ipairs (node_names) do
               node_ids [i] = ocutil.get_content_id (v)
            if node_ids [i] == nil then
                minetest.chat_send_all ("Error: Unknown node " .. v)
                return
            end
        end
        -- Fill area randomly with nodes
        local id_count, rand = #node_ids, math.random
        for i in area:iterp (pos1, pos2) do
            data [i] = node_ids [rand (id_count)]
        end
    end

    if collectgarbage ("count") > 307200 then collectgarbage() end
    manip:set_data (data)
    data = {}
    manip:update_liquids()
    manip:write_to_map()
    manip:update_map()

    if collectgarbage ("count") > 307200 then collectgarbage() end
    return worldedit.volume (pos1, pos2)
end

-- ===================================================================

function worldedit.set (xpos1, xpos2, node_names)

    if worldedit.emerge_busy == 1 then
        if worldedit.use_queue == 0 then
            minetest.chat_send_all ("A previous //operation is busy")
        else
            local qe  = {
                func  = worldedit.wait_set ,
                param = {
                    xpos1=xpos1, xpos2=xpos2, node_names=node_names
                }
            }

            qe = ocutil.clone_table (qe)
            table.insert (worldedit.cmd_queue, qe)
            minetest.after (1, worldedit.pop_queue)
        end
        return 0
    end

    worldedit.emerge_busy = 1
    local pos1, pos2 = worldedit.sort_pos (xpos1, xpos2)
    if collectgarbage ("count") > 307200 then collectgarbage() end
    local vol = worldedit.volume (pos1, pos2)

    if  type (node_names) ~= "string" or
        node_names ~= "default:emerge" then
        if (vol > 190000000) then
            worldedit.emerge_busy = 0
            minetest.chat_send_all ("//set is limited to 190M nodes")
            return 0
        end
    end

    if not coderedit_disable_verbose then
        minetest.chat_send_all ("Starting set of " .. vol ..
            " node(s)")
    end

    local param = { pos1=pos1, pos2=pos2, node_names=node_names }
    minetest.emerge_area (pos1, pos2, emerge_callback_set, param)
    return end_of_start_emerge (pos1, pos2, "SET")
end

-- ===================================================================

--- Sets param2 of a region.
-- @param pos1
-- @param pos2
-- @param param2 Value of param2 to set
-- @return The number of nodes set.

function worldedit.set_param2 (pos1, pos2, param2)

    pos1, pos2 = worldedit.sort_pos (pos1, pos2)

    local manip, area = mh.init (pos1, pos2)
    local param2_data = manip:get_param2_data()

    -- Set param2 for every node
    for i in area:iterp (pos1, pos2) do
        param2_data [i] = param2
    end

    -- Update map
    manip:set_param2_data (param2_data)
    manip:write_to_map()
    manip:update_map()

    return worldedit.volume (pos1, pos2)
end

-- ===================================================================

--- Duplicates a region `amount` times with offset vector `direction`.
-- Stacking is spread across server steps, one copy per step.
-- @return The number of nodes stacked.

function worldedit.stack2 (pos1, pos2, direction, amount, finished)

    local i = 0
    local translated = {x=0, y=0, z=0}
    local function next_one()
        if i < amount then
            i = i + 1
            translated.x = translated.x + direction.x
            translated.y = translated.y + direction.y
            translated.z = translated.z + direction.z

            worldedit.copy2 (pos1, pos2, translated)
            minetest.after (0, next_one)
        else
            if finished then
                finished()
            end
        end
    end

    next_one()
    return worldedit.volume (pos1, pos2) * amount
end

-- ===================================================================

--- Copies a region by offset vector `off`.
-- @param pos1
-- @param pos2
-- @param off
-- @return The number of nodes copied.

function worldedit.copy2 (pos1, pos2, off)

    local pos1, pos2 = worldedit.sort_pos (pos1, pos2)
    worldedit.keep_loaded (pos1, pos2)

    local get_node, get_meta, set_node = minetest.get_node,
            minetest.get_meta, minetest.set_node

    local pos = {}
    pos.x = pos2.x
    while pos.x >= pos1.x do
        pos.y = pos2.y
        while pos.y >= pos1.y do
            pos.z = pos2.z
            while pos.z >= pos1.z do
                local node = get_node(pos) -- Obtain current node
                local meta = get_meta(pos):to_table() -- Get meta of current node
                local newpos = vector.add(pos, off) -- Calculate new position
                set_node(newpos, node) -- Copy node to new position
                get_meta(newpos):from_table(meta) -- Set metadata of new node

                pos.z = pos.z - 1
            end

            pos.y = pos.y - 1
        end

        pos.x = pos.x - 1
    end

    return worldedit.volume (pos1, pos2)
end

-- ===================================================================

-- Moves a region along `axis` by `amount` nodes.
-- @return The number of nodes moved.

function worldedit.old_move (pos1, pos2, axis, amount)

    local pos1, pos2 = worldedit.sort_pos (pos1, pos2)
    worldedit.keep_loaded (pos1, pos2)

    --- TODO: Move slice by slice using schematic method in the move axis
    -- and transfer metadata in separate loop (and if the amount is
    -- greater than the length in the axis, copy whole thing at a time and
    -- erase original after, using schematic method).

    local get_node, get_meta, set_node, remove_node = minetest.get_node,
            minetest.get_meta, minetest.set_node, minetest.remove_node
    -- Copy things backwards when negative to avoid corruption.
    --- FIXME: Lots of code duplication here.

    if amount < 0 then
        local pos = {}
        pos.x = pos1.x

        while pos.x <= pos2.x do
            pos.y = pos1.y

            while pos.y <= pos2.y do
                pos.z = pos1.z

                while pos.z <= pos2.z do

                    -- Obtain current node
                    local node  = get_node (pos)

                    -- Get metadata of current node
                    local meta  = get_meta (pos):to_table()

                    -- Remove current node
                    remove_node (pos)

                    -- Store current position
                    local value = pos [axis]

                    -- Move along axis
                    pos[axis]   = value + amount

                    -- Move node to new position
                    set_node (pos, node)

                    -- Set metadata of new node
                    get_meta (pos):from_table (meta)

                    -- Restore old position
                    pos [axis]  = value

                    pos.z = pos.z + 1
                end

                pos.y = pos.y + 1
            end

            pos.x = pos.x + 1
        end
    else
        local pos = {}
        pos.x = pos2.x

        while pos.x >= pos1.x do
            pos.y = pos2.y

            while pos.y >= pos1.y do
                pos.z = pos2.z

                while pos.z >= pos1.z do

                    -- Obtain current node
                    local node  = get_node (pos)

                    -- Get metadata of current node
                    local meta  = get_meta (pos):to_table()

                    -- Remove current node
                    remove_node (pos)

                    -- Store current position
                    local value = pos [axis]

                    -- Move along axis
                    pos[axis]   = value + amount

                    -- Move node to new position
                    set_node (pos, node)

                    -- Set metadata of new node
                    get_meta (pos):from_table (meta)

                    -- Restore old position
                    pos [axis]  = value

                    pos.z = pos.z - 1
                end

                pos.y = pos.y - 1
            end

            pos.x = pos.x - 1
        end
    end

    return worldedit.volume (pos1, pos2)
end

-- ===================================================================

function worldedit.move (xpos1, xpos2, axis, amount)

    if worldedit.emerge_busy == 1 then
        deblog ("worldedit.move called but WE is busy")
    else
        deblog ("worldedit.move called and WE is free")
    end
    local pos1, pos2 = worldedit.sort_pos (xpos1, xpos2)

    if worldedit.volume (pos1, pos2) > 1500000 then
        minetest.chat_send_all ("//move is limited to 1.5M nodes",
            false)
        return 0
    end

    if worldedit.emerge_busy == 1 then
        if worldedit.use_queue == 0 then
            minetest.chat_send_all ("A previous //operation is busy")
        else
            local qe  = {
                func  = worldedit.wait_move ,
                param = {
                    xpos1=xpos1, xpos2=xpos2, axis=axis, amount=amount
                }
            }

            deblog ("queuing for later: move "   ..
                ocutil.pos_to_str (xpos1) .. " " ..
                ocutil.pos_to_str (xpos2) .. " " ..
                axis .. " " .. amount)

            qe = ocutil.clone_table (qe)
            table.insert (worldedit.cmd_queue, qe)
            minetest.after (1, worldedit.pop_queue)
        end
        return 0
    else
        deblog ("WE is free, proceeding: move " ..
            ocutil.pos_to_str (xpos1) .. " " ..
            ocutil.pos_to_str (xpos2) .. " " ..
            axis  .. " " ..
            amount)
    end

-- ===================================================================

    local newpos1  = { x=pos1.x, y=pos1.y, z=pos1.z }
    local newpos2  = { x=pos2.x, y=pos2.y, z=pos2.z }

    newpos1 [axis] = newpos1 [axis] + amount
    newpos2 [axis] = newpos2 [axis] + amount

-- ===================================================================

    local os1      = minetest.pos_to_string (pos1)
    local os2      = minetest.pos_to_string (pos2)

    local ps1      = minetest.pos_to_string (newpos1)
    local ps2      = minetest.pos_to_string (newpos2)

-- ===================================================================

    if not coderedit_disable_verbose then
        minetest.chat_send_all ("//move " ..
            "Source: " .. os1  .. " " .. os2 .. " " ..
            "Axis: "   .. axis .. " " ..
            "Amount: " .. amount)
        minetest.chat_send_all ("//move Destin:"  ..
            ps1 .. " " .. ps2)
    end

    deblog ("//move " ..
        "Source: " .. os1  .. " " .. os2 .. " " ..
        "Axis: "   .. axis .. " " ..
        "Amount: " .. amount)
    deblog ("//move Destin: " .. ps1 .. " " .. ps2)

-- ===================================================================

    local x1min, x1max = sort2num (pos1.x, pos2.x)
    local y1min, y1max = sort2num (pos1.y, pos2.y)
    local z1min, z1max = sort2num (pos1.z, pos2.z)

    local x2min, x2max = sort2num (newpos1.x, newpos2.x)
    local y2min, y2max = sort2num (newpos1.y, newpos2.y)
    local z2min, z2max = sort2num (newpos1.z, newpos2.z)

    local overlap = true
    if x1max < x2min or x2max < x1min or
       y1max < y2min or y2max < y1min or
       z1max < z2min or z2max < z1min then
        overlap = false
    end

    if overlap then
        minetest.chat_send_all ("Source and dest regions" ..
            " overlap, there may be dark areas")
    end

-- ===================================================================

    worldedit.emerge_busy = 1
    if collectgarbage ("count") > 307200 then collectgarbage() end

    local param = {
        pos1=pos1       , pos2=pos2 , axis=axis , amount=amount ,
        overlap=overlap ,
    }

    minetest.emerge_area (newpos1, newpos2,
        emerge_callback_move, param)

    return end_of_start_emerge (pos1, pos2, "MOVE")
end

-- ===================================================================

-- Duplicates a region along `axis` `amount` times.
-- Stacking is spread across server steps, one copy per step.
-- @param pos1
-- @param pos2
-- @param axis Axis direction, "x", "y", or "z".
-- @param count
-- @return The number of nodes stacked.

function worldedit.stack (pos1, pos2, axis, count)

    local pos1, pos2 = worldedit.sort_pos(pos1, pos2)
    local length = pos2[axis] - pos1[axis] + 1
    if count < 0 then
        count = -count
        length = -length
    end
    local amount = 0
    local copy = worldedit.copy
    local i = 1
    local function next_one()
        if i <= count then
            i = i + 1
            amount = amount + length
            copy(pos1, pos2, axis, amount)
            minetest.after(0, next_one)
        end
    end
    next_one()
    return worldedit.volume(pos1, pos2) * count
end

-- ===================================================================

--- Stretches a region by a factor of positive integers along the X, Y, and Z
-- axes, respectively, with `pos1` as the origin.
-- @param pos1
-- @param pos2
-- @param stretch_x Amount to stretch along X axis.
-- @param stretch_y Amount to stretch along Y axis.
-- @param stretch_z Amount to stretch along Z axis.
-- @return The number of nodes scaled.
-- @return The new scaled position 1.
-- @return The new scaled position 2.

function worldedit.stretch (pos1, pos2, stretch_x, stretch_y, stretch_z)

    local pos1, pos2 = worldedit.sort_pos(pos1, pos2)

    -- Prepare schematic of large node
    local get_node, get_meta, place_schematic = minetest.get_node,
            minetest.get_meta, minetest.place_schematic
    local placeholder_node = {name="", param1=255, param2=0}
    local nodes = {}
    for i = 1, stretch_x * stretch_y * stretch_z do
        nodes[i] = placeholder_node
    end

    local schematic = {size={x=stretch_x, y=stretch_y, z=stretch_z},
        data=nodes}

    local size_x, size_y, size_z = stretch_x - 1,
        stretch_y - 1, stretch_z - 1

    local new_pos2 = {
        x = pos1.x + (pos2.x - pos1.x) * stretch_x + size_x,
        y = pos1.y + (pos2.y - pos1.y) * stretch_y + size_y,
        z = pos1.z + (pos2.z - pos1.z) * stretch_z + size_z,
    }
    worldedit.keep_loaded(pos1, new_pos2)

    local pos = {x=pos2.x, y=0, z=0}
    local big_pos = {x=0, y=0, z=0}
    while pos.x >= pos1.x do
        pos.y = pos2.y
        while pos.y >= pos1.y do
            pos.z = pos2.z
            while pos.z >= pos1.z do
                local node = get_node(pos) -- Get current node
                local meta = get_meta(pos):to_table() -- Get meta of current node

                -- Calculate far corner of the big node
                local pos_x = pos1.x + (pos.x - pos1.x) * stretch_x
                local pos_y = pos1.y + (pos.y - pos1.y) * stretch_y
                local pos_z = pos1.z + (pos.z - pos1.z) * stretch_z

                -- Create large node
                placeholder_node.name = node.name
                placeholder_node.param2 = node.param2
                big_pos.x, big_pos.y, big_pos.z = pos_x, pos_y, pos_z
                place_schematic(big_pos, schematic)

                -- Fill in large node meta
                if next(meta.fields) ~= nil or next(meta.inventory) ~= nil then
                    -- Node has meta fields
                    for x = 0, size_x do
                    for y = 0, size_y do
                    for z = 0, size_z do
                        big_pos.x = pos_x + x
                        big_pos.y = pos_y + y
                        big_pos.z = pos_z + z
                        -- Set metadata of new node
                        get_meta(big_pos):from_table(meta)
                    end
                    end
                    end
                end
                pos.z = pos.z - 1
            end
            pos.y = pos.y - 1
        end
        pos.x = pos.x - 1
    end
    return worldedit.volume(pos1, pos2) * stretch_x * stretch_y * stretch_z, pos1, new_pos2
end

-- ===================================================================

--- Transposes a region between two axes.
-- @return The number of nodes transposed.
-- @return The new transposed position 1.
-- @return The new transposed position 2.

function worldedit.transpose(pos1, pos2, axis1, axis2)
    local pos1, pos2 = worldedit.sort_pos(pos1, pos2)

    local compare
    local extent1, extent2 = pos2[axis1] - pos1[axis1], pos2[axis2] - pos1[axis2]

    if extent1 > extent2 then
        compare = function(extent1, extent2)
            return extent1 > extent2
        end
    else
        compare = function(extent1, extent2)
            return extent1 < extent2
        end
    end

    -- Calculate the new position 2 after transposition
    local new_pos2 = {x=pos2.x, y=pos2.y, z=pos2.z}
    new_pos2[axis1] = pos1[axis1] + extent2
    new_pos2[axis2] = pos1[axis2] + extent1

    local upper_bound = {x=pos2.x, y=pos2.y, z=pos2.z}
    if upper_bound[axis1] < new_pos2[axis1] then upper_bound[axis1] = new_pos2[axis1] end
    if upper_bound[axis2] < new_pos2[axis2] then upper_bound[axis2] = new_pos2[axis2] end
    worldedit.keep_loaded(pos1, upper_bound)

    local pos = {x=pos1.x, y=0, z=0}
    local get_node, get_meta, set_node = minetest.get_node,
            minetest.get_meta, minetest.set_node
    while pos.x <= pos2.x do
        pos.y = pos1.y
        while pos.y <= pos2.y do
            pos.z = pos1.z
            while pos.z <= pos2.z do
                local extent1, extent2 = pos[axis1] - pos1[axis1], pos[axis2] - pos1[axis2]
                if compare(extent1, extent2) then -- Transpose only if below the diagonal
                    local node1 = get_node(pos)
                    local meta1 = get_meta(pos):to_table()
                    local value1, value2 = pos[axis1], pos[axis2] -- Save position values
                    pos[axis1], pos[axis2] = pos1[axis1] + extent2, pos1[axis2] + extent1 -- Swap axis extents
                    local node2 = get_node(pos)
                    local meta2 = get_meta(pos):to_table()
                    set_node(pos, node1)
                    get_meta(pos):from_table(meta1)
                    pos[axis1], pos[axis2] = value1, value2 -- Restore position values
                    set_node(pos, node2)
                    get_meta(pos):from_table(meta2)
                end
                pos.z = pos.z + 1
            end
            pos.y = pos.y + 1
        end
        pos.x = pos.x + 1
    end
    return worldedit.volume(pos1, pos2), pos1, new_pos2
end

-- ===================================================================

--- Flips a region along `axis`.
-- @return The number of nodes flipped.

function worldedit.flip(pos1, pos2, axis)
    local pos1, pos2 = worldedit.sort_pos(pos1, pos2)

    worldedit.keep_loaded(pos1, pos2)

    --- TODO: Flip the region slice by slice along the flip axis using schematic method.
    local pos = {x=pos1.x, y=0, z=0}
    local start = pos1[axis] + pos2[axis]
    pos2[axis] = pos1[axis] + math.floor((pos2[axis] - pos1[axis]) / 2)
    local get_node, get_meta, set_node = minetest.get_node,
            minetest.get_meta, minetest.set_node
    while pos.x <= pos2.x do
        pos.y = pos1.y
        while pos.y <= pos2.y do
            pos.z = pos1.z
            while pos.z <= pos2.z do
                local node1 = get_node(pos)
                local meta1 = get_meta(pos):to_table()
                local value = pos[axis] -- Save position
                pos[axis] = start - value -- Shift position
                local node2 = get_node(pos)
                local meta2 = get_meta(pos):to_table()
                set_node(pos, node1)
                get_meta(pos):from_table(meta1)
                pos[axis] = value -- Restore position
                set_node(pos, node2)
                get_meta(pos):from_table(meta2)
                pos.z = pos.z + 1
            end
            pos.y = pos.y + 1
        end
        pos.x = pos.x + 1
    end
    return worldedit.volume(pos1, pos2)
end

-- ===================================================================

--- Rotates a region clockwise around an axis.
-- @param pos1
-- @param pos2
-- @param axis Axis ("x", "y", or "z").
-- @param angle Angle in degrees (90 degree increments only).
-- @return The number of nodes rotated.
-- @return The new first position.
-- @return The new second position.

function worldedit.rotate(pos1, pos2, axis, angle)
    local pos1, pos2 = worldedit.sort_pos(pos1, pos2)

    if worldedit.volume (pos1, pos2) > 1000000 then
        minetest.chat_send_all ("//rotate is limited to 1M nodes",
            false)
        return
    end

    local other1, other2 = worldedit.get_axis_others(axis)
    angle = angle % 360

    local count
    if angle == 90 then
        worldedit.flip(pos1, pos2, other1)
        count, pos1, pos2 = worldedit.transpose(pos1, pos2, other1, other2)
    elseif angle == 180 then
        worldedit.flip(pos1, pos2, other1)
        count = worldedit.flip(pos1, pos2, other2)
    elseif angle == 270 then
        worldedit.flip(pos1, pos2, other2)
        count, pos1, pos2 = worldedit.transpose(pos1, pos2, other1, other2)
    else
        error("Only 90 degree increments are supported!")
    end
    return count, pos1, pos2
end

-- ===================================================================

-- Rotates all oriented nodes in a region clockwise around the Y axis.
-- @param pos1
-- @param pos2
-- @param angle Angle in degrees (90 degree increments only).
-- @return The number of nodes oriented.
-- TODO: Support 6D facedir rotation along arbitrary axis.

function worldedit.orient(pos1, pos2, angle)
    local pos1, pos2 = worldedit.sort_pos(pos1, pos2)

    if worldedit.volume (pos1, pos2) > 1000000 then
        minetest.chat_send_all ("//orient is limited to 1M nodes",
            false)
        return
    end

    local registered_nodes = minetest.registered_nodes

    local wallmounted = {
        [90]  = {[0]=0, 1, 5, 4, 2, 3},
        [180] = {[0]=0, 1, 3, 2, 5, 4},
        [270] = {[0]=0, 1, 4, 5, 3, 2}
    }
    local facedir = {
        [90]  = {[0]=1, 2, 3, 0},
        [180] = {[0]=2, 3, 0, 1},
        [270] = {[0]=3, 0, 1, 2}
    }

    angle = angle % 360
    if angle == 0 then
        return 0
    end
    if angle % 90 ~= 0 then
        error("Only 90 degree increments are supported!")
    end
    local wallmounted_substitution = wallmounted[angle]
    local facedir_substitution = facedir[angle]

    worldedit.keep_loaded(pos1, pos2)

    local count = 0
    local set_node, get_node, get_meta, swap_node = minetest.set_node,
            minetest.get_node, minetest.get_meta, minetest.swap_node
    local pos = {x=pos1.x, y=0, z=0}
    while pos.x <= pos2.x do
        pos.y = pos1.y
        while pos.y <= pos2.y do
            pos.z = pos1.z
            while pos.z <= pos2.z do
                local node = get_node(pos)
                local def = registered_nodes[node.name]
                if def then
                    if def.paramtype2 == "wallmounted" then
                        node.param2 = wallmounted_substitution[node.param2]
                        local meta = get_meta(pos):to_table()
                        set_node(pos, node)
                        get_meta(pos):from_table(meta)
                        count = count + 1
                    elseif def.paramtype2 == "facedir" then
                        node.param2 = facedir_substitution[node.param2]
                        local meta = get_meta(pos):to_table()
                        set_node(pos, node)
                        get_meta(pos):from_table(meta)
                        count = count + 1
                    end
                end
                pos.z = pos.z + 1
            end
            pos.y = pos.y + 1
        end
        pos.x = pos.x + 1
    end
    return count
end

-- ===================================================================

-- Attempts to fix the lighting in a region.
-- @return The number of nodes updated.

function worldedit.fixlight(pos1, pos2)
    local pos1, pos2 = worldedit.sort_pos (pos1, pos2)

    local epos1 = { x=pos1.x-32, y=pos1.y-32, z=pos1.z-32 }
    local epos2 = { x=pos2.x+32, y=pos2.y+32, z=pos2.z+32 }
    vm = minetest.get_voxel_manip()
    vm:read_from_map (epos1, epos2)
    vm:set_lighting ({day=15,night=4}, epos1, epos2)
    vm:calc_lighting (epos1, epos2)
    vm:update_liquids()
    vm:write_to_map()

    return worldedit.volume (pos1, pos2)
end

-- ===================================================================

-- Clears all objects in a region.
-- @return The number of objects cleared.

function worldedit.clear_objects(pos1, pos2)
    pos1, pos2 = worldedit.sort_pos(pos1, pos2)

    worldedit.keep_loaded(pos1, pos2)

    -- Offset positions to include full nodes (positions are in the center of nodes)
    local pos1x, pos1y, pos1z = pos1.x - 0.5, pos1.y - 0.5, pos1.z - 0.5
    local pos2x, pos2y, pos2z = pos2.x + 0.5, pos2.y + 0.5, pos2.z + 0.5

    -- Center of region
    local center = {
        x = pos1x + ((pos2x - pos1x) / 2),
        y = pos1y + ((pos2y - pos1y) / 2),
        z = pos1z + ((pos2z - pos1z) / 2)
    }
    -- Bounding sphere radius
    local radius = math.sqrt(
            (center.x - pos1x) ^ 2 +
            (center.y - pos1y) ^ 2 +
            (center.z - pos1z) ^ 2)

    local count = 0
    for _, obj in pairs (minetest.get_objects_inside_radius (center, radius)) do

        local entity = obj:get_luaentity()
        -- Avoid players and WorldEdit entities
        if not obj:is_player() and (not entity or
                not entity.name:find("^worldedit:")) then
            local pos = obj:getpos()
            if pos.x >= pos1x and pos.x <= pos2x and
                    pos.y >= pos1y and pos.y <= pos2y and
                    pos.z >= pos1z and pos.z <= pos2z then
                -- Inside region
                obj:remove()
                count = count + 1
            end
        end
    end
    return count
end
