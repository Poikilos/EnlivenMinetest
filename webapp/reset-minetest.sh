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

wget -O $zip_name $url/$zip_name || customDie "no $zip_name at $url"
if [ -d "$extracted_name" ]; then
  if [ "`ls -lR $extracted_name/minetest/bin/*.png | wc -l`" -gt 0 ]; then
    if [ ! -d screenshots ]; then mkdir screenshots; fi
    # NOTE: system-wide install of minetest puts screenshots in ~/ (cwd)
    mv $extracted_name/minetest/bin/*.png screenshots/ || customDie "can't move screenshots from $extracted_name/minetest/bin/*.png"
  fi
  rm -Rf "$extracted_name" || customDie "can't remove $extracted_name"
fi
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
echo "Check libraries.log for errors, then..."
echo "- Run the following manually:"
if [ -f "$extracted_name/mtcompile-program.pl" ]; then
  echo "  cd '$extracted_name'"
  echo "  perl mtcompile-program.pl build >& program.log"
  echo "  # OR (server only):"
  echo "  perl mtcompile-program.pl build --server >& program.log"
else
  echo "  cd '$extracted_name' && bash -e mtcompile-program.sh build >& program.log"
fi
echo
echo
