# minetest-chunkymap
A Minetest online web live map generator not requiring mods, with emphasis on compatibility without regard to speed, efficiency, or ease of use.

Compatible with GNU/Linux systems, Windows, or possibly other systems (but on Windows, chunkymap-regen.py must be scheduled by hand with Scheduled Tasks)

License: (see LICENSE in notepad or your favorite text editor)
This program comes without any warranty, to the extent permitted by applicable law.

## Features:
* Has static html version of map (echo_chunkymap_table() php function)
	* Zoom in and out
	* optionally echo name of world that was detected by the scheduled py file
	* shows player location (and only first 2 characters of name, for privacy; there is no saved setting yet, so to adjust, you must change the value of $nonprivate_name_beginning_char_count in chunkymap.php)	
	* Ghost players if they stay in one spot long enough (see $player_file_age_idle_max_seconds in chunkymap.php)
	* Hide players if they stay in one spot long enough (see $player_file_age_expired_max_seconds in chunkymap.php) avoiding logout detection, and not requiring mods
    
* Has optional script to add crontab entry (to schedule update script every minute that runs the py file unless the py file is not complete [took longer than 1 minute])

## Requirements:
* A minetest version compatible with minetestmapper-numpy.py Made by Jogge, modified by celeron55
* Python 2.7 (any 2.7.x)
* Other requirements for Windows are below; other requirements for GNU/Linux are flock command (only if you schedule the chunkymap-cronjob script), and anything installed by install-chunkymap-on-ubuntu.sh (for other distros, modify it and send me a copy as a GitHub issue as described below in the Installation section)

## Installation
(NOTE: map refresh skips existing tiles unless you delete the related png and text files in your chunkymapdata folder)
* If you are not using Ubuntu, first edit the installer for your distro (and please send the modified file to me [submit as new issue named such as: DISTRONAME installer except instead of DISTRONAME put the distro you made work])
* If you are using Ubuntu
	* Install the git version of minetest (or otherwise install 0.4.13 or other version compatible with the map generators used by chunkymap)
	OPTION 2: IF you are using Ubuntu go to a terminal, cd to this folder,  
	then switch user to the one that will run minetestserver
	(since install-chunkymap-on-ubuntu.sh DOES replace "/home/owner" with current user's home [replace-with-current-user.py, which is automatically called by install, will change /home/owner to current user's folder in each script that install copies to $HOME/minetest/util])  
	then go to Terminal and run:  
	`minetestserver`  
	then when it is finished loading, press Ctrl C then run:  
    `chmod +x install-chunkymap-on-ubuntu.sh && ./install-chunkymap-on-ubuntu.sh`  
	* IF you are using a distro such as Ubuntu 14.04 where first line of /etc/crontab is "m h dom mon dow user command" then if you want regular refresh of map then run
	(otherwise first edit the script to fit your crontab then)
	(if you are not using /var/www/html/minetest/chunkymapdata, edit chunkymap-cronjob script to use the correct folder, then)
    `chmod +x set-minutely-crontab-job.sh && ./set-minutely-crontab-job.sh`
* IF you are using Linux
	* Either copy your code to index-example.php and use it, or just rename it to map.php (or anything you want) then link to it.
	# The commands below will work if you are using the web installer, or have done mv minetest-chunkymap-master "$HOME/Downloads/minetest-chunkymap" (and if you are using /var/www/html/minetest -- otherwise change that)
	MT_MY_WEBSITE_PATH=/var/www/html/minetest
	sudo cp -f "$HOME/Downloads/minetest-chunkymap/web/chunkymap.php" "$MT_MY_WEBSITE_PATH/chunkymap.php"
	sudo cp --no-clobber "$HOME/Downloads/minetest-chunkymap/web/index_example.php" "$MT_MY_WEBSITE_PATH/viewchunkymap.php"
	sudo cp -R --no-clobber "$HOME/Downloads/minetest-chunkymap/web/images/*" "$MT_MY_WEBSITE_PATH/images/"
	#--no-clobber: do not overwrite existing
	# after you do this, the update script will do it for you if you are using /var/www/html/minetest, otherwise edit the update script before using it to get these things updated
* IF you are using Windows
	* put these files anywhere
	* manually schedule a task in Task Scheduler to run C:\Python27\python chunkymap-regen.py every minute
	* python 2.7.x such as from python.org
	* run get_python_architecture.py to make sure you know whether to download the following in 32-bit or 64-bit  
	Administrator Command Prompt (to find it in Win 10, right-click windows menu)
	* update python package system:  
		`C:\python27\python -m pip install --upgrade pip wheel setuptools`
	* numpy such as can be installed via the easy unofficial installer wheel at  
	http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy  
	then:  
	cd to the folder where you downloaded the whl file  
		`C:\python27\python -m pip install "numpy-1.10.4+mkl-cp27-cp27m-win32.whl"`  
	(but put your specific downloaded whl file instead)  
	* Pillow (instead of PIL (Python Imaging Library) which is a pain on Windows): there is a PIL installer wheel for Python such as 2.7 here:  
	http://www.lfd.uci.edu/~gohlke/pythonlibs/  
	as suggested on http://stackoverflow.com/questions/2088304/installing-pil-python-imaging-library-in-win7-64-bits-python-2-6-4  
	then:  
		`C:\python27\python -m pip install "Pillow-3.1.1-cp27-none-win32.whl"`  
	(but put your specific downloaded whl file instead, such as Pillow-3.1.1-cp27-none-win_amd64.whl)
	* edit chunkymap_regen.py and uncomment website_root="/var/www/html/minetest" then change the value in quotes to your web server's htdocs folder such as, if you are using Apache, can be found as the value of the DocumentRoot variable in httpd.conf in the Apache folder in Program Files
	* edit chunkymap_regen.py and change world_name to your world name

## Known Issues
* index-example.php should read the size of the chunks -- see near is_file($chunk_genresult_path) in chunkymap.php
* optionally hide player location
* Make a method (in chunkymap.php) to echo the map as an html5 canvas (refresh players every 10 seconds, check for new map chunks every minute)
* Detect failure of minetestmapper-numpy.py and instead use minetest-mapper if on linux, otherwise show error if neither are present (Windows has no minetest-mapper at least on client 0.4.13)
