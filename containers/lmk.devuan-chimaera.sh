#!/bin/bash
# See https://nextbreakpoint.com/posts/article-compile-code-with-docker.html
# sudo docker build -t lmk-devuan-chimaera-img dyne/devuan:chimaera
me=lmk.devuan-chimera.sh
docker_path="`sudo command -v docker`"
if [ ! -f "$docker_path" ]; then
    cat <<END
This script requires docker. For help, see
<https://github.com/poikilos/linux-preinstall/blob/master/doc/Docker.md>
or Docker's own documentation at
<https://docs.docker.com/engine/install/>.
END
fi
container_name="lmk-devuan-chimaera"
image_name="lmk-devuan-chimaera-img"

source $image_name/project.rc
if [ $? -ne 0 ]; then
    exit 1
fi

# sudo docker image inspect $image_name > /dev/null
sudo docker image inspect $image_name --format "* docker is looking for the image..."
# ^ appending ":latest" to the name also works.
# ^ Get matching images as a JSON list (where each has "Id" and other
#   metadata).
if [ $? -ne 0 ]; then
    if [ ! -d "$local_img_dir" ]; then
        echo "Error: \"$local_img_dir\" (local_img_dir for storing $SRC_URL) doesn't exist."
        exit 1
    fi

    if [ ! -f "$container_build_blob" ]; then
        echo "* downloading $SRC_URL to $DL_SRC_PATH..."
        curl "$SRC_URL" --progress-bar --output "$DL_SRC_PATH"
        if [ $? -ne 0 ]; then
            exit 1
        fi
        if [ ! -f "$container_build_blob" ]; then
            echo "Error: This script requires \"$container_build_blob\"."
            exit 1
        fi
    else
        echo "* using existing \"$container_build_blob\" to build the container image"
    fi
    move_back="false"
    prerelease_path=~/Downloads/minetest.org/insider-prerelease/linux-minetest-kit-220509.zip
    if [ ! -f $container_build_blob ]; then
        if [ -f "$prerelease_path" ]; then
            move_back="true"
            echo "mv $prerelease_path $container_build_blob"
            mv $prerelease_path $container_build_blob
            if [ $? -ne 0 ]; then
                echo "* Error: the mv command failed."
                exit 1
            fi
        fi
    fi
    sudo docker build -t $image_name $local_img_dir
    code=$?
    if [ "@move_back" = "@true" ]; then
        echo "mv \"$prerelease_path\" \"$container_build_blob\""
        mv "$container_build_blob" "$prerelease_path"
        if [ $? -ne 0 ]; then
            echo "* Warning: the mv command failed."
        fi
    fi
    if [ $code -ne 0 ]; then
        exit 1
    fi
else
    echo "* The container will be built using the existing docker image $image_name"
fi

cat <<END
How to use the image:
  # docker options:
  # -i: is interactive (attach STDIN).
  # -d: is daemon mode.

  sudo docker image ls
  # ^ See what images are installed (one image can be used for many containers).

  sudo docker rmi $image_name
  # ^ Remove a docker image (This is necessary after updating the unversioned Docker image to avoid cached RUN commands from doing nothing when the script after RUN changes).

  sudo docker image prune
  # ^ Prune unused images (For this to do anything, first delete containers using the image).

  sudo docker ps -a
  # ^ List containers and show NAMES (The name is necessary for certain subcommands such as exec which operate on a running container).

  sudo docker start $container_name
  # ^ Start a container.

  sudo docker run $container_name
  # ^ "run" is merely a combination of "create" and "start"

  sudo docker -w $contained_repo exec $container_name ls -l $contained_repos
  # ^ Execute a command in a running container (exec shows an error if the container isn't running).
  # This will not work if the run/start command that started the container isn't a command that keeps it open (runs indefinitely)!
  # w: working directory

  sudo docker stop $container_name
  # ^ Stop a container by name (See <https://www.tecmint.com/name-docker-containers/>)
  #   You must use the container name (as determined using the "ps" subcommand), not the image name.

  sudo docker container run -it $image_name /bin/bash
  # ^ Run an interactive terminal (Type 'exit' to exit)
  #   (based on <https://phoenixnap.com/kb/docker-run-command-with-examples>)

  sudo docker attach $container_name
  # ^ Attach your current terminal to a running container (See
  #   <https://docs.docker.com/engine/reference/commandline/attach/>).


  sudo docker rm --force $container_name
  # ^ Delete a container by its name.
  # --force: kill and delete running containers as well.

END

# sudo docker container run -d --name $image_name unzip xvf $contained_arc -C $contained_repos
container_Id=`sudo docker ps -aqf "name=$container_name"`
# ^ ONLY works with container_name not image_name

