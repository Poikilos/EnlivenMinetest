#!/bin/bash

#two-line version:
# if [! -f CMakeLists.txt ]; then git clone https://github.com/MultiCraft/MultiCraft.git && cd MultiCraft || exit 1; fi
# cmake . -DOpenGL_GL_PREFERENCE=GLVND && make

me="$0"
RAN_FROM="`pwd`"
customExit() {
    echo
    echo
    echo "$me ERROR:"
    echo $1
    echo
    exit 1
}
usage() {
    cat <<END



    **************** $0 ****************

    Options:
    --what    (must be followed by a space)
              Specify building a directory other than
              $BUILD_WHAT_DEFAULT.

    1.) Build:
      $0
    2.)
      $0 --install

    If you want to install an existing binary version,
    Run this script from a directory that contains a
    $BUILD_WHAT_DEFAULT directory (If you want to use this location,
    '$srcRepo' would have to exist, otherwise specify an existing
    directory in $RAN_FROM
    after the "--what" option).


END
}

usageDie() {
    usage
    customExit $1
}

dieIfOnline() {
    echo
    echo
    if [ "@$OFFLINE" = "@false" ]; then
        echo "$me ERROR:"
        echo $1
        echo
        exit 1
    else
        echo "$me WARNING:"
        echo $1
        echo
    fi
}

if [ -z "$PREFIX" ]; then
    PREFIX=~/.local
fi

OFFLINE=false
INSTALL=false
UNINSTALL=false
CLEAN=false
GET_WHAT=false
USE_WHAT=false
for var in "$@"
do
    if [ "@$var" = "@--offline" ]; then
        OFFLINE=true
    elif [ "@$var" = "@--uninstall" ]; then
        UNINSTALL=true
    elif [ "@$var" = "@--install" ]; then
        INSTALL=true
    elif [ "@$var" = "@--clean" ]; then
        CLEAN=true
    elif [ "@$var" = "@--what" ]; then
        GET_WHAT=true
    elif [ "@$GET_WHAT" = "@true" ]; then
        if [ -d "$var" ]; then
            BUILD_WHAT="$var"
            USE_WHAT=true
        else
            customExit "'$var' is not a directory."
        fi
    else
        customExit "$var is not a valid option."
    fi
done

if [ "@$USE_WHAT" = "@true" ]; then
    OFFLINE=true
fi

BUILD_WHAT_DEFAULT=MultiCraft

# This is NOT a mistake (MultiCraft is the git username)...
GIT_REPOS_DIR="$HOME/Downloads/git/MultiCraft"
# ...so srcRepo should be MultiCraft/MultiCraft in this case
# (unless user ran script from a directory containing their own
# MultiCraft directory).

if [ -z "$BUILD_WHAT" ]; then
    BUILD_WHAT="$BUILD_WHAT_DEFAULT"
fi
srcRepo="`pwd`/$BUILD_WHAT"
if [ ! -d "$srcRepo" ]; then
    srcRepo="$GIT_REPOS_DIR/$BUILD_WHAT"
    if [ ! -d "$GIT_REPOS_DIR" ]; then
        mkdir -p "$GIT_REPOS_DIR" || customExit echo "mkdir -p '$GIT_REPOS_DIR' FAILED."
    fi
fi
echo "* Using $srcRepo..."
if [ ! -d /tmp/MultiCraft ]; then
    mkdir /tmp/MultiCraft || customExit echo "mkdir -p '/tmp/MultiCraft' FAILED."
fi
artifactsPath=/tmp/MultiCraft/src.txt
cat > $artifactsPath <<END
.git
.clang-format
.gitattributes
.gitignore
.gitmodules
.mailmap
.travis.yml
CMakeLists.txt
build
cmake
src
CMakeFiles
CPackConfig.cmake
CPackSourceConfig.cmake
CMakeDoxyfile.in
CMakeDoxygenDefaults.cmake
CMakeCache.txt
Makefile
cmake_install.cmake
END





srcBin=$srcRepo/bin
srcExe=$srcBin/MultiCraft
iconCaption=MultiCraft
dstShortcuts=$PREFIX/share/applications
dstShortcut=$dstShortcuts/MultiCraft.desktop
#dstPrograms="$HOME"
#DESTINATION="$dstPrograms/MultiCraft"
DESTINATION="$HOME/MultiCraft"
dstIcon=minetest
#tryIcon="$HOME/minetest/misc/minetest-xorg-icon-128.png"
tryIcon="$DESTINATION/misc/MultiCraft-xorg-icon-128.png"
dstBin=$DESTINATION/bin
dstExe=$dstBin/MultiCraft

if [ "@$CLEAN" = "@true" ]; then
    echo "ERROR: --clean is not implemented. See"
    echo "EnlivenMinetest/utilities/MultiCraft/manifests/cmake+make+bin.txt"
    echo "to clean manually."
    exit 1
fi

if [ "@$UNINSTALL" = "@true" ]; then
    echo
    prevDir="`pwd`"
    echo "Uninstalling $DESTINATION..."
    cd "$DESTINATION" || customExit echo "cd $DESTINATION FAILED."
    if [ ! -d /tmp/MultiCraft ]; then
        mkdir /tmp/MultiCraft || customExit echo "mkdir -p '/tmp/MultiCraft' FAILED."
    fi
    manifestPath=/tmp/MultiCraft/manifest.txt
