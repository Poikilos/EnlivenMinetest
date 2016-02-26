# minetest-chunkymap
A Minetest online web live map generator not requiring mods, with emphasis on compatibility without regard to speed, efficiency, or ease of use.

Compatible with GNU/Linux systems, Windows, or possibly other systems (but on Windows, chunkymap-regen.py must be scheduled by hand with Scheduled Tasks)

License: (see LICENSE in notepad or your favorite text editor)
This program comes without any warranty, to the extent permitted by applicable law.

## Features:
* Runs as python script (loop by default to reduce disc reads since stores certain info) run like:
    python chunkymap-regen.py
	or to get back to it later with screen -r, instead install screen command (or tmux may work) then run:
	screen -t chunkymapregen python /home/owner/minetest/util/chunkymap-regen.py
	#where -t chunkymapregen just names the screen chunkymapregen
	#Then if you are using screen and want to leave the output without terminating the process press Ctrl a d
	#NOTE: now that loop is default, cron job scripts, which now disable loop for compatibility with new version, are ALL optional and NOT recommended
    # ( to run only once, run: python chunkymap-regen.py --no-loop true )
* Change program options (or stop it) while looping or rendering by placing chunkymap-signals.txt in the same directory as chunkymap-regen.py (see chunkymap-signals example files)
	- to maintain stability of  your text editor, save the file, close it, then move/copy it to the directory (or save it as something else then rename it to chunkymap-signals.txt).
* Has static html version of map (echo_chunkymap_table() php function) -- see example.php
	* Zoom in and out
	* optionally echo name of world that was detected by the scheduled py file
	* shows player location (can optionally show only first characters of name, for privacy; there is no saved setting yet, so to adjust, you must change the value of $nonprivate_name_beginning_char_count in chunkymap.php)	
	* Ghost players if they stay in one spot long enough (see $player_file_age_idle_max_seconds in chunkymap.php)
	* Hide players if they stay in one spot long enough (see $player_file_age_expired_max_seconds in chunkymap.php) avoiding logout detection, and not requiring mods
* Has optional script to add crontab entry (to schedule update script every minute that runs the py file unless the py file is not complete [took longer than 1 minute])

## Developer Notes:
* the map update function is only able to detect new chunks, and only checks edge chunks if player is present in one

## Requirements:
* A minetest version compatible with minetestmapper-numpy.py Made by Jogge, modified by celeron55
* Python 2.7 (any 2.7.x)
* Other requirements for Windows are below; other requirements for GNU/Linux are flock command (only if you schedule the chunkymap-cronjob script), and anything installed by install-chunkymap-on-ubuntu.sh (for other distros, modify it and send me a copy as a GitHub issue as described below in the Installation section)

## Installation
(NOTE: map refresh skips existing tiles unless you delete the related png and text files in your chunkymapdata directory)
* If you are not using Ubuntu, first edit the installer for your distro (and please send the modified file to me [submit as new issue named such as: DISTRONAME installer except instead of DISTRONAME put the distro you made work])
* If you are using Ubuntu
	* Install the git version of minetest (or otherwise install 0.4.13 or other version compatible with the map generators used by chunkymap)
	OPTION 2: IF you are using Ubuntu go to a terminal, cd to this directory,  
	then switch user to the one that will run minetestserver
	(since install-chunkymap-on-ubuntu.sh DOES replace "/home/owner" with current user's home [replace-with-current-user.py, which is automatically called by install, will change /home/owner to current user's directory in each script that install copies to $HOME/minetest/util])  
	then go to Terminal and run:  
	`minetestserver`  
	then when it is finished loading, press Ctrl C then run:  
    `chmod +x install-chunkymap-on-ubuntu.sh && ./install-chunkymap-on-ubuntu.sh`  
	
	Installing as cron job is OPTIONAL (and NOT recommended):
	* IF you are using a distro such as Ubuntu 14.04 where first line of /etc/crontab is "m h dom mon dow user command" then if you want regular refresh of map then run:
	(otherwise first edit the script to fit your crontab then)
	(if you are not using /var/www/html/minetest/chunkymapdata, edit chunkymap-cronjob script to use the correct directory, then)
    `chmod +x set-minutely-crontab-job.sh && ./set-minutely-crontab-job.sh`
* IF you are using Linux
	* Either copy your code to example.php and use it, or just rename it to map.php (or anything you want) then link to it.
	# The commands below will work if you are using the web installer, or have done mv minetest-chunkymap-master "$HOME/Downloads/minetest-chunkymap" (and if you are using /var/www/html/minetest -- otherwise change that below)
	MT_MY_WEBSITE_PATH=/var/www/html/minetest
	sudo cp -f "$HOME/Downloads/minetest-chunkymap/web/chunkymap.php" "$MT_MY_WEBSITE_PATH/chunkymap.php"
	sudo cp --no-clobber "$HOME/Downloads/minetest-chunkymap/web/example.php" "$MT_MY_WEBSITE_PATH/viewchunkymap.php"
	sudo cp -R --no-clobber "$HOME/Downloads/minetest-chunkymap/web/images/*" "$MT_MY_WEBSITE_PATH/images/"
	#--no-clobber: do not overwrite existing
	# after you do this, the update script will do it for you if you are using /var/www/html/minetest, otherwise edit the update script before using it to get these things updated
* IF you are using Windows
	* put these files anywhere
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
	* run (or if your python executable does not reside in C:\Python27\ then first edit the file):
    chunkymap-regen-loop.bat
	* copy example.php and chunkymap.php (and optionally browser.php) to your DocumentRoot or whatever folder will contain the chunkymapdata folder
## Known Issues
* chunkymap.php should read the size of the chunks -- see near is_file($chunk_genresult_path) in chunkymap.php
* optionally hide player location
* Make a method (in chunkymap.php) to echo the map as an html5 canvas (refresh players every 10 seconds, check for new map chunks every minute)
* Detect failure of minetestmapper-numpy.py and instead use minetest-mapper if on linux, otherwise show error if neither are present (Windows has no minetest-mapper at least on client 0.4.13)
