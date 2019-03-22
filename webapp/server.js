'use strict';
// Howto: see README.md

//function getUserHome() {
    //return process.env[(process.platform == 'win32') ? 'USERPROFILE' : 'HOME'];
//}

var tzOffsetMinutes = 240; //subtract this from server time to get local time; 4hrs is 240; 5hrs is 300
// TODO: handle tzOffsetMinutes not divisible by 60
// var selectedDateStr = null;
// selectedDateStr = "2018-05-08";

const express = require('express'),
    multer = require('multer'),
// var exphbs  = require("express-handlebars");
// exphbs  = require('../../'); // "express-handlebars"
    cookieParser = require('cookie-parser'),
    bodyParser = require('body-parser'),
    //session = require('express-session'),
    fs = require('fs'),
    readlines = require('n-readlines');
const os = require('os');
//var formidable = require('formidable');
const querystring = require("querystring");  // built-in
// TODO: var config = require(storagePath + '/config.js') // config file contains all tokens and other private info
// var fun = require('./functions.js'); // functions file contains our non-app-specific functions including those for our Passport and database work
var mt = require('./minetestinfo.js'); // functions file contains our non-app-specific functions including those for our Passport and database work

// var util = require('util')

var app = express();
app.set('view engine', 'ejs');
// see https://medium.com/@TheJesseLewis/how-to-make-a-basic-html-form-file-upload-using-multer-in-an-express-node-js-app-16dac2476610
const port = process.env.PORT || 64638;
app.use(bodyParser.urlencoded({extended:false}));  // handle body requests
app.use(bodyParser.json());  // make JSON work
app.use('/public', express.static(__dirname + '/public'));

//app.engine('handlebars', exphbs({defaultLayout: 'main'}));
//app.set('view engine', 'handlebars');
var players = [];
var playerIndices = {};
var activityDates = [];
//see https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs/Introduction
var previousLine = null;

//#region derived from mtsenliven.py
var msgPrefixFlags = ["WARNING[Server]: ", "ACTION[Server]: "]
var msgPrefixLists = {}  // where flag is key
var mfLen = msgPrefixFlags.length;
for (var mfIndex=0; mfIndex<mfLen; mfIndex++) {
    msgPrefixLists[msgPrefixFlags[mfIndex]] = [];
}

var nonUniqueWraps = [];
nonUniqueWraps.push({
    "opener":"active block modifiers took ",
    "closer":"ms (longer than 200ms)"
});
var uniqueFlags = [
    "leaves game",
    "joins game"
];
//#endregion derived from mtsenliven.py
const skinStorage = multer.diskStorage({
    // see https://medium.com/@TheJesseLewis/how-to-make-a-basic-html-form-file-upload-using-multer-in-an-express-node-js-app-16dac2476610
    destination: function(req, file, next) {
        next(null, mt.skinsPath());  // or something like './public/photo-storage'
    },
    limits: {
        fileSize: 1*1024*1024  // in bytes
    },

    // Change filename
    filename: function(req, file, next) {
        const ext = "png";
        // var errMsg = null;
        console.log("* Checking name...");
        if (!req.body.userName) {
            return next(new Error("userName is missing"));
        }
        else if (req.body.userName.length < 1) {
            return next(new Error("userName is blank."));
        }
        if (file.size < 1)  {
            return next(new Error("image not selected"));
        }

        //if (errMsg === null) {
        var directName = "player_" + req.body.userName + '.' + ext;
        console.log("* Renaming '" + file + "' to " + directName);
        next(null, directName);
        //}
        //else {
            //console.log(errMsg);
            //next(new Error(errMsg));
        //}
        // const ext = file.mimetype.split('/')[1];
        // next(null, file.fieldname + '-' + Date.now() + '.'+ext);
    }
});
// see https://medium.com/@bmshamsnahid/nodejs-file-upload-using-multer-3a904516f6d2
const skinUpload = multer({
    storage: skinStorage,

    fileFilter: function(req, file, next) {
        const ext = "png";
        console.log("filtering...");
        var errMsg = null;
        // NOTE: return with error aborts the upload.
        if (!file) {
            errMsg = "You did not select a file.";
            req.fileValidationError = errMsg;
            return next(new Error(errMsg));  // next(null, false, new Error(errMsg))
        }
        else if (file.size < 1) {
            errMsg = "Empty file.";
            req.fileValidationError = errMsg;
            return next(new Error(errMsg));
        }

        if (!file.mimetype.startsWith('image/')) {
            errMsg = "* ERROR: file type " + file.mimetype
                        + " is not supported";
            req.fileValidationError = errMsg;
            return next(new Error(errMsg));
        }
        if (errMsg === null) {
            var directName = "player_" + req.body.userName + '.' + ext;
            console.log("* " + file.mimetype + " '" + file + "' uploaded...");
            // set player skin name to new file name:
            mt.setSkin(req.body.userName, directName);
            // TODO: allow setSkin output to res
            next(null, true);
        } else {
            console.log(errMsg);
            return next(new Error(errMsg));
        }
    }
});