cat > $manifestPath <<END
games/default/files/bluestone/mesecons_pistons/textures/mesecons_piston_pusher_front_sticky.png
games/default/files/bluestone/mesecons_pistons/textures/mesecons_piston_pusher_front.png
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_litecrash.ogg
games/default/files/farming/farming_addons/textures/farming_addons_potato_poisonous.png
games/default/files/farming/farming_addons/textures/farming_addons_melon_fruit_side.png
games/default/files/farming/farming_addons/textures/farming_addons_melon_fruit_top.png
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_gsharp2.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_fsharp2.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_dsharp2.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_csharp2.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_asharp2.ogg
games/default/files/bluestone/mesecons_delayer/textures/mesecons_delayer_sides_off.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_bottom_3.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_bottom_2.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_bottom_1.png
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_gsharp.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_fsharp.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_dsharp.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_csharp.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_asharp.ogg
games/default/files/bluestone/mesecons_delayer/textures/mesecons_delayer_sides_on.png
games/default/files/bluestone/mesecons_delayer/textures/mesecons_delayer_ends_off.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_front_3.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_front_2.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_front_1.png
games/default/files/farming/farming_addons/textures/farming_addons_carrot_golden.png
games/default/files/bluestone/mesecons_walllever/textures/jeija_wall_lever_sides.png
games/default/files/bluestone/mesecons_pistons/textures/mesecons_piston_on_front.png
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_snare.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_hihat.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_crash.ogg
games/default/files/bluestone/mesecons_delayer/textures/mesecons_delayer_ends_on.png
games/default/files/farming/farming_addons/textures/farming_addons_pumpkin_side.png
games/default/files/farming/farming_addons/textures/farming_addons_pumpkin_seed.png
games/default/files/farming/farming_addons/textures/farming_addons_potato_baked.png
games/default/files/farming/farming_addons/textures/farming_addons_melon_golden.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_side_3.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_side_2.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_side_1.png
games/default/files/bluestone/mesecons_walllever/textures/jeija_wall_lever_back.png
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_kick.ogg
games/default/files/bluestone/bluestone_torch/textures/bluestone_torch_animated.png
games/default/files/farming/farming_addons/textures/farming_addons_pumpkin_top.png
games/default/files/farming/farming_addons/textures/farming_addons_potato_seed.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_top_3.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_top_2.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_top_1.png
games/default/files/farming/farming_addons/textures/farming_addons_carrot_seed.png
games/default/files/bluestone/mesecons_walllever/textures/jeija_wall_lever_top.png
games/default/files/bluestone/mesecons_pistons/textures/mesecons_piston_bottom.png
games/default/files/farming/farming_addons/textures/farming_addons_melon_seed.png
games/default/files/farming/farming_addons/textures/farming_addons_corn_baked.png
games/default/files/farming/farming_addons/textures/farming_addons_cocoa_bean.png
games/default/files/bluestone/mesecons_walllever/textures/jeija_wall_lever_on.png
games/default/files/bluestone/mesecons_pistons/textures/mesecons_piston_right.png
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_g2.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_f2.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_e2.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_d2.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_c2.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_b2.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_a2.ogg
games/default/files/farming/farming_addons/textures/farming_addons_pumpkin_8.png
games/default/files/farming/farming_addons/textures/farming_addons_pumpkin_7.png
games/default/files/farming/farming_addons/textures/farming_addons_pumpkin_6.png
games/default/files/farming/farming_addons/textures/farming_addons_pumpkin_5.png
games/default/files/farming/farming_addons/textures/farming_addons_pumpkin_4.png
games/default/files/farming/farming_addons/textures/farming_addons_pumpkin_3.png
games/default/files/farming/farming_addons/textures/farming_addons_pumpkin_2.png
games/default/files/farming/farming_addons/textures/farming_addons_pumpkin_1.png
games/default/files/farming/farming_addons/textures/farming_addons_corn_seed.png
games/default/files/farming/farming_addons/textures/farming_addons_chocolate.png
games/default/files/bluestone/mesecons_solarpanel/textures/jeija_solar_panel.png
games/default/files/bluestone/mesecons_pistons/textures/mesecons_piston_left.png
games/default/files/bluestone/mesecons_pistons/textures/mesecons_piston_back.png
games/default/files/bluestone/mesecons_noteblock/textures/mesecons_noteblock.png
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_g.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_f.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_e.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_d.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_c.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_b.ogg
games/default/files/bluestone/mesecons_noteblock/sounds/mesecons_noteblock_a.ogg
games/default/files/bluestone/mesecons_delayer/textures/mesecons_delayer_off.png
games/default/files/farming/farming_addons/textures/farming_addons_potato_4.png
games/default/files/farming/farming_addons/textures/farming_addons_potato_3.png
games/default/files/farming/farming_addons/textures/farming_addons_potato_2.png
games/default/files/farming/farming_addons/textures/farming_addons_potato_1.png
games/default/files/farming/farming_addons/textures/farming_addons_hog_stew.png
games/default/files/farming/farming_addons/textures/farming_addons_carrot_4.png
games/default/files/farming/farming_addons/textures/farming_addons_carrot_3.png
games/default/files/farming/farming_addons/textures/farming_addons_carrot_2.png
games/default/files/farming/farming_addons/textures/farming_addons_carrot_1.png
games/default/files/bluestone/mesecons_pistons/textures/mesecons_piston_top.png
games/default/files/bluestone/mesecons_delayer/textures/mesecons_delayer_on.png
games/default/files/farming/farming_addons/textures/farming_addons_melon_8.png
games/default/files/farming/farming_addons/textures/farming_addons_melon_7.png
games/default/files/farming/farming_addons/textures/farming_addons_melon_6.png
games/default/files/farming/farming_addons/textures/farming_addons_melon_5.png
games/default/files/farming/farming_addons/textures/farming_addons_melon_4.png
games/default/files/farming/farming_addons/textures/farming_addons_melon_3.png
games/default/files/farming/farming_addons/textures/farming_addons_melon_2.png
games/default/files/farming/farming_addons/textures/farming_addons_melon_1.png
games/default/files/farming/farming_addons/textures/farming_addons_potato.png
games/default/files/farming/farming_addons/textures/farming_addons_corn_8.png
games/default/files/farming/farming_addons/textures/farming_addons_corn_7.png
games/default/files/farming/farming_addons/textures/farming_addons_corn_6.png
games/default/files/farming/farming_addons/textures/farming_addons_corn_5.png
games/default/files/farming/farming_addons/textures/farming_addons_corn_4.png
games/default/files/farming/farming_addons/textures/farming_addons_corn_3.png
games/default/files/farming/farming_addons/textures/farming_addons_corn_2.png
games/default/files/farming/farming_addons/textures/farming_addons_corn_1.png
games/default/files/farming/farming_addons/textures/farming_addons_cookie.png
games/default/files/farming/farming_addons/textures/farming_addons_carrot.png
games/default/files/default/textures/default_river_water_flowing_animated.png
games/default/files/default/schematics/snowy_small_pine_tree_from_sapling.mts
games/default/files/bluestone/mesecons_materials/textures/bluestone_block.png
games/default/files/bluestone/mesecons_button/sounds/mesecons_button_push.ogg
games/default/files/farming/farming_addons/textures/farming_addons_melon.png
games/default/files/default/textures/default_river_water_source_animated.png
games/default/files/default/schematics/emergent_jungle_tree_from_sapling.mts
games/default/files/bluestone/mesecons_button/sounds/mesecons_button_pop.ogg
games/default/files/bluestone/bluestone_lamp/textures/bluestone_lamp_off.png
games/default/files/farming/farming_addons/textures/farming_addons_corn.png
games/default/files/farming/farming_addons/textures/farming_addons_bowl.png
games/default/files/bluestone/mesecons_wires/textures/mesecons_wire_off.png
games/default/files/bluestone/mesecons_materials/textures/mesecons_glue.png
games/default/files/bluestone/bluestone_lamp/textures/bluestone_lamp_on.png
games/default/files/default/sounds/default_dig_oddly_breakable_by_hand.ogg
games/default/files/bluestone/mesecons_wires/textures/mesecons_wire_on.png
games/default/files/bluestone/mesecons_walllever/sounds/mesecons_lever.ogg
games/default/files/bluestone/bluestone_torch/textures/bluestone_torch.png
games/default/files/3d_armor/textures/3d_armor_inv_chestplate_leather.png
games/default/files/3d_armor/textures/3d_armor_inv_chestplate_diamond.png
games/default/files/mobs/mobs_monster/textures/mobs_spider_small_egg.png
games/default/files/farming/farming/textures/farming_tool_diamondhoe.png
games/default/files/bluestone/mesecons_wires/textures/bluestone_dust.png
games/default/files/bluestone/mesecons_pistons/sounds/piston_retract.ogg
games/default/files/mobs/mobs_animal/textures/mobs_sheep_dark_green.png
games/default/files/default/textures/default_water_flowing_animated.png
games/default/files/default/schematics/snowy_pine_tree_from_sapling.mts
games/default/files/default/schematics/small_pine_tree_from_sapling.mts
games/default/files/bluestone/mesecons_pistons/sounds/piston_extend.ogg
games/default/files/3d_armor/textures/3d_armor_inv_leggings_leather.png
games/default/files/3d_armor/textures/3d_armor_inv_leggings_diamond.png
games/default/files/3d_armor/textures/3d_armor_inv_chestplate_steel.png
games/default/files/3d_armor/textures/3d_armor_inv_chestplate_chain.png
games/default/files/workbench/textures/formspec_workbench_creating.png
games/default/files/workbench/textures/formspec_workbench_crafting.png
games/default/files/mobs/mobs_redo/textures/mobs_chicken_egg_fried.png
games/default/files/mobs/mobs_animal/textures/mobs_sheep_dark_grey.png
games/default/files/mobs/mobs_animal/textures/mobs_kitten_splotchy.png
games/default/files/mobs/mobs_animal/textures/mobs_chicken_egg_inv.png
games/default/files/farming/farming/textures/farming_tool_stonehoe.png
games/default/files/farming/farming/textures/farming_tool_steelhoe.png
games/default/files/default/textures/default_water_source_animated.png
games/default/files/default/textures/default_lava_flowing_animated.png
games/default/files/3d_armor/textures/3d_armor_inv_chestplate_gold.png
games/default/files/mobs/mobs_monster/textures/mobs_spider_orange.png
games/default/files/mobs/mobs_animal/textures/mobs_kitten_striped.png
games/default/files/farming/farming/textures/farming_tool_woodhoe.png
games/default/files/farming/farming/textures/farming_tool_goldhoe.png
games/default/files/default/textures/default_quartz_chiseled_side.png
games/default/files/default/textures/default_lava_source_animated.png
games/default/files/default/textures/default_furnace_front_active.png
games/default/files/3d_armor/textures/3d_armor_inv_leggings_steel.png
games/default/files/3d_armor/textures/3d_armor_inv_leggings_chain.png
games/default/files/3d_armor/textures/3d_armor_inv_helmet_leather.png
games/default/files/3d_armor/textures/3d_armor_inv_helmet_diamond.png
games/default/files/3d_armor/textures/3d_armor_chestplate_leather.png
games/default/files/3d_armor/textures/3d_armor_chestplate_diamond.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_woman_shirt3.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_woman_shirt2.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_woman_shirt1.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_woman_pants3.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_woman_pants2.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_woman_pants1.png
games/default/files/mobs/mobs_animal/textures/mobs_sheep_magenta.png
games/default/files/mobs/mobs_animal/textures/mobs_parrot_yellow.png
games/default/files/mobs/mobs_animal/textures/mobs_kitten_ginger.png
games/default/files/mobs/mobs_animal/textures/mobs_chicken_brown.png
games/default/files/mobs/mobs_animal/textures/mobs_chicken_black.png
games/default/files/default/textures/default_redsandstone_smooth.png
games/default/files/default/textures/default_redsandstone_normal.png
games/default/files/default/textures/default_redsandstone_carved.png
games/default/files/default/textures/default_redsandstone_bottom.png
games/default/files/default/textures/default_quartz_chiseled_top.png
games/default/files/default/textures/default_quartz_block_bottom.png
games/default/files/3d_armor/textures/3d_armor_inv_leggings_gold.png
games/default/files/3d_armor/textures/3d_armor_inv_boots_leather.png
games/default/files/3d_armor/textures/3d_armor_inv_boots_diamond.png
games/default/files/workbench/textures/formspec_workbench_anvil.png
games/default/files/player/pep/textures/pep_speedreset_particle.png
games/default/files/player/pep/textures/pep_speedminus_particle.png
games/default/files/player/pep/textures/pep_manaregen2_particle.png
games/default/files/mobs/mobs_redo/textures/mobs_chicken_cooked.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_woman_hair3.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_woman_hair2.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_woman_hair1.png
games/default/files/mobs/mobs_monster/textures/mobs_spider_grey.png
games/default/files/mobs/mobs_monster/textures/mobs_monster_egg.png
games/default/files/mobs/mobs_monster/sounds/mobs_zombie_attack.ogg
games/default/files/mobs/mobs_animal/textures/mobs_sheep_yellow.png
games/default/files/mobs/mobs_animal/textures/mobs_sheep_violet.png
games/default/files/mobs/mobs_animal/textures/mobs_sheep_shaved.png
games/default/files/mobs/mobs_animal/textures/mobs_sheep_orange.png
games/default/files/mobs/mobs_animal/textures/mobs_parrot_green.png
games/default/files/mobs/mobs_animal/textures/mobs_kitten_sandy.png
games/default/files/farming/farming/textures/farming_wheat_seed.png
games/default/files/farming/farming/textures/farming_straw_side.png
games/default/files/default/textures/default_tool_diamondshovel.png
games/default/files/default/textures/default_stonebrick_cracked.png
games/default/files/default/textures/default_quartz_pillar_side.png
games/default/files/default/schematics/jungle_tree_from_sapling.mts
games/default/files/default/schematics/acacia_tree_from_sapling.mts
games/default/files/carts/textures/carts_rail_t_junction_dtc_on.png
games/default/files/3d_armor/textures/3d_armor_leggings_leather.png
games/default/files/3d_armor/textures/3d_armor_leggings_diamond.png
games/default/files/3d_armor/textures/3d_armor_inv_helmet_steel.png
games/default/files/3d_armor/textures/3d_armor_inv_helmet_chain.png
games/default/files/3d_armor/textures/3d_armor_chestplate_steel.png
games/default/files/3d_armor/textures/3d_armor_chestplate_chain.png
games/default/files/player/pep/textures/pep_speedplus_particle.png
games/default/files/player/pep/textures/pep_manaregen_particle.png
games/default/files/player/pep/textures/pep_jumpreset_particle.png
games/default/files/player/pep/textures/pep_jumpminus_particle.png
games/default/files/player/pep/textures/pep_gravreset_particle.png
games/default/files/mobs/mobs_redo/textures/mobs_rabbit_cooked.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_man_shirt3.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_man_shirt2.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_man_shirt1.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_man_pants3.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_man_pants2.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_man_pants1.png
games/default/files/mobs/mobs_monster/textures/mobs_spider_egg.png
games/default/files/mobs/mobs_monster/sounds/mobs_zombie_death.ogg
games/default/files/mobs/mobs_animal/textures/mobs_sheep_white.png
games/default/files/mobs/mobs_animal/textures/mobs_sheep_green.png
games/default/files/mobs/mobs_animal/textures/mobs_sheep_brown.png
games/default/files/mobs/mobs_animal/textures/mobs_sheep_black.png
games/default/files/mobs/mobs_animal/textures/mobs_bunny_white.png
games/default/files/mobs/mobs_animal/textures/mobs_bunny_brown.png
games/default/files/farming/farming/textures/farming_straw_top.png
games/default/files/default/textures/default_tool_fishing_pole.png
games/default/files/default/textures/default_tool_diamondsword.png
games/default/files/default/textures/default_stonebrick_carved.png
games/default/files/default/textures/default_quartz_pillar_top.png
games/default/files/default/textures/default_quartz_block_side.png
games/default/files/default/textures/default_mineral_bluestone.png
games/default/files/default/schematics/birch_tree_from_sapling.mts
games/default/files/default/schematics/apple_tree_from_sapling.mts
games/default/files/compatibility/textures/gui_hotbar_selected.png
games/default/files/3d_armor/textures/3d_armor_inv_helmet_gold.png
games/default/files/3d_armor/textures/3d_armor_inv_boots_steel.png
games/default/files/3d_armor/textures/3d_armor_inv_boots_chain.png
games/default/files/3d_armor/textures/3d_armor_chestplate_gold.png
games/default/files/player/pep/textures/pep_jumpplus_particle.png
games/default/files/mobs/mobs_redo/textures/mobs_rotten_flesh.png
games/default/files/mobs/mobs_redo/textures/mobs_cheese_wield.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_woman_egg.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_man_hair3.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_man_hair2.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_man_hair1.png
games/default/files/mobs/mobs_animal/textures/mobs_sheep_pink.png
games/default/files/mobs/mobs_animal/textures/mobs_sheep_grey.png
games/default/files/mobs/mobs_animal/textures/mobs_sheep_cyan.png
games/default/files/mobs/mobs_animal/textures/mobs_sheep_blue.png
games/default/files/mobs/mobs_animal/textures/mobs_pig_motley.png
games/default/files/mobs/mobs_animal/textures/mobs_parrot_red.png
games/default/files/mobs/mobs_animal/textures/mobs_parrot_egg.png
games/default/files/mobs/mobs_animal/textures/mobs_kitten_egg.png
games/default/files/mobs/mobs_animal/textures/mobs_bunny_grey.png
games/default/files/mobs/mobs_animal/textures/mobs_bunny_evil.png
games/default/files/mobs/mobs_animal/models/mobs_sheep_shaved.b3d
games/default/files/flowers/textures/flowers_dandelion_yellow.png
games/default/files/farming/farming/textures/farming_soil_wet.png
games/default/files/default/textures/default_tool_stoneshovel.png
games/default/files/default/textures/default_tool_steelshovel.png
games/default/files/default/textures/default_tool_diamondpick.png
games/default/files/default/textures/default_stonebrick_mossy.png
games/default/files/default/textures/default_sandstone_smooth.png
games/default/files/default/textures/default_sandstone_normal.png
games/default/files/default/textures/default_sandstone_bottom.png
games/default/files/default/textures/default_redsandstone_top.png
games/default/files/default/textures/default_quartz_block_top.png
games/default/files/default/sounds/default_place_node_metal.2.ogg
games/default/files/default/sounds/default_place_node_metal.1.ogg
games/default/files/default/schematics/pine_tree_from_sapling.mts
games/default/files/carts/textures/carts_rail_straight_dtc_on.png
games/default/files/carts/textures/carts_rail_crossing_dtc_on.png
games/default/files/bluestone/mesecons_pressureplates/depends.txt
games/default/files/3d_armor/textures/3d_armor_leggings_steel.png
games/default/files/3d_armor/textures/3d_armor_leggings_chain.png
games/default/files/3d_armor/textures/3d_armor_inv_boots_gold.png
games/default/files/3d_armor/textures/3d_armor_helmet_leather.png
games/default/files/3d_armor/textures/3d_armor_helmet_diamond.png
games/default/files/workbench/textures/workbench_button_back.png
games/default/files/mobs/mobs_redo/textures/mobs_rabbit_hide.png
games/default/files/mobs/mobs_redo/textures/mobs_pork_cooked.png
games/default/files/mobs/mobs_redo/textures/mobs_egg_overlay.png
games/default/files/mobs/mobs_redo/textures/mobs_chicken_raw.png
games/default/files/mobs/mobs_redo/textures/mobs_chicken_egg.png
games/default/files/mobs/mobs_redo/textures/mobs_cheeseblock.png
games/default/files/mobs/mobs_monster/textures/mobs_skeleton.png
games/default/files/mobs/mobs_monster/sounds/mobs_zombie_hit.ogg
games/default/files/mobs/mobs_animal/textures/mobs_sheep_red.png
games/default/files/mobs/mobs_animal/textures/mobs_pig_black.png
games/default/files/mobs/mobs_animal/sounds/mobs_wolf_attack.ogg
games/default/files/mobs/mobs_animal/sounds/mobs_sheep_angry.ogg
games/default/files/itemframes/textures/itemframe_background.png
games/default/files/farming/farming/textures/farming_wheat_8.png
games/default/files/farming/farming/textures/farming_wheat_7.png
games/default/files/farming/farming/textures/farming_wheat_6.png
games/default/files/farming/farming/textures/farming_wheat_5.png
games/default/files/farming/farming/textures/farming_wheat_4.png
games/default/files/farming/farming/textures/farming_wheat_3.png
games/default/files/farming/farming/textures/farming_wheat_2.png
games/default/files/farming/farming/textures/farming_wheat_1.png
games/default/files/doors/textures/doors_trapdoor_steel_side.png
games/default/files/default/textures/default_tool_woodshovel.png
games/default/files/default/textures/default_tool_stonesword.png
games/default/files/default/textures/default_tool_steelsword.png
games/default/files/default/textures/default_tool_goldshovel.png
games/default/files/default/textures/default_tool_diamondaxe.png
games/default/files/default/textures/default_mineral_emerald.png
games/default/files/default/textures/default_mineral_diamond.png
games/default/files/default/textures/default_furnace_fire_fg.png
games/default/files/default/textures/default_furnace_fire_bg.png
games/default/files/default/textures/default_chest_front_big.png
games/default/files/default/textures/default_acacia_tree_top.png
games/default/files/default/sounds/default_place_node_hard.2.ogg
games/default/files/default/sounds/default_place_node_hard.1.ogg
games/default/files/default/sounds/default_gravel_footstep.4.ogg
games/default/files/default/sounds/default_gravel_footstep.3.ogg
games/default/files/default/sounds/default_gravel_footstep.2.ogg
games/default/files/default/sounds/default_gravel_footstep.1.ogg
games/default/files/default/sounds/default_dig_dig_immediate.ogg
games/default/files/carts/textures/carts_rail_t_junction_pwr.png
games/default/files/carts/textures/carts_rail_t_junction_dtc.png
games/default/files/carts/textures/carts_rail_t_junction_brk.png
games/default/files/3d_armor/textures/3d_armor_leggings_gold.png
games/default/files/3d_armor/textures/3d_armor_boots_leather.png
games/default/files/3d_armor/textures/3d_armor_boots_diamond.png
games/default/files/wallet/textures/cobblestonemossy_wallet.png
games/default/files/player/pep/textures/pep_regen2_particle.png
games/default/files/player/pep/textures/pep_breath_particle.png
games/default/files/mobs/mobs_redo/textures/mobs_rabbit_raw.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_man_egg.png
games/default/files/mobs/mobs_animal/textures/mobs_bear_egg.png
games/default/files/mobs/mobs_animal/sounds/mobs_bear_angry.ogg
games/default/files/fire/textures/fire_basic_flame_animated.png
games/default/files/farming/farming/textures/farming_string.png
games/default/files/default/textures/default_wood_fencegate.png
games/default/files/default/textures/default_torch_animated.png
games/default/files/default/textures/default_tool_woodsword.png
games/default/files/default/textures/default_tool_stonepick.png
games/default/files/default/textures/default_tool_steelpick.png
games/default/files/default/textures/default_tool_goldsword.png
games/default/files/default/textures/default_quartz_crystal.png
games/default/files/default/textures/default_jungletree_top.png
games/default/files/default/textures/default_glowstone_dust.png
games/default/files/default/textures/default_dry_grass_side.png
games/default/files/default/textures/default_chest_side_big.png
games/default/files/default/textures/default_button_pressed.png
games/default/files/default/textures/default_birch_tree_top.png
games/default/files/default/textures/default_acacia_sapling.png
games/default/files/default/sounds/default_water_footstep.3.ogg
games/default/files/default/sounds/default_water_footstep.2.ogg
games/default/files/default/sounds/default_water_footstep.1.ogg
games/default/files/default/sounds/default_metal_footstep.3.ogg
games/default/files/default/sounds/default_metal_footstep.2.ogg
games/default/files/default/sounds/default_metal_footstep.1.ogg
games/default/files/default/sounds/default_grass_footstep.3.ogg
games/default/files/default/sounds/default_grass_footstep.2.ogg
games/default/files/default/sounds/default_grass_footstep.1.ogg
games/default/files/default/schematics/emergent_jungle_tree.mts
games/default/files/carts/textures/carts_rail_t_junction_ss.png
games/default/files/carts/textures/carts_rail_t_junction_cp.png
games/default/files/carts/textures/carts_rail_curved_dtc_on.png
games/default/files/3d_armor/textures/3d_armor_helmet_steel.png
games/default/files/3d_armor/textures/3d_armor_helmet_chain.png
games/default/files/player/pep/textures/pep_regen_particle.png
games/default/files/player/pep/textures/pep_grav0_particle.png
games/default/files/mobs/mobs_redo/textures/mobs_protector.png
games/default/files/mobs/mobs_npc/textures/mobs_trader_egg.png
games/default/files/mobs/mobs_npc/textures/formspec_trader.png
games/default/files/mobs/mobs_monster/textures/zombie_head.png
games/default/files/mobs/mobs_monster/textures/mobs_zombie.png
games/default/files/mobs/mobs_monster/textures/mobs_spider.png
games/default/files/mobs/mobs_monster/sounds/mobs_zombie.3.ogg
games/default/files/mobs/mobs_monster/sounds/mobs_zombie.2.ogg
games/default/files/mobs/mobs_monster/sounds/mobs_zombie.1.ogg
games/default/files/mobs/mobs_monster/sounds/mobs_skeleton.ogg
games/default/files/mobs/mobs_animal/textures/mobs_pig_egg.png
games/default/files/mobs/mobs_animal/textures/mobs_cow_egg.png
games/default/files/mobs/mobs_animal/textures/mobs_chicken.png
games/default/files/mobs/mobs_animal/sounds/mobs_pig_angry.ogg
games/default/files/flowers/textures/3dmushrooms_brown_inv.png
games/default/files/farming/farming/textures/farming_wheat.png
games/default/files/farming/farming/textures/farming_flour.png
games/default/files/farming/farming/textures/farming_bread.png
games/default/files/default/textures/hunger_statbar_poisen.png
games/default/files/default/textures/default_tool_woodpick.png
games/default/files/default/textures/default_tool_stoneaxe.png
games/default/files/default/textures/default_tool_steelaxe.png
games/default/files/default/textures/default_tool_goldpick.png
games/default/files/default/textures/default_sugarcane_inv.png
games/default/files/default/textures/default_sandstone_top.png
games/default/files/default/textures/default_pine_tree_top.png
games/default/files/default/textures/default_mineral_lapis.png
games/default/files/default/textures/default_junglesapling.png
games/default/files/default/textures/default_hardened_clay.png
games/default/files/default/textures/default_furnace_front.png
games/default/files/default/textures/default_emerald_block.png
games/default/files/default/textures/default_dry_tallgrass.png
games/default/files/default/textures/default_diamond_block.png
games/default/files/default/textures/default_chest_top_big.png
games/default/files/default/textures/default_charcoal_lump.png
games/default/files/default/textures/default_cactus_bottom.png
games/default/files/default/textures/default_birch_sapling.png
games/default/files/default/textures/default_acacia_leaves.png
games/default/files/default/sounds/default_wood_footstep.2.ogg
games/default/files/default/sounds/default_wood_footstep.1.ogg
games/default/files/default/sounds/default_snow_footstep.5.ogg
games/default/files/default/sounds/default_snow_footstep.4.ogg
games/default/files/default/sounds/default_snow_footstep.3.ogg
games/default/files/default/sounds/default_snow_footstep.2.ogg
games/default/files/default/sounds/default_snow_footstep.1.ogg
games/default/files/default/sounds/default_sand_footstep.2.ogg
games/default/files/default/sounds/default_sand_footstep.1.ogg
games/default/files/default/sounds/default_hard_footstep.3.ogg
games/default/files/default/sounds/default_hard_footstep.2.ogg
games/default/files/default/sounds/default_hard_footstep.1.ogg
games/default/files/default/sounds/default_dirt_footstep.2.ogg
games/default/files/default/sounds/default_dirt_footstep.1.ogg
games/default/files/carts/textures/carts_rail_straight_pwr.png
games/default/files/carts/textures/carts_rail_straight_dtc.png
games/default/files/carts/textures/carts_rail_straight_brk.png
games/default/files/carts/textures/carts_rail_crossing_pwr.png
games/default/files/carts/textures/carts_rail_crossing_dtc.png
games/default/files/carts/textures/carts_rail_crossing_brk.png
games/default/files/bonusbox/textures/chest_open_front_two.png
games/default/files/bluestone/mesecons_pressureplates/init.lua
games/default/files/3d_armor/textures/3d_armor_helmet_gold.png
games/default/files/3d_armor/textures/3d_armor_boots_steel.png
games/default/files/3d_armor/textures/3d_armor_boots_chain.png
games/default/files/vessels/textures/vessels_glass_bottle.png
games/default/files/player/pep/textures/pep_mole_particle.png
games/default/files/mobs/mobs_redo/textures/mobs_pork_raw.png
games/default/files/mobs/mobs_redo/textures/mobs_meat_raw.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_woman.png
games/default/files/farming/farming/textures/farming_soil.png
games/default/files/doors/textures/doors_item_jungle_wood.png
games/default/files/doors/textures/doors_item_acacia_wood.png
games/default/files/doors/textures/doors_door_jungle_wood.png
games/default/files/doors/textures/doors_door_acacia_wood.png
games/default/files/default/textures/formspec_chest_large.png
games/default/files/default/textures/default_tool_woodaxe.png
games/default/files/default/textures/default_tool_goldaxe.png
games/default/files/default/textures/default_pine_sapling.png
games/default/files/default/textures/default_pine_needles.png
games/default/files/default/textures/default_mineral_iron.png
games/default/files/default/textures/default_mineral_gold.png
games/default/files/default/textures/default_mineral_coal.png
games/default/files/default/textures/default_jungleleaves.png
games/default/files/default/textures/default_item_pressed.png
games/default/files/default/textures/default_glass_detail.png
games/default/files/default/textures/default_furnace_side.png
games/default/files/default/textures/default_book_written.png
games/default/files/default/textures/default_birch_leaves.png
games/default/files/default/sounds/default_glass_footstep.ogg
games/default/files/carts/textures/carts_rail_straight_ss.png
games/default/files/carts/textures/carts_rail_straight_cp.png
games/default/files/carts/textures/carts_rail_crossing_ss.png
games/default/files/carts/textures/carts_rail_crossing_cp.png
games/default/files/bonusbox/textures/chest_open_side_two.png
games/default/files/bonusbox/textures/chest_open_back_two.png
games/default/files/bluestone/mesecons_solarpanel/depends.txt
games/default/files/3d_armor/textures/3d_armor_statbar_fg.png
games/default/files/3d_armor/textures/3d_armor_statbar_bg.png
games/default/files/3d_armor/textures/3d_armor_boots_gold.png
games/default/files/mobs/mobs_redo/textures/mobs_nametag.png
games/default/files/mobs/mobs_redo/textures/mobs_leather.png
games/default/files/mobs/mobs_monster/sounds/mobs_spider.ogg
games/default/files/mobs/mobs_monster/models/mobs_zombie.b3d
games/default/files/mobs/mobs_monster/models/mobs_spider.b3d
games/default/files/mobs/mobs_animal/textures/mobs_sheep.png
games/default/files/mobs/mobs_animal/sounds/mobs_chicken.ogg
games/default/files/mobs/mobs_animal/models/mobs_chicken.b3d
games/default/files/flowers/textures/flowers_oxeye_daisy.png
games/default/files/flowers/textures/3dmushrooms_red_inv.png
games/default/files/doors/textures/doors_item_birch_wood.png
games/default/files/doors/textures/doors_door_birch_wood.png
games/default/files/default/textures/default_stone_brick.png
games/default/files/default/textures/default_steel_ingot.png
games/default/files/default/textures/default_steel_block.png
games/default/files/default/textures/default_river_water.png
games/default/files/default/textures/default_mossycobble.png
games/default/files/default/textures/default_liquid_drop.png
games/default/files/default/textures/default_lapis_block.png
games/default/files/default/textures/default_ladder_wood.png
games/default/files/default/textures/default_junglegrass.png
games/default/files/default/textures/default_furnace_top.png
games/default/files/default/textures/default_fish_cooked.png
games/default/files/default/textures/default_chest_front.png
games/default/files/default/textures/default_cactus_side.png
games/default/files/default/textures/default_acacia_wood.png
games/default/files/default/textures/default_acacia_tree.png
games/default/files/default/sounds/default_wool_footstep.ogg
games/default/files/default/sounds/default_tool_breaks.3.ogg
games/default/files/default/sounds/default_tool_breaks.2.ogg
games/default/files/default/sounds/default_tool_breaks.1.ogg
games/default/files/default/sounds/default_break_glass.3.ogg
games/default/files/default/sounds/default_break_glass.2.ogg
games/default/files/default/sounds/default_break_glass.1.ogg
games/default/files/carts/textures/carts_rail_t_junction.png
games/default/files/carts/textures/carts_rail_curved_pwr.png
games/default/files/carts/textures/carts_rail_curved_dtc.png
games/default/files/carts/textures/carts_rail_curved_brk.png
games/default/files/bluestone/mesecons_walllever/depends.txt
games/default/files/bluestone/mesecons_noteblock/depends.txt
games/default/files/bluestone/mesecons_materials/depends.txt
games/default/files/workbench/textures/workbench_hammer.png
games/default/files/vessels/textures/vessels_shelf_slot.png
games/default/files/mobs/mobs_redo/textures/mobs_shears.png
games/default/files/mobs/mobs_redo/textures/mobs_cobweb.png
games/default/files/mobs/mobs_redo/textures/mobs_cheese.png
games/default/files/mobs/mobs_npc/textures/mobs_trader3.png
games/default/files/mobs/mobs_npc/textures/mobs_trader2.png
games/default/files/mobs/mobs_npc/textures/mobs_trader1.png
games/default/files/mobs/mobs_npc/textures/mobs_npc_man.png
games/default/files/mobs/mobs_animal/textures/mobs_wolf.png
games/default/files/mobs/mobs_animal/textures/mobs_cow3.png
games/default/files/mobs/mobs_animal/textures/mobs_cow2.png
games/default/files/mobs/mobs_animal/textures/mobs_bear.png
games/default/files/mobs/mobs_animal/sounds/mobs_kitten.ogg
games/default/files/mobs/mobs_animal/models/mobs_parrot.b3d
games/default/files/mobs/mobs_animal/models/mobs_kitten.b3d
games/default/files/fire/sounds/fire_extinguish_flame.3.ogg
games/default/files/fire/sounds/fire_extinguish_flame.2.ogg
games/default/files/fire/sounds/fire_extinguish_flame.1.ogg
games/default/files/doors/textures/doors_trapdoor_steel.png
games/default/files/doors/textures/doors_item_pine_wood.png
games/default/files/doors/textures/doors_door_pine_wood.png
games/default/files/doors/sounds/doors_steel_door_close.ogg
games/default/files/default/textures/formspec_inventory.png
games/default/files/default/textures/default_wood_fence.png
games/default/files/default/textures/default_slimeblock.png
games/default/files/default/textures/default_quartz_ore.png
games/default/files/default/textures/default_junglewood.png
games/default/files/default/textures/default_jungletree.png
games/default/files/default/textures/default_ice_packed.png
games/default/files/default/textures/default_grass_side.png
games/default/files/default/textures/default_gold_ingot.png
games/default/files/default/textures/default_gold_block.png
games/default/files/default/textures/default_coal_block.png
games/default/files/default/textures/default_clay_brick.png
games/default/files/default/textures/default_chest_side.png
games/default/files/default/textures/default_cactus_top.png
games/default/files/default/textures/default_birch_wood.png
games/default/files/default/textures/default_birch_tree.png
games/default/files/default/textures/default_background.png
games/default/files/default/textures/default_apple_gold.png
games/default/files/default/sounds/default_place_node.3.ogg
games/default/files/default/sounds/default_place_node.2.ogg
games/default/files/default/sounds/default_place_node.1.ogg
games/default/files/carts/textures/carts_rail_curved_ss.png
games/default/files/carts/textures/carts_rail_curved_cp.png
games/default/files/bonusbox/textures/chest_open_bottom.png
games/default/files/workbench/textures/workbench_sides.png
games/default/files/workbench/textures/workbench_front.png
games/default/files/workbench/textures/workbench_anvil.png
games/default/files/wallet/textures/cobblestone_wallet.png
games/default/files/sethome/textures/creative_home_set.png
games/default/files/player/pep/textures/pep_speedreset.png
games/default/files/player/pep/textures/pep_speedminus.png
games/default/files/player/pep/textures/pep_manaregen2.png
games/default/files/mobs/mobs_npc/textures/mobs_trader.png
games/default/files/mobs/mobs_animal/textures/mobs_pig.png
games/default/files/mobs/mobs_animal/textures/mobs_dog.png
games/default/files/mobs/mobs_animal/textures/mobs_cow.png
games/default/files/mobs/mobs_animal/sounds/mobs_sheep.ogg
games/default/files/mobs/mobs_animal/models/mobs_sheep.b3d
games/default/files/mobs/mobs_animal/models/mobs_bunny.b3d
games/default/files/flowers/textures/flowers_waterlily.png
games/default/files/doors/textures/doors_trapdoor_side.png
games/default/files/doors/sounds/doors_steel_door_open.ogg
games/default/files/doors/sounds/doors_fencegate_close.ogg
games/default/files/default/textures/hunger_statbar_fg.png
games/default/files/default/textures/hunger_statbar_bg.png
games/default/files/default/textures/default_tallgrass.png
games/default/files/default/textures/default_sugarcane.png
games/default/files/default/textures/default_snow_side.png
games/default/files/default/textures/default_pine_wood.png
games/default/files/default/textures/default_pine_tree.png
games/default/files/default/textures/default_gunpowder.png
games/default/files/default/textures/default_glowstone.png
games/default/files/default/textures/default_dry_shrub.png
games/default/files/default/textures/default_dry_grass.png
games/default/files/default/textures/default_coal_lump.png
games/default/files/default/textures/default_clay_lump.png
games/default/files/default/textures/default_chest_top.png
games/default/files/default/textures/default_bookshelf.png
games/default/files/default/sounds/default_dug_metal.2.ogg
games/default/files/default/sounds/default_dug_metal.1.ogg
games/default/files/default/sounds/default_dig_crumbly.ogg
games/default/files/default/sounds/default_cool_lava.3.ogg
games/default/files/default/sounds/default_cool_lava.2.ogg
games/default/files/default/sounds/default_cool_lava.1.ogg
games/default/files/default/schematics/small_pine_tree.mts
games/default/files/carts/textures/carts_rail_straight.png
games/default/files/carts/textures/carts_rail_crossing.png
games/default/files/bucket/textures/bucket_river_water.png
games/default/files/bonusbox/textures/chest_open_front.png
games/default/files/bluestone/mesecons_solarpanel/textures
games/default/files/bluestone/mesecons_solarpanel/init.lua
games/default/files/bluestone/mesecons_pistons/depends.txt
games/default/files/bluestone/mesecons_delayer/depends.txt
games/default/files/sethome/textures/creative_home_go.png
games/default/files/player/pep/textures/pep_speedplus.png
games/default/files/player/pep/textures/pep_manaregen.png
games/default/files/player/pep/textures/pep_jumpreset.png
games/default/files/player/pep/textures/pep_jumpminus.png
games/default/files/player/pep/textures/pep_gravreset.png
games/default/files/mobs/mobs_redo/textures/mobs_meat.png
games/default/files/mobs/mobs_animal/sounds/mobs_bear.ogg
games/default/files/mobs/mobs_animal/models/mobs_bear.b3d
games/default/files/flowerpot/textures/flowerpot_item.png
games/default/files/doors/sounds/doors_fencegate_open.ogg
games/default/files/default/textures/formspec_furnace.png
games/default/files/default/textures/default_tree_top.png
games/default/files/default/textures/default_snowball.png
games/default/files/default/textures/default_red_sand.png
games/default/files/default/textures/default_player2d.png
games/default/files/default/textures/default_obsidian.png
games/default/files/default/sounds/item_drop_pickup.4.ogg
games/default/files/default/sounds/item_drop_pickup.3.ogg
games/default/files/default/sounds/item_drop_pickup.2.ogg
games/default/files/default/sounds/item_drop_pickup.1.ogg
games/default/files/default/sounds/default_item_smoke.ogg
games/default/files/default/sounds/default_dug_node.2.ogg
games/default/files/default/sounds/default_dug_node.1.ogg
games/default/files/default/sounds/default_dig_snappy.ogg
games/default/files/default/sounds/default_dig_cracky.ogg
games/default/files/default/sounds/default_dig_choppy.ogg
games/default/files/compatibility/textures/gui_hotbar.png
games/default/files/bonusbox/textures/chest_open_side.png
games/default/files/bonusbox/textures/chest_open_back.png
games/default/files/bluestone/mesecons_walllever/textures
games/default/files/bluestone/mesecons_walllever/init.lua
games/default/files/bluestone/mesecons_noteblock/textures
games/default/files/bluestone/mesecons_noteblock/init.lua
games/default/files/bluestone/mesecons_materials/textures
games/default/files/bluestone/mesecons_materials/init.lua
games/default/files/bluestone/mesecons_button/depends.txt
games/default/files/bluestone/bluestone_torch/depends.txt
games/default/files/workbench/textures/workbench_top.png
games/default/files/workbench/textures/workbench_saw.png
games/default/files/workbench/models/workbench_slope.obj
games/default/files/player/pep/textures/pep_jumpplus.png
games/default/files/mobs/mobs_redo/sounds/mobs_swing.ogg
games/default/files/mobs/mobs_redo/sounds/mobs_spell.ogg
games/default/files/mobs/mobs_animal/sounds/mobs_pig.ogg
games/default/files/mobs/mobs_animal/sounds/mobs_cow.ogg
games/default/files/mobs/mobs_animal/models/mobs_pig.b3d
games/default/files/mobs/mobs_animal/models/mobs_cow.b3d
games/default/files/flowers/models/3dmushrooms_brown.png
games/default/files/fire/sounds/fire_flint_and_steel.ogg
games/default/files/default/textures/default_sapling.png
games/default/files/default/textures/default_emerald.png
games/default/files/default/textures/default_diamond.png
games/default/files/default/textures/default_bedrock.png
games/default/files/default/textures/crack_anylength.png
games/default/files/default/sounds/default_dig_metal.ogg
games/default/files/default/sounds/builtin_item_lava.ogg
games/default/files/carts/textures/carts_rail_curved.png
games/default/files/carts/sounds/carts_cart_moving.3.ogg
games/default/files/carts/sounds/carts_cart_moving.2.ogg
games/default/files/carts/sounds/carts_cart_moving.1.ogg
games/default/files/bonusbox/textures/chest_open_top.png
games/default/files/bluestone/mesecons_wires/depends.txt
games/default/files/bluestone/mesecons_alias/depends.txt
games/default/files/bluestone/bluestone_torch/README.txt
games/default/files/bluestone/bluestone_lamp/depends.txt
games/default/files/mobs/mobs_animal/models/mobs_wolf.x
games/default/files/flowers/textures/flowers_orchid.png
games/default/files/flowers/textures/flowers_allium.png
games/default/files/doors/textures/doors_item_steel.png
games/default/files/doors/textures/doors_door_steel.png
games/default/files/default/textures/formspec_shelf.png
games/default/files/default/textures/formspec_chest.png
games/default/files/default/textures/default_search.png
games/default/files/default/textures/default_leaves.png
games/default/files/default/textures/default_gravel.png
games/default/files/default/textures/default_cobble.png
games/default/files/default/textures/default_button.png
games/default/files/default/schematics/large_cactus.mts
games/default/files/bluestone/mesecons_walllever/sounds
games/default/files/bluestone/mesecons_pistons/textures
games/default/files/bluestone/mesecons_pistons/init.lua
games/default/files/bluestone/mesecons_noteblock/sounds
games/default/files/bluestone/mesecons_mvps/depends.txt
games/default/files/bluestone/mesecons_delayer/textures
games/default/files/bluestone/mesecons_delayer/init.lua
games/default/files/vessels/textures/vessels_shelf.png
games/default/files/player/pep/textures/pep_regen2.png
games/default/files/player/pep/textures/pep_breath.png
games/default/files/flowers/textures/flowers_tulip.png
games/default/files/flowers/models/3dmushrooms_red.png
games/default/files/fire/textures/fire_flint_steel.png
games/default/files/fire/textures/fire_basic_flame.png
games/default/files/farming/farming_addons/pumpkin.lua
games/default/files/farming/farming_addons/license.txt
games/default/files/farming/farming_addons/depends.txt
games/default/files/doors/textures/doors_item_wood.png
games/default/files/doors/textures/doors_door_wood.png
games/default/files/default/textures/default_water.png
games/default/files/default/textures/default_torch.png
games/default/files/default/textures/default_sugar.png
games/default/files/default/textures/default_stone.png
games/default/files/default/textures/default_stick.png
games/default/files/default/textures/default_paper.png
games/default/files/default/textures/default_grass.png
games/default/files/default/textures/default_glass.png
games/default/files/default/textures/default_flint.png
games/default/files/default/textures/default_brick.png
games/default/files/default/textures/default_apple.png
games/default/files/default/textures/close_pressed.png
games/default/files/default/sounds/player_damage.3.ogg
games/default/files/default/sounds/player_damage.2.ogg
games/default/files/default/sounds/player_damage.1.ogg
games/default/files/default/schematics/jungle_tree.mts
games/default/files/default/schematics/acacia_tree.mts
games/default/files/boats/textures/boats_inventory.png
games/default/files/bluestone/mesecons_button/init.lua
games/default/files/bluestone/mesecons/actionqueue.lua
games/default/files/bluestone/bluestone_torch/textures
games/default/files/bluestone/bluestone_torch/init.lua
games/default/files/player/pep/textures/pep_regen.png
games/default/files/player/pep/textures/pep_grav0.png
games/default/files/mobs/mobs_npc/locale/template.txt
games/default/files/flowers/textures/flowers_rose.png
games/default/files/farming/farming_addons/README.txt
games/default/files/farming/farming_addons/potato.lua
games/default/files/farming/farming_addons/carrot.lua
games/default/files/doors/textures/doors_trapdoor.png
games/default/files/doors/sounds/doors_door_close.ogg
games/default/files/default/textures/default_wood.png
games/default/files/default/textures/default_vine.png
games/default/files/default/textures/default_tree.png
games/default/files/default/textures/default_snow.png
games/default/files/default/textures/default_sand.png
games/default/files/default/textures/default_lava.png
games/default/files/default/textures/default_fish.png
games/default/files/default/textures/default_dirt.png
games/default/files/default/textures/default_clay.png
games/default/files/default/textures/default_book.png
games/default/files/default/textures/default_bone.png
games/default/files/default/sounds/player_punch.2.ogg
games/default/files/default/sounds/player_punch.1.ogg
games/default/files/default/schematics/jungle_log.mts
games/default/files/default/schematics/birch_tree.mts
games/default/files/default/schematics/apple_tree.mts
games/default/files/default/schematics/acacia_log.mts
games/default/files/carts/textures/carts_cart_inv.png
games/default/files/bonusbox/textures/chest_front.png
games/default/files/bluestone/mesecons_wires/textures
games/default/files/bluestone/mesecons_wires/init.lua
games/default/files/bluestone/mesecons_pressureplates
games/default/files/bluestone/mesecons_pistons/sounds
games/default/files/bluestone/mesecons_alias/init.lua
games/default/files/bluestone/bluestone_lamp/textures
games/default/files/bluestone/bluestone_lamp/init.lua
games/default/files/player/pep/textures/pep_mole.png
games/default/files/flowers/schematics/waterlily.mts
games/default/files/flowerpot/textures/flowerpot.png
games/default/files/farming/farming_addons/seeds.lua
games/default/files/farming/farming_addons/melon.lua
games/default/files/farming/farming_addons/cocoa.lua
games/default/files/doors/sounds/doors_door_open.ogg
games/default/files/deprecated/models/mobs_chicken.x
games/default/files/default/textures/default_ice.png
games/default/files/default/schematics/sugarcane.mts
games/default/files/default/schematics/pine_tree.mts
games/default/files/default/schematics/birch_log.mts
games/default/files/default/schematics/apple_log.mts
games/default/files/default/models/torch_ceiling.obj
games/default/files/bucket/textures/bucket_water.png
games/default/files/bonusbox/textures/chest_side.png
games/default/files/bonusbox/textures/chest_back.png
games/default/files/bluestone/mesecons_mvps/init.lua
games/default/files/bluestone/mesecons_button/sounds
client/shaders/selection_shader/opengl_fragment.glsl
games/default/files/player_api/models/character.png
games/default/files/player_api/models/character.b3d
games/default/files/farming/farming_addons/textures
games/default/files/farming/farming_addons/init.lua
games/default/files/farming/farming_addons/corn.lua
games/default/files/dye/textures/dye_dark_green.png
games/default/files/deprecated/models/mobs_zombie.x
games/default/files/deprecated/models/mobs_spider.x
games/default/files/deprecated/mesecons_pistons.lua
games/default/files/default/textures/item_smoke.png
games/default/files/default/sounds/player_eat.2.ogg
games/default/files/default/sounds/player_eat.1.ogg
games/default/files/default/schematics/pine_log.mts
games/default/files/bucket/textures/bucket_milk.png
games/default/files/bucket/textures/bucket_lava.png
games/default/files/bonusbox/textures/chest_top.png
games/default/files/bluestone/mesecons/settings.lua
games/default/files/bluestone/mesecons/services.lua
games/default/files/bluestone/mesecons/internal.lua
games/default/files/player/playereffects/README.md
games/default/files/mobs/mobs_redo/locale/template
games/default/files/mobs/mobs_monster/skeleton.lua
games/default/files/flowers/models/3dmushrooms.obj
games/default/files/flowerpot/models/flowerpot.obj
games/default/files/farming/farming_addons/api.lua
games/default/files/dye/textures/dye_dark_grey.png
games/default/files/default/textures/crosshair.png
games/default/files/default/models/torch_floor.obj
games/default/files/bluestone/mesecons/presets.lua
games/default/files/bluestone/mesecons/depends.txt
games/default/files/beds/textures/beds_bed_inv.png
client/shaders/wielded_shader/opengl_fragment.glsl
client/shaders/selection_shader/opengl_vertex.glsl
client/shaders/minimap_shader/opengl_fragment.glsl
client/shaders/default_shader/opengl_fragment.glsl
games/default/files/player/playereffects/init.lua
games/default/files/mobs/mobs_monster/depends.txt
games/default/files/deprecated/models/mobs_bear.x
games/default/files/default/textures/heart_bg.png
games/default/files/default/models/torch_wall.obj
games/default/files/bluestone/mesecons_solarpanel
games/default/files/bluestone/mesecons/legacy.lua
games/default/files/mobs/mobs_redo/locale/ru.txt
games/default/files/mobs/mobs_monster/zombie.lua
games/default/files/mobs/mobs_monster/spider.lua
games/default/files/mobs/mobs_monster/README.txt
games/default/files/mobs/mobs_animal/depends.txt
games/default/files/mobs/mobs_animal/chicken.lua
games/default/files/dye/textures/dye_magenta.png
games/default/files/deprecated/models/mobs_pig.x
games/default/files/deprecated/models/mobs_cow.x
games/default/files/bluestone/mesecons_walllever
games/default/files/bluestone/mesecons_noteblock
games/default/files/bluestone/mesecons_materials
client/shaders/wielded_shader/opengl_vertex.glsl
client/shaders/nodes_shader/opengl_fragment.glsl
client/shaders/minimap_shader/opengl_vertex.glsl
client/shaders/default_shader/opengl_vertex.glsl
games/default/files/mobs/mobs_npc/locale/ru.txt
games/default/files/mobs/mobs_npc/locale/ms.txt
games/default/files/mobs/mobs_npc/locale/de.txt
games/default/files/mobs/mobs_animal/README.txt
games/default/files/mobs/mobs_animal/parrot.lua
games/default/files/mobs/mobs_animal/kitten.lua
games/default/files/fire/sounds/fire_fire.3.ogg
games/default/files/fire/sounds/fire_fire.2.ogg
games/default/files/fire/sounds/fire_fire.1.ogg
games/default/files/farming/farming/license.txt
games/default/files/farming/farming/depends.txt
games/default/files/dye/textures/dye_yellow.png
games/default/files/dye/textures/dye_violet.png
games/default/files/dye/textures/dye_orange.png
games/default/files/default/textures/bubble.png
games/default/files/carts/models/carts_cart.png
games/default/files/carts/models/carts_cart.b3d
games/default/files/bluestone/mesecons/util.lua
games/default/files/bluestone/mesecons/init.lua
doc/Font Licenses/DroidSansFallback-LICENSE.txt
doc/Font Licenses/1001fonts-retron2000-eula.txt
builtin/mainmenu/generate_from_settingtypes.lua
games/default/files/player_api/models/hand.b3d
games/default/files/mobs/mobs_redo/license.txt
games/default/files/mobs/mobs_redo/depends.txt
games/default/files/mobs/mobs_monster/textures
games/default/files/mobs/mobs_monster/init.lua
games/default/files/mobs/mobs_animal/sheep.lua
games/default/files/mobs/mobs_animal/bunny.lua
games/default/files/farming/farming/README.txt
games/default/files/dye/textures/dye_white.png
games/default/files/dye/textures/dye_green.png
games/default/files/dye/textures/dye_brown.png
games/default/files/dye/textures/dye_black.png
games/default/files/default/textures/heart.png
games/default/files/default/textures/close.png
games/default/files/bucket/textures/bucket.png
games/default/files/bluestone/mesecons_pistons
games/default/files/bluestone/mesecons_delayer
games/default/files/beds/textures/beds_bed.png
client/shaders/nodes_shader/opengl_vertex.glsl
games/default/files/mobs/mobs_redo/README.txt
games/default/files/mobs/mobs_redo/crafts.lua
games/default/files/mobs/mobs_npc/depends.txt
games/default/files/mobs/mobs_animal/textures
games/default/files/mobs/mobs_animal/init.lua
games/default/files/mobs/mobs_animal/bear.lua
games/default/files/farming/farming/nodes.lua
games/default/files/dye/textures/dye_pink.png
games/default/files/dye/textures/dye_grey.png
games/default/files/dye/textures/dye_cyan.png
games/default/files/dye/textures/dye_blue.png
games/default/files/boats/models/boats_boat.x
games/default/files/bluestone/mesecons_button
games/default/files/bluestone/bluestone_torch
games/default/files/mobs/mobs_npc/trader.lua
games/default/files/mobs/mobs_npc/README.txt
games/default/files/mobs/mobs_monster/sounds
games/default/files/mobs/mobs_monster/models
games/default/files/mobs/mobs_animal/pig.lua
games/default/files/mobs/mobs_animal/dog.lua
games/default/files/mobs/mobs_animal/cow.lua
games/default/files/farming/farming/textures
games/default/files/farming/farming/init.lua
games/default/files/farming/farming/hoes.lua
games/default/files/dye/textures/dye_red.png
games/default/files/dungeon_loot/LICENSE.txt
games/default/files/bluestone/mesecons_wires
games/default/files/bluestone/mesecons_alias
games/default/files/bluestone/bluestone_lamp
games/default/files/beds/models/beds_bed.obj
games/default/files/mobs/mobs_redo/textures
games/default/files/mobs/mobs_redo/mod.conf
games/default/files/mobs/mobs_redo/init.lua
games/default/files/mobs/mobs_animal/sounds
games/default/files/mobs/mobs_animal/models
games/default/files/farming/farming/api.lua
games/default/files/dungeon_loot/README.txt
games/default/files/dungeon_loot/mapgen.lua
games/default/files/doors/models/door_b.obj
games/default/files/doors/models/door_a.obj
games/default/files/bluestone/mesecons_mvps
games/default/files/player/pep/depends.txt
games/default/files/player_api/license.txt
games/default/files/mobs/mobs_redo/api.lua
games/default/files/mobs/mobs_npc/textures
games/default/files/mobs/mobs_npc/init.lua
games/default/files/itemframes/depends.txt
games/default/files/farming/farming_addons
games/default/files/deprecated/depends.txt
games/default/files/default/craftitems.lua
games/default/files/craftguide/license.txt
games/default/files/compatibility/textures
games/default/files/compatibility/init.lua
builtin/mainmenu/dlg_settings_advanced.lua
textures/base/local_creative_checkbox.png
games/default/files/workbench/depends.txt
games/default/files/wieldview/depends.txt
games/default/files/sethome/locale/ru.txt
games/default/files/player_api/README.txt
games/default/files/mobs/mobs_redo/sounds
games/default/files/mobs/mobs_redo/locale
games/default/files/mobs/mobs_npc/npc.lua
games/default/files/locales/locale/ru.txt
games/default/files/itemframes/README.txt
games/default/files/furniture/license.txt
games/default/files/flowerpot/depends.txt
games/default/files/dungeon_loot/loot.lua
games/default/files/dungeon_loot/init.lua
games/default/files/default/functions.lua
games/default/files/craftguide/README.txt
games/default/files/carts/cart_entity.lua
games/default/files/bluestone/modpack.txt
games/default/files/bluestone/LICENSE.txt
games/default/files/bluestone/COPYING.txt
textures/base/minimap_overlay_square.png
locale/sr_Cyrl/LC_MESSAGES/MultiCraft.mo
games/default/files/workbench/README.txt
games/default/files/wieldview/README.txt
games/default/files/player/playereffects
games/default/files/player/pep/README.md
games/default/files/mobs/mobs_npc/locale
games/default/files/furniture/README.txt
games/default/files/flowerpot/README.txt
games/default/files/default/crafting.lua
games/default/files/creative/license.txt
games/default/files/bucket/locale/ru.txt
games/default/files/bonemeal/license.txt
games/default/files/3d_armor/LICENSE.txt
games/default/files/3d_armor/depends.txt
textures/base/server_flags_favorite.png
textures/base/server_flags_creative.png
textures/base/minimap_overlay_round.png
textures/base/crack_anylength_touch.png
games/default/files/vessels/license.txt
games/default/files/vessels/depends.txt
games/default/files/sethome/license.txt
games/default/files/sethome/depends.txt
games/default/files/player/pep/textures
games/default/files/player/pep/init.lua
games/default/files/player_api/init.lua
games/default/files/itemframes/textures
games/default/files/itemframes/init.lua
games/default/files/flowers/license.txt
games/default/files/flowers/depends.txt
games/default/files/farming/modpack.txt
games/default/files/deprecated/init.lua
games/default/files/default/license.txt
games/default/files/default/furnace.lua
games/default/files/default/aliases.lua
games/default/files/creative/README.txt
games/default/files/craftguide/init.lua
games/default/files/carts/functions.lua
games/default/files/bonusbox/README.txt
games/default/files/bonemeal/README.txt
games/default/files/bluestone/README.md
builtin/mainmenu/dlg_rename_modpack.lua
util/travis/clang-format-whitelist.txt
textures/base/progress_bar_overlay.png
locale/pt_BR/LC_MESSAGES/MultiCraft.mo
games/default/files/xpanes/license.txt
games/default/files/workbench/textures
games/default/files/workbench/init.lua
games/default/files/wieldview/init.lua
games/default/files/vessels/README.txt
games/default/files/sponge/license.txt
games/default/files/sethome/README.txt
games/default/files/player/modpack.txt
games/default/files/player_api/api.lua
games/default/files/furniture/init.lua
games/default/files/flowers/schematics
games/default/files/flowers/README.txt
games/default/files/flowers/mapgen.lua
games/default/files/flowerpot/textures
games/default/files/flowerpot/init.lua
games/default/files/default/schematics
games/default/files/default/README.txt
games/default/files/default/mapgen.lua
games/default/files/default/chests.lua
games/default/files/carts/detector.lua
games/default/files/bucket/license.txt
games/default/files/bucket/depends.txt
games/default/files/bluestone/mesecons
games/default/files/beds/locale/ru.txt
games/default/files/beds/functions.lua
games/default/files/3d_armor/armor.lua
textures/base/server_flags_damage.png
textures/base/minimap_mask_square.png
textures/base/gui_hotbar_selected.png
games/default/files/xpanes/README.txt
games/default/files/walls/license.txt
games/default/files/walls/depends.txt
games/default/files/sponge/README.txt
games/default/files/sfinv/license.txt
games/default/files/sfinv/depends.txt
games/default/files/player_api/models
games/default/files/mobs/mobs_monster
games/default/files/dye/locale/ru.txt
games/default/files/dye/locale/en.txt
games/default/files/doors/license.txt
games/default/files/doors/depends.txt
games/default/files/deprecated/models
games/default/files/default/trees.lua
games/default/files/default/torch.lua
games/default/files/default/tools.lua
games/default/files/default/nodes.lua
games/default/files/creative/init.lua
games/default/files/carts/license.txt
games/default/files/carts/depends.txt
games/default/files/bucket/README.txt
games/default/files/bonusbox/textures
games/default/files/bonusbox/init.lua
games/default/files/bonemeal/init.lua
games/default/files/boats/license.txt
games/default/files/boats/depends.txt
games/default/files/3d_armor/textures
games/default/files/3d_armor/init.lua
doc/Font Licenses/Cousine-LICENSE.txt
builtin/mainmenu/tab_texturepacks.lua
builtin/mainmenu/dlg_delete_world.lua
builtin/mainmenu/dlg_create_world.lua
builtin/mainmenu/dlg_config_world.lua
util/travis/toolchain_mingw.cmake.in
textures/base/minimap_mask_round.png
misc/com.MultiCraft.game.appdata.xml
locale/jbo/LC_MESSAGES/MultiCraft.mo
games/default/files/workbench/models
games/default/files/walls/README.txt
games/default/files/vessels/textures
games/default/files/vessels/init.lua
games/default/files/sfinv/README.txt
games/default/files/sethome/textures
games/default/files/sethome/init.lua
games/default/files/mobs/modpack.txt
games/default/files/mobs/mobs_animal
games/default/files/locales/init.lua
games/default/files/flowers/textures
games/default/files/flowers/init.lua
games/default/files/flowerpot/models
games/default/files/fire/license.txt
games/default/files/fire/depends.txt
games/default/files/doors/README.txt
games/default/files/default/textures
games/default/files/default/init.lua
games/default/files/carts/README.txt
games/default/files/boats/README.txt
games/default/files/beds/license.txt
games/default/files/beds/depends.txt
games/default/files/3d_armor/api.lua
builtin/profiler/instrumentation.lua
textures/base/object_marker_red.png
locale/uk/LC_MESSAGES/MultiCraft.mo
locale/tr/LC_MESSAGES/MultiCraft.mo
locale/sw/LC_MESSAGES/MultiCraft.mo
locale/sv/LC_MESSAGES/MultiCraft.mo
locale/sl/LC_MESSAGES/MultiCraft.mo
locale/ru/LC_MESSAGES/MultiCraft.mo
locale/ro/LC_MESSAGES/MultiCraft.mo
locale/pt/LC_MESSAGES/MultiCraft.mo
locale/pl/LC_MESSAGES/MultiCraft.mo
locale/nl/LC_MESSAGES/MultiCraft.mo
locale/nb/LC_MESSAGES/MultiCraft.mo
locale/ms/LC_MESSAGES/MultiCraft.mo
locale/lt/LC_MESSAGES/MultiCraft.mo
locale/ja/LC_MESSAGES/MultiCraft.mo
locale/it/LC_MESSAGES/MultiCraft.mo
locale/id/LC_MESSAGES/MultiCraft.mo
locale/hu/LC_MESSAGES/MultiCraft.mo
locale/fr/LC_MESSAGES/MultiCraft.mo
locale/et/LC_MESSAGES/MultiCraft.mo
locale/es/LC_MESSAGES/MultiCraft.mo
locale/eo/LC_MESSAGES/MultiCraft.mo
locale/dv/LC_MESSAGES/MultiCraft.mo
locale/de/LC_MESSAGES/MultiCraft.mo
locale/da/LC_MESSAGES/MultiCraft.mo
locale/cs/LC_MESSAGES/MultiCraft.mo
locale/ca/LC_MESSAGES/MultiCraft.mo
games/default/files/xpanes/init.lua
games/default/files/wallet/textures
games/default/files/wallet/init.lua
games/default/files/sponge/init.lua
games/default/files/pie/license.txt
games/default/files/fire/README.txt
games/default/files/farming/farming
games/default/files/dye/license.txt
games/default/files/carts/rails.lua
games/default/files/bucket/textures
games/default/files/bucket/init.lua
games/default/files/beds/spawns.lua
games/default/files/beds/README.txt
builtin/mainmenu/dlg_delete_mod.lua
builtin/game/detached_inventory.lua
textures/base/server_flags_pvp.png
textures/base/gui_hotbar_small.png
textures/base/down_three_press.png
games/default/files/walls/init.lua
games/default/files/sfinv/init.lua
games/default/files/sethome/locale
games/default/files/pie/README.txt
games/default/files/mobs/mobs_redo
games/default/files/locales/locale
games/default/files/flowers/models
games/default/files/dye/README.txt
games/default/files/doors/textures
games/default/files/doors/init.lua
games/default/files/default/sounds
games/default/files/default/models
games/default/files/carts/textures
games/default/files/carts/init.lua
games/default/files/boats/textures
games/default/files/boats/init.lua
textures/base/server_flags_mt.png
textures/base/server_flags_mc.png
textures/base/progress_bar_bg.png
misc/MultiCraft-xorg-icon-128.png
games/default/files/sfinv/api.lua
games/default/files/mobs/mobs_npc
games/default/files/fire/textures
games/default/files/fire/init.lua
games/default/files/compatibility
games/default/files/bucket/locale
games/default/files/beds/textures
games/default/files/beds/init.lua
builtin/mainmenu/tab_settings.lua
worlds/World 5 Flat/map_meta.txt
util/generate-texture-normals.sh
textures/base/up_three_press.png
textures/base/unknown_object.png
textures/base/down_two_press.png
textures/base/down_three_btn.png
textures/base/down_one_press.png
misc/com.MultiCraft.game.desktop
games/default/files/pie/init.lua
games/default/files/dye/textures
games/default/files/dye/init.lua
games/default/files/dungeon_loot
games/default/files/doors/sounds
games/default/files/doors/models
games/default/files/carts/sounds
games/default/files/carts/models
games/default/files/boats/models
games/default/files/beds/api.lua
builtin/mainmenu/tab_credits.lua
textures/base/server_ping_4.png
textures/base/server_ping_3.png
textures/base/server_ping_2.png
textures/base/server_ping_1.png
textures/base/rangeview_btn.png
textures/base/player_marker.png
textures/base/no_screenshot.png
textures/base/inventory_btn.png
games/default/files/fire/sounds
games/default/files/beds/models
games/default/files/beds/locale
client/shaders/selection_shader
builtin/mainmenu/tab_server.lua
builtin/mainmenu/tab_online.lua
builtin/common/misc_helpers.lua
builtin/common/chatcommands.lua
builtin/client/chatcommands.lua
textures/base/up_two_press.png
textures/base/up_three_btn.png
textures/base/up_one_press.png
textures/base/unknown_node.png
textures/base/unknown_item.png
textures/base/down_two_btn.png
textures/base/down_one_btn.png
games/default/files/player/pep
games/default/files/player_api
games/default/files/itemframes
games/default/files/dye/locale
games/default/files/deprecated
games/default/files/craftguide
fonts/mono_dejavu_sans_280.png
fonts/mono_dejavu_sans_260.png
fonts/mono_dejavu_sans_240.png
fonts/mono_dejavu_sans_220.png
fonts/mono_dejavu_sans_200.png
fonts/mono_dejavu_sans_180.png
fonts/mono_dejavu_sans_160.png
fonts/mono_dejavu_sans_140.png
fonts/mono_dejavu_sans_120.png
fonts/mono_dejavu_sans_110.png
fonts/mono_dejavu_sans_100.png
builtin/mainmenu/tab_local.lua
builtin/common/async_event.lua
util/travis/before_install.sh
textures/base/right_press.png
textures/base/minimap_btn.png
games/default/multicraft.conf
games/default/files/workbench
games/default/files/wieldview
games/default/files/furniture
games/default/files/flowerpot
games/default/files/bluestone
games/default/doc/Licence.txt
games/default/doc/LGPL-3.0.md
fonts/mono_dejavu_sans_90.png
fonts/mono_dejavu_sans_80.png
fonts/mono_dejavu_sans_60.png
fonts/mono_dejavu_sans_40.png
fonts/mono_dejavu_sans_28.xml
fonts/mono_dejavu_sans_26.xml
fonts/mono_dejavu_sans_24.xml
fonts/mono_dejavu_sans_22.xml
fonts/mono_dejavu_sans_20.xml
fonts/mono_dejavu_sans_18.xml
fonts/mono_dejavu_sans_16.xml
fonts/mono_dejavu_sans_14.xml
fonts/mono_dejavu_sans_12.xml
fonts/mono_dejavu_sans_11.xml
fonts/mono_dejavu_sans_10.xml
client/shaders/wielded_shader
client/shaders/minimap_shader
client/shaders/default_shader
builtin/profiler/sampling.lua
builtin/profiler/reporter.lua
builtin/mainmenu/textures.lua
builtin/mainmenu/tab_mods.lua
builtin/game/static_spawn.lua
builtin/game/forceloading.lua
builtin/game/chatcommands.lua
builtin/common/filterlist.lua
worlds/World 5 Flat/world.mt
textures/base/up_two_btn.png
textures/base/up_one_btn.png
textures/base/left_press.png
textures/base/gui_hotbar.png
textures/base/escape_btn.png
games/default/files/creative
games/default/files/bonusbox
games/default/files/bonemeal
games/default/files/3d_armor
fonts/mono_dejavu_sans_9.xml
fonts/mono_dejavu_sans_8.xml
fonts/mono_dejavu_sans_6.xml
fonts/mono_dejavu_sans_4.xml
builtin/utf8lib/utf8data.lua
builtin/mainmenu/gamemgr.lua
builtin/game/item_entity.lua
builtin/common/serialize.lua
util/wireshark/minetest.lua
textures/base/sunrisebg.png
textures/base/right_btn.png
textures/base/empty_btn.png
textures/base/bg_online.png
textures/base/bg_dialog.png
textures/base/bg_common.png
misc/MultiCraft.appdata.xml
lib/intl/MessageCatalog.hpp
games/default/files/vessels
games/default/files/sethome
games/default/files/locales
games/default/files/flowers
games/default/files/farming
games/default/files/default
fonts/DroidSansFallback.ttf
client/shaders/nodes_shader
clientmods/preview/init.lua
builtin/mainmenu/modmgr.lua
builtin/mainmenu/common.lua
builtin/intllib/gettext.lua
builtin/game/privileges.lua
builtin/client/register.lua
textures/base/left_btn.png
textures/base/jump_btn.png
textures/base/drop_btn.png
textures/base/down_btn.png
textures/base/chat_btn.png
textures/base/bg_local.png
misc/minetest.exe.manifest
locale/sr_Cyrl/LC_MESSAGES
games/default/files/xpanes
games/default/files/wallet
games/default/files/sponge
games/default/files/player
games/default/files/bucket
builtin/mainmenu/store.lua
builtin/intllib/LICENSE.md
builtin/game/voxelarea.lua
builtin/game/constants.lua
textures/base/refresh.png
misc/MultiCraft-icon.icns
lib/jsoncpp/json/UPDATING
games/default/files/walls
games/default/files/sfinv
games/default/files/doors
games/default/files/carts
games/default/files/boats
fonts/Cousine-Regular.ttf
builtin/profiler/init.lua
builtin/mainmenu/init.lua
builtin/game/statbars.lua
builtin/game/register.lua
builtin/common/vector.lua
builtin/common/strict.lua
util/test_multiplayer.sh
textures/base/search.png
textures/base/ignore.png
po/sr_Cyrl/MultiCraft.po
locale/pt_BR/LC_MESSAGES
lib/jsoncpp/libjsoncpp.a
games/default/files/mobs
games/default/files/fire
games/default/files/beds
builtin/utf8lib/init.lua
builtin/settingtypes.txt
builtin/intllib/init.lua
builtin/game/falling.lua
builtin/fstk/tabview.lua
builtin/common/after.lua
worlds/World 4/world.mt
worlds/World 3/world.mt
worlds/World 2/world.mt
worlds/World 1/world.mt
textures/base/trash.png
textures/base/blank.png
multicraft.conf.example
misc/MultiCraft.desktop
lib/jsoncpp/json/json.h
lib/jsoncpp/jsoncpp.cpp
games/default/README.md
games/default/game.conf
games/default/files/pie
games/default/files/dye
builtin/intllib/lib.lua
builtin/game/hunger.lua
builtin/fstk/dialog.lua
builtin/client/init.lua
util/sectors2sqlite.py
util/minetestmapper.py
textures/base/halo.png
po/zh_TW/MultiCraft.po
po/zh_CN/MultiCraft.po
po/pt_BR/MultiCraft.po
locale/jbo/LC_MESSAGES
doc/MultiCraftServer.6
builtin/async/init.lua
util/travis/script.sh
util/travis/common.sh
locale/uk/LC_MESSAGES
locale/tr/LC_MESSAGES
locale/sw/LC_MESSAGES
locale/sv/LC_MESSAGES
locale/sl/LC_MESSAGES
locale/ru/LC_MESSAGES
locale/ro/LC_MESSAGES
locale/pt/LC_MESSAGES
locale/pl/LC_MESSAGES
locale/nl/LC_MESSAGES
locale/nb/LC_MESSAGES
locale/ms/LC_MESSAGES
locale/lt/LC_MESSAGES
locale/ja/LC_MESSAGES
locale/it/LC_MESSAGES
locale/id/LC_MESSAGES
locale/hu/LC_MESSAGES
locale/fr/LC_MESSAGES
locale/et/LC_MESSAGES
locale/es/LC_MESSAGES
locale/eo/LC_MESSAGES
locale/dv/LC_MESSAGES
locale/de/LC_MESSAGES
locale/da/LC_MESSAGES
locale/cs/LC_MESSAGES
locale/ca/LC_MESSAGES
doc/texture_packs.txt
doc/client_lua_api.md
builtin/game/misc.lua
builtin/game/item.lua
builtin/game/init.lua
builtin/game/auth.lua
util/bump_version.sh
textures/base/bg.png
po/jbo/MultiCraft.po
lib/intl/libintl.cpp
fonts/Retron2000.ttf
doc/world_format.txt
doc/Other License.md
doc/menu_lua_api.txt
builtin/game/hud.lua
worlds/World 5 Flat
util/travis/lint.sh
po/uk/MultiCraft.po
po/tr/MultiCraft.po
po/sw/MultiCraft.po
po/sv/MultiCraft.po
po/sl/MultiCraft.po
po/ru/MultiCraft.po
po/ro/MultiCraft.po
po/pt/MultiCraft.po
po/pl/MultiCraft.po
po/nl/MultiCraft.po
po/nb/MultiCraft.po
po/ms/MultiCraft.po
po/lt/MultiCraft.po
po/ky/MultiCraft.po
po/ko/MultiCraft.po
po/ja/MultiCraft.po
po/it/MultiCraft.po
po/id/MultiCraft.po
po/hu/MultiCraft.po
po/he/MultiCraft.po
po/fr/MultiCraft.po
po/et/MultiCraft.po
po/es/MultiCraft.po
po/eo/MultiCraft.po
po/dv/MultiCraft.po
po/de/MultiCraft.po
po/da/MultiCraft.po
po/cs/MultiCraft.po
po/ca/MultiCraft.po
po/be/MultiCraft.po
misc/winresource.rc
misc/MultiCraft.svg
misc/MultiCraft.ico
misc/debpkg-control
games/default/files
doc/CONTRIBUTING.md
builtin/fstk/ui.lua
lib/intl/libintl.h
lib/gmp/mini-gmp.h
lib/gmp/mini-gmp.c
clientmods/preview
po/MultiCraft.pot
lib/lua/COPYRIGHT
lib/intl/Util.hpp
games/default/doc
doc/main_page.dox
doc/Font Licenses
client/serverlist
util/updatepo.sh
lib/jsoncpp/json
doc/protocol.txt
doc/MultiCraft.6
builtin/profiler
builtin/mainmenu
builtin/init.lua
util/colors.txt
misc/Info.plist
lib/intl/README
doc/lua_api.txt
doc/LGPL-3.0.md
doc/fst_api.txt
doc/Doxyfile.in
builtin/utf8lib
builtin/intllib
worlds/World 4
worlds/World 3
worlds/World 2
worlds/World 1
util/wireshark
locale/sr_Cyrl
client/shaders
builtin/common
builtin/client
bin/MultiCraft
textures/base
games/default
doc/Readme.md
builtin/async
locale/pt_BR
doc/Doxyfile
builtin/game
builtin/fstk
util/travis
lib/jsoncpp
po/sr_Cyrl
locale/jbo
clientmods
README.md
locale/uk
locale/tr
locale/sw
locale/sv
locale/sl
locale/ru
locale/ro
locale/pt
locale/pl
locale/nl
locale/nb
locale/ms
locale/lt
locale/ja
locale/it
locale/id
locale/hu
locale/fr
locale/et
locale/es
locale/eo
locale/dv
locale/de
locale/da
locale/cs
locale/ca
textures
po/zh_TW
po/zh_CN
po/pt_BR
lib/intl
lib/lua
lib/gmp
builtin
worlds
po/jbo
locale
client
po/uk
po/tr
po/sw
po/sv
po/sl
po/ru
po/ro
po/pt
po/pl
po/nl
po/nb
po/ms
po/lt
po/ky
po/ko
po/ja
po/it
po/id
po/hu
po/he
po/fr
po/et
po/es
po/eo
po/dv
po/de
po/da
po/cs
po/ca
po/be
games
fonts
util
misc
lib
doc
bin
po
END
    if [ -z "$DESTINATION" ]; then
        customExit "DESTINATION is blank."
    fi
    while read p; do
        if [ -f "$DESTINATION/$p" ]; then
            # echo "rm '$p'"
            rm "$DESTINATION/$p"
        fi
    done <$manifestPath
    while read p; do
        if [ -d "$DESTINATION/$p" ]; then
            rmdir --ignore-fail-on-non-empty "$DESTINATION/$p"
        fi
    done <$manifestPath
    rm $manifestPath
    rmdir --ignore-fail-on-non-empty /tmp/MultiCraft
    rmdir --ignore-fail-on-non-empty "$DESTINATION"
    echo "$0 --uninstall is complete."
    exit 0
