#!/bin/bash -e
zip_name=linux-minetest-kit.zip
extracted_name=linux-minetest-kit
in_use_name=minetest
running=`ps ax | grep -v grep | grep $in_use_name | wc -l`
if [ $running -gt 0 ]; then
  echo "killing minetest processes..."
  killall $in_use_name
fi
wget -O $zip_name https://downloads.minetest.org/$zip_name || exit 1
if [ -d "$extracted_name" ]; then
  if [ "`ls -lR $extracted_name/minetest/bin/*.png | wc -l`" -gt 0 ]; then
    if [ ! -d screenshots ]; then mkdir screenshots; fi
    # NOTE: system-wide install of minetest puts screenshots in ~/ (cwd)
    mv $extracted_name/minetest/bin/*.png screenshots/ || exit 2
  fi
  rm -Rf "$extracted_name" || exit 3
fi
unzip -u $zip_name || exit 4
cd "$extracted_name"
echo "compiling libraries..."
bash -e mtcompile-libraries.sh build >& libraries.log
echo "  (see libraries.log in case of any errors)"
#echo "compiling program..."
#bash -e mtcompile-program.sh build >& program.log
echo "done."
echo
echo "Run the following manually:"
echo "  cd '$extracted_name' && bash -e mtcompile-program.sh build >& program.log"
echo
echo
