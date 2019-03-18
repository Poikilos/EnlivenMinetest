#!/bin/bash
zip_name=linux-minetest-kit.zip
extracted_name=linux-minetest-kit
in_use_name=minetest
#not reliable with bash -e (if not running, check throws error):
#running=`ps ax | grep -v grep | grep $in_use_name | wc -l`
#if [ $running -gt 0 ]; then
#  echo "killing minetest processes..."
#  killall $in_use_name
#fi
url=https://downloads.minetest.org

customDie () {
    echo "ERROR: Cannot continue since"
    echo "$1"
    exit 1
}
if [ -d "$extracted_name" ]; then
  if [ "`ls -lR screenshots/*.png | wc -l`" -gt 0 ]; then
    mv screenshots/*.png ~/ || customDie "can't move screenshots from $extracted_name/minetest/bin/*.png"
    rmdir --ignore-fail-on-non-empty screenshots
  fi
  if [ "`ls -lR $extracted_name/minetest/bin/*.png | wc -l`" -gt 0 ]; then
    # if [ ! -d screenshots ]; then mkdir screenshots; fi
    # NOTE: system-wide install of minetest puts screenshots in ~/ (cwd)
    mv $extracted_name/minetest/bin/*.png ~/ || customDie "can't move screenshots from $extracted_name/minetest/bin/*.png"
  fi
  rm -Rf "$extracted_name" || customDie "can't remove $extracted_name"
fi

wget -O $zip_name $url/$zip_name || customDie "no $zip_name at $url"
unzip -u $zip_name || customDie "Can't unzip $zip_name"
cd "$extracted_name"
echo "compiling libraries..."
bash -e mtcompile-libraries.sh build >& libraries.log
echo "  (see libraries.log in case of any errors)"
#echo "compiling program..."
#bash -e mtcompile-program.sh build >& program.log
echo "done."
echo
echo
echo
echo
echo
cd ..
echo "Check libraries.log for errors, then..."
echo "- Run the following manually for SERVER only (no graphical client):"
echo "  bash install-mts.sh"
echo
echo
