#!/bin/bash
me=`basename "$0"`

# Create a "fake branch" (base and patch, only containing files
# selected, and automatically-gathered readme files if named as
# expected)
# --install    Install the specified patch.

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
branch=
enable_install=false
enable_meld=false
next_var=
enable_bare_param=false
param1="$1"
#what=$1
for var in "$@"
do
    if [ "@$next_var" = "@--install" ]; then
        next_var=
        branch="$var"
        enable_install=true
    elif [ "@$next_var" = "@--meld" ]; then
        next_var=
        branch="$var"
        enable_meld=true
        #echo "enable_meld:$enable_meld"
    elif [ "@$var" = "@--install" ]; then
        next_var="$var"
    elif [ "@$var" = "@--meld" ]; then
        next_var="$var"
        #echo "next_var:$next_var"
    elif [ "@$var" = "@$param1" ]; then
        what="$var"
    else
        next_var=
        #branch="$var"
        enable_bare_param=true
        echo "selected branch: $var"
    fi
done
if [ "@$enable_bare_param" = "@true" ]; then
    branch="$2"
fi
project0=Bucket_Game
project1=Bucket_Game-base
project2=Bucket_Game-branches
# project0_path="$HOME/git/EnlivenMinetest/webapp/linux-minetest-kit/minetest/games/$project0"
project0_path="$HOME/minetest/games/$project0"

#patches="$HOME/git/EnlivenMinetest/patches"
#patches="$HOME/git/1.pull-requests/Bucket_Game-branches"
repo="$HOME/git/EnlivenMinetest"
patches="$HOME/git/EnlivenMinetest"
project1_path="$repo/$project1/$branch"
project2_path="$repo/$project2/$branch"
if [ "@$enable_meld" = "@true" ]; then
    echo "meld..."
    if [ -z "$branch" ]; then
        customExit "You must specify a branch name after --meld."
    fi
    subgame=
    patch_game_src=
    if [ -d "$project1_path/mods" ]; then
        branch_basis="$project1_path"
    fi
    if [ -d "$project2_path/mods" ]; then
        patch_game_src="$project2_path"
    else
        customExit "Cannot detect mods directory in $project2_path/mods"
    fi
    #below (commented part) should only happen if $project2_path already has been edited (diverged from $project1_path)
    #echo "meld $patch_game_src/ $HOME/minetest/games/ENLIVEN..."
    #if [ -f "`command -v meld`" ]; then
        #if [ -f "`command -v nohup`" ]; then
            #nohup meld "$patch_game_src/" "$HOME/minetest/games/ENLIVEN" &
        #else
            #meld "$patch_game_src/" "$HOME/minetest/games/ENLIVEN" &
            #echo "* install nohup to prevent programs from dumping output to console..."
        #fi
    #fi
    if [ ! -z "$branch_basis" ]; then
        echo "meld '$branch_basis' '$patch_game_src'..."
        if [ -f "`command -v meld`" ]; then
            if [ -f "`command -v nohup`" ]; then
                nohup meld "$branch_basis" "$patch_game_src" &
            else
                meld "$patch_game_src/" "$HOME/minetest/games/ENLIVEN" &
                echo "* install nohup to prevent programs from dumping output to console..."
            fi
        else
            customExit "You do not have meld installed."
        fi
    else
        echo "meld '$HOME/minetest/games/ENLIVEN' '$patch_game_src'..."
        if [ -f "`command -v meld`" ]; then
            if [ -f "`command -v nohup`" ]; then
                nohup meld "$HOME/minetest/games/ENLIVEN" "$patch_game_src" &
            else
                meld "$$HOME/minetest/games/ENLIVEN" "$patch_game_src" &
                echo "* install nohup to prevent programs from dumping output to console..."
            fi
        else
            customExit "You do not have meld installed."
        fi
    fi
    echo
    echo
    exit 0
elif [ "@$enable_install" = "@true" ]; then
    if [ -z "$branch" ]; then
        customExit "You must specify a branch name after --install."
    fi
    echo "* installing $branch branch..."
    subgame=
    if [ -d "$project2_path/mods" ]; then
        patch_game_src="$project2_path"
    elif [ -d "$project2_path/patched/mods" ]; then
        patch_game_src="$project2_path/patched"
    else
        customExit "Cannot detect mods directory in $project2_path/mods"
    fi
    echo "rsync -rt $patch_game_src/ $HOME/minetest/games/ENLIVEN..."
    rsync -rt "$patch_game_src/" "$HOME/minetest/games/ENLIVEN"
    # echo "#patches:$patches"
    # echo "#branch:$branch"
    echo "Done."
    echo
    echo
    exit 0
fi
if [ ! -d "$patches" ]; then
    customExit "You are missing $patches so a patch basis and patched target cannot be created there."
fi
licenses="license.txt LICENSE LICENSE.txt oldcoder.txt LICENSE.md license.md"
usage() {
    echo
    echo
    echo "Usage:"
    echo
    echo "$me <file_path> <new-fake-branch-name>"
    echo "* will be copied to $project1 and $project2"
    echo
    echo "Example:"
    echo "$me mods/coderfood/food_basic/init.lua milk-patch"
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
if [ -z "$2" ]; then
    usage
    exit 1
fi

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
if [ -f "`command -v zbstudio`" ]; then
    nohup zbstudio "$file2_path" &
else
    if [ -f "`command -v geany`" ]; then
        nohup geany "$file2_path" &
    fi
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
echo "To apply, set BUCKET_GAME then:"
echo "cd EnlivenMinetest && git pull && rsync -rt Bucket_Game-branches/$branch/ $BUCKET_GAME"
echo

