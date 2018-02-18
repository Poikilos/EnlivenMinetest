if [ ! -f "install_manifest.txt" ]; then
  echo "missing install_manifest.txt, cannot uninstall unless you properly run cmake source and are running this script from the base repo directory"
  exit 1
fi
sudo xargs rm < install_manifest.txt
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
sudo rm -Rf /usr/local/mods
sudo rmdir /usr/local/textures
sudo rmdir /usr/local/doc
sudo rmdir /usr/local/fonts
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
