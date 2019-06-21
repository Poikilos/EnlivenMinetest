-- Minetest mod: bucket
-- See "LICENSE" for licenses and related information.

local bucket_gels_lava  =
      ocutil.bool_default ("bucket_gels_lava"  , true)
local bucket_gels_water =
      ocutil.bool_default ("bucket_gels_water" , false)

minetest.register_alias (       "bucket"                 ,
                                "bucket:empty"           )

minetest.register_alias (       "bucket_empty"           ,
                                "bucket:empty"           )
minetest.register_alias ("bucket:bucket_empty"           ,
                                "bucket:empty"           )

minetest.register_alias (       "bucket_lava"            ,
                                "bucket:lava"            )
minetest.register_alias ("bucket:bucket_lava"            ,
                                "bucket:lava"            )

minetest.register_alias (       "bucket_lava_crust"      ,
                                "bucket:lava_crust"      )
minetest.register_alias ("bucket:bucket_lava_crust"      ,
                                "bucket:lava_crust"      )

minetest.register_alias (       "bucket_water"           ,
                                "bucket:water"           )
minetest.register_alias ("bucket:bucket_water"           ,
                                "bucket:water"           )

minetest.register_alias (       "bucket_water_gel"       ,
                                "bucket:water_gel"       )
minetest.register_alias ("bucket:bucket_water_gel"       ,
                                "bucket:water_gel"       )

minetest.register_alias (       "bucket_water_gel_slope" ,
                                "bucket:water_gel_slope" )
minetest.register_alias ("bucket:bucket_water_gel_slope" ,
                                "bucket:water_gel_slope" )

minetest.register_craft({
    output = 'bucket:empty 1',
    recipe = {
        {'default:steel_ingot', '', 'default:steel_ingot'},
        {'', 'default:steel_ingot', ''},
    }
})

bucket = {}
bucket.liquids = {}

local function check_protection(pos, name, text)
    if minetest.is_protected(pos, name) then
        minetest.log("action", (name ~= "" and name or "A mod")
            .. " tried to " .. text
            .. " at protected position "
            .. minetest.pos_to_string(pos)
            .. " with a bucket")
        minetest.record_protection_violation(pos, name)
        return true
    end
    return false
end

-- Register a new liquid
--    source   = name of the source  node
--    itemname = name of the new bucket item (or nil if liquid is not takeable)
--    inventory_image = texture of the new bucket item (ignored if itemname == nil)
--    name = text description of the bucket item
--    groups = (optional) groups of the bucket item, for example {water_bucket = 1}
--    force_renew = (optional) bool. Force the liquid source to renew if it has a
--                  source neighbour, even if defined as 'liquid_renewable = false'.
--                  Needed to avoid creating holes in sloping rivers.
--
-- This function can be called from any mod that depends on bucket.

function bucket.register_liquid(source, flowing, itemname, inventory_image, name,
        groups, force_renew)

    bucket.liquids [source] = {
        source      = source      ,
        itemname    = itemname    ,
        force_renew = force_renew ,
    }
    if flowing then
        bucket.liquids [source] ["flowing"] = flowing
        bucket.liquids [flowing] = bucket.liquids[source]
    end

    if itemname ~= nil then
        minetest.register_craftitem(itemname, {
            description = name,
            inventory_image = inventory_image,
            stack_max = 1,
            liquids_pointable = true,
            groups = groups,

            on_place = function(itemstack, user, pointed_thing)
                -- Must be pointing to node
                if pointed_thing.type ~= "node" then
                    return
                end

                local node = minetest.get_node_or_nil(pointed_thing.under)
                local ndef = node and minetest.registered_nodes[node.name]

                -- Call on_rightclick if the pointed node defines it
                if ndef and ndef.on_rightclick and
                   user and not user:get_player_control().sneak then
                    return ndef.on_rightclick(
                        pointed_thing.under,
                        node, user,
                        itemstack)
                end

                local lpos

                -- Check if pointing to a buildable node
                if ndef and ndef.buildable_to then
                    -- buildable; replace the node
                    lpos = pointed_thing.under
                else
                    -- not buildable to; place the liquid above
                    -- check if the node above can be replaced

                    lpos = pointed_thing.above
                    node = minetest.get_node_or_nil(lpos)
                    local above_ndef = node and minetest.registered_nodes[node.name]

                    if not above_ndef or not above_ndef.buildable_to then
                        -- do not remove the bucket with the liquid
                        return itemstack
                    end
                end

                if check_protection(lpos, user
                        and user:get_player_name()
                        or "", "place "..source) then
                    return
                end

                minetest.set_node(lpos, {name = source})
                return ItemStack("bucket:empty")
            end
        })
    end
end

