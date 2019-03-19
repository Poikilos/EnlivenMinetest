var fs = require('fs');

const profilePath = require('os').homedir();
exports.profilePath = profilePath;

var minetestPath = profilePath + "/minetest";  // TODO: differs from .minetest if not RUN_IN_PLACE
exports.minetestPath = function() {
    return minetestPath;
}

const myName = "minetestinfo.js";
var skinsPath = "";
exports.skinsPath = function () {
    return skinsPath;
}

var selectableSkinFileNames = [];

exports.selectableSkinFileNames = function() {
    return selectableSkinFileNames;
}

exports.players = function(isLoggedIn) {
    return [];  // TODO: implement this
}

exports.setSkin = function(userName, skinFileName) {
    var indirectName = "player_" + userName + ".skin";
    var indirectPath = exports.skinsPath() + "/" + indirectName;
    //if (skinName.endsWith('.png')) {
        //console.log("WARNING: skinName should not specify extension--removing .png");
        //skinName = skinName.substring(0, skinName.length-4);
    //}
    //var skinFileName = skinName + ".png";
    fs.writeFile(indirectPath, skinFileName, function(err, data) {
        if (err) {
            msg = err.message;
            console.log(err);
            // res.write(msg + "<br/>")
        }
        else {
            // res.write("Before the skin is applied, The minetestserver instance must be restarted.<br/>")
            msg = "Successfully wrote " + skinFileName;
            console.log(msg + " to " + indirectPath + ".");
            // res.write(msg + "<br/>")
        }
        // res.end(ending);
    });
}

exports.regeneratePaths = function () {
    skinsPath = minetestPath + "/games/Bucket_Game/mods/codercore/coderskins/textures";
    if (fs.existsSync( minetestPath + "/games/ENLIVEN")) {
        skinsPath = minetestPath + "/games/ENLIVEN/mods/codercore/coderskins/textures";
    }
    console.log("[" + myName + "] skinsPath: \"" + skinsPath + "\"");
    var publicPath = __dirname + "/public";
    var publicSkinsPath = publicPath + "/skins";
    if (!fs.existsSync(publicPath)) {
        fs.mkdirSync(publicPath, 0744);
    }
    if (!fs.existsSync(publicSkinsPath)) {
        fs.mkdirSync(publicSkinsPath, 0744);
        fs.readdir(skinsPath, (err, files) => {
            selectableSkinFileNames = [];
            files.forEach(file => {
                if (file.startsWith("skin_") && file.endsWith(".png")) {
                    var srcPath = skinsPath + '/' + file;
                    var dstPath = publicSkinsPath + '/' + file;
                    console.log("copying '" + srcPath +  "' to '" + dstPath + "'");
                    fs.copyFile(srcPath, dstPath, fs.constants.COPYFILE_EXCL, (err) => {
                        if (err) throw err;
                        selectableSkinFileNames.push(file);
                        // console.log('source.txt was copied to destination.txt');
                    });
                }
                else {
                    console.log("not a skin: " + file)
                }
                // console.log(file);
            });
        });
    }
    else {
        fs.readdir(publicSkinsPath, (err, files) => {
            selectableSkinFileNames = [];
            files.forEach(file => {
                if (file.startsWith("skin_") && file.endsWith(".png")) {
                    selectableSkinFileNames.push(file);
                    // console.log("detected existing " + file);
                }
                else {
                    console.log("bad skin: " + file)
                }
                // console.log(file);
            });
        });
    }

}
var thisMinetest = "/tank/local/owner/minetest";
if (fs.existsSync(thisMinetest)) {
    minetestPath = thisMinetest;
}
exports.regeneratePaths();
