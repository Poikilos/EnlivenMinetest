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
auto_branch="$branchUpstream-$date_string-$whatname"
if [ "@$enable_bare_param" = "@true" ]; then
    branch="$2"
else
    branch="$auto_branch"
    echo "* The branch name defaulted to \"$auto_branch\" since you didn't provide a second sequential argument."
fi
branchUpstream=bucket_game-211114a
branchBase=Bucket_Game-base
branchHead=Bucket_Game-branches
# project0_path="$HOME/git/EnlivenMinetest/webapp/linux-minetest-kit/minetest/games/$branchUpstream"
project0_path="$HOME/minetest/games/$branchUpstream"
tryUnpatched="$HOME/minetest/$branchUpstream"
if [ -d "$tryUnpatched" ]; then
    project0_path="$tryUnpatched"
fi

#patches="$HOME/git/EnlivenMinetest/patches"
#patches="$HOME/git/1.pull-requests/Bucket_Game-branches"
repo="$HOME/git/EnlivenMinetest"
patches="$HOME/git/EnlivenMinetest"
branchesName="Bucket_Game-branches"
if [ -d "$branchesName" ]; then
    patches="`realpath $branchesName`"
fi
branchBasePath="$repo/$branchBase/$branch"
branchHeadPath="$repo/$branchHead/$branch"
if [ "@$enable_meld" = "@true" ]; then
    echo "meld..."
    if [ -z "$branch" ]; then
        customExit "You must specify a branch name after --meld."
    fi
    subgame=
    patch_game_src=
    if [ -d "$branchBasePath/mods" ]; then
        branch_basis="$branchBasePath"
    fi
    if [ -d "$branchHeadPath/mods" ]; then
        patch_game_src="$branchHeadPath"
    else
        customExit "Cannot detect mods directory in $branchHeadPath/mods"
    fi
    #below (commented part) should only happen if $branchHeadPath already has been edited (diverged from $branchBasePath)
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
    if [ -d "$branchHeadPath/mods" ]; then
        patch_game_src="$branchHeadPath"
    elif [ -d "$branchHeadPath/patched/mods" ]; then
        patch_game_src="$branchHeadPath/patched"
    else
        customExit "Cannot detect mods directory in $branchHeadPath/mods"
    fi
    echo "rsync -rtv $patch_game_src/ $HOME/minetest/games/ENLIVEN..."
    rsync -rtv "$patch_game_src/" "$HOME/minetest/games/ENLIVEN"
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
    echo "* will be copied to $branchBase and $branchHead"
    echo
    echo "Example:"
    echo "$me mods/coderfood/food_basic/init.lua milk-patch"
    echo
    echo "* copies the file to $branchBase and $branchHead)"
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

branchUpstreamFilePath="$project0_path/$what"
branchBaseFilePath="$branchBasePath/$what"
branchHeadFilePath="$branchHeadPath/$what"
whatname=`basename $branchUpstreamFilePath`
date_string=$(date +%Y%m%d)
# patchcmd="diff -u $branchBaseFilePath $branchHeadFilePath > $patches/$auto_branch.patch"
patchcmd="diff -u $branchBaseFilePath $branchHeadFilePath > $patches/$branch.patch"
echo
echo "After editing $branchHeadFilePath, then create a patch by running:"
echo "$patchcmd"
echo
echo "* getting parent of $branchUpstreamFilePath..."
dirUpstream="$(dirname -- "$(realpath -- "$branchUpstreamFilePath")")"
# can't get realpath when directory doesn't exist yet (we make it):
dirBase="$(dirname -- "$branchBaseFilePath")"
dirHead="$(dirname -- "$branchHeadFilePath")"

dirUpstreamParent="$(dirname -- "$(realpath -- "$dirUpstream")")"
dirBaseParent="$(dirname -- "$dirBase")"
dirHeadParent="$(dirname -- "$dirHead")"

dirUpstreamGrandParent="$(dirname -- "$(realpath -- "$dirUpstreamParent")")"
dirBaseGrandParent="$(dirname -- "$dirBaseParent")"
dirHeadGrandParent="$(dirname -- "$dirHeadParent")"

#echo "* checking $dirUpstreamGrandParent..."
#echo "* checking $dirBaseGrandParent..."
#echo "* checking $dirHeadGrandParent..."

if [ ! -d "$project0_path" ]; then
    customExit "ERROR: You must have '$branchUpstream' installed as '$project0_path'"
fi

if [ ! -f "$branchUpstreamFilePath" ]; then
    customExit "ERROR: Missing '$branchUpstreamFilePath')"
