'use strict';

var express = require('express'),
//var exphbs  = require("express-handlebars");
//	exphbs  = require('../../'); // "express-handlebars"
	cookieParser = require('cookie-parser'),
	bodyParser = require('body-parser'),
	//session = require('express-session'),
	fs = require('fs');
const os = require('os');
var app = express();
//app.engine('handlebars', exphbs({defaultLayout: 'main'}));
//app.set('view engine', 'handlebars');
var players = [];
//see https://developer.mozilla.org/en-US/docs/Learn/Server-side/Express_Nodejs/Introduction
var prev_line = null;

//#region derived from mtsenliven.py
var msg_flags = ["WARNING[Server]: ", "ACTION[Server]: "]
var msg_lists = {}  // where flag is key
for (flag in msg_flags) {
	msg_lists[flag] = [];
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

function process_logline(line) {
	var player_name = "";
	var verb = "";
	index = -1;
	
	if (player_name != "") {
		if (player_indices.hasOwnProperty(player_name)) {
			index = player_indices[player_name];
		}
		else {
			index = player_count;
			players[index] = {};
			players[index].display_name = player_name;
			player_count++;
		}
		
	}
	if (verb == "leaves game") {
		players[index].logout_time = "";
	}
	else if (verb == "joins game") {
		players[index].login_time = "";
	}	
}

function relog_unique_only(output, err_flag=false) {
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
		var mf_len = msg_flags.length;
		for (var mf_i=0; mf_i<mf_len; mf_i++) {
			// such as '2018-02-06 21:08:06: WARNING[Server]: Deprecated call to get_look_yaw, use get_look_horizontal instead'
			// or 2018-02-06 21:08:05: ACTION[Server]: [playereffects] Wrote playereffects data into /home/owner/.minetest/worlds/FCAGameAWorld/playereffects.mt.
			f_i = output.find(msg_flags[mf_i]);
			if (f_i >= 0) {
				found_flag = msg_flags[mf_i];
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
			if (msg_lists[found_flag].indexOf(sub_msg) > -1) {
				show_enable = false;
			}
			else {
				msg_lists[found_flag].push(sub_msg);
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

app.get('/', function (req, res) {
	var ret = "";
	// Whenever server starts the following is logged
	// (see also etc/example-input.txt):
	//
	//-------------
	//  Separator
	//-------------
	//
	ret += os.homedir();
	//see ~/.minetest/debug.txt
	//and logs archived by EnlivenMinetest:
	//~/.minetest/debug_archived/2018/05/08.txt
	var ret += `<canvas id="myCanvas" width="100" height="1540"> <!--style="border:1px solid #c3c3c3;">-->
Your browser does not support the canvas element.
</canvas>
<div style="color:gray" id="outputArea">loading...</div>
<script>
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
var outputE = document.getElementById("outputArea");
outputE.innerHTML = stats_html;`;

	
	var arrayLength = players.length;
	player_count = 0;
	player_indices = {};
	var index = -1;
	for () {
		process_logline(line);
	}
	for (var i = 0; i < arrayLength; i++) {
		ret += 'players[' + i + '] = {};' + "\n";
		ret += 'players[' + i + '].login_time = "' + players[i].login_time + '";' + "\n";
		ret += 'players[' + i + '].logout_time = "' + players[i].logout_time + '";' + "\n";
		ret += 'players[' + i + '].display_name = "' + players[i].display_name + '";' + "\n";
	}
	ret += `var canvas = document.getElementById("myCanvas");
canvas.width = canvas_w;
var ctx = canvas.getContext("2d");
ctx.font = text_size+"px Arial";
var arrayLength = players.length;
var text_x;
var index = -1;
for (var i = 0; index < arrayLength; i++) {
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
		var login_places = players[index].login_time.split(':');
		var logout_places = players[index].logout_time.split(':');
		var login_second = (+login_places[0]) * 60 * 60 + (+login_places[1]) * 60 + (+login_places[2]);
		var login_m = login_second / 60.0;
		var logout_second = (+logout_places[0]) * 60 * 60 + (+logout_places[1]) * 60 + (+logout_places[2]);
		var logout_m = logout_second / 60.0;
		var left_x = border_x + (login_m-start_m)*pixels_per_m;
		var right_x = border_x + (logout_m-start_m)*pixels_per_m;
		if (right_x<left_x) {
			right_x = canvas_w; //not logged out yet, so end of bar is at end
		}
		ctx.fillStyle = "#FF0000";
		ctx.fillRect(left_x, border_y+(row_y_offset/3.0), right_x-left_x, row_y_offset/3.0);
		ctx.fillStyle = "#000000";
		ctx.fillText(login_places[0]+":"+login_places[1], left_x, text_y-(row_y_offset/3.0));
		ctx.fillStyle = "#808080";
		ctx.fillText(logout_places[0]+":"+logout_places[1], right_x, text_y+(row_y_offset/3.0));
	}
	ctx.stroke();
	text_y += row_y_offset;
	border_y += row_y_offset;
	index++;
}
</script>`;
	res.send(ret);
	//res.render('home');
});

var server = app.listen(3000, function () {
	//console.log('express-handlebars example server listening on: 3000');
	var host = server.address().address;
	var port = server.address().port;
	var this_log_path = os.homedir() + "/.minetest/debug_archived/2018/05/08.txt";
	console.log("EnlivenMinetest webapp reading '" + this_log_path + "'...");
	
	console.log("EnlivenMinetest webapp listening at http://%s:%s", host, port);
});
