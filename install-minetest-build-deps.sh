#!/bin/bash
# Do not use sudo, in case sudo is not installed (such as in some
# default installations including the dyne/devuan:chimaera docker image
# on docker hub.
me=`basename $0`
usage(){
    cat <<END
Usage:
$0 [redis] [postgres] [leveldb]

Examples:
sudo ./$me
sudo ./$me leveldb

END
}
customExit(){
    >&2 echo "Error:"
    echo "$1"
    code=1
    if [ "@$2" -ne "@" ]; then
        code=$2
    fi
    exit $code
}
me=install-minetest-build-deps.sh
if [ "$EUID" -ne 0 ]; then
    >&2 echo "Error: $me must run as root."
    exit 1
fi
enable_postgres="false"
enable_redis="false"
enable_leveldb="false"
for arg in "$@"
do
    if [ "$arg" = "redis" ]; then enable_redis="true"
    elif [ "$arg" = "postgres" ]; then enable_postgres="true"
    elif [ "$arg" = "leveldb" ]; then enable_leveldb="true"
    fi
done
usage
echo
echo "Current Options:"
echo "enable_postgres:$enable_postgres"
echo "enable_redis:$enable_redis"
echo "enable_leveldb:$enable_leveldb"
if [ "x$enable_postgres$enable_redis$enable_leveldb" = "xfalsefalsefalse" ]; then
    echo "Usage:"
    echo "$0 [redis] [postgres] [leveldb]"
fi
#if [ -f "`command -v minetest`" ]; then
#echo "* trying to remove any non-git (packaged) version first (Press Ctrl C  to cancel)..."
luajit_path="/usr/include/luajit-2.1"
ext_lua=""
#fi
sleep 1
echo "3..."
sleep 1
echo "2..."
sleep 1
echo "1..."
sleep 1
echo
this_dnf=""
if [ -f "`command -v dnf`" ]; then
    this_dnf="dnf"
else
    if [ -f "`command -v yum`" ]; then
        this_dnf="yum"
        echo "WARNING: dnf not found, reverting to yum."
    fi
fi
this_apt=""
if [ -f "`command -v apt`" ]; then
    this_apt="apt"
else
    if [ -f "`command -v apt-get`" ]; then
        this_apt="apt-get"
        echo "WARNING: apt not found, reverting to apt-get."
    fi
fi


LEVELDB_DEV_PKG="leveldb-devel"
# ^ yum- or dnf-based distros
if [ ! -z "$this_apt" ]; then
    LEVELDB_DEV_PKG="libleveldb-dev"
    echo "Using $this_apt..."
    # $this_apt -y remove minetest-server
    # $this_apt -y remove minetest
    $this_apt update
    if [ $? -ne 0 ]; then exit 1; fi
    $this_apt -y install \
        autoconf        automake       autopoint      autotools-dev   \
        bash            binutils       bison          bzip2           \
        cmake           coreutils      e2fsprogs      expat           \
        flex            fontconfig     g++            gawk            \
        gcc             gettext        git            g++-multilib    \
        gperf           grep           gzip           htop            \
        icu-devtools    intltool       joe            less            \
        libbz2-dev      libc6-dev-i386 libedit-dev    libexpat1-dev   \
        libgmp-dev      libjpeg-dev    libltdl-dev    libncurses5-dev \
        libogg-dev      libopenal-dev  libpng-dev     libreadline-dev \
        libsqlite3-dev  libssl-dev     libtool             \
        libvorbis-dev   libx11-dev     libxxf86vm-dev lynx            \
        nano            nettle-dev     p7zip-full     patch           \
        perl            pkgconf        python3        python3-dev     \
        make           ruby           sed             \
        tar             tcl            unzip          util-linux      \
        wget            xz-utils       zip            perl            \
        dnsutils        make \
    \
        libcurl4-openssl-dev  \
        libfreetype6-dev      \
        libgdk-pixbuf2.0-dev  \
        libglu1-mesa-dev      \
        libxml-parser-perl    \
        xserver-xorg-dev      \
    ;
    # NOTE: installing pkgconf removes pkg-config:
    # "pkgconf is a newer, actively maintained implementation of pkg-config that supports more aspects of the pkg-config file specification and provides a library interface that applications can use to incorporate intelligent handling of pkg-config files into themselves (such as build file generators, IDEs, and compilers)."
    # -<https://fedoraproject.org/wiki/Changes/pkgconf_as_system_pkg-config_implementation#:~:text=pkgconf%20is%20a%20newer%2C%20actively,%2C%20IDEs%2C%20and%20compilers).>
    # NOTE: build-essentials installs the following according to <https://www.cyberciti.biz/faq/debian-linux-install-gnu-gcc-compiler/>:
    cat > /dev/null <<END
    build-essential dpkg-dev fakeroot g++ g++-4.7 gcc gcc-4.7
    libalgorithm-diff-perl libalgorithm-diff-xs-perl
    libalgorithm-merge-perl libc-dev-bin libc6-dev libdpkg-perl
    libfile-fcntllock-perl libitm1 libstdc++6-4.7-dev libtimedate-perl
    linux-libc-dev make manpages-dev
