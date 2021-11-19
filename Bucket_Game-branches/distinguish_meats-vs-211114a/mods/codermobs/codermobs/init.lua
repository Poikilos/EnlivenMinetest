codermobs  = {}
mobs_param = {}

codermobs.modname = minetest.get_current_modname()
codermobs.modpath = ocutil.get_modpath (codermobs.modname)

local modname     = codermobs.modname
local nm          = modname
local mp          = codermobs.modpath

local lua_exists  = function (basename)
    return ocutil.lua_exists  (modname, basename)
end

local lua_missing = function (basename)
    return ocutil.lua_missing (modname, basename)
end

local enable_moontest =
    minetest.setting_getbool ("enable_moon"     ) or
    minetest.setting_getbool ("enable_moontest" )

-- ===================================================================

codermobs.log_mob_loaded = ocutil.any_bool_setting ({
    "logmob"         ,
    "log_mob"        ,
    "logmobloaded"   ,
    "log_mob_loaded" ,
})

-- ===================================================================

codermobs.model_exists  = function (m3dfile)
    return ocutil.model_exists  (modname, m3dfile)
end
local     model_exists  = codermobs.model_exists

-- ===================================================================

codermobs.model_missing = function (m3dfile)
    return ocutil.model_missing (modname, m3dfile)
end
local     model_missing = codermobs.model_missing

-- ===================================================================

codermobs.mob_exists = function (basename)
    local model_1 = "codermobs_" .. basename .. ".b3d"
    local model_2 = "codermobs_" .. basename .. ".x"

    local both_missing = model_missing (model_1) and
                         model_missing (model_2)

    if lua_missing (basename) or both_missing then
        return false
    end

    return true
end
local     mob_exists   = codermobs.mob_exists

-- ===================================================================

codermobs.textu_exists = function (imgfile)
    return ocutil.mod_texture_exists (modname, imgfile)
end
local     textu_exists = codermobs.textu_exists

-- ===================================================================
-- These must come first.

dofile (mp .. "/globals.lua" )
dofile (mp .. "/util.lua"    )


local enable_animal_materials =  lua_exists("animal_materials")
-- This is an object as opposed to a mob
if not minetest.get_modpath("animalmaterials") then
    -- ^ another way is: if not minetest.registered_items["animalmaterials:meat_raw"] then
    if  enable_animal_materials then
        dofile (mp .. "/animal_materials.lua"   )
    end
else
    -- Someone added the animalmaterials mod in this case,
    -- so only create aliases:
    if  enable_animal_materials then
        -- ^ Only consider the presence of themain file
        --   (animal_materials.lua), since OldCoder may
        --   have added that condition further up in order to
        --   exclude the animal_materials namespace in
        --   differently-packaged copies of bucket_game.
        --   -Poikilos (distinguish_meats-vs-211114a patch) 
        dofile (mp .. "/animal_materials_aliases.lua"   )
    end
end

dofile (mp .. "/animal_materials_overrides.lua"   )

-- This is an object as opposed to a mob
if  lua_exists    ("vombie_flame"           ) then
    dofile (mp .. "/vombie_flame.lua"       )
end

-- ===================================================================

-- Hen, Rooster, and Baby Chick should be loaded in that order.

-- Filenames are a special case for this mob
if  lua_exists    ("hen"                    ) then
    dofile (mp .. "/hen.lua"                )
end

-- Filenames are a special case for this mob
if  lua_exists    ("rooster"                ) then
    dofile (mp .. "/rooster.lua"            )
end

if  mob_exists    ("baby_chick"             ) then
    dofile (mp .. "/baby_chick.lua"         )
end

-- ===================================================================

if  mob_exists    ("duck_walking"           ) then
    dofile (mp .. "/duck_walking.lua"       )
end

if  mob_exists    ("baby"                   ) then
    dofile (mp .. "/baby.lua"               )
end

if  mob_exists    ("badger"                 ) then
    dofile (mp .. "/badger.lua"             )
end

if  mob_exists    ("bat"                    ) then
    dofile (mp .. "/bat.lua"                )
end