minetest.register_craftitem("bucket:empty", {
    description = "Empty Bucket",
    inventory_image = "bucket.png",
    stack_max = 99,
    liquids_pointable = true,
    on_use = function(itemstack, user, pointed_thing)
        if pointed_thing.type == "object" then
            pointed_thing.ref:punch(user, 1.0, { full_punch_interval=1.0 }, nil)
            return user:get_wielded_item()
        elseif pointed_thing.type ~= "node" then
            -- do nothing if it's neither object nor node
            return
        end

        -- Check if pointing to a liquid source
        local node       = minetest.get_node (pointed_thing.under)
        local liquiddef  = bucket.liquids [node.name]
        local item_count = user:get_wielded_item():get_count()

        if  liquiddef          ~= nil
        and liquiddef.itemname ~= nil
        and node.name == liquiddef.source then
            if check_protection (pointed_thing.under,
                    user:get_player_name(),
                    "take ".. node.name) then
                return
            end

            -- default set to return filled bucket
            local giving_back = liquiddef.itemname

            -- check if holding more than 1 empty bucket
            if item_count > 1 then

                -- if space in inventory add filled bucked, otherwise drop as item
                local inv = user:get_inventory()
                if inv:room_for_item("main", {name=liquiddef.itemname}) then
                    inv:add_item("main", liquiddef.itemname)
                else
                    local pos = user:getpos()
                    pos.y = math.floor(pos.y + 0.5)
                    minetest.add_item(pos, liquiddef.itemname)
                end

                -- set to return empty buckets minus 1
                giving_back = "bucket:empty "..tostring(item_count-1)

            end

            -- force_renew requires a source neighbour
            local source_neighbor = false
            if liquiddef.force_renew then
                source_neighbor =
                    minetest.find_node_near(pointed_thing.under, 1, liquiddef.source)
            end
            if not (source_neighbor and liquiddef.force_renew) then
                minetest.add_node(pointed_thing.under, {name = "air"})
            end

            return ItemStack(giving_back)
        else
            -- non-liquid nodes will have their on_punch triggered
            local node_def = minetest.registered_nodes[node.name]
            if node_def then
                node_def.on_punch(pointed_thing.under, node, user, pointed_thing)
            end
            return user:get_wielded_item()
        end
    end,
})

-- ===================================================================

bucket.register_liquid (
    "default:water_source" ,
    "default:water_flowing" ,
    "bucket:water"         ,
    "bucket_water.png"     ,
    "Water Bucket"         ,
    { water_bucket = 1 }
)

if bucket_gels_water then
bucket.register_liquid (
    "default:water_gel"    ,
    nil                    ,
    "bucket:water"         ,
    "bucket_water.png"     ,
    "Water Gel Bucket"     ,
    { water_bucket = 1 }
)
end

-- ===================================================================

bucket.register_liquid (
    "default:water_gel"       ,
    nil                       ,
    "bucket:water_gel"        ,
    "bucket_water.png"        ,
    "Water Gel Bucket"        ,
    { water_bucket = 1 }
)

bucket.register_liquid (
    "default:water_gel_slope" ,
    nil                       ,
    "bucket:water_gel_slope"  ,
    "bucket_water.png"        ,
    "Water Gel Slope Bucket"  ,
    { water_bucket = 1 }
)

-- ===================================================================

bucket.register_liquid (
    "default:lava_source"  ,
    nil                    ,
    "bucket:lava"          ,
    "bucket_lava.png"      ,
    "Lava Bucket"
)

if bucket_gels_lava then
bucket.register_liquid (
    "default:lava_gel"     ,
    nil                    ,
    "bucket:lava"          ,
    "bucket_lava.png"      ,
    "Lava Gel Bucket"
)
end

-- ===================================================================

bucket.register_liquid (
    "default:lava_crust_source" ,
    nil                         ,
    "bucket:lava_crust"         ,
    "bucket_lava_crust.png"     ,
    "Lava Crust Bucket"
)

-- ===================================================================

bucket.register_liquid(
    "default:river_water_source" ,
    nil                          ,
    "bucket:river_water"         ,
    "bucket_river_water.png"     ,
    "River Water Bucket"         ,
    { water_bucket = 1 } ,
    true
)

minetest.register_craft ({
    type         = "fuel",
    recipe       = "bucket:lava",
    burntime     = 60 ,
    replacements = {{ "bucket:lava", "bucket:empty" }} ,
})

-- ===================================================================

for name, ucname in pairs (default.waters) do

    local dename = "default:" .. name
    local bcname = "bucket:"  .. name

    local img    = "default_" .. name ..
        ".png^bucket_extmask.png^[makealpha:128,0,0^bucket_overlay.png"

    bucket.register_liquid (
        dename .. "_source"           ,
        nil                           ,
        bcname                        ,
        img                           ,
        ucname .. " Bucket"           ,
        { water_bucket = 1 }
    )

    if bucket_gels_water then
        bucket.register_liquid (
            dename .. "_gel"          ,
            nil                       ,
            bcname                    ,
            img                       ,
            ucname .. " Gel Bucket"   ,
            { water_bucket = 1 }
        )
    end

    bucket.register_liquid (
        dename .. "_gel"              ,
        nil                           ,
        bcname .. "_gel"              ,
        img                           ,
        ucname .. " Gel Bucket"       ,
        { water_bucket = 1 }
    )

    bucket.register_liquid (
        dename .. "_gel_slope"        ,
        nil                           ,
        bcname .. "_gel_slope"        ,
        img                           ,
        ucname .. " Gel Slope Bucket" ,
        { water_bucket = 1 }
    )
end