fi

if [ "@$INSTALL" = "@true" ]; then
    echo "* installing from '$srcRepo' to '$DESTINATION'..."
    if [ ! -f "`command -v rsync`" ]; then
        customExit "You must first install rsync to use the install option."
    fi
    if [ ! -d "$DESTINATION" ]; then
        mkdir -p "$DESTINATION" || customExit "mkdir -p '$DESTINATION' FAILED."
    fi
    if [ -f "$DESTINATION/multicraft.conf" ]; then
        echo "  - The existing multicraft.conf will not be overwritten."
        rsync -rt --info=progress2 --exclude-from "$artifactsPath" --exclude 'multicraft.conf' "$srcRepo/" "$DESTINATION" || customExit "rsync failed."
    else
        rsync -rt --info=progress2 --exclude-from "$artifactsPath" "$srcRepo/" "$DESTINATION" || customExit "rsync failed."
    fi
    rm $artifactsPath
    rmdir --ignore-fail-on-non-empty /tmp/MultiCraft

    if [ -f "$tryIcon" ]; then
        dstIcon="$tryIcon"
    else
        echo "WARNING: rsync did not provide '$tryIcon'."
        echo "  The shortcut will try to use the system's $dstIcon icon."
    fi

    if [ ! -f "$dstExe" ]; then
        customExit "Install did not result in '$dstExe'."
    fi
    if [ ! -d "$dstShortcuts" ]; then
        mkdir -p "$dstShortcuts" || customExit echo "mkdir -p '$dstShortcuts' FAILED."
    fi