if  mob_exists    ("bear"                   ) then
    dofile (mp .. "/bear.lua"               )
end

if  mob_exists    ("bee"                    ) then
    dofile (mp .. "/bee.lua"                )
end

if  mob_exists    ("beetle"                ) then
    dofile (mp .. "/beetle.lua"            )
end

-- Filenames are a special case for this mob
if  lua_exists    ("bird"                   ) then
    dofile (mp .. "/bird.lua"               )
end

-- Filenames are a special case for this mob
if  lua_exists ("bom"                       ) and
    model_exists ("codermobs_bom.b3d"       ) then
    dofile (mp .. "/bom.lua"                )
end

if  mob_exists    ("fox"                    ) then
    dofile (mp .. "/fox.lua"                )
end

-- Filenames are a special case for this mob
if  lua_exists ("icebom"                    ) and
    model_exists ("codermobs_bom.b3d"       ) then
    dofile (mp .. "/icebom.lua"             )
end

if  mob_exists    ("bug"                    ) then
    dofile (mp .. "/bug.lua"                )
end

if  mob_exists    ("bunny"                  ) then
    dofile (mp .. "/bunny.lua"              )
end

if  mob_exists    ("butterfly"              ) then
    dofile (mp .. "/butterfly.lua"          )
end

if  mob_exists    ("cacodemon"              ) then
    dofile (mp .. "/cacodemon.lua"          )
end

if  mob_exists    ("camel"                  ) then
    dofile (mp .. "/camel.lua"              )
end

if  mob_exists    ("car"                    ) then
    dofile (mp .. "/car.lua"                )
end

if  mob_exists    ("caveman"                ) then
    dofile (mp .. "/caveman.lua"            )
end

if  mob_exists    ("cow"                    ) then
    dofile (mp .. "/cow.lua"                )
end

if  mob_exists    ("cyberdemon"             ) then
    dofile (mp .. "/cyberdemon.lua"         )
end

if  mob_exists    ("deer"                   ) then
    dofile (mp .. "/deer.lua"               )
end

if  mob_exists    ("denny"                  ) then
    dofile (mp .. "/denny.lua"              )
end

if  mob_exists    ("digibug"                ) then
    dofile (mp .. "/digibug.lua"            )
end

-- Filenames are a special case for this mob
if  lua_exists    ("dirt_monster"           ) then
    dofile (mp .. "/dirt_monster.lua"       )
end

if  mob_exists    ("dog"                    ) then
    dofile (mp .. "/dog.lua"                )
end

if  mob_exists    ("elephant"               ) then
    dofile (mp .. "/elephant.lua"           )
end

if  mob_exists    ("elk"                    ) then
    dofile (mp .. "/elk.lua"                )
end

if  mob_exists    ("farhorse"               ) then
    dofile (mp .. "/farhorse.lua"           )
end

if  mob_exists    ("flying_pig"             ) then
    dofile (mp .. "/flying_pig.lua"         )
end

if  mob_exists    ("ghost"                  ) then
    dofile (mp .. "/ghost.lua"              )
end

if  mob_exists    ("goat"                   ) then
    dofile (mp .. "/goat.lua"               )
end

if  mob_exists    ("hedgehog"               ) then
    dofile (mp .. "/hedgehog.lua"           )
end

if  mob_exists    ("hippo"                  ) then
    dofile (mp .. "/hippo.lua"              )
end

if  mob_exists    ("hotdog"                 ) then
    dofile (mp .. "/hotdog.lua"             )
end

if  mob_exists    ("jeraf"                  ) then
    dofile (mp .. "/jeraf.lua"              )
end

if  mob_exists    ("kangaroo"               ) then
    dofile (mp .. "/kangaroo.lua"           )
end

if  mob_exists    ("kitten"                 ) then
    dofile (mp .. "/kitten.lua"             )
end

if  mob_exists    ("lava_flan"              ) then
    dofile (mp .. "/lava_flan.lua"          )
end

if  mob_exists    ("lawyer"                 ) then
    dofile (mp .. "/lawyer.lua"             )
end

