'use strict';

var tz_offset = 240; //subtract this from server time to get local time; 4hrs is 240; 5hrs is 300
//TODO: handle tz_offset not divisible by 60
//var selected_date_s = null;
//selected_date_s = "2018-05-08";

var express = require('express'),
//var exphbs  = require("express-handlebars");
//	exphbs  = require('../../'); // "express-handlebars"
	cookieParser = require('cookie-parser'),
	bodyParser = require('body-parser'),
	//session = require('express-session'),
	fs = require('fs'),
	readlines = require('n-readlines');
const os = require('os');
var app = express();
//app.engine('handlebars', exphbs({defaultLayout: 'main'}));
//app.set('view engine', 'handlebars');
var players = [];
var player_indices = {};
var play_dates = [];
//see https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs/Introduction
var prev_line = null;

//#region derived from mtsenliven.py
var msgprefix_flags = ["WARNING[Server]: ", "ACTION[Server]: "]
var msgprefix_lists = {}  // where flag is key
var mf_len = msgprefix_flags.length;
for (var mf_i=0; mf_i<mf_len; mf_i++) {
	msgprefix_lists[msgprefix_flags[mf_i]] = [];
}

var non_unique_wraps = [];
non_unique_wraps.push({
	"opener":"active block modifiers took ",
	"closer":"ms (longer than 200ms)"
});
var unique_flags = [
	"leaves game",
	"joins game"
];
//#endregion derived from mtsenliven.py

