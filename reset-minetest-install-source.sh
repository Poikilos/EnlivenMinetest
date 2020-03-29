#!/bin/bash
echo
echo
echo
echo "Starting cleanup and library rebuild..."
date
MY_NAME="reset-minetest-install-source.sh"
config_path=$HOME/.config/EnlivenMinetest

zip_name=linux-minetest-kit.zip
extracted_name=linux-minetest-kit
config_path=~/.config/EnlivenMinetest
if [ ! -d "$config_path" ]; then
    mkdir -p "$config_path"
fi

in_use_name=minetest
#not reliable with bash -e (if not running, check throws error):
#running=`ps ax | grep -v grep | grep $in_use_name | wc -l`
#if [ $running -gt 0 ]; then
#  echo "killing minetest processes..."
#  killall $in_use_name
#fi
url=https://downloads.minetest.org
release_txt_url=http://downloads.minetest.org/release.txt
customWarn() {
    cat <<END

WARNING:
$1


END
    echo -en "\a" > /dev/tty0  # beep (You must specify a tty path if not in console mode)
    echo "Press Ctrl+C to cancel..."
    sleep 1
    echo -en "\a" > /dev/tty0
    echo "3..."
    sleep 1
    echo -en "\a" > /dev/tty0
    echo "2..."
    sleep 1
    echo -en "\a" > /dev/tty0
    echo "1..."
    sleep 1
}

customDie () {
    echo "ERROR: Cannot continue since"
    echo "$1"
    exit 1
}
available_release_line=`curl http://downloads.minetest.org/release.txt | head -n 1`
# echo "Release data: $available_release_line"  # "Release *" where * is YYMMDD
# See <https://unix.stackexchange.com/questions/174037/extracting-the-second-word-from-a-string-variable>
available_version=$(echo $available_release_line | awk '{print $2}')
# OR: available_version="${available_release_line##* }"  # get second word
if [ ${#available_version} -ne 6 ]; then
    customDie "The available version is not recognized: $available_version"
fi
installed_release_line=`head -n 1 ~/minetest/release.txt`
installed_version=$(echo $installed_release_line | awk '{print $2}')
compiled_release_line=`head -n 1 ~/minetest/release.txt`
compiled_version=$(echo $compiled_release_line | awk '{print $2}')
echo "installed_version: $installed_version"
echo "compiled_version: $compiled_version"
echo "available_version: $available_version"
if [ "@$installed_version" = "@$available_version" ]; then
    echo "You already have the latest version installed."
    exit 1
fi
if [ "@$compiled_version" != "@$installed_version" ]; then
    echo "ERROR: You have not yet installed version $compiled_version which you already compiled (you have installed $installed_version)."
    echo "You should run ./install-mts.sh instead (with --client option if you want more than minetestserver)"
    exit 2
fi
enable_offline=false
for var in "$@"
do
    if [ "@$var" = "@--offline" ]; then
        enable_offline=true
    else
        customDie "Invalid argument: $var"
    fi
done
cd "$config_path" || customDie "[$MY_NAME] cd \"$config_path\" failed."
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

if [ "@$enable_offline" = "@true" ]; then
    if [ ! -f "$zip_name" ]; then
        customDie "* Offline install is impossible without '`pwd`/$zip_name'."
    fi
else
    wget -O $zip_name $url/$zip_name || customDie "no $zip_name at $url"
fi
unzip -u $zip_name || customDie "Can't unzip $zip_name"
cd "$extracted_name"
cat "$extracted_name/release.txt"
echo "compiling libraries..."
date
start=`date +%s`
bash -e mtcompile-libraries.sh build >& libraries.log
end=`date +%s`
compile_time=$((end-start))
echo "Compiling libraries finished in $compile_time seconds."
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
echo "- Run the following manually for SERVER only (no graphical client unless an old copy of ~/minetest/bin/minetest is detected):"
echo "  bash install-mts.sh"
echo "- Run the following manually for both minetestserver and minetest:"
echo "  bash install-mts.sh --client"
echo
echo
