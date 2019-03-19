var fs = require('fs');

const profilePath = require('os').homedir();
exports.profilePath = profilePath;

var minetestPath = profilePath + "/minetest";  // TODO: differs from .minetest if not RUN_IN_PLACE
exports.minetestPath = function() {
    return minetestPath;
}

const myName = "minetestinfo.js";
var skinDir = "";
exports.skinDir = function () {
    return skinDir;
}


exports.regeneratePaths = function () {
    exports.skinDir = exports.minetestPath + "/games/Bucket_Game/mods/codercore/coderskins/textures";
    if (fs.existsSync( minetestPath + "/games/ENLIVEN")) {
	skinDir = minetestPath + "/games/ENLIVEN/mods/codercore/coderskins/textures";
    }
    console.log("[" + myName + "] skinDir: \"" + skinDir + "\"");
}
var thisMinetest = "/tank/local/owner/minetest";
if (fs.existsSync(thisMinetest)) {
    minetestPath = thisMinetest;
}
exports.regeneratePaths();