function processLogLine(line, lineNumber) {
    //selectedDateStr
    //TODO: use storeUniqueLogData instead of this function
    var playerName = null;
    var verb = "";
    var timeStr = "";
    var dateStr = "";
    var playerIP = null;
    const timeStartInt = 11;
    var ufLen = uniqueFlags.length;
    mfLen = msgPrefixFlags.length;
    var verbIndex = -1;
    var verbNumber = -1;
    var msgPrefixIndex = -1;
    var msgPrefixNumber = -1;
    var msgprefix = null;
    var indexMsg = "";
    for (var mfIndex=0; mfIndex<mfLen; mfIndex++) {
        msgPrefixIndex = line.indexOf(msgPrefixFlags[mfIndex]);
        if (msgPrefixIndex > -1) {
            msgPrefixNumber = mfIndex;
            msgprefix = msgPrefixFlags[mfIndex];
            break;
        }
    }
    var skipDateEnable = false;
    for (var ufIndex=0; ufIndex<ufLen; ufIndex++) {
        verbIndex = line.indexOf(uniqueFlags[ufIndex]);
        if (verbIndex > -1) {
            verbNumber = ufIndex;
            verb = uniqueFlags[ufIndex];
            dateStr = line.substring(0,10).trim();
            //if (selectedDateStr==null || selectedDateStr==dateStr) {
                //console.log("(verbose message in processLogLine) using '" + dateStr + "' since selected '"+selectedDateStr+"'");
                timeStr = line.substring(timeStartInt, timeStartInt+8);
                //console.log("using time "+timeStr);
                if (msgprefix!=null) {
                    playerName = line.substring(msgPrefixIndex+msgprefix.length, verbIndex).trim();
                    var ipFlag = " [";
                    var ipIndex = playerName.indexOf(ipFlag);
                    if (ipIndex > -1) {
                        playerIP = playerName.substring(ipIndex+ipFlag.length, playerName.length-1);
                        playerName = playerName.substring(0, ipIndex);
                    }
                }
                else {
                    playerName = "&lt;missing msgprefix&rt;";
                }
            //}
            //else {
            //  skipDateEnable = true;
                //console.log("WARNING in processLogLine: skipping '" + dateStr + "' since not '"+selectedDateStr+"'");
            //}
            break;
        }
    }
    var index = -1;  // player index
    if (playerName != null) {
        if (playerName.length > 0) {
            if (playerIndices.hasOwnProperty(playerName)) {
                index = playerIndices[playerName];
                indexMsg = "cached ";
            }
            else {
                index = players.length;
                //players.push({});
                players[index] = {};
                players[index].displayName = playerName;
                playerIndices[playerName] = index;
                //console.log("created new index "+index);
            }
        }
        else {
            console.log("WARNING in processLogLine: zero-length player name");
        }
    }
    if (index<0 && (verb=="leaves game"||verb=="joins game")) {
        console.log("(ERROR in processLogLine) " + indexMsg +
                    "index was '"+index+"' but date was present '" +
                    dateStr + "' for '"+line+"' (no player found, but" +
                    "verb is a player verb).");
    }
    var playDateEnable = false;
    if (verb == "leaves game") {
        if (index > -1) {
            var playIndex = -1;
            if (!players[index].hasOwnProperty("plays")) {
                players[index].plays = {};
            }
            if (!players[index].plays.hasOwnProperty(dateStr)) {
                //leave login time blank--player must have logged in before the available part of the log began
                players[index].plays[dateStr] = [];
                players[index].plays[dateStr].push({});
                playIndex = 0;
            }
            else {
                if (players[index].plays[dateStr].length==0) players[index].plays[dateStr].push({});
                playIndex = players[index].plays[dateStr].length - 1;
                if (players[index].plays[dateStr][playIndex].hasOwnProperty("logoutTime")) {
                    //If last entry is incomplete, start a new one:
                    players[index].plays[dateStr].push({});
                    playIndex++;
                }
            }
            players[index].plays[dateStr][playIndex].logoutTime = timeStr;
            playDateEnable = true;
        }
    }
    else if (verb == "joins game") {
        if (index > -1) {
            if (playerIP!=null) {
                players[index].playerIP = playerIP;
                var playIndex = -1;
                if (!players[index].hasOwnProperty("plays")) {
                    players[index].plays = {};
                }
                if (!players[index].plays.hasOwnProperty(dateStr)) {
                    players[index].plays[dateStr] = [];
                    playIndex = 0;
                }
                else playIndex = players[index].plays[dateStr].length;
                players[index].plays[dateStr].push({});
                //console.log(verb+" on "+dateStr+" (length "+players[index].plays[dateStr].length+") play "+playIndex+"+1 for player ["+index+"] "+playerName+"...");
                players[index].plays[dateStr][playIndex].loginTime = timeStr;
                playDateEnable = true;
            }
            // else redundant (server writes " joins game " again
            // and shows list of players instead of ip).
            //TODO: else analyze list of players to confirm in case player logged in all day
        }
    }
    if (playDateEnable) {
        if (dateStr.length>0) {
            if (activityDates.indexOf(dateStr) < 0) {
                activityDates.push(dateStr);
            }
        }
    }
}

