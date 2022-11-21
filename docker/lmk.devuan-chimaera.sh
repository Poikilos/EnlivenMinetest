#!/bin/bash
# See https://nextbreakpoint.com/posts/article-compile-code-with-docker.html
# sudo docker build -t lmk-devuan-chimaera-img dyne/devuan:chimaera
docker_path="`sudo bash -c 'command -v docker'`"
ENABLE_CLASSIC=false
for var in "$@"
do
    if [ "@$var" = "@--classic" ]; then
        ENABLE_CLASSIC=true
    fi
done

if [ ! -f "$docker_path" ]; then
    cat <<END
This script requires docker. For help, see
<https://github.com/poikilos/linux-preinstall/blob/master/doc/Docker.md>
or Docker's own documentation at
<https://docs.docker.com/engine/install/>.
END
fi
# container_name="linux-minetest-kit-build-libraries-devuan-chimaera"
# ^ This is no longer necessary since the IMAGE does the building (build was moved to Dockerfile)
this_rc="lmk.devuan-chimaera.rc"
if [ ! -f "$this_rc" ]; then
    echo "Error: $0 must run in the directory containing $this_rc."
    exit 1
fi
source $this_rc
if [ $? -ne 0 ]; then exit 1; fi
source finetestserver.rc
if [ $? -ne 0 ]; then exit 1; fi
if [ ! -d "$libraries_image_dir" ]; then
    echo "Error: $0 must run from the directory containing the container image directory: $libraries_image_dir"
    exit 1
fi
# ^ libraries_image_dir has to be in the same directory as Dockerfile or
#   the COPY command in the Dockerfile won't work.

source $libraries_image_dir/lmk.rc
if [ $? -ne 0 ]; then
    exit 1
fi

if [ "@$DL_SRC_PATH" = "@" ]; then
    # DL_SRC_PATH="$HOME/Downloads/$DL_SRC_NAME"
    DL_SRC_PATH="$libraries_image_dir"
    # ^ $DL_SRC_PATH has to be in the same directory as Dockerfile or
    #   the COPY command in the Dockerfile won't work.
    #   The file should be added to .gitignore for the reason that it
    #   is in the repo in the docker image directory.
fi


# sudo docker image inspect $libraries_image > /dev/null
sudo docker image inspect $libraries_image --format "* docker is looking for the image..."
# ^ appending ":latest" to the name also works.
# ^ Get matching images as a JSON list (where each has "Id" and other
#   metadata).
if [ $? -ne 0 ]; then
    if [ ! -d "$libraries_image_dir" ]; then
        echo "Error: \"$libraries_image_dir\" (libraries_image_dir for storing $SRC_URL) doesn't exist in \"`pwd`\"."
        exit 1
    fi

    echo "* building image $libraries_image..."
    if [ ! -f "$libraries_image_build_blob" ]; then
        echo "* downloading $SRC_URL to $DL_SRC_PATH..."
        curl "$SRC_URL" --progress-bar --output "$DL_SRC_PATH"
        if [ $? -ne 0 ]; then
            exit 1
        fi
        if [ ! -f "$libraries_image_build_blob" ]; then
            echo "Error: This script requires \"$libraries_image_build_blob\"."
            exit 1
        fi
    else
        echo "* using existing \"$libraries_image_build_blob\" to build the container image"
    fi
    cp ../install-minetest-build-deps.sh $libraries_image_dir/
    # ^ This copy of it is in .gitignore.
    if [ $? -ne 0 ]; then
        echo "Error: 'cp ../install-minetest-build-deps.sh $libraries_image_dir/' failed."
        exit 1
    fi
    move_back="false"
    if [ ! -f $libraries_image_build_blob ]; then
        if [ -f "$prerelease_path" ]; then
            move_back="true"
            echo "mv $prerelease_path $libraries_image_build_blob"
            mv $prerelease_path $libraries_image_build_blob
            if [ $? -ne 0 ]; then
                echo "* Error: the mv command failed."
                exit 1
            fi
        fi
    fi
    sudo docker build -t $libraries_image $libraries_image_dir
    # -t: Name and optionally a tag in the 'name:tag' format
    code=$?
    if [ "@move_back" = "@true" ]; then
        echo "mv \"$prerelease_path\" \"$libraries_image_build_blob\""
        mv "$libraries_image_build_blob" "$prerelease_path"
        if [ $? -ne 0 ]; then
            echo "* Warning: the mv command failed."
        fi
    fi
    if [ $code -ne 0 ]; then
        exit 1
    fi