if  mob_exists    ("letterg"                ) then
    dofile (mp .. "/letterg.lua"            )
end

if  mob_exists    ("lostsoul"               ) then
    dofile (mp .. "/lostsoul.lua"           )
end

if  mob_exists    ("lott_spider"            ) then
    dofile (mp .. "/lott_spider.lua"        )
end

if  mob_exists    ("mammoth"                ) then
    dofile (mp .. "/mammoth.lua"            )
end

if  mob_exists    ("mcpig"                  ) then
    dofile (mp .. "/mcpig.lua"              )
end

if  mob_exists    ("mdskeleton"             ) then
    dofile (mp .. "/mdskeleton.lua"         )
end

if  mob_exists    ("oerkki"                 ) then
    dofile (mp .. "/oerkki.lua"             )
end

if  mob_exists    ("oldlady"                ) then
    dofile (mp .. "/oldlady.lua"            )
end

if  mob_exists    ("ostrich"                ) then
    dofile (mp .. "/ostrich.lua"            )
end

if  mob_exists    ("owl"                    ) then
    dofile (mp .. "/owl.lua"                )
end

if  mob_exists    ("panda"                  ) then
    dofile (mp .. "/panda.lua"              )
end

if  mob_exists    ("penguin"                ) then
    dofile (mp .. "/penguin.lua"            )
end

if  mob_exists    ("plane"                  ) then
    dofile (mp .. "/plane.lua"              )
end

if  mob_exists    ("polar_bear"             ) then
    dofile (mp .. "/polar_bear.lua"         )
end

if  mob_exists    ("rat"                    ) then
    dofile (mp .. "/rat.lua"                )
end

if  mob_exists    ("rat_better"             ) then
    dofile (mp .. "/rat_better.lua"         )
end

if  mob_exists    ("robotted"               ) then
    dofile (mp .. "/robotted.lua"           )
end

-- Filenames are a special case for this mob
if  lua_exists ("santa"                     ) and
    textu_exists ("codermobs_santa.png"     ) then
    dofile (mp .. "/santa.lua"              ) 
end

if  mob_exists    ("sheep"                  ) then
    dofile (mp .. "/sheep.lua"              )
end

if  mob_exists    ("silverfish"             ) then
    dofile (mp .. "/silverfish.lua"         )
end

if  mob_exists    ("snail"                  ) then
    dofile (mp .. "/snail.lua"              )
end

-- Filenames are a special case for this mob
if  lua_exists    ("snake_garter"           ) and
    model_exists ("codermobs_snake.x"       ) then
    dofile (mp .. "/snake_garter.lua"       )
end

-- Filenames are a special case for this mob
if  lua_exists    ("snake_ice"              ) and
    model_exists ("codermobs_snake.x"       ) then
    dofile (mp .. "/snake_ice.lua"          )
end

if  mob_exists    ("snowman"                ) then
    dofile (mp .. "/snowman.lua"            )
end

if  mob_exists    ("tiger"                  ) then
    dofile (mp .. "/tiger.lua"              )
end

if  mob_exists    ("tree_monster"           ) then
    dofile (mp .. "/tree_monster.lua"       )
end

if  mob_exists    ("trex"                   ) then
    dofile (mp .. "/trex.lua"               )
end

-- Filenames are a special case for this mob
if  lua_exists    ("vombie"                 ) then
    dofile (mp .. "/vombie.lua"             )
end

if  mob_exists    ("warthog"                ) then
    dofile (mp .. "/warthog.lua"            )
end

if  mob_exists    ("wolf"                   ) then
    dofile (mp .. "/wolf.lua"               )
end

-- Filenames are a special case for this mob
if  lua_exists    ("zebra"                  ) then
    dofile (mp .. "/zebra.lua"              )
end

-- Moon Cow should be defined after regular cow.
--
if enable_moontest and mob_exists ("cow") then
    dofile (mp .. "/mooncow.lua"            )
end

-- This is an object as opposed to a mob
if  lua_exists ("dungeon_spawner"           ) then
    dofile (mp .. "/dungeon_spawner.lua"    )
end

-- ===================================================================
-- End of file.
