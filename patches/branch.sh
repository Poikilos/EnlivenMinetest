#!/bin/bash
master=~/minetest/games/Bucket_Game
branches=~/git/1.pull-requests/Bucket_Game-branches
if [ ! -d "$branches" ]; then
    mkdir -p "$branches" || customDie "Failed to mkdir -p '$branches'"
    echo "Created '$branches'"
fi

customDie() {
    errcode=1
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    if [ ! -z "$2" ]; then errcode=$2; fi
    exit $errcode
}

usage() {
    cat<<END

Usage
=====

Example:
  branch mods/default/textures/default_gravel.png --branch gravel-patch

* Specify a path relative to master.

Settings:
master=$master
branches=$branches

END
}

masterSub=
branchSub=
masterFile=
branchFile=
next=
branch=
partial=

for var in "$@"
do
    if [ "@$var" = "@--branch" ]; then
        next="branch"
    else
        if [ "@$next" = "@branch" ]; then
            # NOT -p on purpose--guarantee normal name (and no spaces)
            branch="$var"
            mkdir "$branches/$branch" || customDie "The new branch name must be valid directory name--can't create '$branches/$var'"
        else
            tryPath="$master/$var"
            if [ -f "$tryPath" ]; then
                partial=$var
            else
                customDie "File does not exist: '$tryPath'"
            fi
        fi
        next=
    fi
done

if [ -z "$branch" ]; then
    usage
    customDie "You must specify a branch name"
fi

if [ -z "$partial" ]; then
    usage
    customDie "You must specify a file to fork"
fi

masterFile="$master/$partial"
branchFile="$branches/$branch"
masterSub="`dirname "$masterFile"`"
branchSub="`dirname "$branchFile"`"


parent=`dirname "$masterSub"`
if [ ! -d "$branchSub" ]; then
    echo "* creating '$branchSub'"
    #mkdir -p "$branchSub"
fi
if [ ! -f "$branchFile" ]; then
    #cp "$masterFile" "$branchFile"
    echo "Copied '$masterFile'"
    echo "to '$branchFile'"
else
    echo "Already exists: '$branchFile'"
fi
