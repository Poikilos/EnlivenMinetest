# EnlivenMinetest webapp
EnlivenMinetest Node.js webapp for web management of minetest
* Before using this webapp, make sure you have installed minetest to
  $HOME/minetest with the RUN_IN_PLACE option (this option is true by
  default in Final Minetest builds). In the future, this webapp should
  ask you which minetest to use.
* Must run as same user as minetestserver, and neither should be root.

## Install
* Using Terminal, cd to your EnlivenMinetest/webapp diretory, then:
```bash
npm install
```

## Features
* upload skin

## Usage
* start like:
  `node server.js`
* public/skins will be created automatically. To force updating skins
  during startup, delete the public/skins directory if already exists
  and is outdated.
* In browser, go to http://localhost:64638
* for security, no overwrite is allowed


## Planned Features
(~=optional)
* Replace the "write" (stdout) method of the minetestserver process (see
  <https://stackoverflow.com/questions/18543047/mocha-monitor-application-output>)
* parse Lua mods
  - show armor strengths
* list mods (only additional ones vs basis such as Bucket_Game)
* store config file in ~/.config/EnlivenMinetest/webapp.json
* allow user to choose path of minetestserver on first run
  * (~) detect location of minetestserver (based on running executable
    maybe, or which is most recent in expected directories)
* choose minetest games directory separately from bin in case
  not `RUN_IN_PLACE`
* choose minetest worlds directory separately from bin in case
  not `RUN_IN_PLACE`
* try https://github.com/timbuchwaldt/node-async-fileupload
* try nodemon (automatically reloads changed js)

## Developer Notes

* Uses passport (see <https://code.tutsplus.com/tutorials/authenticating-nodejs-applications-with-passport--cms-21619>

### Things webapp should deprecate
* mtanalyze/web
* /home/owner/GitHub/EnlivenMinetest/etc/change_hardcoded_world_name_first/eauth
  * shell script which contains only `nano ~/.minetest/worlds/FCAGameAWorld/auth.txt`
* mts-ENLIVEN and mtsenliven.py (run minetestserver with selected game and world)
```
var path = require('path');

results = {}
if (!has_setting("system.minetestserver_path")):
    results.error="[ mtsenliven.py ] ERROR: minetestserver_path was not found in your version of minetestinfo.py";
    return results;
var mts = peek_setting("system.minetestserver_path")
if (!has_setting("owner.primary_world_path")):
    results.error= "[ mtsenliven.py ] ERROR: primary_world_path was selected by minetestinfo.py";
    return results;

var world_path = peek_setting("owner.primary_world_path");
var world_name = path.basename(wp);
//var mts_proc;
//mts_proc = /*TODO: finish this*/([mts, '--gameid ENLIVEN', '--worldname ' + world_name]);
mts_proc.write = mts_out;
return results;
```

### Development Log
(for changelog, see CHANGELOG.md)
```bash
#!/bin/sh
sudo apt update
sudo apt install nodejs npm mongodb
# NOTE: mongo daemon is called mongod
target_dir=$HOME/enlivenode
if [ ! -d "$target_dir" ]; then
  print "ERROR: Nothing done since missing $target_dir"
  exit 1
fi
cd "$target_dir"
npm init
#except changed jade to pug
npm install express static-favicon morgan cookie-parser body-parser debug pug passport passport-local mongoose multer mv
#NOTE: multiparty has streaming like busboy, but is non-trivial to implement
```

### Old (Unused)

```
#!/bin/sh
wget https://raw.githubusercontent.com/ericf/express-handlebars/master/examples/basic/server.js
wget https://raw.githubusercontent.com/ericf/express-handlebars/master/examples/basic/package.json
mkdir views
cd views
wget https://raw.githubusercontent.com/ericf/express-handlebars/master/examples/basic/views/home.handlebars
mkdir layouts
cd layouts
wget https://raw.githubusercontent.com/ericf/express-handlebars/master/examples/basic/views/layouts/main.handlebars

if [ -d ../layouts ]; then
  cd ..
fi
if [ -d ../views ]; then
  cd ..
fi
```