fi

if [ ! -d "$dirBase" ]; then
    mkdir -p "$dirBase" || customExit "Cannot mkdir $dirBase"
fi

if [ ! -d "$dirHead" ]; then
    mkdir -p "$dirHead" || customExit "Cannot mkdir $dirHead"
fi

# if file1 exists, overwriting is ok--update basis so diff will make patch correctly
echo "* updating $branchBaseFilePath"
cp -f "$branchUpstreamFilePath" "$branchBaseFilePath" || customExit "Cannot cp '$branchUpstreamFilePath' '$branchBaseFilePath'"

openImageAsync(){
    lximage-qt "$1" &
}

openTextAsync(){
    if [ -f "`command -v zbstudio`" ]; then
        nohup zbstudio "$1" &
    else
        if [ -f "`command -v geany`" ]; then
            nohup geany "$1" &
        fi
    fi
}

if [ -f "$branchHeadFilePath" ]; then
    if [ -f "`command -v lximage-qt`" ]; then
        openImageAsync "$branchHeadFilePath"
    fi
    customExit "Nothing done since '$branchHeadFilePath' already exists."
fi
echo "* creating $branchHeadFilePath"
cp -f "$branchUpstreamFilePath" "$branchHeadFilePath" || customExit "Cannot cp '$branchUpstreamFilePath' '$branchHeadFilePath'"
gotMimeType="`mimetype -b $branchHeadFilePath`"
if [ "$gotMimeType" = "image/png" ]; then
    if [ -f "`command -v lximage-qt`" ]; then
        openImageAsync "$branchHeadFilePath"
    fi
elif [ "$gotMimeType" = "image/jpeg" ]; then
    if [ -f "`command -v lximage-qt`" ]; then
        openImageAsync "$branchHeadFilePath"
    fi
elif [ "$gotMimeType" = "image/bmp" ]; then
    if [ -f "`command -v lximage-qt`" ]; then
        openImageAsync "$branchHeadFilePath"
    fi
else
    openTextAsync "$branchHeadFilePath"
    if [ -d "$HOME/minetest/games/ENLIVEN" ]; then
        if [ -f "`command -v meld`" ]; then
            nohup meld "$branchHeadFilePath" "$HOME/minetest/games/ENLIVEN/$what" &
        fi
    fi
fi

eval "arr=($licenses)"
for license in "${arr[@]}"; do
    upstreamLicense="$dirUpstream/$license"
    baseLicense="$dirBase/$license"
    headLicense="$dirHead/$license"
    if [ -f "$upstreamLicense" ]; then
        echo "* updating LICENSE '$baseLicense'..."
        cp -f "$upstreamLicense" "$baseLicense" || customExit "Cannot cp -f '$upstreamLicense' '$baseLicense'"
        if [ ! -f "$headLicense" ]; then
            echo "  - also for $branchHead..."
            cp --no-clobber "$upstreamLicense" "$headLicense" || customExit "Cannot cp -f '$upstreamLicense' '$headLicense'"
        fi
    fi
    upstreamLicense="$dirUpstreamParent/$license"
    baseLicense="$dirBaseParent/$license"
    headLicense="$dirHeadParent/$license"
    if [ -f "$upstreamLicense" ]; then
        echo "* updating LICENSE '$baseLicense'..."
        cp -f "$upstreamLicense" "$baseLicense" || customExit "Cannot cp -f '$upstreamLicense' '$baseLicense'"
        if [ ! -f "$headLicense" ]; then
            echo "  - also for $branchHead..."
            cp --no-clobber "$upstreamLicense" "$headLicense" || customExit "Cannot cp -f '$upstreamLicense' '$headLicense'"
        fi
    fi
    upstreamLicense="$dirUpstreamGrandParent/$license"
    baseLicense="$dirBaseGrandParent/$license"
    headLicense="$dirHeadGrandParent/$license"
    if [ -f "$upstreamLicense" ]; then
        echo "* updating '$baseLicense'..."
        cp -f "$upstreamLicense" "$baseLicense" || customExit "Cannot cp -f '$upstreamLicense' '$baseLicense'"
        if [ ! -f "$headLicense" ]; then
            echo "  - also for $branchHead..."
            cp --no-clobber "$upstreamLicense" "$headLicense" || customExit "Cannot cp -f '$upstreamLicense' '$headLicense'"
        fi
    fi
done

echo "Done."
echo "To apply, set BUCKET_GAME then:"
echo "cd EnlivenMinetest && git pull && rsync -rtv Bucket_Game-branches/$branch/ \$BUCKET_GAME"
echo