function process_logline(line, line_number) {
	//selected_date_s
	//TODO: use store_unique_log_data instead of this function
	var player_name = null;
	var verb = "";
	var time_s = "";
	var date_s = "";
	var player_ip = null;
	const time_start_i = 11;
	var uf_len = unique_flags.length;
	mf_len = msgprefix_flags.length;
	var verb_i = -1;
	var verb_number = -1;
	var msgprefix_i = -1;
	var msgprefix_number = -1;
	var msgprefix = null;
	var index_msg = "";
	for (var mf_i=0; mf_i<mf_len; mf_i++) {
		msgprefix_i = line.indexOf(msgprefix_flags[mf_i]);
		if (msgprefix_i > -1) {
			msgprefix_number = mf_i;
			msgprefix = msgprefix_flags[mf_i];
			break;
		}
	}
	var skip_date_enable = false;
	for (var uf_i=0; uf_i<uf_len; uf_i++) {
		verb_i = line.indexOf(unique_flags[uf_i]);
		if (verb_i > -1) {
			verb_number = uf_i;
			verb = unique_flags[uf_i];
			date_s = line.substring(0,10).trim();
			//if (selected_date_s==null || selected_date_s==date_s) {
				//console.log("(verbose message in process_logline) using '" + date_s + "' since selected '"+selected_date_s+"'");
				time_s = line.substring(time_start_i, time_start_i+8);
				//console.log("using time "+time_s);
				if (msgprefix!=null) {
					player_name = line.substring(msgprefix_i+msgprefix.length, verb_i).trim();
					var ip_flag = " [";
					var ip_i = player_name.indexOf(ip_flag);
					if (ip_i > -1) {
						player_ip = player_name.substring(ip_i+ip_flag.length, player_name.length-1);
						player_name = player_name.substring(0,ip_i);
					}
				}
				else {
					player_name = "&lt;missing msgprefix&rt;";
				}
			//}
			//else {
			//	skip_date_enable = true;
				//console.log("WARNING in process_logline: skipping '" + date_s + "' since not '"+selected_date_s+"'");
			//}
			break;
		}
	}
	var index = -1;  // player index
	if (player_name != null) {
		if (player_name.length > 0) {
			if (player_indices.hasOwnProperty(player_name)) {
				index = player_indices[player_name];
				index_msg = "cached ";
			}
			else {
				index = players.length;
				//players.push({});
				players[index] = {};
				players[index].display_name = player_name;
				player_indices[player_name] = index;
				//console.log("created new index "+index);
			}
		}
		else {
			console.log("WARNING in process_logline: zero-length player name");
		}
	}
	if (index<0 && (verb=="leaves game"||verb=="joins game")) {
		console.log("(ERROR in process_logline) " + index_msg +
		            "index was '"+index+"' but date was present '" +
		            date_s + "' for '"+line+"' (no player found, but" +
		            "verb is a player verb).");
	}
	var play_date_enable = false;
	if (verb == "leaves game") {
		if (index > -1) {
			var play_i = -1;
			if (!players[index].hasOwnProperty("plays")) {
				players[index].plays = {};
			}
			if (!players[index].plays.hasOwnProperty(date_s)) {
				//leave login time blank--player must have logged in before the available part of the log began
				players[index].plays[date_s] = [];
				players[index].plays[date_s].push({});
				play_i = 0;
			}
			else {
				if (players[index].plays[date_s].length==0) players[index].plays[date_s].push({});
				play_i = players[index].plays[date_s].length - 1;
				if (players[index].plays[date_s][play_i].hasOwnProperty("logout_time")) {
					//If last entry is incomplete, start a new one:
					players[index].plays[date_s].push({});
					play_i++;
				}
			}
			players[index].plays[date_s][play_i].logout_time = time_s;
			play_date_enable = true;
		}
	}
	else if (verb == "joins game") {
		if (index > -1) {
			if (player_ip!=null) {
				players[index].player_ip = player_ip;
				var play_i = -1;
				if (!players[index].hasOwnProperty("plays")) {
					players[index].plays = {};
				}
				if (!players[index].plays.hasOwnProperty(date_s)) {
					players[index].plays[date_s] = [];
					play_i = 0;
				}
				else play_i = players[index].plays[date_s].length;
				players[index].plays[date_s].push({});
				//console.log(verb+" on "+date_s+" (length "+players[index].plays[date_s].length+") play "+play_i+"+1 for player ["+index+"] "+player_name+"...");
				players[index].plays[date_s][play_i].login_time = time_s;
				play_date_enable = true;
			}
			// else redundant (server writes " joins game " again
			// and shows list of players instead of ip).
			//TODO: else analyze list of players to confirm in case player logged in all day
		}
	}
	if (play_date_enable) {
		if (date_s.length>0) {
			if (play_dates.indexOf(date_s) < 0) {
				play_dates.push(date_s);
			}
		}
	}
}

function store_unique_log_data(output, line_number, err_flag=false) {
	var ret = "";
	var output_strip = output.trim();
	var u_prefix = "active block modifiers took ";
	var u_suffix = "ms (longer than 200ms)";
	// (out_bytes is bytes)
	var show_enable = true;
	var found_flag = null;
	var f_i = null;
	var always_show_enable = false;
	var msg_msg = "previous message";
	var uf_len = unique_flags.length;
	for (var uf_i=0; uf_i<uf_len; uf_i++) {
		if (output.includes(unique_flags[uf_i])) {
			always_show_enable = true;
		}
	}
	if (!always_show_enable) {
		var mf_len = msgprefix_flags.length;
		for (var mf_i=0; mf_i<mf_len; mf_i++) {
			// such as '2018-02-06 21:08:06: WARNING[Server]: Deprecated call to get_look_yaw, use get_look_horizontal instead'
			// or 2018-02-06 21:08:05: ACTION[Server]: [playereffects] Wrote playereffects data into /home/owner/.minetest/worlds/FCAGameAWorld/playereffects.mt.
			f_i = output.find(msgprefix_flags[mf_i]);
			if (f_i >= 0) {
				found_flag = msgprefix_flags[mf_i];
				break;
			}
		}
		if (found_flag!=null) {
			var sub_msg = output.substring(f_i+flag.length).trim();
			var nuw_len = non_unique_wraps.length;
			for (var nuw_i=0; nuw_i<nuw_len; nuw_i++) {
			//for (wrap in non_unique_wraps) {
				var wrap = non_unique_wraps[nuw_i];
				if (sub_msg.includes(wrap["opener"]) && sub_msg.includes(wrap["closer"])) {
					sub_msg = wrap["opener"] + "..." + wrap["closer"];
					msg_msg = "similar messages";
					break;
				}
			}
			if (msgprefix_lists[found_flag].indexOf(sub_msg) > -1) {
				show_enable = false;
			}
			else {
				msgprefix_lists[found_flag].push(sub_msg);
			}
		}
	}
	if (show_enable) {
		ret = output_strip;
		if (found_flag != null) {
			ret += "\n  [ EnlivenMinetest ] " + msg_msg + " will be suppressed";
		}
	}
	return ret;
}

