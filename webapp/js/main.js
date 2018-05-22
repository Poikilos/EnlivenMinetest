var tzElement = document.getElementById("tzArea");
var tz_offset = tzElement.innerHTML;
var dateElement = document.getElementById("dateArea");
var date_s = dateElement.innerHTML;
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
	var index = -1;
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
outputElement.innerHTML = stats_html;
//NOTE: window.location.href is the entire address including query params!
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