cat > $dstShortcut <<END
[Desktop Entry]
Name=$iconCaption
GenericName[en_US]=$iconCaption
GenericName=$iconCaption
Icon=$dstIcon
Path=$dstBin
Exec=$dstExe
Categories=Game;Simulation;
Comment[en_US]=Multiplayer infinite-world block sandbox
Comment=Multiplayer infinite-world block sandbox
Comment[de]=Mehrspieler-Sandkastenspiel mit unendlichen Blockwelten
Comment[es]=Juego sandbox multijugador con mundos infinitos
Comment[fr]=Jeu multijoueurs de type bac \xc3\xa0 sable avec des mondes infinis
Comment[ja]=\xe3\x83\x9e\xe3\x83\xab\xe3\x83\x81\xe3\x83\x97\xe3\x83\xac\xe3\x82\xa4\xe3\x81\xab\xe5\xaf\xbe\xe5\xbf\x9c\xe3\x81\x97\xe3\x81\x9f\xe3\x80\x81\xe7\x84\xa1\xe9\x99\x90\xe3\x81\xae\xe4\xb8\x96\xe7\x95\x8c\xe3\x81\xae\xe3\x83\x96\xe3\x83\xad\xe3\x83\x83\xe3\x82\xaf\xe5\x9e\x8b\xe3\x82\xb5\xe3\x83\xb3\xe3\x83\x89\xe3\x83\x9c\xe3\x83\x83\xe3\x82\xaf\xe3\x82\xb9\xe3\x82\xb2\xe3\x83\xbc\xe3\x83\xa0\xe3\x81\xa7\xe3\x81\x99
Comment[ru]=\xd0\x98\xd0\xb3\xd1\x80\xd0\xb0-\xd0\xbf\xd0\xb5\xd1\x81\xd0\xbe\xd1\x87\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb0 \xd1\x81 \xd0\xb1\xd0\xb5\xd0\xb7\xd0\xb3\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x87\xd0\xbd\xd1\x8b\xd0\xbc \xd0\xbc\xd0\xb8\xd1\x80\xd0\xbe\xd0\xbc, \xd1\x81\xd0\xbe\xd1\x81\xd1\x82\xd0\xbe\xd1\x8f\xd1\x89\xd0\xb8\xd0\xbc \xd0\xb8\xd0\xb7 \xd0\xb1\xd0\xbb\xd0\xbe\xd0\xba\xd0\xbe\xd0\xb2
Comment[tr]=Tek-\xc3\x87ok oyuncuyla k\xc3\xbcplerden sonsuz d\xc3\xbcnyalar in\xc5\x9fa et
Keywords=sandbox;world;mining;crafting;blocks;nodes;multiplayer;roleplaying;
MimeType=
StartupNotify=false
Terminal=false
TerminalOptions=
Type=Application
X-DBUS-ServiceName=
X-DBUS-StartupType=
X-KDE-SubstituteUID=false
X-KDE-Username=
END
if [ $? -eq 0 ]; then
    echo "* Created $dstShortcut."