else
    echo "* The container will be built using the existing docker image $libraries_image"
fi

# sudo docker container run -d --name $libraries_image unzip xvf $contained_arc -C $contained_repos
container_Id=`sudo docker ps -aqf "name=$container_name"`
# ^ ONLY works with container_name not libraries_image

cat > /dev/null <<END
if [ "@$container_Id" = "@" ]; then
    echo "* creating a container named $container_name"
    sudo docker create --name=$container_name $libraries_image
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

END

# echo "building within the container..."
# sudo docker start $container_name
# ^ NOTE: start is useless here since it won't stay open unless the
#   command is set to "bash" or something, which isn't desirable.
#   Therefore, use run instead of exec below.
# ^ output is $container_name

if [ "@$container_Id" != "@" ]; then
    echo "* The container already appears to be set up, so checking for the image will not be attempted."
else
    echo "There is no container_Id for container_name=$container_name, so checking for image:"
    sudo docker image inspect $server_image --format "* docker is looking for the image..."
    if [ $? -ne 0 ]; then
        echo "NOT FOUND, so:"
        echo "* building $server_image ($server_image_dir inherits $libraries_image, so using built libraries from that should work)..."
        if [ ! -d "$server_image_dir" ]; then
            echo "Error: \"$server_image_dir\" doesn't exist in `pwd`."
            exit 1
        fi
        sudo docker build -t $server_image $server_image_dir
        # ^ ./mtcompile-program.pl --build --finetest --server returns 1 for some reason, so there is a custom build script used in the Dockerfile
        # -t: Name and optionally a tag in the 'name:tag' format
        if [ $? -ne 0 ]; then
            exit 1
        fi
    else
        echo "* using existing $server_image"
    fi
fi

if [ "@$container_Id" = "@" ]; then
    # sudo docker run --name $container_name $libraries_image $run_all_build_commands_script
    # ^ build was moved to the Dockerfile
    if [ "@$finetestserver_bin" = "@" ]; then
        echo "Error: The image is not fully described since finetestserver_bin is blank. No container will be created."
        exit 1
    fi
    echo "* creating container $container_name from image $server_image"
    sudo docker run --name $container_name $server_image $finetestserver_bin
    code=$?
    if [ $code -ne 0 ]; then
        cat <<END
* $finetestserver_bin FAILED

- Remove the container as follows:
  sudo docker rm --force $container_name
- Update the image as follows:
  sudo docker rm --force $container_name
  sudo docker rmi $server_image
  sudo docker image prune --force
  # --force: Don't prompt for confirmation.

- Then you may try again:
  $0

- However, first view errors and note the reason for the problem.
  - If the program didn't complete startup view the startup error via:
    sudo docker start $container_name --attach
  - If the progam has an "ERROR[Main]" error, you need to edit
    minetest.conf and then try the start subcommand above again.

END
        exit $code
    else
        echo "* $finetestserver_bin completed OK"
    fi
else
    echo "* using existing container named $container_name with Id $container_Id."
    # exit 0
fi
echo
# echo "If the build output appeared successful, ignore the error above and create the minetest client image as follows:"
# echo "$0 --client"

# NOTE: The "start" subcommand is useless here since it won't stay open
# unless the command is set to "bash" or something, which wouldn't be
# an automated image. The proper way to modify a container is to make
# a new image from it
# and
#   sudo docker start $container_name
# doesn't work (The script specified by "run" earlier doesn't run) so:

# echo "* Creating client image..."
# docker commit $container_Id $client_classic_image
# sudo docker container run --name $client_classic_container $client_classic_image $client_bin_path
# ^ This doesn't work for the client due to:
# "2022-05-13 03:59:00: ERROR[Main]: Subgame specified in default_game [Bucket_Game] is invalid.
# 2022-05-13 03:59:00: ERROR[Main]: Irrlicht: Error: Need running XServer to start Irrlicht Engine.
# 2022-05-13 03:59:00: ERROR[Main]: Irrlicht: Could not open display, set DISPLAY variable"
# as expected. See <https://www.howtogeek.com/devops/how-to-run-gui-applications-in-a-docker-container/>.
# Therefore:

