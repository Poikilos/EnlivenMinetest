<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
if (($_SERVER['PHP_SELF'] == "chunkymap.php") or endsWith($_SERVER['PHP_SELF'],"/chunkymap.php")) {
	echo "<html><body style=\"font-family:calibri,arial,helvetica,sans\">This is the backend--don't call it directly. instead do include_once('chunkymap.php'); To use the map, go to <a href=\"viewchunkymap.php\">viewchunkymap.php</a> instead.</body></html>";
}


//NOTE: for parse errors, MUST add the following line to  php.ini (such as /etc/php5/apache2/php.ini): display_errors = on
if (is_file('browser.php')) {
    include_once('browser.php');
}
else {
    echo "<!--missing browser.php...-->";
}
$chunkymap_anchor_name="chunkymap_top";
$is_verbose = false;
if ($is_verbose) echo "REQUEST...";
foreach($_REQUEST as $key => $value) {
    //in case auto_globals is not enabled
    $GLOBALS[$key]=$value;
    if ($is_verbose) echo "$key:$value...";
}
if ($is_verbose) echo "timezone...";
date_default_timezone_set('EST'); //required by PHP >=5.1.0

if ($is_verbose) echo "globals...";
//$chunkymap_view_x=0;
//$chunkymap_view_z=0;
//$chunkymap_view_zoom=25;
if (!isset($chunkymap_view_x)) {
    $chunkymap_view_x=0;
}
if (!isset($chunkymap_view_z)) {
    $chunkymap_view_z=0;
}
if (!isset($chunkymap_view_zoom)) {
    $chunkymap_view_zoom=.25;
}

$chunkymapdata_path = "chunkymapdata";
$chunkymapdata_worlds_path = $chunkymapdata_path."/worlds";
$chunkymapdata_thisworld_path = null;
$showplayers=true;

// NOT OPTIONAL for table version:
$chunkymap_tile_original_w=16;
$chunkymap_tile_original_h=16;

$chunk_dimension_min=$chunkymap_tile_original_w;
if ($chunkymap_tile_original_h<$chunk_dimension_min) $chunk_dimension_min=$chunkymap_tile_original_h;
$chunkymap_change_zoom_multiplier=1.5;
$chunkymap_camera_pan_delta=.5;
$chunkymap_view_min_zoom=0.0173415299; //1.0/$chunk_dimension_min; //should be a number that would get to exactly 100 eventually if multiplied by chunkymap_zoom_delta repeatedly (such as 0.09765625 if chunkymap_zoom_delta were 2); 0.005 was avoided since tiles used to be 80x80 pixels
$chunkymap_view_max_zoom=16585998.48141; //13107200.0;


$decachunk_prefix_string="decachunk_";
$decachunk_prefix_then_x_string=$decachunk_prefix_string."x";
$chunk_prefix_string="chunk_";
$chunk_prefix_then_x_string=$chunk_prefix_string."x";
$z_opener="z";
$dot_yaml=".yml";
$decachunk_dot_and_ext=".jpg";
$chunk_dot_and_ext = ".png";

//$more_attribs_string="; -webkit-filter: opacity(0%); filter: opacity(0%)";
$more_attribs_string="";
$td_decachunk_placeholder_content="<!--widening table--><img src=\"chunkymapdata/images/decachunk-blank.jpg\" style=\"width:100%; background-color:black".$more_attribs_string."\"/>";
$td_chunk_placeholder_content="<!--widening table--><img src=\"chunkymapdata/images/chunk-blank.jpg\" style=\"width:100%; background-color:black".$more_attribs_string."\"/>";
$td_1px_placeholder_content="<!--widening table--><img src=\"chunkymapdata/images/chunk-blank.jpg\" style=\"width:1px; background-color:black".$more_attribs_string."\"/>";


function echo_error($val) {
    if (!isset($val)) {
        $val="Unknown Error";
    }
    echo '<span style="color:red">'.$val.'</span><br/>'."\n";
}

