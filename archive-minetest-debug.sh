#!/bin/sh
echo ""
minetest_data_path=$HOME/.minetest
logs_folder_name=debug_archived
logs_folder_path=$minetest_data_path/$logs_folder_name
year_string=`date +%Y`
if [ -f "$minetest_data_path/debug.txt" ];
then
  #date_string=`date +%Y-%m-%d`
  month_string=`date +%m`
  day_string=`date +%d`
  if [ ! -d "$logs_folder_path" ];
  then
  mkdir "$logs_folder_path"
  fi
  if [ ! -d "$logs_folder_path/$year_string" ];
  then
    mkdir "$logs_folder_path/$year_string"
  fi
  if [ ! -d "$logs_folder_path/$year_string/$month_string" ];
  then
    mkdir "$logs_folder_path/$year_string/$month_string"
  fi
  
  mts_log_archive_today_file_path=$logs_folder_path/$year_string/$month_string/$day_string.txt
  mv "$minetest_data_path/debug.txt" "$mts_log_archive_today_file_path"
  if [ -f "$mts_log_archive_today_file_path" ]; then
    echo "log saved to $mts_log_archive_today_file_path"
  else
    echo "Failed to save log to $mts_log_archive_today_file_path"
  fi
else
  echo "nothing to do (no $minetest_data_path/debug.txt is present--perhaps it was already archived--check $year_string folder (perhaps this month's $year_string/$month_string folder) in $logs_folder_path/"
fi


