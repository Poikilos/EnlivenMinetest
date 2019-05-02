codermobs  = {}
mobs_param = {}

codermobs.modname = minetest.get_current_modname()
codermobs.modpath = minetest.get_modpath (codermobs.modname)
local mp          = codermobs.modpath

local enable_moontest =
    minetest.setting_getbool ("enable_moon"     ) or
    minetest.setting_getbool ("enable_moontest" )

-- ===================================================================
-- These must come first.

dofile (mp .. "/globals.lua"          )
dofile (mp .. "/util.lua"             )
dofile (mp .. "/animal_materials.lua" )
dofile (mp .. "/vombie_flame.lua"     )

-- ===================================================================

dofile (mp .. "/badger.lua"       )
dofile (mp .. "/bat.lua"          )
dofile (mp .. "/bear.lua"         )
dofile (mp .. "/bee.lua"          )
dofile (mp .. "/beetle.lua"       )

dofile (mp .. "/bird.lua"         )
dofile (mp .. "/bug.lua"          )
dofile (mp .. "/bunny.lua"        )
dofile (mp .. "/butterfly.lua"    )
dofile (mp .. "/cacodemon.lua"    )

dofile (mp .. "/car.lua"          )
dofile (mp .. "/chicken.lua"      )
dofile (mp .. "/cow.lua"          )
dofile (mp .. "/cyberdemon.lua"   )

dofile (mp .. "/deer.lua"         )
dofile (mp .. "/dirt_monster.lua" )
dofile (mp .. "/dog.lua"          )
dofile (mp .. "/elephant.lua"     )
dofile (mp .. "/elk.lua"          )

dofile (mp .. "/farhorse.lua"     )
dofile (mp .. "/flying_pig.lua"   )
dofile (mp .. "/ghost.lua"        )
dofile (mp .. "/goat.lua"         )
dofile (mp .. "/hedgehog.lua"     )

dofile (mp .. "/jeraf.lua"        )
dofile (mp .. "/kitten.lua"       )
dofile (mp .. "/lava_flan.lua"    )
dofile (mp .. "/lostsoul.lua"     )
dofile (mp .. "/lott_spider.lua"  )

dofile (mp .. "/mammoth.lua"      )
dofile (mp .. "/mdskeleton.lua"   )
dofile (mp .. "/oerkki.lua"       )
dofile (mp .. "/ostrich.lua"      )
dofile (mp .. "/owl.lua"          )

dofile (mp .. "/panda.lua"        )
dofile (mp .. "/penguin.lua"      )
dofile (mp .. "/plane.lua"        )
dofile (mp .. "/polar_bear.lua"   )
dofile (mp .. "/rat.lua"          )

dofile (mp .. "/rat_better.lua"   )
dofile (mp .. "/sacreeper.lua"    )
dofile (mp .. "/santa.lua"        )
dofile (mp .. "/sheep.lua"        )
dofile (mp .. "/silverfish.lua"   )

dofile (mp .. "/snake_garter.lua" )
dofile (mp .. "/snake_ice.lua"    )
dofile (mp .. "/snowman.lua"      )
dofile (mp .. "/tree_monster.lua" )
dofile (mp .. "/vombie.lua"       )

dofile (mp .. "/warthog.lua"      )
dofile (mp .. "/wolf.lua"         )
dofile (mp .. "/zebra.lua"        )

dofile (mp .. "/baby_chick.lua"   )

-- Moon Cow must be defined after regular cow.

if enable_moontest then
    dofile (mp .. "/mooncow.lua")
end

-- ===================================================================
-- End of file.