function get_dict_from_conf($path, $assignment_operator) {
    global $is_verbose;
    if ($is_verbose) echo "get_dict...";
    $handle = fopen($path, "r");
    $result = null;
    if ($handle) {
        while (($line = fgets($handle)) !== false) {
            $line_strip = trim($line);
            if (strlen($line_strip)>0) {
                if (substr($line_strip,0,1)!="#") {
                    $ao_index = strpos($line_strip, $assignment_operator);
                    if ($ao_index>0 and $ao_index<(strlen($line_strip)-1)) { //skip blank variable OR value
                        $found_name = substr($line_strip, 0, $ao_index);
                        $found_value_index = $ao_index + 1;
                        $found_value = substr($line_strip, $found_value_index, strlen($line_strip)-$found_value_index);
                        if ($result===null) {
                            $result = array();
                        }
                        $result[$found_name]=$found_value;
                    }
                }
            }
        }
        fclose($handle);
    } else {
        echo "<span style=\"color:read\">Failed to read $path</span> (run chunkymap-cronjob script as root first, otherwise see README.md in minetest-chunkymap to ensure installation is correct).<br/>";
    }
    return $result;
}//end get_dict_from_conf



$map_dict = null;

//startsWith and endsWith are from:
//Salmon A. stackoverflow. <http://stackoverflow.com/questions/834303/startswith-and-endswith-functions-in-php>. 5 Feb 2016. 19 Feb, 2016.
function startsWith($haystack, $needle) {
    // search backwards starting from haystack length characters from the end
    return $needle === "" || strrpos($haystack, $needle, -strlen($haystack)) !== false;
}
function endsWith($haystack, $needle) {
    // search forward starting from end minus needle length characters
    return $needle === "" || (($temp = strlen($haystack) - strlen($needle)) >= 0 && strpos($haystack, $needle, $temp) !== false);
}

//NOTE: This function is here since the builtin is_int checks type (which is not needed in this webapp) and the builtin is_numeric includes decimal and exponent (see http://php.net/manual/en/function.is-numeric.php)
function is_int_string($val) {
    global $is_verbose;
    if ($is_verbose) echo "is_int_string...";
    $result = true;
    $int_chars="0123456789-";
    for ($i=0; $i<strlen($val); $i++) {
        $digit_index = strpos($int_chars, substr($val, $i, 1));
        if ($digit_index===false) {
            $result = false;
            break;
        }
    }
    return $result;
}
function set_chunkymap_view($set_chunkymap_view_x, $set_chunkymap_view_z, $set_chunkymap_view_zoom) {
    global $chunkymap_view_x;
    global $chunkymap_view_z;
    global $chunkymap_view_zoom;
    $chunkymap_view_x = $set_chunkymap_view_x;
    $chunkymap_view_z = $set_chunkymap_view_z;
    $chunkymap_view_zoom = $set_chunkymap_view_zoom;
}

function echo_map_heading_text() {
    echo "Chunkymap";
    //echo "Map of ";
    //echo_worldname();
}
// function echo_worldname() {
    // global $map_dict;
    // if (isset($map_dict["world_name"])) {
        // echo $map_dict["world_name"];
    // }
    // else echo "<span style=\"color:red\">(missing world name)</span>";
// }
function get_chunk_folder_path_from_chunky_coords($chunky_x, $chunky_z) {
	global $chunkymapdata_thisworld_path;
	//NOTE: floor converts -.5 to -1 (and -1.5 to -2) but .5 to 0
	$decachunk_x = get_decachunky_coord_from_chunky_coord($chunky_x);
	$decachunk_z = get_decachunky_coord_from_chunky_coord($chunky_z);
	//if ($x<0) { $decachunk_x = $x + $x%10; }
	//else { $decachunk_x = $x - $x%10; }
	//if ($z<0) { $decachunk_z = $z + $z%10; }
	//else { $decachunk_z = $z - $z%10; }
	$result = $chunkymapdata_thisworld_path.'/16px/'.$decachunk_x.'/'.$decachunk_z;
	return $result;
}

function get_decachunk_folder_path_from_location($x, $z) {
	global $chunkymapdata_thisworld_path;
	//NOTE: floor converts -.5 to -1 (and -1.5 to -2) but .5 to 0
	$chunky_x = get_chunky_coord_from_location($x);
	$chunky_z = get_chunky_coord_from_location($z);
	$decachunky_x = get_decachunky_coord_from_chunky_coord($chunky_x);
	$decachunky_z = get_decachunky_coord_from_chunky_coord($chunky_z);
	$hectochunk_x = get_hectochunky_coord_from_decachunky_coord($decachunky_x);
	$hectochunk_z = get_hectochunky_coord_from_decachunky_coord($decachunky_z);
	$result = $chunkymapdata_thisworld_path.'/160px/'.$hectochunk_x.'/'.$hectochunk_z;
	return $result;
}

