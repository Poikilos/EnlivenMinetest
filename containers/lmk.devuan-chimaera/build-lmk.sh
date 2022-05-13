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
    printf "Warning: the Docker image isn't up to date. Unzipping manually..."
    printf "checking for unzip..."
    container_unzip="`which unzip`"
    if [ "@$container_unzip" = "@" ]; then
        echo "NOT FOUND. Installing..."
        # This should never happen if the Dockerfile was used.
        apt-get update
        if [ $? -ne 0 ]; then exit 1; fi
        apt-get install -y unzip
        if [ $? -ne 0 ]; then exit 1; fi
        container_unzip="`which unzip`"
        if [ "@$container_unzip" = "@" ]; then
            echo "Error: Installing unzip in the container did not succeed. Install unzip inside the container manually then try again, or extract linux-minetest-kit such that $contained_good_repo_flag_path exists."
            exit 1
        fi
    else
        echo "FOUND"
    fi
    # sudo docker container run $image_name unzip xvf $contained_arc -d $contained_repos
    echo "* extracting $contained_arc"
    unzip $contained_arc -d $contained_repos
    # -d: is destination, like -C or --directory for tar.
    # -v: verbose (prevents extraction)
    if [ $? -ne 0 ]; then
        echo "Error: unzip failed within the container. Install unzip inside the container manually then try again, or extract linux-minetest-kit such that $contained_good_repo_flag_path exists."
        exit 1
    fi
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



if [ "@$contained_user" = "@" ]; then
    echo "Error: contained_user can't be blank, or checking for the user within the container will not work."
    exit 1
fi

id -u $contained_user
if [ $? -ne 0 ]; then
    printf "* creating $contained_user in container $container_name..."
    adduser --disabled-password --gecos "" $contained_user --home $contained_home
    if [ $? -ne 0 ]; then
        echo "FAILED"
        exit 1
    else
        echo "OK"
    fi
else
    echo "* using the $container_name container's existing contained_user: $contained_user"
fi

# sudo docker container run --name $container_name $image_name ls $contained_repos

# chown -R $contained_user $contained_repos
# ^ Usually you could do this, but run as root since this script is used to test the safety of linux-minetest-kit:

# curl https://raw.githubusercontent.com/poikilos/EnlivenMinetest/master/install-minetest-build-deps.sh --output /opt/install-minetest-build-deps.sh
# chmod +x $repo_build_assumptions_cmd
# $repo_build_assumptions_cmd

# ^ moved to Dockerfile

if [ ! -d "$contained_repo" ]; then
    echo "Error: \"$contained_repo\" doesn't exist."
    exit 1
fi
echo "* building libraries using $repo_build_libs_cmd..."
cd "$contained_repo"
if [ $? -ne 0 ]; then exit 1; fi
$repo_build_libs_cmd
if [ $? -ne 0 ]; then exit 1; fi
echo
echo
echo
echo
echo
echo
echo "* building program using $repo_build_cmd..."
$repo_build_cmd
code=$?
if [ $code -ne 0 ]; then
    echo "$repo_build_cmd FAILED (code $code)"
    exit $code
fi