else
    customExit "Creating $dstShortcut FAILED."
fi
    echo
    echo
    echo "Installation is complete."
    echo "Find $iconCaption in your application menu."
    echo
    echo "Uninstall:"
    echo "$0 --uninstall"
    echo
    echo "Uninstall manually (game and data):"
    echo "#This will delete all data such as worlds and screenshots!"
    echo "rm -rf '$DESTINATION'"
    echo "rm '$dstShortcut'"
    echo
    echo
    echo "$0 is complete."
    exit 0
fi

if [ ! -d "$srcRepo" ]; then
    cd "$GIT_REPOS_DIR" || customExit "cd '$GIT_REPOS_DIR' FAILED"
fi
goodFlagFile=MultiCraft/CMakeLists.txt
if [ -f "`command -v git`" ]; then
    echo "In `pwd`..."
    if [ ! -d "$BUILD_WHAT" ]; then
        if [ "@$OFFLINE" = "@false" ]; then
            git clone https://github.com/MultiCraft/MultiCraft.git || customExit "Cannot clone MultiCraft from `pwd`"
        fi
        cd "$BUILD_WHAT" || customExit "Cannot cd '$BUILD_WHAT' from `pwd`"
    else
        cd "$BUILD_WHAT" || customExit "Cannot cd '$BUILD_WHAT' from `pwd`"
        if [ "@$OFFLINE" = "@false" ]; then
            git pull || dieIfOnline "WARNING: Cannot pull '$BUILD_WHAT' from `pwd`"
        fi
    fi
