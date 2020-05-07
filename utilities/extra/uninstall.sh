#!/bin/sh
extracted_path=$HOME/Downloads/minetest
mnf_name=install_manifest.txt
customExit() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
if [ ! -f "$extracted_path/$mnf_name" ]; then
    customExit "$extracted_path/$mnf_name is missing, so $0 cannot continue."
fi

if [ ! -f "`command -v xargs`" ]; then
    customExit "This script cannot work without xargs. Try uninstall.py."
fi

cd $extracted_path || customExit "* cannot cd $extracted_path."
echo "- about to run 'sudo xargs rm < $mnf_name'..."
xargs rm < $mnf_name
echo "- about to run 'sudo xargs rmdir --ignore-fail-on-non-empty < $mnf_name'..."
xargs rmdir --ignore-fail-on-non-empty < $mnf_name
echo "  - removing level 7 empty directories..."
xargs rmdir --ignore-fail-on-non-empty < $mnf_name
echo "  - removing level 6 empty directories..."
xargs rmdir --ignore-fail-on-non-empty < $mnf_name
echo "  - removing level 5 empty directories..."
xargs rmdir --ignore-fail-on-non-empty < $mnf_name
echo "  - removing level 4 empty directories..."
xargs rmdir --ignore-fail-on-non-empty < $mnf_name
echo "  - removing level 3 empty directories..."
xargs rmdir --ignore-fail-on-non-empty < $mnf_name
echo "  - removing level 2 empty directories..."
xargs rmdir --ignore-fail-on-non-empty < $mnf_name
echo "  - removing level 1 empty directories..."
xargs rmdir --ignore-fail-on-non-empty < $mnf_name
# as per http://irc.minetest.net/minetest/2015-08-06
