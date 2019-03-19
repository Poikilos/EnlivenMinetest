
var express = require('express');
var app = express();

app.get('/get-players', function (req, res) {
	res.setHeader('Content-Type', 'application/json');
	res.send(JSON.stringify(players));
});

var last_announce_string = "none";

app.get('/last-announce', function (req, res) {
	res.setHeader('Content-Type', 'text/plain');
	res.send(last_announce_string);
});

app.get('/announce', function (req, res) {
	last_announce_string = JSON.stringify(req.body);
	console.log("announce got:"+last_announce_string);
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
