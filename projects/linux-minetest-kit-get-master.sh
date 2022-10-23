#!/bin/bash
WHY_FORCE=""
if [ "x$FORCE_LMK_UPDATE" = "x" ]; then
    FORCE_LMK_UPDATE=false
elif "x$FORCE_LMK_UPDATE" = "xtrue" ]; then
    WHY_FORCE="FORCE_LMK_UPDATE=true"
fi
if [ "x$1" = "x--force" ]; then
    FORCE_LMK_UPDATE=true
    WHY_FORCE="--force"
fi

if [ "x$LOCAL_MASTER" = "x" ]; then
    LOCAL_MASTER="$HOME/src/minetest.org-master"
fi
echo "LOCAL_MASTER=\"$LOCAL_MASTER\""

mkdir -p "$LOCAL_MASTER"
code=$?
if [ $code -ne 0 ]; then exit $code; fi

cd "$LOCAL_MASTER"
code=$?
if [ $code -ne 0 ]; then exit $code; fi

DO_UPDATE_ZIP=true
DO_EXTRACT=true
TRY_VERSION="`date '+%y%m%d'`"
EXISTING_VERSION=""
EXISTING_NAME="linux-minetest-kit"
GOT_NAME="linux-minetest-kit"
GOT_VERSION=""
TRY_NAME="linux-minetest-kit-$TRY_VERSION"
printf "* checking for '$TRY_NAME' or '$EXISTING_NAME'..."

FOUND=false
# Wipe out the linux-minetest-kit/ first if do_update so it is ready to use:
if [ -d "$EXISTING_NAME" ]; then
    FOUND=true
    if [ ! -f "$EXISTING_NAME/release.txt" ]; then
        echo "Error: '`realpath $EXISTING_NAME`' doesn't contain release.txt."
        exit 1
    fi
    EXISTING_VERSION="`cat $EXISTING_NAME/release.txt`"
    if [ "x$FORCE_LMK_UPDATE" != "true" ]; then
        echo "Warning: using existing '`realpath $EXISTING_NAME`'. Specify --force to replace it with the remote version."
        OLD_EXISTING_NAME="$EXISTING_NAME"
        EXISTING_NAME="linux-minetest-kit-$EXISTING_VERSION"
        if [ -d "$EXISTING_NAME" ]; then
            echo "Error: '`realpath $EXISTING_NAME`' already exists and conflicts with the new '`realpath linux-minetest-kit`' which is the same version so you can remove the new linux-minetest-kit."
            exit 1
        fi
        printf "mv '$OLD_EXISTING_NAME' '$EXISTING_NAME'..."
        mv '$OLD_EXISTING_NAME' '$EXISTING_NAME'
        code=$?
        if [ $code -ne 0 ]; then
            echo "FAILED"
            exit $code;
        else
            echo "OK"
        fi
        echo "'`realpath $EXISTING_NAME`' is ready to use."
        DO_EXTRACT=false
    else
        echo "removing $EXISTING_NAME ($WHY_FORCE)."
        rm -Rf "$EXISTING_NAME"
    fi
fi

if [ -d "$TRY_NAME" ]; then
    FOUND=true
    if [ "x$FORCE_LMK_UPDATE" != "true" ]; then
        DO_UPDATE_ZIP=false
        EXISTING_NAME="$TRY_NAME"
        EXISTING_VERSION="$TRY_VERSION"
        echo "Warning: using existing '`realpath $TRY_NAME`'. Specify --force to replace it with the remote version."
        DO_EXTRACT=false
        echo "'`realpath $TRY_NAME`' is ready to use."
    # else true, so check for it later if version matches.
    else
        echo "Found `realpath $TRY_NAME` (will be replaced if same version as remote due to $WHY_FORCE)"
    fi
fi

if [ "$FOUND" != "true" ]; then
    echo "no."
fi


if [ "x$DO_UPDATE_ZIP" = "xtrue" ]; then
    printf "* checking for linux-minetest-kit.zip..."
    if [ -f "linux-minetest-kit.zip" ]; then
        if [ "x$FORCE_LMK_UPDATE" != "true" ]; then
            echo "Warning: using existing '`realpath linux-minetest-kit.zip`'. Specify --force to update it."
            DO_UPDATE_ZIP=false
        else
            printf "updating..."
        fi
    else
        printf "downloading (this may take a while)..."
    fi
fi

if [ "x$DO_UPDATE_ZIP" = "xtrue" ]; then
    rsync -t minetest.io:/opt/minebest/assemble/prod/linux-minetest-kit.zip ./
    code=$?
    if [ $code -ne 0 ]; then
        echo "FAILED"
        exit $code
    else
        echo "OK"
    fi
fi

if [ "x$DO_EXTRACT" = "xtrue" ]; then
    if [ -d "linux-minetest-kit" ]; then
        echo "Error: $WHY_FORCE extracting but linux-minetest-kit still exists"
        exit 1
    fi
    printf "* extracting linux-minetest-kit in `pwd`..."
    unzip linux-minetest-kit.zip
    code=$?
    if [ $code -ne 0 ]; then
        echo "FAILED"
        exit $code
    else
        echo "OK"
    fi
    if [ ! -d "linux-minetest-kit" ]; then
        echo "Error: The structure of the archive is unknown. It extracted ok but didn't produce linux-minetest-kit/ in '`pwd`'"
        exit 1
    fi
    if [ ! -f "linux-minetest-kit/release.txt" ]; then
        echo "Error: The structure of the archive is unknown. It extracted ok but '`realpath linux-minetest-kit`' doesn't contain a release.txt file."
        exit 1
    fi
    GOT_VERSION="`cat linux-minetest-kit/release.txt`"
    if [ -z "$GOT_VERSION" ]; then
        echo "Error: The structure of the archive is unknown. It extracted ok but '`realpath linux-minetest-kit/release.txt`' is blank."
        exit 1
    fi
    echo "* extracted version=$GOT_VERSION"
    GOT_NAME="linux-minetest-kit-$GOT_VERSION"
    if [ -d "$GOT_NAME" ]; then
        if [ "x$FORCE_LMK_UPDATE" != "true" ]; then
            echo "Warning: using existing '`realpath $GOT_NAME`'. Specify --force (or delete it and re-run this script normally) to replace it with the remote version."
            echo "'`realpath $GOT_NAME`' is ready to use."
        else
            echo "* merging (and moving) '`realpath linux-minetest-kit`' into '`realpath $GOT_NAME`'..."
            rsync -rtv --delete --remove-source-files linux-minetest-kit/ "$GOT_NAME"
            code=$?
            if [ $code -ne 0 ]; then
                echo "FAILED"
                exit $code
            else
                echo "OK"
            fi
            if [ -d "linux-minetest-kit" ]; then
                rm -Rf linux-minetest-kit
                code=$?
                if [ $code -ne 0 ]; then
                    echo "Warning: 'rm -Rf linux-minetest-kit' failed in '`pwd`'. Remove the incomplete copy manually."
                fi
            fi
            echo "'`realpath $GOT_NAME`' is ready to use."
        fi
    else
        mv linux-minetest-kit "$GOT_NAME"
        code=$?
        printf "* mv 'linux-minetest-kit' '`realpath $GOT_NAME`'..."
        if [ $code -ne 0 ]; then exit $code; fi
        echo "'`realpath $GOT_NAME`' is ready to use."
    fi
fi



echo Done
