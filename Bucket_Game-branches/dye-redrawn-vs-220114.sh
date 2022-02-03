#!/bin/bash
patch_name="dye-redrawn-vs-220114"
try_bg="$HOME/minetest/games/bucket_game"
if [ -z "$BUCKET_GAME" ]; then
    if [ -d "$try_bg" ]; then
        echo "* detected \"$try_bg\""
        BUCKET_GAME="$try_bg"
    fi
fi


if [ -z "$BUCKET_GAME" ]; then
    echo "* You must first set $BUCKET_GAME (Since it wasn't detected at \"$try_bg\")."
    exit 1
fi

if [ ! -d "$BUCKET_GAME/mods" ]; then
    echo "Error: the destination BUCKET_GAME \"$BUCKET_GAME\" doesn't appear to be a game (It has no mods folder)."
    echo "* Set $BUCKET_GAME to your bucket_game directory."
    exit 1
fi

try_patches_dir="Bucket_Game-branches"
patch_src="$patch_name"
if [ ! -d "$patch_name" ]; then
    if [ -d "$try_patches_dir/$patch_name" ]; then
        patch_src="$try_patches_dir/$patch_name"
    fi
fi

if [ ! -d "$patch_name" ]; then
    echo "Error: \"$patch_src\" is not here."
    echo "You  must run this patch script from EnlivenMinetest or EnlivenMinetest/$try_patches_dir."
    exit 1
fi
echo "rsync -rtv \"$patch_src/\" \"$BUCKET_GAME\""
rsync -rtv "$patch_src/" "$BUCKET_GAME"