# echo "* Creating image \"$server_image\"..."
# sudo docker commit $container_Id $server_image
# if [ $? -ne 0 ]; then
#     echo "FAILED (sudo docker commit $container_Id $server_image)"
# fi
# echo "* Running $server_bin_path in container \"$server_container\""
# sudo docker container run --name $server_container $server_image $server_bin_path
# if [ $? -ne 0 ]; then
#     echo "FAILED (sudo docker container run --name $server_container $server_image $server_bin_path)"
# fi
# ^ Build the server as a separate step instead (see further up)


cat <<END
How to use the image:
  # docker options:
  # -i: is interactive (attach STDIN).
  # -d: is daemon mode.

  sudo docker image ls
  # ^ See what images are installed (one image can be used for many containers).

  sudo docker rmi $libraries_image
  # ^ Remove a docker image (This is necessary after updating the unversioned Docker image to avoid cached RUN commands from doing nothing when the script after RUN changes).

  sudo docker image prune --force
  # ^ Prune unused images (For this to do anything, first delete containers using the image).
  # --force: Do not ask for confirmation.

  sudo docker ps -a
  # ^ List containers and show NAMES (The name is necessary for certain subcommands such as exec which operate on a running container).
  # -a: Show all containers including stopped ones.

  sudo docker start $container_name
  # ^ Start a container. This will merely run $run_all_build_commands_script again since that is the container's main process.

  sudo docker start $container_name --attach
  # ^ Show messages while starting a container.

  sudo docker logs $container_Id
  # ^ Show logs for a container.

  sudo docker attach $container_name
  # ^ attach the current terminal to a running container.

  sudo docker run --name $container_name $server_image $finetestserver_bin
  # ^ "run" is merely a combination of "create" and "start"

  sudo docker -w $contained_repo exec $container_name ls -l $contained_repos
  # ^ Execute a command in a running container (exec shows an error if the container isn't running).
  # This will not work if the run/start command that started the container isn't a command that keeps it open (runs indefinitely)!
  # That is because the Dockerfile ENTRYPOINT (or if customized on a per-container basis, the "docker run" command) specifies the entry point (permanently) for the container.
  # If you need a container that has changes after $run_all_build_commands_script runs or runs a different command, you must use the "commit" subcommand to create a new image.
  # w: working directory

  sudo docker stop $container_name
  # ^ Stop a container by name (See <https://www.tecmint.com/name-docker-containers/>)
  #   You must use the container name (as determined using the "ps" subcommand), not the image name.

  sudo docker container run -it $libraries_image /bin/bash
  # ^ Run an interactive terminal (Type 'exit' to exit)
  #   (based on <https://phoenixnap.com/kb/docker-run-command-with-examples>)

  sudo docker commit $container_Id $server_image
  sudo docker container run --name tmp_test_im -it $server_image /bin/bash
  # ^ Transform the container into an image and inspect the internals manually
  #   (based on <https://www.thorsten-hans.com/how-to-run-commands-in-stopped-docker-containers/>).
  #   Then: sudo docker rm --force tmp_test_im

  sudo docker attach $container_name
  # ^ Attach your current terminal to a running container (See
  #   <https://docs.docker.com/engine/reference/commandline/attach/>).

  sudo docker rm --force $container_name
  # ^ Delete a container by its name.
  # --force: kill and delete running containers as well.

  sudo docker image inspect $libraries_image
  sudo docker image inspect $server_image
  # ^ Get JSON metadata for the image.

  sudo docker container inspect $container_name
  # ^ Get JSON metadata for the container.

  - If the program didn't complete startup view the startup error via:
    sudo docker start $container_name --attach
  - If the progam has any "ERROR[Main]" error(s), you need to edit
    minetest.conf and then try the start subcommand above again.

END


# How to use docker-compose (See <https://docs.docker.com/compose/>):
# "1. Define your app’s environment with a Dockerfile so it can be reproduced anywhere."
# "2. Define the services that make up your app in docker-compose.yml so they can be run together in an isolated environment."
# "3. Run docker compose up and the Docker compose command starts and runs your entire app. You can alternatively run docker-compose up using the docker-compose binary."