function storeUniqueLogData(output, lineNumber, errFlag=false) {
    var ret = "";
    var outputTrim = output.trim();
    var uPrefix = "active block modifiers took ";
    var uSuffix = "ms (longer than 200ms)";
    // (outBytes is bytes)
    var showEnable = true;
    var foundFlag = null;
    var fIndex = null;
    var alwaysShowEnable = false;
    var msgMsg = "previous message";
    var ufLen = uniqueFlags.length;
    for (var ufIndex=0; ufIndex<ufLen; ufIndex++) {
        if (output.includes(uniqueFlags[ufIndex])) {
            alwaysShowEnable = true;
        }
    }
    if (!alwaysShowEnable) {
        var mfLen = msgPrefixFlags.length;
        for (var mfIndex=0; mfIndex<mfLen; mfIndex++) {
            // such as '2018-02-06 21:08:06: WARNING[Server]: Deprecated call to get_look_yaw, use get_look_horizontal instead'
            // or 2018-02-06 21:08:05: ACTION[Server]: [playereffects] Wrote playereffects data into /home/owner/.minetest/worlds/FCAGameAWorld/playereffects.mt.
            fIndex = output.find(msgPrefixFlags[mfIndex]);
            if (fIndex >= 0) {
                foundFlag = msgPrefixFlags[mfIndex];
                break;
            }
        }
        if (foundFlag!=null) {
            var subMsg = output.substring(fIndex+flag.length).trim();
            var nUWLen = nonUniqueWraps.length;
            for (var nUWIndex=0; nUWIndex<nUWLen; nUWIndex++) {
            //for (wrap in nonUniqueWraps) {
                var wrap = nonUniqueWraps[nUWIndex];
                if (subMsg.includes(wrap["opener"]) && subMsg.includes(wrap["closer"])) {
                    subMsg = wrap["opener"] + "..." + wrap["closer"];
                    msgMsg = "similar messages";
                    break;
                }
            }
            if (msgPrefixLists[foundFlag].indexOf(subMsg) > -1) {
                showEnable = false;
            }
            else {
                msgPrefixLists[foundFlag].push(subMsg);
            }
        }
    }
    if (showEnable) {
        ret = outputTrim;
        if (foundFlag != null) {
            ret += "\n  [ EnlivenMinetest ] " + msgMsg + " will be suppressed";
        }
    }
    return ret;
}