cat > /dev/null <<END
if [ "@$container_Id" = "@" ]; then
    echo "* creating a container named $container_name"
    sudo docker create --name=$container_name $image_name
    # ^ output is the Id
    if [ $? -ne 0 ]; then
        echo "FAILED"
        exit 1
    fi
    container_Id=`sudo docker ps -aqf "name=$container_name"`
    if [ -z "$container_Id" ]; then
        echo "The container_Id couldn't be obtained from sudo docker ps -aqf \"name=$container_name\", so creating the named image failed."
        exit 1
    fi
fi
echo "container_Id=$container_Id"
END

printf "starting the docker image..."
# sudo docker start $container_name
# ^ NOTE: start is useless here since it won't stay open unless the
#   command is set to "bash" or something, which isn't desirable.
#   Therefore, use run instead of exec below.
# ^ output is $container_name
sudo docker run --name $container_name $image_name /opt/build-lmk.sh
if [ $? -ne 0 ]; then
    echo "FAILED"
    exit 1
else
    echo "OK"
fi
# ^ NOTE: start is useless here since it won't stay open unless the
#   command is set to "bash" or something, which isn't desirable.
#   Therefore, use run instead of exec below.


if [ "@$contained_repo" = "@" ]; then
    echo "Error: contained_repo can't be blank or checking for its files in the container won't work."
    exit 1
fi

contained_good_repo_flag_path="$contained_repo/$good_repo_flag_name"

# sudo docker exec $container_name ls $contained_repo
echo "* checking for $contained_good_repo_flag_path on the destination..."
sudo docker exec $container_name ls $contained_good_repo_flag_path > /dev/null
if [ $? -ne 0 ]; then
    printf "NO...checking for unzip..."
    container_unzip="`sudo docker exec $container_name which unzip`"
    if [ "@$container_unzip" = "@" ]; then
        echo "NO. Installing..."
        # This should never happen if the Dockerfile was used.
        sudo docker exec $container_name apt-get update
        if [ $? -ne 0 ]; then exit 1; fi
        sudo docker exec $container_name apt-get install -y unzip
        if [ $? -ne 0 ]; then exit 1; fi
        container_unzip="`sudo docker exec $container_name which unzip`"
        if [ "@$container_unzip" = "@" ]; then
            echo "Error: Installing unzip in the container did not succeed. Install unzip inside the container manually then try again, or extract linux-minetest-kit such that $contained_good_repo_flag_path exists."
            exit 1
        fi
    else
        echo "FOUND"
    fi
    # sudo docker container run $image_name unzip xvf $contained_arc -d $contained_repos
    echo "* extracting $contained_arc"
    sudo docker exec $container_name unzip $contained_arc -d $contained_repos
    # -d: is destination, like -C or --directory for tar.
    # -v: verbose (prevents extraction)
    if [ $? -ne 0 ]; then
        echo "Error: unzip failed within the container. Install unzip inside the container manually then try again, or extract linux-minetest-kit such that $contained_good_repo_flag_path exists."
        exit 1
    fi
else
    echo "FOUND (already extracted)"
fi

# sudo docker exec $container_name ls $contained_repo > /dev/null
sudo docker exec $container_name ls $contained_good_repo_flag_path > /dev/null
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

sudo docker exec $container_name id -u $contained_user
if [ $? -ne 0 ]; then
    printf "* creating $contained_user in container $container_name..."
    sudo docker exec $container_name adduser --disabled-password --gecos "" $contained_user --home $contained_home
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

# sudo docker exec $container_name chown -R $contained_user $contained_repos
# ^ Usually you could do this, but run as root since this script is used to test the safety of linux-minetest-kit:

# sudo docker exec $container_name curl https://raw.githubusercontent.com/poikilos/EnlivenMinetest/master/install-minetest-build-deps.sh --output /opt/install-minetest-build-deps.sh
# sudo docker exec $container_name chmod +x $repo_build_assumptions_cmd
# sudo docker exec $container_name $repo_build_assumptions_cmd

# ^ moved to Dockerfile

echo "* building libraries using $repo_build_libs_cmd..."
sudo docker exec -w $contained_src $container_name $repo_build_libs_cmd
if [ $? -ne 0 ]; then exit 1; fi
# echo "* building program using $repo_build_cmd..."
# sudo docker exec -w $contained_src $container_name $repo_build_cmd
if [ $? -ne 0 ]; then exit 1; fi
# -w: working directory


# How to use docker-compose (See <https://docs.docker.com/compose/>):
# "1. Define your app’s environment with a Dockerfile so it can be reproduced anywhere."
# "2. Define the services that make up your app in docker-compose.yml so they can be run together in an isolated environment."
# "3. Run docker compose up and the Docker compose command starts and runs your entire app. You can alternatively run docker-compose up using the docker-compose binary."
