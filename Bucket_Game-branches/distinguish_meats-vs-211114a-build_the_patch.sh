#!/bin/bash
SOURCE_MP="$HOME/git/animalmaterials"
# ^ the source modpack
cd "$SOURCE_MP"

if [ ! -d "$SOURCE_MP/animalmaterials/textures" ]; then
    printf "Error: SOURCE_MP \"$SOURCE_MP\" doesn't seem to be the animalmaterials modpack directory. Make sure you run this script from animalmaterials"
    if [ -d "$SOURCE_MP/textures" ]; then
        printf " (SOURCE_MP seems to be animalmaterials/animalmaterials--or some other mod directory--since it contains a textures directory)"
    fi
    echo "."
    exit 1
fi

patchFileOrFail(){
    src="$1"
    if [ ! -f "$src" ]; then
        src="$SOURCE_MP/$1"
    fi
    if [ ! -f "$src" ]; then
        echo "  Error: The source file $src doesn't exist. The script refuses to continue."
        exit 1
    fi
    dst="$2"
    if [ ! -f "$dst" ]; then
        echo "  Error: The destination file $dst doesn't exist. This script refuses to continue unless the destination is recognized."
        exit 1
    fi
    echo "  * $dst"
    cp "$src" "$dst"
}

patchBucketGame(){
    BUCKET_GAME="$1"
    if [ ! -d "$BUCKET_GAME/mods" ]; then
        echo "Error: \"$BUCKET_GAME\" doesn't seem to be a game because it doesn't contain a mods directory."
        exit 1
    fi
    echo "* patching \"$BUCKET_GAME\"..."
    patchFileOrFail animalmaterials/textures/animalmaterials_meat_raw.png $BUCKET_GAME/mods/codermobs/codermobs/textures/animal_materials_meat_raw.png
    patchFileOrFail animalmaterials/textures/animalmaterials_meat_raw.png $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_meat_raw.png
    patchFileOrFail animalmaterials/textures/animalmaterials_meat_raw.png $BUCKET_GAME/mods/coderfood/unified_foods/textures/mobs_meat_raw.png
    patchFileOrFail animalmaterials/textures/animalmaterials_meat_raw.png $BUCKET_GAME/mods/codermobs/mobs/textures/mobs_meat_raw.png
    patchFileOrFail animalmaterials/textures/animalmaterials_meat_toxic_raw.png $BUCKET_GAME/mods/codermobs/codermobs/textures/animal_materials_meat_toxic_raw.png
    patchFileOrFail animalmaterials/textures/animalmaterials_meat_undead_raw.png $BUCKET_GAME/mods/codermobs/codermobs/textures/animal_materials_meat_undead_raw.png
    patchFileOrFail animalmaterials/textures/animalmaterials_pork_raw.png $BUCKET_GAME/mods/codermobs/codermobs/textures/animal_materials_pork_raw.png
    patchFileOrFail animalmaterials/textures/animalmaterials_pork_raw.png $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_pork_raw.png
    patchFileOrFail animalmaterials/textures/animalmaterials_egg_big.png $BUCKET_GAME/mods/codermobs/codermobs/textures/animal_materials_egg_big.png
    patchFileOrFail cooking/textures/cooking_cooked_meat.png $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_meat.png
    patchFileOrFail cooking/textures/cooking_cooked_meat.png $BUCKET_GAME/mods/codermobs/mobs/textures/mobs_meat.png
    patchFileOrFail cooking/textures/cooking_cooked_meat.png $BUCKET_GAME/mods/coderfood/unified_foods/textures/mobs_meat.png
    patchFileOrFail cooking/textures/cooking_pork_cooked.png $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_pork_cooked.png

    # These were added in an earlier patch but renamed due to code-only changes in this page
    # (See TODO manually further down)
    # patchFileOrFail animalmaterials/textures/cooking_ostrich.png $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_ostrich_raw.png
    # patchFileOrFail cooking/textures/cooking_ostrich_cooked.png $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_ostrich_cooked.png
    # patchFileOrFail animalmaterials/textures/cooking_beef_raw.png $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_beef_raw.png
    # patchFileOrFail animalmaterials/textures/cooking_venison_raw.png $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_venison_raw.png
    # patchFileOrFail cooking/textures/cooking_beef_cooked.png $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_beef.png
    # patchFileOrFail cooking/textures/cooking_venison_cooked.png $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_venison.png
    echo "  * done"
}

patchBucketGame ~/minetest/games/bucket_game
patchBucketGame ~/git/EnlivenMinetest/Bucket_Game-branches/distinguish_meats-vs-211114a

cat >/dev/null <<END
TODO:

Sources:

Destinations:
# See https://github.com/poikilos/EnlivenMinetest
# (EnlivenMinetest/patches/distinguish_meats-vs-211114a)
patchFileOrFail ? $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_chicken_cooked.png
patchFileOrFail ? $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_chicken_raw.png
patchFileOrFail ? $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_cooked_rat.png
patchFileOrFail ? $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_rat_better_inv.png
patchFileOrFail ? $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_rat_cooked.png
patchFileOrFail ? $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_rat_inventory.png

# See https://github.com/poikilos/whinny:
patchFileOrFail ? $BUCKET_GAME/mods/codermobs/whinny/textures/whinny_meat.png
patchFileOrFail ? $BUCKET_GAME/mods/codermobs/whinny/textures/whinny_meat_raw.png
END

cat <<END
TODO manually:
mv $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_ostrich_meat_raw.png $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_ostrich_raw.png
mv $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_ostrich_meat_cooked.png $BUCKET_GAME/mods/codermobs/codermobs/textures/codermobs_ostrich_cooked.png
END