function readLog() {
    if (players==null) players = [];
    if (playerIndices==null) playerIndices = {};
    // os.homedir() + "/.minetest/debug_archived/2018/05/08.txt",
    // var logPaths = [os.homedir() + "/.minetest/debug.txt"];
    var logPaths = [os.homedir() + "/minetest/bin/debug.txt"];
    var lpLen = logPaths.length;
    for (var lpIndex=0; lpIndex<lpLen; lpIndex++) {
        var thisLogPath = logPaths[lpIndex];
        console.log("EnlivenMinetest webapp reading '" + thisLogPath + "'...");
        var lineNumber = 1;
        if (fs.existsSync(thisLogPath)) {
            //uses n-readlines package: see https://stackoverflow.com/questions/34223065/read-lines-synchronously-from-file-in-node-js
            var readLines = new readlines(thisLogPath);
            var nextLine = true;
            while (nextLine) {
                nextLine = readLines.next();
                if (nextLine!=false) {
                    processLogLine(nextLine.toString('ascii'), lineNumber);
                    lineNumber++;
                }
            }
        }
        else {
            console.log("WARNING: file not found: '" + thisLogPath + "' (listing actual archived log folders is not yet implemented, so this is a hard-coded demo folder only on poikilos' server)");
        }
    }
}

app.get('/modding', function(req, res, next) {
    res.render('pages/modding', {
        msg: "",
    });
});
app.get('/skin-upload-form', function(req, res, next) {
    //var ending = "";
    //ending += '<a href="/">Back to Main Site</a><br/>' + "\n";
    ////ending += '<a href="/skin-upload-form">Back to Upload</a><br/>' + "\n";
    //ending += '</body></html>';
    //res.write('<html><body style="font-family:calibri,sans">'+"\n");
    //res.write('<form action="/upload-skin" method="post" enctype="multipart/form-data">'+"\n");
    //res.write('User Name (case-sensitive): <input type="text" name="userName" id="userName">'+"\n");
    //res.write('Select a png image to upload:'+"\n");
    //res.write('<input type="file" name="userFile" id="userFile">'+"\n");
    //res.write('<input type="submit" value="Upload Image" name="submit">'+"\n");
    //res.write('</form>'+"\n");
    //res.end(ending);
    var msg = "";
    res.render('pages/skin-upload-form', {
        msg: msg
    });
});
app.get('/skin-selection-form', function(req, res, next) {
    var msg = "";
    res.render('pages/skin-selection-form', {
        msg: msg,
        skinFileNames: mt.selectableSkinFileNames()
    });
});


// see "new way" of handling multer errors: https://github.com/expressjs/multer#error-handling
var singleSkinUpload = skinUpload.single('userFile');
app.post('/upload-skin', function(req, res) {
    singleSkinUpload(req, res, function(err) {
        if (err instanceof multer.MulterError) {
            // A Multer error occurred when uploading.
            res.render('multer error', { error: err });
            //res.render('pages/result', {
                //msg: "An error occurred in processing the form: " + err,
            //});
        } else if (err) {
            // An unknown error occurred when uploading.
            res.render('unknown error', { error: err });
            //res.render('pages/result', {
                //msg: "An error occurred in processing: " + err,
            //});
        }
        else {
            // var ending = "";
            var msg = "";
            // ending += '<a href="/">Back to Main Site</a><br/>' + "\n";
            // ending += '<a href="/skin-upload-form">Back to Upload</a><br/>' + "\n";
            // ending += '</body></html>';
            // res.write('<html>');
            // res.write('<body style="font-family:calibri,sans">');
            if (!req.fileValidationError) {
                // res.write('<p>Complete!</p>');
                msg = "Complete!";
            }
            else {
                msg = req.fileValidationError;
                // res.write('<p>' + req.fileValidationError + '</p>');
            }
            //res.end(ending);
            res.render('pages/result', {
                msg: msg
            });
        }
    })
});

app.get('/select-skin', function(req, res, next) {
    mt.setSkin(req.query.userName, req.query.skinFileName);
    res.render('pages/result', {
        msg: "Complete."
    });
});


