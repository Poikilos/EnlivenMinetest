#!/bin/bash
# such as meld /home/owner/minetest/games/ENLIVEN/ /home/owner/git/EnlivenMinetest/patches/Bucket_Game-patched/
me=`basename "$0"`

customExit() {
    echo
    if [ -z "$1" ]; then
        echo "Unknown error."
    else
        echo "ERROR:"
    fi
    echo "$1"
    echo
    echo
    exit 1
}

project0=Bucket_Game
project1=Bucket_Game-basis
project2=Bucket_Game-patched
project0_path="$HOME/git/EnlivenMinetest/webapp/linux-minetest-kit/minetest/games/$project0"
patches="$HOME/git/EnlivenMinetest/patches"
project1_path="$patches/$project1"
project2_path="$patches/$project2"
if [ ! -d "$patches" ]; then
    customExit "You are missing $patches so a patch basis and patched target cannot be created there."
fi
licenses="license.txt LICENSE LICENSE.txt oldcoder.txt LICENSE.md license.md"
usage() {
    echo "$me <file_path>"
    echo "* will be copied to $project1 and $project2"
    echo
    echo "Example:"
    echo "$me mods/coderfood/food_basic/init.lua"
    echo
    echo "* copies the file to $project1 and $project2)"
    echo "* also copies $licenses and same in .. and ../.."
    echo
    echo
}



if [ -z "$1" ]; then
    usage
    exit 1
fi

what=$1



file0_path="$project0_path/$what"
file1_path="$project1_path/$what"
file2_path="$project2_path/$what"
whatname=`basename $file0_path`
date_string=$(date +%Y%m%d)
patchcmd="diff -u $file1_path $file2_path > $patches/$project0-$date_string-$whatname.patch"
echo
echo "After editing $file2_path, then create a patch by running:"
echo "$patchcmd"
echo
echo "* getting parent of $file0_path..."
dir0="$(dirname -- "$(realpath -- "$file0_path")")"
# can't get realpath when directory doesn't exist yet (we make it):
dir1="$(dirname -- "$file1_path")"
dir2="$(dirname -- "$file2_path")"

dir0_p="$(dirname -- "$(realpath -- "$dir0")")"
dir1_p="$(dirname -- "$dir1")"
dir2_p="$(dirname -- "$dir2")"

dir0_pp="$(dirname -- "$(realpath -- "$dir0_p")")"
dir1_pp="$(dirname -- "$dir1_p")"
dir2_pp="$(dirname -- "$dir2_p")"

#echo "* checking $dir0_pp..."
#echo "* checking $dir1_pp..."
#echo "* checking $dir2_pp..."

if [ ! -d "$project0_path" ]; then
    customExit "ERROR: You must have '$project0' installed as '$project0_path'"
fi

if [ ! -f "$file0_path" ]; then
    customExit "ERROR: Missing '$file0_path')"
fi

if [ ! -d "$dir1" ]; then
    mkdir -p "$dir1" || customExit "Cannot mkdir $dir1"
fi

if [ ! -d "$dir2" ]; then
    mkdir -p "$dir2" || customExit "Cannot mkdir $dir2"
fi

# if file1 exists, overwriting is ok--update basis so diff will make patch correctly
echo "* updating $file1_path"
cp -f "$file0_path" "$file1_path" || customExit "Cannot cp '$file0_path' '$file1_path'"

if [ -f "$file2_path" ]; then
    customExit "Nothing done since '$file2_path' already exists."
fi
echo "* creating $file2_path"
cp -f "$file0_path" "$file2_path" || customExit "Cannot cp '$file0_path' '$file2_path'"
if [ -f "`command -v geany`" ]; then
    nohup geany "$file2_path" &
fi
if [ -d "$HOME/minetest/games/ENLIVEN" ]; then
    if [ -f "`command -v meld`" ]; then
        nohup meld "$file2_path" "$HOME/minetest/games/ENLIVEN/$what" &
    fi
fi

eval "arr=($licenses)"
for license in "${arr[@]}"; do
    lic0="$dir0/$license"
    lic1="$dir1/$license"
    lic2="$dir2/$license"
    if [ -f "$lic0" ]; then
        echo "* updating LICENSE '$lic1'..."
        cp -f "$lic0" "$lic1" || customExit "Cannot cp -f '$lic0' '$lic1'"
        if [ ! -f "$lic2" ]; then
            echo "  - also for $project2..."
            cp --no-clobber "$lic0" "$lic2" || customExit "Cannot cp -f '$lic0' '$lic2'"
        fi
    fi
    lic0="$dir0_p/$license"
    lic1="$dir1_p/$license"
    lic2="$dir2_p/$license"
    if [ -f "$lic0" ]; then
        echo "* updating LICENSE '$lic1'..."
        cp -f "$lic0" "$lic1" || customExit "Cannot cp -f '$lic0' '$lic1'"
        if [ ! -f "$lic2" ]; then
            echo "  - also for $project2..."
            cp --no-clobber "$lic0" "$lic2" || customExit "Cannot cp -f '$lic0' '$lic2'"
        fi
    fi
    lic0="$dir0_pp/$license"
    lic1="$dir1_pp/$license"
    lic2="$dir2_pp/$license"
    if [ -f "$lic0" ]; then
        echo "* updating '$lic1'..."
        cp -f "$lic0" "$lic1" || customExit "Cannot cp -f '$lic0' '$lic1'"
        if [ ! -f "$lic2" ]; then
            echo "  - also for $project2..."
            cp --no-clobber "$lic0" "$lic2" || customExit "Cannot cp -f '$lic0' '$lic2'"
        fi
    fi
done

echo "Done."
echo
echo

