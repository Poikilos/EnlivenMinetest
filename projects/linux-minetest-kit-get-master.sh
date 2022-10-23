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
MASTER_PATH=""
MASTER_VERSION=""
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
        MASTER_PATH="`realpath $EXISTING_NAME`"
        echo "'$MASTER_PATH' (EXISTING_NAME) is ready to use."
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
        MASTER_PATH="`realpath $TRY_NAME`"
        echo "'$MASTER_PATH' (local copy: $TRY_NAME today's datestamp) is ready to use."
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
            MASTER_PATH="`realpath $GOT_NAME`"
            echo "'$MASTER_PATH' (GOT_NAME from previously-extracted local copy's version) is ready to use."
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
            MASTER_PATH="`realpath $GOT_NAME`"
            echo "'$MASTER_PATH' (GOT_NAME from version downloaded) is ready to use."
        fi
    else
        mv linux-minetest-kit "$GOT_NAME"
        code=$?
        printf "* mv 'linux-minetest-kit' '`realpath $GOT_NAME`'..."
        if [ $code -ne 0 ]; then exit $code; fi
        MASTER_PATH="`realpath $GOT_NAME`"
        echo "'$MASTER_PATH' (GOT_NAME newly downloaded and renamed to that) is ready to use."
    fi
fi


# if [ -z "$GOT_VERSION" ]; then
#     echo "Error: GOT_VERSION is blank."
#     exit 1
# fi

if [ -z "$MASTER_PATH" ]; then
    echo "Error: MASTER_PATH was not set (This path of logic is incomplete)."
    exit 1
fi

if [ ! -f "$MASTER_PATH/release.txt" ]; then
    echo "Error: MASTER_PATH $MASTER_PATH doesn't contain release.txt"
    exit 1
fi
MASTER_VERSION="`cat $MASTER_PATH/release.txt`"

VERSION="$MASTER_VERSION"


# VERSION="$GOT_VERSION"
BG_VERSIONS=$HOME/bucket_game-versions
mkdir -p "$BG_VERSIONS"


if [ -z "$VERSION" ]; then
    echo
    echo "error: cat release.txt in $MASTER_PATH did not produce a version."
    echo
    exit 1
fi
echo "linux-minetest-kit VERSION=$VERSION"
cat <<END

# build via:
cd "$MASTER_PATH"
mtcompile-libraries.sh build
# or to give the program out (to do the later step and use the --makeprod option for creating a binary that will run on computers with different configurations), instead run: env DOBOOTSTRAP=1 ./mtcompile-libraries.sh build
perl mtcompile-program.pl build --finetest --client
# ^ based on MoNTE48's protocol-detecting client
# or: perl mtcompile-program.pl build --classic --client
# ^ minetest.org MT6
# or: perl mtcompile-program.pl build --trolltest --client
# ^ based on MT5 client
END
echo
echo "Checking destination..."
DST_MT="$HOME/minetest"  # should be a symlink to the latest version such as ~/minetest-220509
DST_DST_MT="`readlink $DST_MT`"
if [ -z "$DST_DST_MT" ]; then
    echo "DST_MT=$DST_MT"
else
    echo "DST_MT=$DST_MT -> $DST_DST_MT"
fi

echo

echo "Processing bucket_game..."

BG_VERSION=$VERSION

cd $MASTER_PATH/mtsrc/game
code=$?
if [ $code -ne 0 ]; then
    exit $code
fi
DST_BG_ARCHIVE=$BG_VERSIONS/bucket_game-$VERSION.tgz
if [ ! -f "$DST_BG_ARCHIVE" ]; then cp bucket_game.tgz "$DST_BG_ARCHIVE"; fi
cd $BG_VERSIONS/
SRC_GAME_NAME=bucket_game-$VERSION
SRC_GAME_PATH=$BG_VERSIONS/$SRC_GAME_NAME
if [ ! -d "$SRC_GAME_PATH" ]; then
    tar xfv "$DST_BG_ARCHIVE"
    mv bucket_game "$SRC_GAME_PATH"
else
    echo "* using existing '$SRC_GAME_PATH' (not extracting '$DST_BG_ARCHIVE')"
fi
BG_VERSION=$VERSION


if [ -f "$SRC_GAME_PATH/release.txt" ]; then BG_VERSION=`cat "$SRC_GAME_PATH/release.txt"`; fi
if [ "$BG_VERSION" != "$VERSION" ]; then
    echo "Warning: The bucket_game is version $BG_VERSION but the linux-minetest-kit is version $VERSION. Renaming..."
    OLD_DST_BG_ARCHIVE="$DST_BG_ARCHIVE"
    DST_BG_ARCHIVE=$BG_VERSIONS/bucket_game-$BG_VERSION.tgz
    echo "mv '$OLD_DST_BG_ARCHIVE' '$DST_BG_ARCHIVE'"
    mv "$OLD_DST_BG_ARCHIVE" "$DST_BG_ARCHIVE"
    TMP_SRC_GAME_PATH="$SRC_GAME_PATH"
    SRC_GAME_NAME=bucket_game-$BG_VERSION
    SRC_GAME_PATH=$BG_VERSIONS/$SRC_GAME_NAME
    if [ -d "$SRC_GAME_PATH" ]; then
        echo "Warning: $SRC_GAME_PATH already exists, so $TMP_SRC_GAME_PATH will be removed."
        rm -Rf "$TMP_SRC_GAME_PATH"
    else
        echo "mv '$TMP_SRC_GAME_PATH' '$SRC_GAME_PATH'"
        mv "$TMP_SRC_GAME_PATH" "$SRC_GAME_PATH"
        code=$?
        if [ $code -ne 0 ]; then exit $code; fi
    fi
fi
echo "OK"
echo
echo "'$SRC_GAME_PATH' is ready to use such as via:"
# RM_DST_BG_PREFIX="   "
# if [ ! -d "$DST_MT/games/bucket_game" ]; then
#     RM_DST_BG_PREFIX="#  (doesn't exist so not necessary) "
# fi
# echo "$RM_DST_BG_PREFIX rm -Rf $DST_MT/games/bucket_game"
echo "rsync -rt --delete $SRC_GAME_PATH/ $DST_MT/games/bucket_game"
if [ -d "$DST_MT/games/bucket_game" ]; then
    DST_BG_VERSION="`cat $DST_MT/games/bucket_game/version.txt`"
    # ^ Poikilos-style version writeup with patch names
    if [ -z "$DST_BG_VERSION" ]; then
        DST_BG_VERSION="`cat $DST_MT/games/bucket_game/release.txt`"
        # ^ new style suggested by Poikilos and implemented by OldCoder
    fi
    if [ -z "$DST_BG_VERSION" ]; then
        echo "^ BE CAREFUL: The version is not known, so make a backup before doing this command!"
    elif [ "x$DST_BG_VERSION" != "x$BG_VERSION" ]; then
        echo "^ BEFORE PROCEEDING: The source version is $BG_VERSION but the destination version is '$DST_BG_VERSION', so make a backup before doing this command!"
    fi
fi

echo