app.get('/', function(req, res, next) {
    //var ret = "";

    //res.write('<html>');
    //res.write('<body style="font-family:calibri,sans">');
    // Whenever server starts the following is logged
    // (see also etc/example-input.txt):
    //
    //-------------
    //  Separator
    //-------------
    //
    var selectedDateStr = null;
    var msg = "";
    if (req.query.date) selectedDateStr = req.query.date
    if (req.query.msg != undefined) {
        //res.write("<br/>");
        //res.write("<b>" + querystring.parse(req.query.msg) + "</b><br>\n");
        // line above causes:
        //TypeError: Cannot convert object to primitive value
        //at /home/owner/git/EnlivenMinetest/webapp/server.js:390:16
        //at Layer.handle [as handle_request] (/home/owner/git/EnlivenMinetest/webapp/node_modules/express/lib/router/layer.js:95:5)
        //at next (/home/owner/git/EnlivenMinetest/webapp/node_modules/express/lib/router/route.js:137:13)
        //at Route.dispatch (/home/owner/git/EnlivenMinetest/webapp/node_modules/express/lib/router/route.js:112:3)
        //at Layer.handle [as handle_request] (/home/owner/git/EnlivenMinetest/webapp/node_modules/express/lib/router/layer.js:95:5)
        //at /home/owner/git/EnlivenMinetest/webapp/node_modules/express/lib/router/index.js:281:22
        //at Function.process_params (/home/owner/git/EnlivenMinetest/webapp/node_modules/express/lib/router/index.js:335:12)
        //at next (/home/owner/git/EnlivenMinetest/webapp/node_modules/express/lib/router/index.js:275:10)
        //at expressInit (/home/owner/git/EnlivenMinetest/webapp/node_modules/express/lib/middleware/init.js:40:5)
        //at Layer.handle [as handle_request] (/home/owner/git/EnlivenMinetest/webapp/node_modules/express/lib/router/layer.js:95:5)

        //res.write("<br/>");
    }
    //res.write('<p><a href="/skin-upload-form">Upload Skin</a></p>');
    //res.write("<h3>Server info</h3>");
    //res.write("<ul>");
    //res.write("<li>assuming minetestserver ran as: " + os.homedir() + "</li>");
    //res.write("<li>timezone (tzOffsetMinutes/60*-1): " + (Math.floor(tzOffsetMinutes/60)*-1) + '<span name="tzArea" id="tzArea"></span>' + "</li>");
    //res.write('<li>date: <span id="dateArea" name="dateArea">' + ((selectedDateStr!=null)?selectedDateStr:"not selected") + '</span>' + "</li>");
    //res.write('var activityDates = [];');
    var pdLength = 0;
    if (activityDates != null) pdLength = activityDates.length;
    var logDates = [];
    for (var pdIndex = 0; pdIndex < pdLength; pdIndex++) {
        //res.write('activityDates.push("' + activityDates[pdIndex] + '");');
        if (selectedDateStr!=activityDates[pdIndex]) {
            //res.write('<a href="?date='+activityDates[pdIndex]+'">'+activityDates[pdIndex]+'</a> ');
            logDates.push( { date:activityDates[pdIndex], active:true});
        }
        else {
            logDates.push( { date:activityDates[pdIndex], active:false});
            //res.write(activityDates[pdIndex]+' ');
        }
    }
    //if (selectedDateStr==null) {
        //res.write('<a href="?date=2018-05-08">2018-05-08</a>');
    //}
    //see ~/.minetest/debug.txt
    //and logs archived by EnlivenMinetest:
    //~/.minetest/debug_archived/2018/05/08.txt
    //res.write('</body></html>');
    //res.end('</body></html>');
    //res.render('home');

    res.render('pages/index', {
        msg: msg,
        serverUser: os.homedir(),
        tzOffset: (Math.floor(tzOffsetMinutes/60)*-1),
        selectedDate: ((selectedDateStr!=null)?selectedDateStr:"not selected"),
        logDates: logDates
    });
});



var server = app.listen(port, function () {
    // 8123 is default for Minecraft DynMap
    // 64638 spells 'minet' on a telephone keypad, but 6463, 6472 is already Discord RPC server
    //console.log('express-handlebars example server listening on: ' + port);
    var host = server.address().address;
    var port = server.address().port;
    console.log("server address:");
    console.log(JSON.stringify(server.address()));
    console.log("reading log...");
    readLog();
    console.log("EnlivenMinetest webapp is listening at http://%s:%s", host, port);
});