else
    if [ ! -f "$goodFlagFile" ]; then
        customExit "You are missing git, and offline install is not possible without in current directory (`pwd`)"
    else
        cd "$BUILD_WHAT" || usageDie "Cannot cd '$BUILD_WHAT' from `pwd`"
    fi
fi
cd games || usageDie "cd games FAILED in `pwd`"
rmdir --ignore-fail-on-non-empty default
if [ ! -d "default" ]; then
    if [ "@$OFFLINE" = "@false" ]; then
        git clone https://github.com/MultiCraft/MultiCraft_game default || customExit "git clone https://github.com/MultiCraft/MultiCraft_game FAILED"
    else
        echo
        echo
        echo
        echo "ERROR: default is not in `pwd`--worlds cannot load without a game."
        echo
        echo
        sleep 2
    fi
else
    if [ "@$OFFLINE" = "@false" ]; then
        cd default || customExit "cd default FAILED in `pwd`"
        git pull || customExit "git pull FAILED in `pwd`"
        cd .. || customExit "cd .. FAILED in `pwd`"
    fi
fi
cd .. || usageDie "cd .. FAILED in `pwd`"
srcPath=.
flag1="-DOpenGL_GL_PREFERENCE=GLVND"
echo
echo "Running cmake srcPath..."
# NOTE: you can make a Code::Blocks project by adding the cmake option: -G"CodeBlocks - Unix Makefiles"
# usually: cmake . -DOpenGL_GL_PREFERENCE=GLVND -DRUN_IN_PLACE=1 -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1
cmake $srcPath $flag1 -G"CodeBlocks - Unix Makefiles" -DRUN_IN_PLACE=1 -DENABLE_GETTEXT=1 -DENABLE_FREETYPE=1 -DENABLE_LEVELDB=1 || usageDie "cmake failed in `pwd`. See any messages above for more information. Run ./install-minetest-build-deps.sh if you did not."
echo
echo "Running make..."
make -j$(nproc) || customExit "make failed. See any messages above for more information. Run ./install-minetest-build-deps.sh if you did not."
if [ -f "`pwd`/bin/MultiCraft" ]; then
    echo "`pwd`/bin/MultiCraft"
else
    echo "`pwd`"
fi
#if [ -d "$GIT_REPOS_DIR/MultiCraft-poikilos" ]; then
#    rsync -rt --info=progress2 --exclude 'multicraft.conf' "$srcRepo/" "$GIT_REPOS_DIR/MultiCraft-poikilos"
#fi
echo "$0 is complete."
echo "To Install:"
if [ "@$BUILD_WHAT" = "@$BUILD_WHAT_DEFAULT" ]; then
    echo "  $0 --install"
else
    echo "  $0 --what '$BUILD_WHAT' --install"
fi
echo
echo
