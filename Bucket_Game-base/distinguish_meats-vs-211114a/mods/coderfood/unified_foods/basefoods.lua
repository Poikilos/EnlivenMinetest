-- ===================================================================
-- "ufoods" common header.

local S
if minetest.get_modpath ("intllib") then
    S = intllib.Getter()
else
    S = function (s) return s end
end

local item_eat     = unified_foods.item_eat
local keep_vessels = unified_foods.keep_vessels
local mra          = minetest.registered_aliases
local mri          = minetest.registered_items

local reg_alias    = ocutil.safe_register_alias
local reg_craft    = minetest.register_craft
local reg_food     = unified_foods.register_food
local reg_item     = ocutil.safe_register_item
local reg_juice    = unified_foods.register_juice

local needitem

-- ===================================================================

needitem = reg_food ("juicer",
    {
        description    = "Juicer"         ,
        external_items = "farming:juicer" ,
    })

reg_craft ({
    output = neednode ,
    recipe = {
        { ""              , "default:stone" , ""              } ,
        { "default:stone" , ""              , "default:stone" } ,
    }
})

-- ===================================================================

needitem = reg_food ("sugar",
    {
        description    = "Sugar"   ,

        external_items = {
            "farming:sugar" , "jkfarming:sugar" ,
            "bushes:sugar"  , "mtfoods:sugar"   ,
        }
    })

if ocutil.thing_exists ("default:papyrus") then
    reg_craft ({
        output = needitem .. " 20" ,
        recipe = {
            { "default:papyrus" }  ,
        }
    })
end

-- ===================================================================

-- Note: The fallback definition provided here isn't fully functional.
-- However,  the  expectation is that "bucket" is usually present,  so
-- the fallback usually shouldn't be needed.

needitem = reg_food ("bucket_water",
    {
        description    = "Bucket of water"     ,
        extra_groups   = { bucket_water=1 }    ,
        external_items = "bucket:bucket_water" ,
    })

reg_alias ("bucket:bucket_water", needitem)

-- ===================================================================

needitem = reg_food ("salt",
    {
        description    = "Salt"         ,
        satiate        = 0              ,
        external_items = "farming:salt" ,
    })

reg_craft ({
    type         = "cooking"            ,
    cooktime     = 15                   ,
    output       = needitem             ,
    recipe       = "group:bucket_water" ,
    replacements = keep_vessels         ,
})

reg_alias ("farming:salt", needitem)

-- ===================================================================

needitem = reg_food ("wheat",
    {
        description    = "Wheat" ,

        external_items = {
            "farming:wheat", "plantlib:wheat"
        } ,
    })

reg_craft ({
    output = needitem ,
    recipe = {
        { "default:dry_shrub" } ,
    }
})

reg_alias ("farming:wheat", needitem)

-- ===================================================================

needitem = reg_food ("flour",
    {
        description    = "Flour"         ,
        external_items = "farming:flour" ,
    })

reg_craft ({
    output = needitem ,
    recipe = {
        { "group:food_wheat" } ,
        { "group:food_wheat" } ,
    }
})

reg_alias ("farming:flour", needitem)

-- ===================================================================

needitem = reg_food ("bread",
    {
        description    = "Bread"         ,
        stack_max      = 3               ,
        satiate        = 5               ,
        external_items = "farming:bread" ,
    })

reg_craft ({
    type     = "cooking"          ,
    cooktime = 15                 ,
    output   = needitem           ,
    recipe   = "group:food_flour" ,
})

reg_alias ("farming:bread", needitem)

-- ===================================================================

needitem = reg_food ("egg",
    {
        description    = "Egg" ,
        stack_max      = 10    ,
        satiate        =  1    ,

        external_items = {
            "mobs:egg"                , "animalmaterials:egg" ,
            "animalmaterials:egg_big" , "jkanimals:egg"       ,
        } ,
    })

reg_alias ("mobs:egg", needitem)

-- ===================================================================

needitem = reg_food ("meat_raw",
    {
        description    = "Raw meat" ,
        stack_max      = 25         ,
        satiate        =  1         ,

        extra_groups   = { meat=1 } ,
        external_items = {
            "mobs:meat_raw", "animalmaterials:meat_raw"
        } ,
    })

reg_alias ("mobs:meat_raw", needitem)

-- ===================================================================

needitem = reg_food ("meat",
    {
        description    = "Cooked Meat" ,
        satiate        = 3             ,
        extra_groups   = { meat=1 }    ,

        external_items = {
            "mobs:meat"               , "jkanimals:meat"             ,
            "mobs:chicken_cooked"     , "mobfcooking:cooked_pork"    ,
            "mobfcooking:cooked_beef" , "mobfcooking:cooked_chicken" ,
            "mobfcooking:cooked_lamb" , "mobfcooking:cooked_venison" ,
        } ,
    })

reg_craft ({
    type     = "cooking"             ,
    output   = needitem              ,
    recipe   = "group:food_meat_raw" ,
    cooktime = 30                    ,
})

-- ===================================================================
-- End of file.
