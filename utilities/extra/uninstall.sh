#!/bin/sh
extracted_path=/home/owner/Downloads/minetest
mnf_name=install_manifest.txt
customDie() {
    echo
    echo "ERROR:"
    echo "$1"
    echo
    echo
    exit 1
}
if [ ! -f "$extracted_path/$mnf_name" ]; then
    customDie "$extracted_path/$mnf_name is missing, so $0 cannot continue."
fi


cd $extracted_path || customDie "* cannot cd $extracted_path."
echo "- about to run 'sudo xargs rm < $mnf_name'..."
sudo xargs rm < $mnf_name
# as per http://irc.minetest.net/minetest/2015-08-06