function get_decachunk_folder_path_from_decachunk($chunky_x, $chunky_z) {
	global $chunkymapdata_thisworld_path;
	//NOTE: floor converts -.5 to -1 (and -1.5 to -2) but .5 to 0
	$hectochunk_x = get_hectochunky_coord_from_decachunky_coord($chunky_x);
	$hectochunk_z = get_hectochunky_coord_from_decachunky_coord($chunky_z);
	$result = $chunkymapdata_thisworld_path.'/160px/'.$hectochunk_x.'/'.$hectochunk_z;
	return $result;
}

function get_chunky_coord_from_location($location_coord) {
	$chunk_coord = intval(floor((float)$location_coord/16));
	return $chunk_coord;
}

function get_decachunky_coord_from_chunky_coord($chunky_x) {
	return intval(floor((float)$chunky_x/10.0));
}

function get_hectochunky_coord_from_decachunky_coord($chunky_x) {
	return intval(floor((float)$chunky_x/10.0));
}

function get_decachunky_coord_from_location($location_x) {
	$chunk_x = get_chunky_coord_from_location($location_x);
	$decachunk_x = get_decachunky_coord_from_chunky_coord($chunk_x);
	return $decachunk_x;
}

function get_decachunk_image_path_from_decachunk($decachunky_x, $decachunky_z) {
	return get_decachunk_folder_path_from_decachunk($decachunky_x, $decachunky_z)."/".get_decachunk_image_name_from_decachunk($decachunky_x, $decachunky_z);
}

function get_decachunk_image_name_from_decachunk($x, $z) {
	global $decachunk_prefix_string;
	global $decachunk_dot_and_ext;
	return "$decachunk_prefix_string"."$x"."z"."$z"."$decachunk_dot_and_ext";
}
function get_chunk_yaml_path_from_chunky_coords($chunky_x, $chunky_z) {
	return get_chunk_folder_path_from_chunky_coords($chunky_x, $chunky_z).'/'.get_chunk_yaml_file_name($chunky_x, $chunky_z);
}
function get_chunk_image_path_from_chunky_coords($chunky_x, $chunky_z) {
	return get_chunk_folder_path_from_chunky_coords($chunky_x, $chunky_z).'/'.get_chunk_file_name($chunky_x, $chunky_z);
}
function get_chunk_yaml_file_name($chunky_x, $chunky_z) {
	global $chunk_prefix_then_x_string;
	global $dot_yaml;
	global $z_opener;
	return $chunk_prefix_then_x_string.$chunky_x.$z_opener.$chunky_z.$dot_yaml;
}
function get_chunk_file_name($chunky_x, $chunky_z) {
	global $chunk_prefix_then_x_string;
	global $dot_yaml;
	global $z_opener;
	global $chunk_dot_and_ext;
	return $chunk_prefix_then_x_string.$chunky_x.$z_opener.$chunky_z."$chunk_dot_and_ext";
}

function get_javascript_bool_value($this_bool) {
	$result = "false";
	if ($this_bool == true) {
		$result = "true";
	}
	return $result;
}

