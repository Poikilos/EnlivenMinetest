# EnlivenMinetest webapp
EnlivenMinetest Node.js webapp for web management of minetest
* Must run as same user as minetestserver, and neither should be root!

## Install
* Using Terminal, cd to your EnlivenMinetest/webapp diretory, then:
```bash
npm install
```

## Usage
* start like:
  `node server.js`
* then it will listen on port 3000
* change skin at localhost:3000/skin-form
* for security, no overwrite is allowed


## Planned Features
* Replace the "write" (stdout) method of the minetestserver process (see
  <https://stackoverflow.com/questions/18543047/mocha-monitor-application-output>)

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
npm install express static-favicon morgan cookie-parser body-parser debug pug passport passport-local mongoose formidable
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
