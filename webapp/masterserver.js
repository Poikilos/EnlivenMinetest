
var express = require('express');
var app = express();
var mt = require('./minetestinfo.js');
app.get('/get-players', function (req, res) {
    res.setHeader('Content-Type', 'application/json');
    res.send(JSON.stringify(mt.players(true)));
});

var previousAnnounceStr = "none";

app.get('/last-announce', function (req, res) {
    res.setHeader('Content-Type', 'text/plain');
    res.send(previousAnnounceStr);
});

app.get('/announce', function (req, res) {
    previousAnnounceStr = JSON.stringify(req.body);
    console.log("announce got:" + previousAnnounceStr);
    res.setHeader('Content-Type', 'text/plain');
    res.send();
});


var server = app.listen(3000, function () {
    //console.log('express-handlebars example server listening on: 3000');
    var host = server.address().address;
    var port = server.address().port;
    console.log("listserver address:");
    console.log(JSON.stringify(server.address()));
    console.log("(experimental WIP) Minetest master server is listening at http://%s:%s", host, port);
});