END
    if [ $? -ne 0 ]; then exit 1; fi
    if [ ! -f "`command -v libtool`" ]; then
        . /etc/os-release
        if [ ! -z "$VERSION_ID" ]; then
            if [ -f "`command -v bc`" ]; then
                # bc is bash calculator (-l: mathlib)
                if [ `echo "$VERSION_ID>14.04" | bc -l` = 1 ]; then
                    $this_apt -y install libtool-bin
                    # ^ not necessary on Trusty (See
                    # <https://askubuntu.com/questions/989510/how-do-i-install-libtool-bin-on-ubuntu-14-04>).
                fi
            else
                echo "* WARNING: The bc command isn't present, so the libtool-bin package will be skipped (it is only in Ubuntu >14.04 [not known in 15.x])"
            fi
        else
            echo "* WARNING: VERSION_ID is not in /etc/os-release, so the libtool-bin package name is unknown (it is only in Ubuntu >14.04 [not known in 15.x])"
            echo "  * trying libtool-bin..."
            $this_apt -y install libtool-bin
        fi
    fi
    #libcurl4-openssl-dev: for announce to work


    if [ "$enable_redis" = "true" ]; then
        $this_apt -y install libhiredis-dev
    fi
    if [ "$enable_postgres" = "true" ]; then
        $this_apt -y install libpq-dev postgresql-server-dev-all
    fi
    if [ "$enable_leveldb" = "true" ]; then
        $this_apt -y install $LEVELDB_DEV_PKG
    fi
    # ^ Don't fail on these commands, in case the user installed them
    #   a different way.

    # Some issues on Fedora ~27:
    # apt -y install libncurses5-dev libgettextpo-dev doxygen libspatialindex-dev libpq-dev postgresql-server-dev-all
    # if you skip the above, the next step says missing: GetText, Curses, ncurses, Redis, SpatialIndex, Doxygen


elif [ -f "`command -v pacman`" ]; then
    LEVELDB_DEV_PKG="leveldb"
    echo "Using pacman..."
    # pacman -R --noconfirm minetest-server
    # pacman -R --noconfirm minetest
    pacman -Syu --noconfirm \
        autoconf    automake       bzip2        cmake        \
        curl        expat          flex         freetype2    \
        gcc         git            gmp          libedit      \
        libgccjit   libjpeg-turbo  libogg       libpng       \
        libstdc++5  libtool        libvorbis    make         \
        ncurses     openal         openssl      patch        \
        pkgconf     python         readline     \
        ruby        tcl            which        xorg-server  \
        xz          zlib           sqlite
    if [ $? -ne 0 ]; then exit 1; fi
    # The above should work since taken from the build kit instructions
    # (When writing my old script, I somehow couldn't find equivalents of:
    # libjpeg8-dev libxxf86vm-dev mesa sqlite libogg vorbis -poikilos)
    if [ "$enable_redis" = "true" ]; then
        pacman -Syu --noconfirm hiredis redis
    fi
    if [ "$enable_postgres" = "true" ]; then
        pacman -Syu --noconfirm postgresql-libs
    fi
    if [ "$enable_leveldb" = "true" ]; then
        pacman -Syu --noconfirm $LEVELDB_DEV_PKG
    fi
    echo "The dev package name is unknown for pacman."
elif [ ! -z "$this_dnf" ]; then
    echo "Using $this_dnf..."
    # $this_dnf -y remove minetest-server
    # $this_dnf -y remove minetest
    $this_dnf -y install \
        autoconf           automake          bzip2            \
        bzip2-devel        cmake             expat-devel      \
        flex               fontconfig-devel  freetype-devel   \
        gcc                gcc-c++           git              \
        glibc-devel        gmp-devel         libcurl-devel    \
        libedit-devel      libgcc            libjpeg-devel    \
        libogg-devel       libpng-devel      libstdc++-devel  \
        libtool            libvorbis-devel   libX11-devel     \
        lzo-devel          make              ncurses-devel    \
        openal-soft-devel  openssl-devel     patch            \
        pkgconf            readline-devel    ruby             \
        tcl                which             xz               \
        zlib-devel         xorg-x11-server-devel              \
        sqlite-devel \
    ;
    if [ $? -ne 0 ]; then exit 1; fi

    if [ "$enable_redis" = "true" ]; then
        $this_dnf -y install redis hiredis-devel
    fi
    if [ "$enable_postgres" = "true" ]; then
        $this_dnf -y install postgresql-devel
    fi
    if [ "$enable_leveldb" = "true" ]; then
        $this_dnf -y install $LEVELDB_DEV_PKG
    fi

else
    # echo "WARNING: cannot remove packaged version, because your package manager is not known by this script."
    echo "WARNING: cannot Install dependencies, because your package manager is not known by this script."
    exit 1
fi

