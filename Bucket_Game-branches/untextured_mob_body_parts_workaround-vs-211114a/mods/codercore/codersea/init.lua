-- File:     codersea/init.lua
-- Purpose:  CoderSea "init.lua" (i.e., main) module
-- Credits:  See "codersea.md"
-- Licenses: See "LICENSE"

codersea         = {}
codersea.modname = "codersea"
codersea.modpath = minetest.get_modpath (codersea.modname)

codersea.multiply_texture = function(texture, mesh_count)
	-- by Poikilos
	-- mesh_count -- This must be the # of meshes in model.
	-- texture -- Provide a single texture or variants to use randomly.
	--
	--     If texture is not a table, it will be assumed to be a
	--     string, and table of length mesh_count will be returned so
	--     you don't have to type something like:
	--     { textures, textures, textures, ...}
	--     (The same texture will be applied to multiple body parts.)
	--
	--     If texture is a table, it will be assumed to be a list of
	--     variants (for mobs that get a random texture), and a nested
	--     table will be returned where each element is of length
	--     mesh_count so you don't have to type something like
	--     {
	--         {texturemonkey.png, texturemonkey.png, texturemonkey.png, ...},
	--         {texturemonkey2.png, texturemonkey2.png, texturemonkey2.png, ...},
	--         {texturemonkey3.png, texturemonkey3.png, texturemonkey3.png, ...},
	--     }
	--     (The same variant will be applied to multiple body
	--     parts, but a variant is still selected at random by
	--     register_mob.)
	if not texture then
		error("You must provide a texture string or table of variants.")
	end
	if not mesh_count then
		error(
			"You must provide a mesh_count" ..
			" (The number of meshes in the model file)." ..
			" See the traceback below for what file called" ..
			" multiply_texture incorrectly."
		)
	end
	local multi_mesh_texture = {}
	if type(texture) == "table" then
		-- It is a list-like table of variant texture filenames.
		local texture_filename = nil
		for variant_i = 1,#texture,1 do
			multi_mesh_texture[variant_i] = {}
			texture_filename = texture[variant_i]
			if type(texture_filename) == "table" then
				texture_filename = texture_filename[1]
				-- ^ In case the mobs-style nested table was passed,
				--   copy the single texture for each variant.
			end
			for multimesh_texture_i = 1,mesh_count,1 do
				multi_mesh_texture[variant_i][multimesh_texture_i] = texture_filename
			end
		end
	else
		-- It is a single texture filename string.
		for multimesh_texture_i = 1,mesh_count,1 do
			multi_mesh_texture[multimesh_texture_i] = texture
		end
	end
	return multi_mesh_texture
end

local has_mobs   = ocutil.mod_exists ("mobs")
local modpath    = codersea.modpath

local                       liteworld =
      ocutil.bool_setting ("liteworld")

-- "util.lua" and "settings.lua" should come first.
--
dofile (modpath .. "/util.lua"          );
dofile (modpath .. "/settings.lua"      );
dofile (modpath .. "/tidyup.lua"        );

if ocutil.model_missing (codersea.modname,
    "codersea_turtle.x") then
    codersea_disable_turtle = true
end

if has_mobs then
    ocutil.log ("codersea: has_mobs")
else
    ocutil.log ("codersea: not has_mobs")
    codersea_disable_urchin = true
    codersea_disable_mobs   = true
end

if not codersea_disable_shine then
dofile (modpath .. "/seashine.lua"      );
end

dofile (modpath .. "/seasprites.lua"    );

if not codersea_reset then
    dofile (modpath .. "/seaglass.lua");
end

if not codersea_disable_seastone then
    dofile (modpath .. "/seacobble.lua" );
    dofile (modpath .. "/seagravel.lua" );
    dofile (modpath .. "/seastone.lua"  );
    dofile (modpath .. "/seabrick.lua"  );
end

-- Should come after seaglass and seastone mods
dofile (modpath .. "/seaplants.lua"     );

if not codersea_disable_shipwrecks then
    dofile (modpath .. "/shipwrecks.lua");
end

dofile (modpath .. "/legacy.lua"        );

-- "fixwater.lua" should  come after the other "codersea" modules ex-
-- cept for the "mobs" ones.
--
dofile (modpath .. "/fixwater.lua"      );

-- Future change: Perhaps use a clone-table utility function here.

if not codersea_drowning then
    local function overwrite_drowning (name)
        local table  = minetest.registered_nodes [name]
        if table ~= nil then
            local table2 = {}
            for i,v in pairs (table) do table2 [i] = v end
            table2.drowning = false
            minetest.register_node (":" .. name, table2)
        end
    end

    overwrite_drowning ("default:water_source"  )
    overwrite_drowning ("default:water_flowing" )
    overwrite_drowning ("default:water_gel"     )
    overwrite_drowning ("default:lava_source"   )
    overwrite_drowning ("default:lava_flowing"  )
end

if not codersea_disable_mobs then
    if not codersea_disable_fish         then
        dofile (modpath ..  "/codersea-carp.lua"      )
        dofile (modpath ..  "/codersea-trout.lua"     )
        dofile (modpath ..  "/codersea-morefish.lua"  )
    end

    if not codersea_disable_jellyfish   then
        dofile (modpath ..  "/codersea-jellyfish.lua" )
    end
    if not codersea_disable_lobster  then
        dofile (modpath ..  "/codersea-lobster.lua"   )
    end
    if not codersea_disable_seahorse then
        dofile (modpath ..  "/codersea-seahorse.lua"  )
    end
    if not codersea_disable_shark       then
        dofile (modpath ..  "/codersea-shark.lua"     )
    end
    if not codersea_disable_urchin      then
        dofile (modpath ..  "/codersea-urchin.lua"    )
    end

    if liteworld == false then

--      if not codersea_disable_dolidro     then
--          dofile (modpath ..  "/codersea-dolidro.lua" )
--      end

--      if not codersea_disable_octopus then
--          dofile (modpath ..  "/codersea-octopus.lua" )
--      end

        if not codersea_disable_turtle  then
            dofile (modpath ..  "/codersea-turtle.lua"  )
        end
    end
end

-- ===================================================================

minetest.register_craftitem ("codersea:cookedfish" , {
    description     = ( "Cooked Fish" )         ,
    inventory_image = "codersea_cookedfish.png" ,
    on_use          = minetest.item_eat (5)     ,
    groups          = {
        food_meat=1, flammable=2
    } ,
})

minetest.register_craft ({
    type     = "cooking"             ,
    output   = "codersea:cookedfish" ,
    recipe   = "codersea:sushi"      ,
    cooktime = 5                     ,
})

minetest.register_craftitem ("codersea:fishfood", {
    description     = ("Fish Food")           ,
    inventory_image = "codersea_fishfood.png" ,
})

-- ===================================================================
-- End of file.