function read_log() {
	if (players==null) players = [];
	if (player_indices==null) player_indices = {};
	// os.homedir() + "/.minetest/debug_archived/2018/05/08.txt",
	var log_paths = [os.homedir() + "/.minetest/debug.txt"];
	var lp_len = log_paths.length;
	for (var lp_i=0; lp_i<lp_len; lp_i++) {
		var this_log_path = log_paths[lp_i];
		console.log("EnlivenMinetest webapp reading '" + this_log_path + "'...");
		var line_number = 1;
		if (fs.existsSync(this_log_path)) {
			//uses n-readlines package: see https://stackoverflow.com/questions/34223065/read-lines-synchronously-from-file-in-node-js
			var liner = new readlines(this_log_path);
			var next = true;
			while (next) {
				next = liner.next();
				if (next!=false) {
					process_logline(next.toString('ascii'), line_number);
					line_number++;
				}
			}
		}
		else {
			console.log("WARNING: file not found: '" + this_log_path + "' (listing actual archived log folders is not yet implemented, so this is a hard-coded demo folder only on poikilos' server)");
		}
	}
}

app.get('/get-players', function (req, res) {
	res.setHeader('Content-Type', 'application/json');
	 res.send(JSON.stringify(players));
});

app.get('/', function (req, res) {
	var ret = "";
	ret += '<html><body style="font-family:calibri,sans">';
	// Whenever server starts the following is logged
	// (see also etc/example-input.txt):
	//
	//-------------
	//  Separator
	//-------------
	//
	var selected_date_s = null;
	if (req.query.date) selected_date_s = req.query.date
	ret += "assuming minetestserver ran as: " + os.homedir() + "<br/>\n";
	ret += "timezone (tz_offset/60*-1): " + (Math.floor(tz_offset/60)*-1) + "<br/>\n";
	ret += "date: " + selected_date_s + "<br/>\n";
	//ret += 'var play_dates = [];';
	var pdLength = 0;
	if (play_dates != null) pdLength = play_dates.length;
	for (var pd_i = 0; pd_i < pdLength; pd_i++) {
		//ret += 'play_dates.push("' + play_dates[pd_i] + '");';
		if (selected_date_s!=play_dates[pd_i]) {
			ret += '<a href="?date='+play_dates[pd_i]+'">'+play_dates[pd_i]+'</a> ';
		}
		else {
			ret += play_dates[pd_i]+' ';
		}
	}
	//if (selected_date_s==null) {
		//ret += '<a href="?date=2018-05-08">2018-05-08</a>';
	//}
	//see ~/.minetest/debug.txt
	//and logs archived by EnlivenMinetest:
	//~/.minetest/debug_archived/2018/05/08.txt
	ret += `
<div style="color:gray" id="statusArea"></div>
<canvas id="myCanvas" width="100" height="1540"> <!--style="border:1px solid #c3c3c3;">-->
Your browser does not support the canvas element.
</canvas>
<div style="color:gray" id="outputArea">loading...</div>
<script>
`;
	ret += 'var date_s = ' + (selected_date_s?('"'+selected_date_s+'"'):"null") + ';';
	ret += `
var start_hour = 0;
var start_m = start_hour*60;
var start_s = start_m*60;
var endbefore_hour = 24;
var hour_count = endbefore_hour - start_hour;
var hour_width = 60;  // 60 pixels per hour
var pixels_per_m = hour_width/60.0;
var pixels_per_s = pixels_per_m/60.0;
var player_name_width = 100;
var text_size = 16.0;
var row_y_offset = text_size * (22.0/16.0); // if 16px font is drawn at (x,16), line at (x,21) is one pixel away from the bottom of the descenders
var border_y = 0.5; //canvas uses 0.5 as middle of pixel
var border_start_x = 0.5+player_name_width;
var border_x = border_start_x;
var text_y = text_size;
var text_start_x = 3.5;

var players = [];
var stats_html = "";
var time_area_width = hour_width*hour_count;
var canvas_w = player_name_width + time_area_width;
stats_html += '<div>' + hour_count + "hrs * " + hour_width + "px = " + time_area_width + '</div>'
stats_html += '<div>' + time_area_width + "px + " + player_name_width + "px player name = " + canvas_w + 'px canvas width</div>'
var outputElement = document.getElementById("outputArea");
var statusElement = document.getElementById("statusArea");
statusElement.innerHTML="...";
function draw_players() {
	var canvas = document.getElementById("myCanvas");
	canvas.width = canvas_w;
	var ctx = canvas.getContext("2d");
	ctx.font = text_size+"px Arial";
	var arrayLength = players.length;
	var text_x;
	var index = -1;`
		ret += 'var tz_offset = ' + tz_offset + ';';
		ret += `
	for (var i = 0; index < arrayLength; i++) {
		ctx.font = text_size+"px Arial";
		text_x = text_start_x;
		ctx.fillStyle = "#dce5ea";
		ctx.fillRect(0, border_y+1.0, player_name_width, row_y_offset-1.0);
		//ctx.stroke();
		ctx.fillStyle = "#000000";
		ctx.moveTo(0, border_y);
		ctx.strokeStyle = "#000000";
		ctx.lineTo(canvas_w, border_y);

		//ctx.stroke();
		ctx.fillStyle = "#000000";
		if (index==-1) {
			ctx.font = "bold "+text_size+"px Arial";
			ctx.fillText("Name", text_x, text_y);
			ctx.font = text_size+"px Arial";
			text_x = player_name_width+0.5;

			//ctx.fillStyle = "#000000";
			ctx.strokeStyle = "#008000";
			for (var hour=0; hour<endbefore_hour; hour++) {
				ctx.fillStyle = "#B0B0B0";
				ctx.moveTo(text_x, border_y);
				ctx.lineTo(text_x, border_y+row_y_offset-0.5);
				//ctx.stroke();
				ctx.fillText(hour+":00", text_x+3, text_y);
				text_x += hour_width;
			}
		}
		else {
			ctx.fillText(players[index].display_name, text_x, text_y);
			var border_x = border_start_x;
			var playsLength = 0;
			var plays = null;
			if (date_s!=null) {
				if (players[index].plays != undefined) {
					if (players[index].plays.hasOwnProperty(date_s)) {
						plays = players[index].plays[date_s];
						playsLength = plays.length;
					}
				}
			}
			for (var s_i = 0; s_i < playsLength; s_i++) {
				if (!plays[s_i].hasOwnProperty("login_time")) {
					plays[s_i].login_time = "00:00:00";
				}
				var login_places = plays[s_i].login_time.split(':');
				if (login_places.length>=3) {
					login_places[0] -= Math.floor(tz_offset/60);
				}
				if (!plays[s_i].hasOwnProperty("logout_time")) {
					plays[s_i].logout_time = "23:59:59";
				}
				var logout_places = plays[s_i].logout_time.split(':');
				if (logout_places.length>=3) {
					logout_places[0] -= Math.floor(tz_offset/60);
				}
				var login_second = (+login_places[0]) * 60 * 60 + (+login_places[1]) * 60 + (+login_places[2]);
				var login_m = login_second / 60.0;
				var logout_second = (+logout_places[0]) * 60 * 60 + (+logout_places[1]) * 60 + (+logout_places[2]);
				var logout_m = logout_second / 60.0;
				var left_x = border_x + (login_m-start_m)*pixels_per_m;
				var right_x = border_x + (logout_m-start_m)*pixels_per_m;
				if (right_x<left_x) {
					right_x = canvas_w; //not logged out yet, so end of bar is at end
				}
				ctx.fillStyle = "#008000";
				ctx.fillRect(left_x, border_y+(row_y_offset/3.0), right_x-left_x, row_y_offset/3.0);
				ctx.font = (text_size*.66)+"px Arial";
				ctx.fillStyle = "#000000";
				ctx.fillText(login_places[0]+":"+login_places[1], left_x, text_y-(row_y_offset/3.0));
				ctx.fillStyle = "#808080";
				var logout_s = logout_places[0]+":"+logout_places[1];
				ctx.fillText(logout_s, right_x-ctx.measureText(logout_s).width, text_y+(row_y_offset/3.0));
			}
		}
		ctx.stroke();
		text_y += row_y_offset;
		border_y += row_y_offset;
		index++;
	}
}
outputElement.innerHTML = stats_html;`;
	//NOTE: window.location.href is the entire address including query params!
	ret += `
var request = new XMLHttpRequest();
var getUrl = window.location;
var request_href = getUrl.protocol + "//" + getUrl.host + "/"+'get-players';
statusElement.innerHTML = request_href+"...";
request.open('GET', request_href, true);

request.onload = function() {
  if (this.status >= 200 && this.status < 400) {
	// Success!
	statusElement.innerHTML = "loaded player(s)";
	if (!statusElement.classList.contains('alert') ) {
		statusElement.classList.add('alert');
	}
	try {
		players = JSON.parse(this.response);
		statusElement.classList.add('alert-success');
		statusElement.innerHTML = "loaded " + players.length + ' player(s) <span style="color:white">from "'+this.responseURL+'"</span>';
		draw_players();
	}
	catch(e) {
		statusElement.classList.add('alert-warning');
        statusElement.innerHTML = e + " for URL '"+request_href+"'";
        //alert(this.response);
    }
  } else {
	// We reached our target server, but it returned an error
	statusElement.innerHTML = "Error " + this.status + " accessing " + request_href;
  }
};

request.onerror = function() {
  // There was a connection error of some sort
};

request.send();
	`;
	/*
	var arrayLength = players.length;
	for (var i = 0; i < arrayLength; i++) {
		ret += 'players[' + i + '] = {};' + "\n";
		if (players.plays!=undefined) {
			ret += 'players[' + i + '].plays = {};' + "\n";

			//var playsLength = players.plays.length;
			for (var s_i = 0; s_i < playsLength; s_i++) {
				ret += 'players[' + i + '].plays[' + s_i + '].login_time = "' + players[i].plays[s_i].login_time + '";' + "\n";
				ret += 'players[' + i + '].plays[' + s_i + '].logout_time = "' + players[i].plays[s_i].logout_time + '";' + "\n";
			}
		}
		ret += 'players[' + i + '].display_name = "' + players[i].display_name + '";' + "\n";
	}
	*/
	ret += `</script>`;
	ret += '</body></html>';
	res.send(ret);
	//res.render('home');
});



var server = app.listen(3000, function () {
	//console.log('express-handlebars example server listening on: 3000');
	var host = server.address().address;
	var port = server.address().port;
	console.log("reading log...");
	read_log();
	console.log("EnlivenMinetest webapp listening at http://%s:%s", host, port);
});