//chunk_mode_enable: shows chunk png images instead of decachunk jpg images (slower)
//debug_mode_enable: draws colored rectangles based on yml files instead of drawing images
function echo_chunkymap_canvas($chunk_mode_enable, $debug_mode_enable, $html4_mode_enable) {
    global $chunkymap_view_x;
    global $chunkymap_view_z;
    global $chunkymap_view_zoom;
    global $chunkymap_view_max_zoom;
    global $chunkymap_view_min_zoom;
	global $showplayers;
	global $chunkymap_change_zoom_multiplier;
	global $chunkymap_camera_pan_delta;
	global $world_name;
	
	check_world();
	
	if (isset($world_name)) {
		$chunks_per_tile_x_count = 10;
		$chunks_per_tile_z_count = 10;
		
		//use decachunk jpgs by default for speed:
		$tile_w = 160;
		$tile_h = 160;
		
		if (isset($chunk_mode_enable) and ($chunk_mode_enable===true)) {
			$tile_w = 16;
			$tile_h = 16;
			$chunks_per_tile_x_count = 1;
			$chunks_per_tile_z_count = 1;
		}
		else {
			$chunk_mode_enable=false;
		}
		
		$locations_per_tile_x_count = $chunks_per_tile_x_count*16;
		$locations_per_tile_z_count = $chunks_per_tile_z_count*16;
			
		if ($chunkymap_view_zoom<$chunkymap_view_min_zoom) $chunkymap_view_zoom = $chunkymap_view_min_zoom;
		if ($chunkymap_view_zoom>$chunkymap_view_max_zoom) $chunkymap_view_zoom = $chunkymap_view_max_zoom;

		$EM_PER_WIDTH_COUNT = 800.0/12.0;
		
		$world_camera_w = (800/$tile_w) * (1.0/$chunkymap_view_zoom); //screen should be 800pt wide always (so 12pt is similar on all screens and only varies with physical size of screen in inches, and since pt was invented to replace px)
		$world_camera_left = $chunkymap_view_x-$world_camera_w/2.0;
		
		$world_camera_h = $world_camera_w; //start with square camera to make sure enough chunks are loaded and since neither screen height nor ratio can be known from php since it is only run on server-side
		$world_camera_top = $chunkymap_view_z+$world_camera_h/2.0; //plus since cartesian until drawn [then flipped]
		
		$chunky_view_x = get_chunky_coord_from_location($chunkymap_view_x);
		$chunky_view_z = get_chunky_coord_from_location($chunkymap_view_z);

		#tile is either chunk or decachunk
		$min_tiley_x = -1;
		$max_tiley_x = 0;
		$min_tiley_z = -1;
		$max_tiley_z = 0;
		
		$world_camera_right = $world_camera_left+$world_camera_w;
		$world_camera_bottom = $world_camera_top-$world_camera_h; //minus since cartesian until drawn [then flipped]
		
		//Only whether the near edges are in the canvas matters (get bottom of max since always cartesian until drawn [then inverted]):
		$min_tiley_x__chunk_location_right = $min_tiley_x*$locations_per_tile_x_count+$locations_per_tile_x_count;
		$max_tiley_x__chunk_location_left = $max_tiley_x*$locations_per_tile_x_count;
		$min_tiley_z__chunk_location_top = $min_tiley_z*$locations_per_tile_z_count;
		$max_tiley_z__chunk_location_bottom = $max_tiley_z*$locations_per_tile_z_count+$locations_per_tile_z_count;
		
		while ($min_tiley_x__chunk_location_right>$world_camera_left) {
			$min_tiley_x -= 1;
			$min_tiley_x__chunk_location_right = $min_tiley_x*$locations_per_tile_x_count+$locations_per_tile_x_count;
		}
		while ($max_tiley_x__chunk_location_left<$world_camera_right) {
			$max_tiley_x += 1;
			$max_tiley_x__chunk_location_left = $max_tiley_x*$locations_per_tile_x_count;
		}
		while ($min_tiley_z__chunk_location_top>$world_camera_bottom) {
			$min_tiley_z -= 1;
			$min_tiley_z__chunk_location_top = $min_tiley_z*$locations_per_tile_z_count;
		}
		while ($max_tiley_z__chunk_location_bottom<$world_camera_top) {
			$max_tiley_z += 1;
			$max_tiley_z__chunk_location_bottom = $max_tiley_z*$locations_per_tile_z_count+$locations_per_tile_z_count;
		}
		
		$tile_x_count = $max_tiley_x-$min_tiley_x+1;
		$tile_z_count = $max_tiley_z-$min_tiley_z+1;	
		if ($html4_mode_enable!==true) {
			echo '<canvas id="myCanvas"></canvas> ';
			echo '<script>
				var my_canvas = document.getElementById("myCanvas");
				var chunkymap_view_x='.$chunkymap_view_x.';
				var chunkymap_view_z='.$chunkymap_view_z.';
				var chunkymap_view_zoom='.$chunkymap_view_zoom.';
				var chunkymap_view_max_zoom='.$chunkymap_view_max_zoom.';
				var chunkymap_view_min_zoom='.$chunkymap_view_min_zoom.';
				var chunkymap_zoom_delta='.$chunkymap_change_zoom_multiplier.';
				var chunk_mode_enable='.get_javascript_bool_value($chunk_mode_enable).';
				var debug_mode_enable='.get_javascript_bool_value($debug_mode_enable).';
				var chunks_per_tile_x_count='.$chunks_per_tile_x_count.';
				var chunks_per_tile_z_count='.$chunks_per_tile_z_count.';
				var tile_w='.$tile_w.';
				var tile_h='.$tile_h.';
				var EM_PER_WIDTH_COUNT = '.$EM_PER_WIDTH_COUNT.';
				var size_1em_pixel_count = null;
				var font_string = null;
				//var ctx = my_canvas.getContext("2d");
				//ctx.canvas.width = window.innerWidth;
				//ctx.canvas.height = window.innerHeight;
				//ctx.fillStyle = "rgb(r,g,b)";
				var size_1pt_pixel_count = null;
				var padding_w = null;
				var padding_h = null;
				var pen_x = null;
				var world_camera_w = null; //calculated below
				var world_camera_h = null; //calculated below
				var current_w = null;
				var current_h = null;
				var current_ratio = null;
				var zoom_in_button_index = null;
				var zoom_out_button_index = null;
				var zoom_out_label_index = null;
				var location_label_index = null;
				
				function zoom_in() {
					chunkymap_view_zoom*=chunkymap_zoom_delta;
					draw_map();
				}
				function zoom_out() {
					chunkymap_view_zoom/=chunkymap_zoom_delta;
					draw_map();
				}
				function process_view_change() {
					//NOTE: this should be exactly the same math as php uses to make sure there are the same #of tiles displayed as were loaded by php
					if (current_w>current_h) {
						world_camera_w = (800/tile_w) * (1.0/chunkymap_view_zoom);
						world_camera_h = world_camera_w/current_ratio;
					}
					else {
						world_camera_h = (800/tile_h) * (1.0/chunkymap_view_zoom);
						world_camera_w = world_camera_h*current_ratio;
					}
				}
				
				function process_resize(ctx) {
					//var ctx = my_canvas.getContext("2d");
					ctx.canvas.width = window.innerWidth;
					ctx.canvas.height = window.innerHeight;
					//current_w = ctx.canvas.width;
					//current_h = ctx.canvas.width;
					current_w = window.innerWidth;
					current_h = window.innerHeight;
					current_ratio = current_w/current_h;
					
					//if (ctx.canvas.height<ctx.canvas.width) {
					//	size_1em_pixel_count = Math.round(ctx.canvas.height/32);
					//}
					//else {
					size_1em_pixel_count = Math.round(ctx.canvas.width/EM_PER_WIDTH_COUNT);
					//}
					font_string = Math.round(size_1em_pixel_count)+"px Arial";
					size_1pt_pixel_count = size_1em_pixel_count/16;
					padding_w = size_1em_pixel_count/2;
					padding_h = size_1em_pixel_count/2;
					
					process_view_change();
				}
				
				var bw_count = 0;
				var bawidgets = new Array();
				var last_bawidget = null;
				function add_bawidget(x, y, width, height, this_onclick, name) {
					this_widget = Array();
					this_widget["x"] = x;
					this_widget["y"] = y;
					this_widget["width"] = width;
					this_widget["height"] = height;
					this_widget["click_event"] = this_onclick;
					this_widget["name"] = name;

					this_widget["image"] = null;
					this_widget["text"] = null;
					bawidgets[bw_count] = this_widget;
					last_bawidget = this_widget;
					bw_count++;
				}
				function contains_coords(bawidget, cursor_x, cursor_y) {
					right = bawidget.x+bawidget.width;
					bottom = bawidget.y+bawidget.height;
					return cursor_x>=bawidget.x && cursor_y>=bawidget.y && cursor_x<right && cursor_y<bottom;
				}
				function click_if_contains(bawidget, cursor_x, cursor_y) {
					if (contains_coords(bawidget, cursor_x, cursor_y)) {
						if (bawidget["click_event"] != null) {
							bawidget["click_event"]();
						}
					}
				}
				
				function process_zoom_change() {
					var zoom_in_img = null;
					var zoom_out_img = null;
					var zoom_in_img_disabled = null;
					var zoom_out_img_disabled = null;
					var tmp_zoom_out_ptr = zoom_out;
					var tmp_zoom_in_ptr = zoom_in;
					
					if (chunkymap_view_zoom<chunkymap_view_min_zoom) {chunkymap_view_zoom = chunkymap_view_min_zoom;}
					if (chunkymap_view_zoom>chunkymap_view_max_zoom) {chunkymap_view_zoom = chunkymap_view_max_zoom;}
					
					if (chunkymap_view_zoom==chunkymap_view_min_zoom) {
						zoom_out_img = document.getElementById("zoom_out_disabled");
						tmp_zoom_out_ptr = null;
					}
					else {
						zoom_out_img = document.getElementById("zoom_out");
					}
					if (chunkymap_view_zoom==chunkymap_view_max_zoom) {
						zoom_in_img = document.getElementById("zoom_in_disabled");
						tmp_zoom_in_ptr = null;
					}
					else {
						zoom_in_img = document.getElementById("zoom_in");
					}
					location_label["text"] = chunkymap_view_x+","+chunkymap_view_z;
					
					zoom_label_value=chunkymap_view_zoom*100;
					if (zoom_label_value>1) {
						zoom_label_value = Math.round(zoom_label_value, 1);
					}
					else {
						zoom_label_value = Math.round(zoom_label_value, 7);
					}
					zoom_label["text"]=zoom_label_value+"%";
					
					zoom_in_button["click_event"]=tmp_zoom_in_ptr;
					zoom_in_button["image"]=zoom_in_img;
					zoom_out_button["click_event"]=tmp_zoom_out_ptr;
					zoom_out_button["image"]=zoom_out_img;
				}
				
				
				function draw_map() {
					process_zoom_change();
					var r = 0; //border
					var g = 0; //exists
					var b = 0; //
					
					var alert_string="";
					if (current_ratio==null) {
						alert_string+="current_ratio is null; ";
					}
					if (font_string==null) {
						alert_string+="font_string is null; ";
					}
					if (current_w==null) {
						alert_w+="current_ratio is null; ";
					}
					if (current_w==null) {
						alert_w+="current_ratio is null; ";
					}
					if (current_ratio==null) {
						alert_string+="current_ratio is null; ";
					}
					if (alert_string.length>0) {
						alert(alert_string);
					}
					
					var ctx = my_canvas.getContext("2d");
					process_resize(ctx);
					
					ctx.fillStyle = "black";
					ctx.fillRect(0,0,ctx.canvas.width,ctx.canvas.height);
					
					ctx.fillStyle = "white";
					ctx.rect(20,20,150,100);
					ctx.stroke(); 
					
					//size_1pt_pixel_count = ctx.canvas.height/600.0;
					var bw_index = 0;
					
					
					
					for (i=0; i<bawidgets.length; i++) {
						this_widget = bawidgets[i];
						this_img = this_widget["image"]				
						if (this_widget["text"] != null) {
							ctx.font = font_string;
							ctx.fillStyle = "rgb(255,255,255)";
							ctx.fillText(this_widget["text"], this_widget["x"], this_widget["y"]);
						}
						else if (this_img != null) {
							ctx.drawImage(this_img, this_widget.x, this_widget.y, this_widget.width, this_widget.height);
						}
					}
				}
				
				window.onload = function() {
					my_canvas.onclick = function(event) {
						for (i=0; i<bawidgets.length; i++) {
							click_if_contains(bawidgets[i], event.clientX, event.clientY);
						}
					};
					
					var ctx = my_canvas.getContext("2d");
					process_resize(ctx);
					
					var pen_x = size_1em_pixel_count;
					var pen_y = size_1em_pixel_count;
					var tmp_w = null;
					var tmp_h = null;
					var compass_rose_w = size_1em_pixel_count*5;
					
					
					
					
					//LOCATION LABEL (no click):
					bw_index = add_bawidget(pen_x+compass_rose_w/4, pen_y, tmp_w, tmp_h, null, "location_label");
					location_label = last_bawidget;
					//done on each draw: last_bawidget["text"] = 
					
					pen_y += size_1em_pixel_count + padding_h;
					
					//COMPASS ROSE (no click):
					var compass_rose_img = document.getElementById("compass-rose");
					var this_h_ratio = compass_rose_img.height/compass_rose_img.width;
					tmp_w = compass_rose_w;
					tmp_h = tmp_w*this_h_ratio;
					bw_index = add_bawidget(pen_x-padding_w, pen_y, tmp_w, tmp_h, null, "compass-rose");
					last_bawidget["image"] = compass_rose_img;
					compass_rose_img.style.visibility="hidden";
					pen_y += last_bawidget.height+padding_h;
					
					//ZOOM LABEL (no click):
					bw_index = add_bawidget(pen_x+compass_rose_w/5, pen_y, tmp_w, tmp_h, null, "zoom_label");
					zoom_label = last_bawidget;
					//done on each draw: last_bawidget["text"] = (chunkymap_view_zoom*100)+"%"
					pen_y += size_1em_pixel_count + padding_h;

					//ZOOM IN:
					var zoom_in_img = document.getElementById("zoom_in");
					this_h_ratio = zoom_in_img.height/zoom_in_img.width;
					tmp_w = size_1em_pixel_count*2;
					tmp_h = tmp_w*this_h_ratio;
					bw_index = add_bawidget(pen_x, pen_y, tmp_w, tmp_h, null, "zoom_in", null);
					//zoom_in_button_index = bw_index;
					zoom_in_button = last_bawidget;
					last_bawidget["image"]=zoom_in_img;
					zoom_in_img.style.visibility="hidden";
					document.getElementById("zoom_in_disabled").style.visibility="hidden";
					//pen_y += tmp_h+padding_h;
					pen_x += tmp_w;
					
					//ZOOM OUT
					var zoom_out_img = document.getElementById("zoom_out");
					this_h_ratio = zoom_out_img.height/zoom_out_img.width;
					tmp_w = size_1em_pixel_count*2;
					tmp_h = tmp_w*this_h_ratio;
					bw_index = add_bawidget(pen_x, pen_y, tmp_w, tmp_h, null, "zoom_out", null);
					zoom_out_button = last_bawidget;
					//zoom_out_button_index = bw_index;
					last_bawidget["image"]=zoom_out_img;
					zoom_out_img.style.visibility="hidden";
					document.getElementById("zoom_out_disabled").style.visibility="hidden";
					pen_y += tmp_h+padding_h;
					pen_x -= tmp_w;			
					
					
					draw_map();
				}
				</script>
				';
		}//end if not $html4_mode_enable
		global $td_decachunk_placeholder_content;
		global $td_chunk_placeholder_content;
		$td_tile_placeholder_content = null;
		if ($chunk_mode_enable) {
			$td_tile_placeholder_content = $td_chunk_placeholder_content;
		}
		else {
			$td_tile_placeholder_content = $td_decachunk_placeholder_content
		}
		echo '<img id="compass-rose" src="chunkymapdata/images/compass_rose.png"/>';
		echo '<img id="zoom_in" src="chunkymapdata/images/zoom_in.png"/>';
		echo '<img id="zoom_in_disabled" src="chunkymapdata/images/zoom_in_disabled.png"/>';
		echo '<img id="zoom_out" src="chunkymapdata/images/zoom_out.png"/>';
		echo '<img id="zoom_out_disabled" src="chunkymapdata/images/zoom_out_disabled.png"/>';
		$this_tiley_z=$max_tiley_z; //start at max since screen is inverted cartesian
		if ($debug_mode_enable!==true) {
			//this table loads the images then is hidden when javascript runs successfully, but it is also a map though not very functional
			echo '<table id="chunkymap_table" cellspacing="0" cellpadding="0" style="width:100%">'."\r\n";
			echo '  <tr>'."\r\n";
			echo '    <td style="width:5%">'."$td_tile_placeholder_content".'</td>'."\r\n";
			echo "    <td style=\"width:95%\"><a href=\"?world_name=$world_name&chunkymap_view_zoom=$chunkymap_view_zoom&chunkymap_view_x=$chunkymap_view_x&chunkymap_view_z=".($chunkymap_view_z+($world_camera_h*$chunkymap_camera_pan_delta))."#chunkymap_top\">".'<img src="chunkymapdata/images/arrow-wide-up.png" style="width:90%"/>'.'</a></td>'."\r\n";
			echo '    <td style="width:5%">'."$td_tile_placeholder_content".'</td>'."\r\n";
			echo '  </tr>'."\r\n";
			$cell_perc=intval(round(100.0/$decachunky_count_x));
			echo '  <tr>'."\r\n";
			echo "    <td style=\"width:5%\"><a href=\"?world_name=$world_name&chunkymap_view_zoom=$chunkymap_view_zoom&chunkymap_view_x=".($chunkymap_view_x-($world_camera_w*$chunkymap_camera_pan_delta))."&chunkymap_view_z=$chunkymap_view_z#chunkymap_top\">".'<img src="chunkymapdata/images/arrow-wide-left.png" style="width:90%"/>'.'</a></td>'."\r\n";
			echo '    <td style="width:95%">'."\r\n";		
			echo '      <table id="chunk_table" cellpadding="0" cellspacing="0" style="width:100%">'."\r\n";
			while ($this_tiley_z>=$min_tiley_z) {
				$this_tiley_x=$min_tiley_x;
				echo "        <tr>\r\n";
				while ($this_tiley_x<=$max_tiley_x) {
					$img_path=null;
					echo "        <td>";
					if ($chunk_mode_enable) {
						$img_path=get_chunk_image_path_from_chunky_coords($this_tiley_x, $this_tiley_z);
						if (!is_file($img_path)) {
							echo "<!-- no chunk $img_path -->";
							$img_path="chunkymapdata/images/chunk-blank.jpg";
						}
					}
					else {
						$img_path=get_decachunk_image_path_from_decachunk($this_tiley_x, $this_tiley_z);
						if (!is_file($img_path)) {
							echo "<!-- no decachunk $img_path -->";
							$img_path="chunkymapdata/images/decachunk-blank.jpg";
						}
					}
					echo "<img class=\"maptileimg\" src=\"$img_path\" style=\"width:100%\"/>"."</td>\r\n";
					$this_tiley_x++;
				}
				echo "        </tr>\r\n";
				$this_tiley_z-=1;
			}
			echo '      </table>';
			echo '    </td>'."\r\n";
			echo "    <td style=\"width:5%\"><a href=\"?world_name=$world_name&chunkymap_view_zoom=$chunkymap_view_zoom&chunkymap_view_x=".($chunkymap_view_x+($world_camera_w*$chunkymap_camera_pan_delta))."&chunkymap_view_z=$chunkymap_view_z#chunkymap_top\">".'<img src="chunkymapdata/images/arrow-wide-right.png" style="width:100%"/>'.'</a></td>'."\r\n";
			echo '  </tr>'."\r\n";
			echo '  <tr>'."\r\n";
			echo '    <td style="width:5%">'."$td_decachunk_placeholder_content".'</td>'."\r\n";
			echo "    <td style=\"width:90%\"><a href=\"?world_name=$world_name&chunkymap_view_zoom=$chunkymap_view_zoom&chunkymap_view_x=$chunkymap_view_x&chunkymap_view_z=".($chunkymap_view_z-($world_camera_h*$chunkymap_camera_pan_delta))."#chunkymap_top\">".'<img src="chunkymapdata/images/arrow-wide-down.png" style="width:100%"/>'.'</a></td>'."\r\n";
			echo '    <td style="width:5%">'."$td_decachunk_placeholder_content".'</td>'."\r\n";
			echo '  </tr>'."\r\n";
			echo '</table>'."\r\n";
		}
	}
	else { //not isset($world_name)
		echo "<h4>Choose world:</h4>";
		echo "<ul>";
		if ($chunkymapdata_handle = opendir($chunkymapdata_worlds_path)) {
			$append_vars="&";
			if (isset($chunkymap_view_zoom)) {
				$prefix = "";
				if (strlen($append_vars)>0 and !endsWith($append_vars,"&")) {
					$prefix = "&";
				}
				$append_vars.="$prefix"."&chunkymap_view_zoom=$chunkymap_view_zoom";
			}
			if (isset($chunkymap_anchor_name)) {
				$prefix = "";
				if (strlen($append_vars)>0) {
					$prefix = "&";
				}
				$append_vars.="$prefix"."#$chunkymap_anchor_name";
			}
			global $chunkymap_anchor_name;
			while (false !== ($this_world_name = readdir($chunkymapdata_handle))) {
				if (substr($this_world_name, 0, 1) != ".") {
					$this_world_path = $chunkymapdata_worlds_path."/".$this_world_name;
					echo "<li><a href=\"?world_name=$this_world_name"."$append_vars#$chunkymap_anchor_name"."\">$this_world_name</a></li>";
				}
			}
			closedir($chunkymapdata_handle);
		}
		echo "</ul>";
	}
	
	//TODO: $chunkymap_view_zoom SHOULD BE interpreted so each block (pixel) is 1pt: 1066x600 pt canvas would have 66+2/3 blocks horizontally, is 37.5 blocks vertically
	//so, at zoom 1.0 canvas should show 60 chunks across (6 decachunks across)
}//end echo_chunkymap_canvas


function check_world() {
	global $chunkymapdata_thisworld_path;
	global $world_name;
	global $chunkymapdata_worlds_path;
	if (!isset($world_name)) {
		if ($handle = opendir($chunkymapdata_worlds_path)) {
			while (false !== ($file_name = readdir($handle))) {
				if (substr($file_name, 0, 1) != ".") {
					$file_path = $chunkymapdata_worlds_path."/".$file_name;
					if (is_dir($file_path)) {
						$world_name=$file_name;
						break;
					}
				}
			}
			closedir($handle);
		}
	}
	if (isset($world_name)) {
		$chunkymapdata_thisworld_path = $chunkymapdata_worlds_path."/".$world_name;
	}
}

?>

