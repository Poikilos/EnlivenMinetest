#!/bin/bash
cd /opt
if [ $? -ne 0 ]; then
    exit 1
fi
source lmk.rc
me=build-lmk.sh
if [ $? -ne 0 ]; then
    exit 1
fi

if [ "@$contained_repo" = "@" ]; then
    echo "Error: contained_repo can't be blank or checking for its files in the container won't work."
    exit 1
fi

# ls $contained_repo
echo "* checking for $contained_good_repo_flag_path on the destination..."
ls $contained_good_repo_flag_path > /dev/null
if [ $? -ne 0 ]; then
    echo "NOT FOUND"
    exit 1
else
    echo "FOUND (already extracted)"
fi

# ls $contained_repo > /dev/null
ls $contained_good_repo_flag_path > /dev/null
if [ $? -ne 0 ]; then
    echo "Error: extracting linux-minetest-kit.zip in the container didn't work. Extract linux-minetest-kit.zip to $contained_repos such that $contained_good_repo_flag_path exists in the container and try again."
    exit 1
else
    echo "* detected $contained_good_repo_flag_path (So the source directory is assumed to be ok)"
fi

if [ ! -d "$contained_repo" ]; then
    echo "Error: \"$contained_repo\" doesn't exist."
    exit 1
fi
echo "* building libraries using $repo_build_libs_cmd..."
cd "$contained_repo"
if [ $? -ne 0 ]; then exit 1; fi
# $repo_build_libs_cmd
# if [ $? -ne 0 ]; then exit 1; fi
echo
echo "* building program using $repo_build_cmd..."
$repo_build_cmd
code=$?
if [ $code -ne 0 ]; then
    echo "$repo_build_cmd FAILED (code $code)"
    exit $code
else
    echo "SUCCESS"
    echo "Note that if you run this again, it will just compile again."
    echo
    echo "To run Minetest, follow the instructions that appear below (if you ran $docker_image_build_script_name)"
    echo
fi
