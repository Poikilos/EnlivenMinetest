# minetest-chunkymap
A Minetest online web live map generator not requiring mods, with emphasis on compatibility without regard to speed, efficiency, or ease of use.

Compatible with GNU/Linux systems, Windows, or possibly other systems (but on Windows, chunkymap-regen.py must be scheduled by hand with Scheduled Tasks)

License: GPLv3 (see LICENSE.txt and always include it and way to access your source code when copying your program)
This program comes without any warranty, to the extent permitted by applicable law.

## Requirements:
* A minetest version compatible with minetestmapper-numpy.py Made by Jogge, modified by celeron55
* Python 2.7 (any 2.7.x)
* Other requirements for Windows are below; other requirements for Ubuntu are installed by install-chunkymap-on-ubuntu.sh (for other distros, modify it and send me a copy as a GitHub issue as described below in the Installation section)

## Installation
(NOTE: map refresh skips existing tiles unless you delete the related png and text files in your chunkymapdata folder)
* change set-minutely-crontab-job.sh to replace "owner" with the user that has the minetest folder (with util folder under it, not .minetest)
* Install the git version of minetest (or otherwise install 0.4.13 or other version compatible with the map generators used by chunkymap)
* IF you are using Ubuntu go to a terminal, cd to this folder, then run
	chmod +x install-chunkymap-on-ubuntu.sh && ./install-chunkymap-on-ubuntu.sh
	otherwise first edit the file for your distro (and please send the modified file to me [submit as new issue named such as: DISTRONAME installer except instead of DISTRONAME put the distro you made work])
* IF you are using a distro such as Ubuntu 14.04 where first line of /etc/crontab is "m h dom mon dow user command" then if you want regular refresh of map then run
	(otherwise first edit the script to fit your crontab then)
    chmod +x set-minutely-crontab-job.sh && ./set-minutely-crontab-job.sh
* IF you are using Windows
	* put these files anywhere
	* manually schedule a task in Task Scheduler to run C:\Python27\python chunkymap-regen.py every minute
	* python 2.7.x such as from python.org
	* run mapper-pyarch.py to make sure you know whether to download the following in 32-bit or 64-bit
	Administrator Command Prompt (to find it in Win 10, right-click windows menu)
	* update python package system:
		C:\python27\python -m pip install --upgrade pip wheel setuptools
	* numpy such as can be installed via the easy unofficial installer wheel at
	http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy
	then:
	cd to the folder where you downloaded the whl file
	C:\python27\python -m pip install "numpy-1.10.4+mkl-cp27-cp27m-win32.whl"
	(but put your specific downloaded whl file instead)
	* Pillow (instead of PIL (Python Imaging Library) which is a pain on Windows): there is a PIL installer wheel for Python such as 2.7 here:
	http://www.lfd.uci.edu/~gohlke/pythonlibs/
	as suggested on http://stackoverflow.com/questions/2088304/installing-pil-python-imaging-library-in-win7-64-bits-python-2-6-4
	then:
		C:\python27\python -m pip install "Pillow-3.1.1-cp27-none-win32.whl"
	(but put your specific downloaded whl file instead, such as Pillow-3.1.1-cp27-none-win_amd64.whl)
	* edit chunkymap_regen.py and uncomment website_root="/var/www/html/minetest" then change the value in quotes to your web server's htdocs folder such as, if you are using Apache, can be found as the value of the DocumentRoot variable in httpd.conf in the Apache folder in Program Files
	* edit chunkymap_regen.py and change world_name to your world name

## Known Issues
* Make a php file that shows the map on an html5 canvas (refresh players every 10 seconds, check for new map chunks every minute)
* Make players invisible if they stay in one spot too long (consider them logged out by that method alone since not requiring mods)
* Detect failure of minetestmapper-numpy.py and instead use minetest-mapper if on linux, otherwise show error (since Windows has no minetest-mapper at least on client 0.4.13)