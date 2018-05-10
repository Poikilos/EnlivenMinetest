#!/bin/bash
me="$(basename "$(test -L "$0" && readlink "$0" || echo "$0")")"
#LOCAL_REPO_DIR=$HOME/Downloads/minetest
#if [ ! -f "$LOCAL_REPO_DIR/install_manifest.txt" ]; then
#  echo "missing $LOCAL_REPO_DIR/install_manifest.txt, cannot uninstall unless you properly run cmake source and are running this script from the base repo directory (only runs from that specific location specified for safety)"
if [ ! -f "install_manifest.txt" ]; then
  echo "missing install_manifest.txt, cannot uninstall unless you properly run cmake source and are running this script from the base repo directory"
  exit 1
fi
#cd "$LOCAL_REPO_DIR"
sudo xargs rm < install_manifest.txt
if [ -d /usr/local/mods ]; then
  echo "Remove botched folders from faulty make install path apparently caused by running sudo make install without -DRUN_IN_PLACE=FALSE"
  echo "This should be safe since only removes directories if empty (except removes /usr/local/mods recursively)..."
  rmdir /usr/local/mods
  rmdir /usr/local/textures
  rmdir /usr/local/games
  rmdir /usr/local/fonts
  rmdir /usr/local/builtin
  rmdir /usr/local/doc
  rmdir /usr/local/unix
  rmdir /usr/local/fonts
  if [ -d /usr/local/mods/default ]; then
    sudo rm -Rf /usr/local/mods
  elif [ -d /usr/local/mods ]; then
    sudo rmdir /usr/local/mods
    if [ -d /usr/local/mods ]; then
      echo "WARNING: not removing errant /usr/local/mods, since not unrecognized (no /usr/local/mods/default found)"
    fi
  fi
  sudo rmdir /usr/local/textures
  sudo rmdir /usr/local/doc
  sudo rmdir /usr/local/fonts
  if [ -d /usr/local/unix ]; then
    echo "WARNING: not removing deprecated folder since may not be an errant minetest folder: /usr/local/unix"
    echo "(to resolve this issue at your own risk, open $me then paste everything indented below the 'exit 0' line into a terminal"
    exit 0
    sudo rmdir /usr/local/unix/*
    #rmdir: failed to remove 'icons': Directory not empty
    #rmdir: failed to remove 'man': Directory not empty
    sudo rmdir /usr/local/unix/man/man6
    sudo rmdir /usr/local/unix/man
    sudo rmdir /usr/local/unix/icons/hicolor/128x128/*
    sudo rmdir /usr/local/unix/icons/hicolor/128x128
    sudo rmdir /usr/local/unix/icons/hicolor/scalable/*
    sudo rmdir /usr/local/unix/icons/hicolor/scalable
    sudo rmdir /usr/local/unix/icons/hicolor
    sudo rmdir /usr/local/unix/icons
    sudo rmdir /usr/local/unix
    sudo rmdir /usr/local/builtin/*
    sudo rmdir /usr/local/builtin
  fi
fi

if [ -f "`command -v update-desktop-database`" ]; then
  echo "updating desktop database as per https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=minetest-git"
  update-desktop-database &>/dev/null && update-desktop-database -q
fi
if [ -f "`command -v gtk-update-icon-cache`" ]; then
  echo "updating gtk icon cache as per https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=minetest-git"
  gtk-update-icon-cache &>/dev/null && gtk-update-icon-cache -q -t -f usr/share/icons/hicolor
fi

