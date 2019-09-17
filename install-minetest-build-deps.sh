#!/bin/bash
enable_postgres="false"
enable_redis="false"
if [ "$1" = "redis" ]; then enable_redis="true"; fi
if [ "$2" = "redis" ]; then enable_redis="true"; fi
if [ "$3" = "redis" ]; then enable_redis="true"; fi
if [ "$1" = "postgres" ]; then enable_postgres="true"; fi
if [ "$2" = "postgres" ]; then enable_postgres="true"; fi
if [ "$3" = "postgres" ]; then enable_postgres="true"; fi
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

if [ ! -z "$this_apt" ]; then
    echo "Using $this_apt..."
    # sudo $this_apt -y remove minetest-server
    # sudo $this_apt -y remove minetest
    sudo $this_apt update
    sudo $this_apt -y install \
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
        libsqlite3-dev  libssl-dev     libtool        libtool-bin     \
        libvorbis-dev   libx11-dev     libxxf86vm-dev lynx            \
        nano            nettle-dev     p7zip-full     patch           \
        perl            pkg-config     python3        python3-dev     \
        python-dev      rake           ruby           sed             \
        tar             tcl            unzip          util-linux      \
        wget            xz-utils       zip                            \
    \
        libcurl4-openssl-dev  \
        libfreetype6-dev      \
        libgdk-pixbuf2.0-dev  \
        libglu1-mesa-dev      \
        libxml-parser-perl    \
        xserver-xorg-dev

    #libcurl4-openssl-dev: for announce to work


    if [ "$enable_redis" = "true" ]; then
        sudo $this_apt -y install libhiredis-dev
    fi
    if [ "$enable_postgres" = "true" ]; then
        sudo $this_apt -y install libpq-dev postgresql-server-dev-all
    fi

    # Some issues on Fedora ~27:
    # sudo apt -y install libncurses5-dev libgettextpo-dev doxygen libspatialindex-dev libpq-dev postgresql-server-dev-all
    # if you skip the above, the next step says missing: GetText, Curses, ncurses, Redis, SpatialIndex, Doxygen


elif [ -f "`command -v pacman`" ]; then
    echo "Using pacman..."
    # sudo pacman -R --noconfirm minetest-server
    # sudo pacman -R --noconfirm minetest
    sudo pacman -Syu --noconfirm \
        autoconf    automake       bzip2        cmake        \
        curl        expat          flex         freetype2    \
        gcc         git            gmp          libedit      \
        libgccjit   libjpeg-turbo  libogg       libpng       \
        libstdc++5  libtool        libvorbis    make         \
        ncurses     openal         openssl      patch        \
        pkgconf     python         python2      readline     \
        ruby        tcl            which        xorg-server  \
        xz          zlib
    # The above should work since taken from the build kit instructions
    # (When writing my old script, I somehow couldn't find equivalents of:
    # libjpeg8-dev libxxf86vm-dev mesa sqlite libogg vorbis -poikilos)
    if [ "$enable_redis" = "true" ]; then
        sudo pacman -Syu --noconfirm hiredis redis
    fi
    if [ "$enable_postgres" = "true" ]; then
        sudo pacman -Syu --noconfirm postgresql-libs
    fi

elif [ ! -z "$this_dnf" ]; then
    echo "Using $this_dnf..."
    # sudo $this_dnf -y remove minetest-server
    # sudo $this_dnf -y remove minetest
    sudo $this_dnf -y install \
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
        zlib-devel         xorg-x11-server-devel

    if [ "$enable_redis" = "true" ]; then
        sudo $this_dnf -y install redis hiredis-devel
    fi
    if [ "$enable_postgres" = "true" ]; then
        sudo $this_dnf -y install postgresql-devel
    fi

else
    # echo "WARNING: cannot remove packaged version, because your package manager is not known by this script."
    echo "WARNING: cannot Install dependencies, because your package manager is not known by this script."
    exit 1
fi

