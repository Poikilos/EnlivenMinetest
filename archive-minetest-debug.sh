#!/bin/bash

MT_DATA="$HOME"
# DEBUG_TXT is Detected later.
logs_folder_name=debug_archived
logs_folder_path=$MT_DATA/$logs_folder_name
year_string=`date +%Y`


archive_debug() {
    DEBUG_TXT="$1"
    if [ -f "$DEBUG_TXT" ]; then
        #date_string=`date +%Y-%m-%d`
        month_string=`date +%m`
        day_string=`date +%d`
        if [ ! -d "$logs_folder_path" ]; then
            mkdir "$logs_folder_path"
        fi
        if [ ! -d "$logs_folder_path/$year_string" ]; then
            mkdir "$logs_folder_path/$year_string"
        fi
        if [ ! -d "$logs_folder_path/$year_string/$month_string" ]; then
            mkdir "$logs_folder_path/$year_string/$month_string"
        fi

        this_prefix="$logs_folder_path/$year_string/$month_string/$day_string"
        this_path="$this_prefix.txt"
        i=2
        if [ -f "$this_path" ]; then
            while [[ -e "$this_prefix-$i.txt" ]]; do
                let i++
            done
            echo "- '$this_path' already exists."
            this_prefix="$this_prefix-$i"
            this_path="$this_prefix.txt"
            echo "  * using '$this_path'..."
        else
            echo "* saving '$this_path'"
        fi
        mv "$DEBUG_TXT" "$this_path" || echo "  - ERROR: Moving log '$DEBUG_TXT' to '$this_path' FAILED."
        #if [ -f "$this_path" ]; then
        #    echo "  * saved log '$this_path'"
        #else
        #    echo "  * ERROR: Moving log '$DEBUG_TXT' to '$this_path' FAILED."
        #fi
    else
        echo
        echo "- There is nothing to do (no $MT_DEBUG is present--perhaps it was already archived--check $year_string folder (perhaps this month's $year_string/$month_string folder) in $logs_folder_path/"
        echo
        echo
    fi
}

count=0
last_not_found=
if [ "$MT_DATA" = "$HOME" ]; then
    TRY_FILE="$HOME/debug.txt"
    if [ -f "$TRY_FILE" ]; then
        let count++
        archive_debug "$TRY_FILE"
    else
        last_not_found="$TRY_FILE"
    fi
else
    TRY_FILE="$HOME/debug.txt"
    if [ -f "$TRY_FILE" ]; then
        let count++
        archive_debug "$TRY_FILE"
    else
        last_not_found="$TRY_FILE"
    fi
fi

TRY_FILE="$HOME/minetest/debug.txt"
if [ -f "$TRY_FILE" ]; then
    let count++
    archive_debug "$TRY_FILE"
else
    last_not_found="$TRY_FILE"
fi

TRY_FILE="$HOME/minetest/bin/debug.txt"
if [ -f "$TRY_FILE" ]; then
    let count++
    archive_debug "$TRY_FILE"
else
    last_not_found="$TRY_FILE"
fi

if [ "$count" -lt "1" ]; then
    echo
    echo "- There is not yet a minetest log in a known location such as"
    echo "  '$last_not_found'."
    echo "  Maybe it was already archived."
    echo
    echo
fi


