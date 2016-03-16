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
$chunkymap_zoom_delta=1.5;
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
function echo_chunkymap_anchor() {
    global $chunkymap_anchor_name;
    echo "<a name=\"$chunkymap_anchor_name\"></a>";
}
function echo_chunkymap_controls() {
    global $chunkymap_view_x;
    global $chunkymap_view_z;
    global $chunkymap_view_zoom;
    global $chunkymap_view_max_zoom;
    global $chunkymap_view_min_zoom;
    global $chunkymap_anchor_name;
    $is_in=false;
    $is_out=false;
    $in_img_name = "zoom-in.png";
    $out_img_name = "zoom-out.png";

    $in_zoom = $chunkymap_view_zoom;
    if ($in_zoom<$chunkymap_view_max_zoom) {
        $is_in=true;
        $in_zoom = $chunkymap_view_zoom*2.0;
        //echo "in:$in_zoom ";
    }
    else $in_img_name = "zoom-in_disabled.png";

    $out_zoom = $chunkymap_view_zoom;
    if ($out_zoom>$chunkymap_view_min_zoom) {
        $is_out=true;
        $out_zoom = ($chunkymap_view_zoom/2.0);
    }
    else $out_img_name = "zoom-out_disabled.png";

    $zoom_clip = $chunkymap_view_max_zoom;
    $found=false;
    while ($zoom_clip>=$chunkymap_view_min_zoom) {
        if ($out_zoom>$zoom_clip) {
            $out_zoom=$zoom_clip*2;
            $found=true;
            break;
        }
        $zoom_clip = $zoom_clip/2;
    }
    if (!$found) {
        $out_zoom=$chunkymap_view_min_zoom;
    }
    //if ($in_zoom>$chunkymap_view_max_zoom) {
    //  $in_zoom=$chunkymap_view_max_zoom;
    //  echo "<!--clipping to max $chunkymap_view_max_zoom-->";
    //}
    //elseif ($in_zoom>200) $in_zoom=400;
    //elseif ($in_zoom>100) $in_zoom=200;
    //elseif ($in_zoom>75) $in_zoom=100;
    //if ($in_zoom>50) $in_zoom=75;
    //elseif ($in_zoom>25) $in_zoom=50;
    //elseif ($in_zoom>12) $in_zoom=25;
    //elseif ($in_zoom>4) $in_zoom=12;
    //elseif ($in_zoom>2) $in_zoom=4;
    //elseif ($in_zoom>1) $in_zoom=2;
    //else $in_zoom=$chunkymap_view_min_zoom;  // if ($in_zoom>1) $in_zoom=5;
    //echo "in:$in_zoom ";
    // if ($out_zoom<$chunkymap_view_min_zoom) $out_zoom=$chunkymap_view_min_zoom;
    // elseif ($out_zoom<2) $out_zoom=1;
    // elseif ($out_zoom<4) $out_zoom=2;
    // elseif ($out_zoom<12) $out_zoom=4;
    // elseif ($out_zoom<25) $out_zoom=12;
    // elseif ($out_zoom<50) $out_zoom=25;
    // elseif ($out_zoom<75) $out_zoom=50;
    // elseif ($out_zoom<100) $out_zoom=75;
    //elseif ($out_zoom<200) $out_zoom=100;
    //elseif ($out_zoom<$chunkymap_view_max_zoom) $out_zoom=(int)($chunkymap_view_max_zoom/2);
    //else $out_zoom=$chunkymap_view_max_zoom; //if ($out_zoom>76) $out_zoom=100;
    $zoom_clip=$chunkymap_view_min_zoom;
    $found=false;
    while ($zoom_clip<=$chunkymap_view_max_zoom) {
        if ($in_zoom<($zoom_clip*2)) {
            $in_zoom=$zoom_clip;
            $found=true;
            break;
        }
        $zoom_clip = $zoom_clip * 2;
    }
    if (!$found) $in_zoom=$chunkymap_view_max_zoom;

    $in_html="<img src=\"chunkymapdata/images/$in_img_name\" style=\"width:0.5in; height:0.5in\" />";
    $out_html="<img src=\"chunkymapdata/images/$out_img_name\" style=\"width:0.5in; height:0.5in\" />";
	global $world_name;
	$append_vars="";
	if (isset($world_name)) {
		$append_vars.="&"."world_name=$world_name";
	}
    if ($is_in) $in_html="<a href=\"?chunkymap_view_zoom=$in_zoom"."$append_vars"."#$chunkymap_anchor_name\">$in_html</a>";
    if ($is_out) $out_html="<a href=\"?chunkymap_view_zoom=$out_zoom"."$append_vars"."#$chunkymap_anchor_name\">$out_html</a>";
    echo $in_html;
    echo $out_html;
}

$is_echo_never_held=false;
$held_echos="";
function echo_hold($val) {
    global $is_echo_never_held;
    global $held_echos;
    if (!$is_echo_never_held) $held_echos.="$val";
    else echo "$val";
}

function echo_release() {
    global $held_echos;
    global $is_echo_never_held;
    if (!$is_echo_never_held) echo "$held_echos";
    $held_echos="";
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

function get_javascript_bool_value($this_bool) {
	$result = "false";
	if ($this_bool == true) {
		$result = "true";
	}
	return $result;
}

//chunk_mode_enable: shows chunk png images instead of decachunk jpg images (slower)
//debug_mode_enable: draws colored rectangles based on yml files instead of drawing images
function echo_chunkymap_canvas($chunk_mode_enable, $debug_mode_enable) {
    global $chunkymap_view_x;
    global $chunkymap_view_z;
    global $chunkymap_view_zoom;
    global $chunkymap_view_max_zoom;
    global $chunkymap_view_min_zoom;
	global $showplayers;
	global $chunkymap_zoom_delta;
	
	check_world();
	
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
	
	//$tile_x_count = $max_tiley_x-$min_tiley_x+1;
	//$tile_z_count = $max_tiley_z-$min_tiley_z+1;	

	echo '<canvas id="myCanvas"></canvas> ';
	echo '<script>
		var my_canvas = document.getElementById("myCanvas");
		var chunkymap_view_x='.$chunkymap_view_x.';
		var chunkymap_view_z='.$chunkymap_view_z.';
		var chunkymap_view_zoom='.$chunkymap_view_zoom.';
		var chunkymap_view_max_zoom='.$chunkymap_view_max_zoom.';
		var chunkymap_view_min_zoom='.$chunkymap_view_min_zoom.';
		var chunkymap_zoom_delta='.$chunkymap_zoom_delta.';
		var chunk_mode_enable='.get_javascript_bool_value($chunk_mode_enable).';
		var debug_mode_enable='.get_javascript_bool_value($debug_mode_enable).';
		var chunks_per_tile_x_count='.$chunks_per_tile_x_count.';
		var chunks_per_tile_z_count='.$chunks_per_tile_z_count.';
		var tile_w='.$tile_w.';
		var tile_h='.$tile_h.';
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
			if (ctx.canvas.height<ctx.canvas.width) {
				size_1em_pixel_count = Math.round(ctx.canvas.height/32);
			}
			else {
				size_1em_pixel_count = Math.round(ctx.canvas.width/32);
			}
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
				zoom_out_img = document.getElementById("zoom-out_disabled");
				tmp_zoom_out_ptr = null;
			}
			else {
				zoom_out_img = document.getElementById("zoom-out");
			}
			if (chunkymap_view_zoom==chunkymap_view_max_zoom) {
				zoom_in_img = document.getElementById("zoom-in_disabled");
				tmp_zoom_in_ptr = null;
			}
			else {
				zoom_in_img = document.getElementById("zoom-in");
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
			var zoom_in_img = document.getElementById("zoom-in");
			this_h_ratio = zoom_in_img.height/zoom_in_img.width;
			tmp_w = size_1em_pixel_count*2;
			tmp_h = tmp_w*this_h_ratio;
			bw_index = add_bawidget(pen_x, pen_y, tmp_w, tmp_h, null, "zoom-in", null);
			//zoom_in_button_index = bw_index;
			zoom_in_button = last_bawidget;
			last_bawidget["image"]=zoom_in_img;
			zoom_in_img.style.visibility="hidden";
			document.getElementById("zoom-in_disabled").style.visibility="hidden";
			//pen_y += tmp_h+padding_h;
			pen_x += tmp_w;
			
			//ZOOM OUT
			var zoom_out_img = document.getElementById("zoom-out");
			this_h_ratio = zoom_out_img.height/zoom_out_img.width;
			tmp_w = size_1em_pixel_count*2;
			tmp_h = tmp_w*this_h_ratio;
			bw_index = add_bawidget(pen_x, pen_y, tmp_w, tmp_h, null, "zoom-out", null);
			zoom_out_button = last_bawidget;
			//zoom_out_button_index = bw_index;
			last_bawidget["image"]=zoom_out_img;
			zoom_out_img.style.visibility="hidden";
			document.getElementById("zoom-out_disabled").style.visibility="hidden";
			pen_y += tmp_h+padding_h;
			pen_x -= tmp_w;			
			
			
			draw_map();
		}
		</script>
		';
	echo '<img id="compass-rose" src="chunkymapdata/images/compass-rose.png"/>';
	echo '<img id="zoom-in" src="chunkymapdata/images/zoom-in.png"/>';
	echo '<img id="zoom-in_disabled" src="chunkymapdata/images/zoom-in_disabled.png"/>';
	echo '<img id="zoom-out" src="chunkymapdata/images/zoom-out.png"/>';
	echo '<img id="zoom-out_disabled" src="chunkymapdata/images/zoom-out_disabled.png"/>';
	$this_tiley_z=$max_tiley_z; //start at max since screen is inverted cartesian
	if ($debug_mode_enable!==true) {
		//this table is hidden when javascript runs successfully, but it is also a map though not very functional
		echo '<table id="chunk_table" cellpadding="0" cellspacing="0" style="width:100%">'."\r\n";
		while ($this_tiley_z>=$min_tiley_z) {
			$this_tiley_x=$min_tiley_x;
			echo "  <tr>\r\n";
			while ($this_tiley_x<=$max_tiley_x) {
				$img_path=null;
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
				echo "  <td>"."<img class=\"maptileimg\" src=\"$img_path\" style=\"width:100%\"/>"."</td>\r\n";
				$this_tiley_x++;
			}
			echo "  </tr>\r\n";
			$this_tiley_z-=1;
		}
		echo '</table>';
	}
	
	//TODO: $chunkymap_view_zoom SHOULD BE interpreted so each block (pixel) is 1pt: 1066x600 pt canvas would have 66+2/3 blocks horizontally, is 37.5 blocks vertically
	//so, at zoom 1.0 canvas should show 60 chunks across (6 decachunks across)
}

function echo_decachunk_table() {
    global $chunkymap_view_x;
    global $chunkymap_view_z;
    global $chunkymap_view_zoom;
    global $chunkymap_view_max_zoom;
    global $chunkymap_view_min_zoom;
	global $showplayers;
	global $decachunk_dot_and_ext;
	global $decachunk_prefix_then_x_string;
	
	check_world();
	global $chunkymapdata_thisworld_path;
	global $world_name;
	global $chunkymapdata_worlds_path;
	global $z_opener;
	
    if ($chunkymap_view_zoom<$chunkymap_view_min_zoom) $chunkymap_view_zoom = $chunkymap_view_min_zoom;
    if ($chunkymap_view_zoom>$chunkymap_view_max_zoom) $chunkymap_view_zoom = $chunkymap_view_max_zoom;
	
	$decachunks_per_page = intval(6.0/$chunkymap_view_zoom);
	if ($decachunks_per_page<1) {
		$decachunks_per_page = 1;
	}
	$viewer_ratio = 16.0/9.0;
	$world_camera_w = 6.0 * (1.0/$chunkymap_view_zoom);
	$world_camera_h = $world_camera_w;
	//$world_camera_w = (($decachunks_per_page*160.0));
	//$world_camera_h = (($decachunks_per_page*160.0));
	
	$view_left = (($chunkymap_view_x)) - (($world_camera_w/2.0));
	$view_right = $view_left + $world_camera_w;
	//z is cartesian still:
	$view_top = (($chunkymap_view_z)) + (($world_camera_h/2.0));
	$view_bottom = $view_top - $world_camera_h;

	echo_chunkymap_anchor();
	echo_chunkymap_controls();
	echo "\r\n";
	echo " ".($chunkymap_view_zoom*100.0)."%\r\n";//(string)((int)($chunkymap_view_zoom*100+.5));
	//"chunkymapdata/images/compass-rose.png"
	//"chunkymapdata/images/start.png"
	$decachunky_min_x = get_decachunky_coord_from_location($view_left);
	$decachunky_min_z = get_decachunky_coord_from_location($view_bottom);
	$decachunky_max_x = get_decachunky_coord_from_location($view_right);
	$decachunky_max_z = get_decachunky_coord_from_location($view_top);
	$decachunky_count_x = $decachunky_max_x-$decachunky_min_x+1;
	$decachunky_count_z = $decachunky_max_z-$decachunky_min_z+1;
	
	//#region local vars
	$generated_yml_path = $chunkymapdata_thisworld_path."/generated.yml";
	//#endregion local vars
	
	$decachunky_z=$decachunky_max_z;
	//echo "<br/>";
	//echo "$decachunky_min_x:$decachunky_max_x,$decachunky_min_z:$decachunky_max_z<br/>";
	$td_placeholder_content="<!--widening table--><img src=\"chunkymapdata/images/decachunk-blank.jpg\" style=\"width:100%; -webkit-filter: opacity(40%); filter: opacity(40%); background-color:black\"/>";
	$td_1px_placeholder_content="<!--widening table--><img src=\"chunkymapdata/images/decachunk-blank.jpg\" style=\"width:1px; -webkit-filter: opacity(40%); filter: opacity(40%); background-color:black\"/>";
	echo '<table id="chunkymap_table" cellspacing="0" cellpadding="0" style="width:100%">'."\r\n";
	echo '  <tr>'."\r\n";
	echo '    <td style="width:5%">'."$td_placeholder_content".'</td>'."\r\n";
	echo "    <td style=\"width:95%\"><a href=\"?world_name=$world_name&chunkymap_view_zoom=$chunkymap_view_zoom&chunkymap_view_x=$chunkymap_view_x&chunkymap_view_z=".($chunkymap_view_z+($world_camera_h/2.0))."#chunkymap_top\">".'<img src="chunkymapdata/images/arrow-wide-up.png" style="width:90%"/>'.'</a></td>'."\r\n";
	echo '    <td style="width:5%">'."$td_placeholder_content".'</td>'."\r\n";
	echo '  </tr>'."\r\n";
	$cell_perc=intval(round(100.0/$decachunky_count_x));
	echo '  <tr>'."\r\n";
	echo "    <td style=\"width:5%\"><a href=\"?world_name=$world_name&chunkymap_view_zoom=$chunkymap_view_zoom&chunkymap_view_x=".($chunkymap_view_x-($world_camera_w/2.0))."&chunkymap_view_z=$chunkymap_view_z#chunkymap_top\">".'<img src="chunkymapdata/images/arrow-wide-left.png" style="width:90%"/>'.'</a></td>'."\r\n";
	echo '    <td style="width:95%">'."\r\n";
	echo '      <table id="decachunk_table" cellspacing="0" cellpadding="0" style="width:100%; background-color:black">'."\r\n";
	while ($decachunky_z>=$decachunky_min_z) {
		echo '        <tr>'."\r\n";
		$decachunky_x=$decachunky_min_x;
		$cell_perc_remaining=100;
		while ($decachunky_x<=$decachunky_max_x) {
			$decachunk_file_name=get_decachunk_image_name_from_decachunk($decachunky_x, $decachunky_z);
			$decachunk_file_path=get_decachunk_folder_path_from_decachunk($decachunky_x, $decachunky_z).'/'.$decachunk_file_name;
			$td_content="<!--no decachunk $decachunk_file_path--><img src=\"chunkymapdata/images/decachunk-blank.jpg\" style=\"width:100%\"/>";
			if (is_file($decachunk_file_path)) {
				$td_content="<img src=\"$decachunk_file_path\" style=\"width:100%\"/>";
			}
			$this_cell_perc=$cell_perc;
			if ($cell_perc_remaining>=$this_cell_perc) {
				echo "          <td style=\"width:$this_cell_perc%\">"."$td_content".'</td>'."\r\n";
				//echo '          <td>'."$decachunky_x,$decachunky_z".'</td>'."\r\n";
				$cell_perc_remaining-=$this_cell_perc;
			}
			$decachunky_x+=1;
		}
		if ($cell_perc_remaining>0) {
			$td_content=$td_1px_placeholder_content;
			echo "          <td>$td_content</td>"."\r\n";
		}
		echo '          </tr>'."\r\n";
		$decachunky_z-=1;
	}
	echo '      </table>'."\r\n";
	echo '    </td>'."\r\n";
	echo "    <td style=\"width:5%\"><a href=\"?world_name=$world_name&chunkymap_view_zoom=$chunkymap_view_zoom&chunkymap_view_x=".($chunkymap_view_x+($world_camera_w/2.0))."&chunkymap_view_z=$chunkymap_view_z#chunkymap_top\">".'<img src="chunkymapdata/images/arrow-wide-right.png" style="width:100%"/>'.'</a></td>'."\r\n";
	echo '  </tr>'."\r\n";
	echo '  <tr>'."\r\n";
	echo '    <td style="width:5%">'."$td_placeholder_content".'</td>'."\r\n";
	echo "    <td style=\"width:90%\"><a href=\"?world_name=$world_name&chunkymap_view_zoom=$chunkymap_view_zoom&chunkymap_view_x=$chunkymap_view_x&chunkymap_view_z=".($chunkymap_view_z-($world_camera_h/2.0))."#chunkymap_top\">".'<img src="chunkymapdata/images/arrow-wide-down.png" style="width:100%"/>'.'</a></td>'."\r\n";
	echo '    <td style="width:5%">'."$td_placeholder_content".'</td>'."\r\n";
	echo '  </tr>'."\r\n";
	echo '</table>'."\r\n";
}

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
//formerly echo_chunkymap_table
function echo_chunkymap_as_chunk_table($show_all_enable) {
    ini_set('display_errors', 1);
    ini_set('display_startup_errors', 1);
    error_reporting(E_ALL);
    //error_reporting(-1);


    global $is_echo_never_held;
    $is_echo_never_held=true;
    global $chunkymap_view_x;
    global $chunkymap_view_z;
    global $chunkymap_view_zoom;
    global $chunkymap_view_max_zoom;
    global $chunkymap_view_min_zoom;
    global $chunkymapdata_path;
	global $chunkymapdata_worlds_path;
    global $map_dict;
    global $is_verbose;
    global $chunkymap_tile_original_w;
    global $chunkymap_tile_original_h;
    global $chunkymap_view_max_zoom;
	global $world_name;
	global $chunk_dot_and_ext;
	global $z_opener;
	global $dot_yaml;

	echo_chunkymap_anchor();
	echo_chunkymap_controls();
	echo " ".($chunkymap_view_zoom*100.0)."%";//(string)((int)($chunkymap_view_zoom*100+.5));

    if ($chunkymap_view_zoom<$chunkymap_view_min_zoom) $chunkymap_view_zoom = $chunkymap_view_min_zoom;
    if ($chunkymap_view_zoom>$chunkymap_view_max_zoom) $chunkymap_view_zoom = $chunkymap_view_max_zoom;
    //$zoom_divisor = (int)(100/$chunkymap_view_zoom);
    $chunk_assoc = array();  // used for storing players; and used for determining which chunks are on the edge, since not all generated map tiles are the same size (edge tile images are smaller and corner ones are smaller yet)
    $chunk_count = 0;
    $chunk_prefix_then_x_string="chunk_x";
    
    
    $min_chunkx = 0;
    $min_chunkz = 0;
    $max_chunkx = 0;
    $max_chunkz = 0;
	$chunks_per_page = (1.0/$chunkymap_view_zoom)*10;

	$world_camera_w = (($chunks_per_page*16.0));
	$world_camera_h = (($chunks_per_page*16.0));
	$view_left = (($chunkymap_view_x)) - (($world_camera_w/2.0));
	$view_right = $view_left + $world_camera_w;
	//z is cartesian still:
	$view_top = (($chunkymap_view_z)) + (($world_camera_h/2.0));
	$view_bottom = $view_top - $world_camera_h;
	
	if (!$show_all_enable) {
		$min_chunkx=intval($view_left/$chunkymap_tile_original_w);
		$max_chunkx=intval($view_right/$chunkymap_tile_original_w);
		$min_chunkz=intval($view_bottom/$chunkymap_tile_original_w);
		$max_chunkz=intval($view_top/$chunkymap_tile_original_w);
	}
    global $showplayers;
    $players = array();
    $player_count = 0;
    $character_icon_w=8;
    $character_icon_h=8;
	global $chunkymapdata_thisworld_path;
	check_world();
	if (isset($world_name)) {
		$generated_yml_path = $chunkymapdata_thisworld_path."/generated.yml";
		if (is_file($generated_yml_path)) {
			$map_dict = get_dict_from_conf($generated_yml_path,":");
		}
		else {
			echo_error("Missing '".$generated_yml_path."'");
		}
		if ($showplayers==true) {
			$chunkymap_players_path = $chunkymapdata_thisworld_path."/players";
			if ($handle = opendir($chunkymap_players_path)) {
				while (false !== ($file_name = readdir($handle))) {
					if (substr($file_name, 0, 1) != ".") {
						$file_lower = strtolower($file_name);
						if (endsWith($file_lower, ".yml")) {
							$player_id=substr($file_name,0,strlen($file_name)-4); //-4 for .yml
							$file_path = $chunkymap_players_path."/".$file_name;
							if (is_file($file_path)) {
								$player_dict = get_dict_from_conf($file_path,":");
							}
							else {
								echo_error("Missing '$player_dict'");
							}
							$player_dict["id"]=$player_id;
							//$players[$player_count]=get_dict_from_conf($file_path);
							//$players[$player_count]["id"]=$player_id;
							//if (isset($player_dict["position"])) {
							if (isset($player_dict["x"]) and isset($player_dict["z"])) {
								//$tuple_string=trim($player_dict["position"]);
								//if ( startsWith($tuple_string, "(") and endsWith($tuple_string, ")") ) {
								//  $tuple_string=substr($tuple_string,1,strlen($tuple_string)-2);
								//}
								//$coordinates = explode(",", $tuple_string);
								//if (count($coordinates)==3) {
								//$nonchunky_x=(int)$coordinates[0];
								//$nonchunky_z=(int)$coordinates[2];
								$nonchunky_x=(int)$player_dict["x"];
								$nonchunky_z=(int)$player_dict["z"];
								$x = (int)( $nonchunky_x/$chunkymap_tile_original_w );
								$z = (int)( $nonchunky_z/$chunkymap_tile_original_h );
								$chunk_luid = "x".$x."z".$z;
								$rel_x = $nonchunky_x - ($x*$chunkymap_tile_original_w);
								$rel_z = $nonchunky_z - ($z*$chunkymap_tile_original_h);
								if (!isset($chunk_assoc[$chunk_luid])) {
									$chunk_assoc[$chunk_luid] = array();
								}
								if (!isset($chunk_assoc[$chunk_luid]["players"])) {
									$chunk_assoc[$chunk_luid]["players"] = array();
								}
								if (!isset($chunk_assoc[$chunk_luid]["players_count"])) {
									$chunk_assoc[$chunk_luid]["players_count"] = 0;
								}
								//already checked for position in outer case
								//DEPRECATED: $chunk_assoc[$chunk_luid][ "players" ][ $chunk_assoc[$chunk_luid]["players_count"] ][ "position" ] = $player_dict["position"];
								$chunk_assoc[$chunk_luid][ "players" ][ $chunk_assoc[$chunk_luid]["players_count"] ][ "x" ] = $player_dict["x"];
								$chunk_assoc[$chunk_luid][ "players" ][ $chunk_assoc[$chunk_luid]["players_count"] ][ "z" ] = $player_dict["z"];
								$chunk_assoc[$chunk_luid][ "players" ][ $chunk_assoc[$chunk_luid]["players_count"] ][ "rel_x" ] = $rel_x;
								$chunk_assoc[$chunk_luid][ "players" ][ $chunk_assoc[$chunk_luid]["players_count"] ][ "rel_z" ] = $rel_z;
								$chunk_assoc[$chunk_luid][ "players" ][ $chunk_assoc[$chunk_luid]["players_count"] ][ "file_path" ] = $file_path;

								if (isset($player_dict["name"])) {
									$chunk_assoc[$chunk_luid][ "players" ][ $chunk_assoc[$chunk_luid]["players_count"] ][ "text" ] = $player_dict["name"];
								}
								else {
									$chunk_assoc[$chunk_luid][ "players" ][ $chunk_assoc[$chunk_luid]["players_count"] ][ "text" ] = $player_dict["id"];
								}
								$chunk_assoc[$chunk_luid]["players_count"] += 1;
								//}
								//else {
								//  echo_error("Bad coordinates $tuple_string for player.");
								//}
							}
							else {
								echo_error("Missing player location in data: ".implode(" ",$player_dict));
							}

							//$player_count++;
						}
					}
				}
				closedir($handle);
			}
		}
		
		$chunkymap_markers_path = $chunkymapdata_thisworld_path."/markers";
		if ($handle = opendir($chunkymap_markers_path)) {
			while (false !== ($file_name = readdir($handle))) {
				if (substr($file_name, 0, 1) != ".") {
					$file_name_lower = strtolower($file_name);
					if (endsWith($file_name_lower, ".yml")) {
						$file_path = $chunkymap_markers_path."/".$file_name;
						$marker_vars = get_dict_from_conf($file_path, ":");
						$abs_pos = explode(",",$marker_vars["location"]);
						if (count($abs_pos)==3) {
							//convert from 3d to 2d:
							$abs_pos[1]=$abs_pos[3];
						}
						//$text = "";
						//if (isset($marker_vars["text"])) {
						//	$text = $marker_vars["text"];
						//}
						if (count($abs_pos)>=2) {
							$chunky_x = intval($abs_pos[0]/$chunkymap_tile_original_w);
							$chunky_z = intval($abs_pos[1]/$chunkymap_tile_original_h);
							$rel_x = intval($abs_pos[0]) - ($chunky_x*$chunkymap_tile_original_w);
							$rel_z = intval($abs_pos[1]) - ($chunky_z*$chunkymap_tile_original_h);
							$chunk_luid = 'x'.$chunky_x.'z'.$chunky_z;
							if (!isset($chunk_assoc[$chunk_luid])) {
								$chunk_assoc[$chunk_luid] = array();
							}
							if (!isset($chunk_assoc[$chunk_luid]["markers"])) {
								$chunk_assoc[$chunk_luid]["markers"] = array();
							}
							if (!isset($chunk_assoc[$chunk_luid]["markers_count"])) {
								$chunk_assoc[$chunk_luid]["markers_count"] = 0;
							}
							
							$chunk_assoc[$chunk_luid][ "markers" ][ $chunk_assoc[$chunk_luid]["markers_count"] ][ "x" ] = $abs_pos[0];
							$chunk_assoc[$chunk_luid][ "markers" ][ $chunk_assoc[$chunk_luid]["markers_count"] ][ "z" ] = $abs_pos[1];
							$chunk_assoc[$chunk_luid][ "markers" ][ $chunk_assoc[$chunk_luid]["markers_count"] ][ "rel_x" ] = $rel_x;
							$chunk_assoc[$chunk_luid][ "markers" ][ $chunk_assoc[$chunk_luid]["markers_count"] ][ "rel_z" ] = $rel_z;
							if (isset($marker_vars["image"])) {
								$chunk_assoc[$chunk_luid][ "markers" ][ $chunk_assoc[$chunk_luid]["markers_count"] ][ "image" ] = $marker_vars["image"];
							}
							if (isset($marker_vars["text"])) {
								$chunk_assoc[$chunk_luid][ "markers" ][ $chunk_assoc[$chunk_luid]["markers_count"] ][ "text" ] = $marker_vars["text"];
							}
							
							$chunk_assoc[$chunk_luid]["markers_count"] += 1;
						}
						else {
							echo_error("Bad location in marker file '$file_path'");
						}
					}
				}
			}
		}
		
		
		//if ($map_dict != null) {
		//  $min_chunkx = $map_dict["min_chunkx"];
		//  $min_chunkz = $map_dict["min_chunkz"];
		//  $max_chunkx = $map_dict["max_chunkx"];
		//  $max_chunkz = $map_dict["max_chunkz"];
		//}
		//else {
			//echo "calculating range...";
			//NOTE: even though *min and *max could be known from $map_dict, build a dict of chunks in order to align images properly since they are not all the same size:
			$chunks_16px_path = $chunkymapdata_thisworld_path.'/'."16px";
			if ($chunks_16px_handle = opendir($chunks_16px_path)) {
				while (false !== ($decachunk_x_name = readdir($chunks_16px_handle))) {
					$decachunk_x_path = $chunks_16px_path."/".$decachunk_x_name;
					if ((substr($decachunk_x_name, 0, 1) != ".") and is_dir($decachunk_x_path)) {
						$decachunk_x_handle = opendir($decachunk_x_path);
						while (false !== ($decachunk_z_name = readdir($decachunk_x_handle))) {
							$decachunk_folder_path = $decachunk_x_path."/".$decachunk_z_name;
							if ((substr($decachunk_z_name, 0, 1) != ".") and is_dir($decachunk_folder_path)) {
								$decachunk_z_handle = opendir($decachunk_folder_path);
								while (false !== ($chunk_name = readdir($decachunk_z_handle))) {
									$file_lower = strtolower($chunk_name);
									if (endsWith($file_lower, $chunk_dot_and_ext) and startsWith($file_lower, $chunk_prefix_then_x_string)) {
										$z_opener_index = strpos($file_lower, $z_opener, strlen($chunk_prefix_then_x_string));
										if ($z_opener_index !== false) {
											$x_len = $z_opener_index - strlen($chunk_prefix_then_x_string);
											$remaining_len = strlen($file_lower) - strlen($chunk_prefix_then_x_string) - $x_len - strlen($z_opener) - strlen($chunk_dot_and_ext);
											$x = substr($file_lower, strlen($chunk_prefix_then_x_string), $x_len);
											$z = substr($file_lower, $z_opener_index + strlen($z_opener), $remaining_len);
											if (is_int_string($x) and is_int_string($z)) {
												$chunk_luid = "x".$x."z".$z;
												if (!isset($chunk_assoc[$chunk_luid])) {
													$chunk_assoc[$chunk_luid] = array();
												}
												$chunk_assoc[$chunk_luid]["is_rendered"] = true;
												if ($is_verbose) echo "$chunk_luid,";
												if ($show_all_enable) {
													if ($x<$min_chunkx) {
														$min_chunkx=(int)$x;
													}
													if ($x>$max_chunkx) {
														$max_chunkx=(int)$x;
													}
													if ($z<$min_chunkz) {
														$min_chunkz=(int)$z;
													}
													if ($z>$max_chunkz) {
														$max_chunkz=(int)$z;
													}
												}
											}
											else {
												echo "misnamed chunk tile image '$chunk_name' had coordinates ".$x.",".$z." for x,z.";
											}
										}
									}
								}
								closedir($decachunk_z_handle);
							}
						}
						closedir($decachunk_x_handle);
					}
				}
				if ($is_verbose) echo "checked all chunks.";
				echo "<!--found chunks in x $min_chunkx to $max_chunkx and z $min_chunkz to $max_chunkz.-->";
				closedir($chunks_16px_handle);
			}
			else {
				echo_error("could not open $chunks_16px_path");
			}
		//}

		$x_count = $max_chunkx - $min_chunkx;
		$z_count = $max_chunkz - $min_chunkz;
		echo "\r\n";
		echo "<center>\r\n";
		//cellpadding="0" cellspacing="0" still needed for IE
		echo_hold( "  <table id=\"chunkymapstatictable\" cellpadding=\"0\" cellspacing=\"0\" style=\"border-spacing: 0px; border-style:solid; border-color:gray; border-width:0px\">\r\n");
		$z = (int)$max_chunkz;
		$scale=(float)$chunkymap_view_zoom; // no longer /100
		$zoomed_w=(int)((float)$chunkymap_tile_original_w*$scale+.5);
		$zoomed_h=(int)((float)$chunkymap_tile_original_h*$scale+.5);
		$genresult_suffix_then_dot_then_ext="_mapper_result.txt";
		
		$minute=60;
		$player_file_age_expired_max_seconds=20*$minute-1;
		$player_file_age_idle_max_seconds=5*$minute-1;
		$chunks_16px_path = $chunkymapdata_thisworld_path.'/'."16px";
		while ($z >= $min_chunkz) {
			echo_hold( "    <tr>\r\n");
			$x = (int)$min_chunkx;
			while ($x <= $max_chunkx) {
				$this_zoomed_w = $zoomed_w;
				$this_zoomed_h = $zoomed_h;

				//$chunk_yaml_path = $chunkymapdata_thisworld_path.'/'.$chunk_yaml_name;
				//$chunk_yaml_path = $chunks_16px_path.'/'.
				$chunk_yaml_path = get_chunk_yaml_path_from_chunky_coords($x,$z);
				//$chunk_genresult_name = $chunk_prefix_then_x_string.$x.$z_opener.$z.$genresult_suffix_then_dot_then_ext;
				//$chunk_genresult_path = $chunkymapdata_thisworld_path.'/'.$chunk_img_name;
				$td_style_suffix="";
				$element_align_style_suffix="";
				$alignment_comment="";
				//if (is_file($chunk_genresult_path)) {
					// contains lines such as:
					//    Result image (w=80 h=64) will be written to chunk_x0z1.png
					//    ('PNG Region: ', [0, 64, 80, 128])
					//    ('Pixels PerNode: ', 1)
					// where PNG Region's list value is an exclusive rect ordered as x1, y1, x2, y2
					//$found_original_w = null;
					//$found_original_h = null;
					//$this_zoomed_w=(int)((float)$found_original_w*$scale+.5);
					//this_zoomed_h=(int)((float)$found_original_h*$scale+.5);
				//}
				if (is_file($chunk_yaml_path)) {
					// contains lines such as:
					//is_marked_empty:False
					//is_marked:True
					//image_w:80
					//image_h:80
					//image_left:0
					//image_top:64
					//image_right:-80
					//image_bottom:-16
					// where if is_marked_empty, the remaining values don't exist
					$expected_left = (int)$x * (int)$chunkymap_tile_original_w;
					$expected_top = (int)$z * (int)$chunkymap_tile_original_h;
					$expected_right = (int)$x + (int)$chunkymap_tile_original_w;
					$expected_bottom = (int)$z + (int)$chunkymap_tile_original_h;
					$chunk_dict = get_dict_from_conf($chunk_yaml_path,":");
					if (isset($chunk_dict["image_w"])) {
						$this_zoomed_w=(int)((float)$chunk_dict["image_w"]*$scale+.5);
					}
					if (isset($chunk_dict["image_h"])) {
						$this_zoomed_h=(int)((float)$chunk_dict["image_h"]*$scale+.5);
					}
					//TODO: use image_* to determine (if the doesn't touch certain sides of image_w x image_h rect, change the following accordingly)
					if (isset($chunk_dict["image_left"])) {
						if (isset($chunk_dict["image_right"])) {
							if ( (int)$chunk_dict["image_left"] > $expected_left ) {
								$td_style_suffix.="text-align:right;";
								//$alignment_comment.="<!-- image_left:".$chunk_dict["image_left"]." is greater than expected $expected_left-->";
							}
							//elseif ( (int)$chunk_dict["image_right"] < $expected_right ) {
							//  $td_style_suffix.="text-align:left;";
							//}
							else {
								$td_style_suffix.="text-align:left;";
								//$alignment_comment.="<!-- image_left:".$chunk_dict["image_left"]." was the expected $expected_left-->";
							}
						}
					}

					//if (isset($chunk_dict["image_right"])) {
					//  if ( (int)$chunk_dict["image_right"] != $expected_right ) {
					//      $td_style_suffix.="text-align:left;";
					//  }
					//  //else {
					//  //  $td_style_suffix.="text-align:left;";
					//  //}
					//}

					if (isset($chunk_dict["image_top"])) {
						if (isset($chunk_dict["image_bottom"])) {
							if ( (int)$chunk_dict["image_top"] > $expected_top) {
								$element_align_style_suffix.="vertical-align:bottom;";
								//$alignment_comment.="<!-- image_top:".$chunk_dict["image_top"]." is greater than expected $expected_top-->";
							}
							//elseif ( (int)$chunk_dict["image_bottom"] < $expected_bottom) {
							//  $element_align_style_suffix.="vertical-align:top;";
							//}
							else {
								$element_align_style_suffix.="vertical-align:top;";
								//$alignment_comment.="<!-- image_top:".$chunk_dict["image_top"]." was the expected $expected_top-->";
							}
						}
					}
					//if (isset($chunk_dict["image_bottom"])) {
					//  if ( (int)$chunk_dict["image_bottom"] != $expected_bottom) {
					//      $element_align_style_suffix.="vertical-align:top;";
					//  }
					//  //else {
					//  //  $element_align_style_suffix.="vertical-align:bottom;";
					//  //}
					//}

					//$element_align_style_suffix.="vertical-align:left;";
				}

				echo_hold( "      <td width=\"1\" style=\"padding:0px; background-color:lightgray; $td_style_suffix $element_align_style_suffix\">");
				echo_hold("<div style=\"position: relative\">"); //causes child's absolute position to be relative to this div's location, as per http://www.w3schools.com/css/tryit.asp?filename=trycss_position_absolute
				$chunk_luid = "x".$x."z".$z;
				$chunk_img_path = get_chunk_image_path_from_chunky_coords($x, $z);
				if (is_file($chunk_img_path)) {
					echo_hold( "<img class=\"maptileimg\" style=\"width:$this_zoomed_w; height:$this_zoomed_h;\" src=\"$chunk_img_path\"/>");
				}
				else {
					//echo_hold( "<span style=\"font-size:1px\">&nbsp;</span>");
				}
				if (isset($chunk_assoc[$chunk_luid]["players_count"])) {
					echo "<!--CHUNK $chunk_luid: players_count=".$chunk_assoc[$chunk_luid]["players_count"]."-->";
					$nonprivate_name_beginning_char_count = 20;

					for ($player_count=0; $player_count<$chunk_assoc[$chunk_luid]["players_count"]; $player_count++) {
						$rel_x = $chunk_assoc[$chunk_luid][ "players" ][ $player_count ]["rel_x"];
						$rel_z = $chunk_assoc[$chunk_luid][ "players" ][ $player_count ]["rel_z"];
						$is_expired=false;
						$is_idle=false;
						if (isset($chunk_assoc[$chunk_luid][ "players" ][ $player_count ]["file_path"])) {
							$last_player_update_time=filemtime($chunk_assoc[$chunk_luid][ "players" ][ $player_count ]["file_path"]);
							if (time()-$last_player_update_time > $player_file_age_expired_max_seconds) {
								$is_expired=true;
							}
							elseif (time()-$last_player_update_time > $player_file_age_idle_max_seconds) {
								$is_idle=true;
							}
						}
						$text = $chunk_assoc[$chunk_luid]["players"][$player_count]["text"];
						if (strlen($chunk_assoc[$chunk_luid]["players"][$player_count]["text"])>$nonprivate_name_beginning_char_count) {
							$text = substr($text, 0, $nonprivate_name_beginning_char_count)."*";
						}
						//show head full size (not zoomed):
						$zoomed_head_w=$character_icon_w;//(int)((float)$character_icon_w*$scale+.5);
						$zoomed_head_h=$character_icon_h;//(int)((float)$character_icon_h*$scale+.5);
						$rel_x -= (int)($zoomed_head_w/2);
						$rel_z -= (int)($zoomed_head_h/2);
						//$img_style="position:absolute; ";
						$img_style="";
						$img_border_style="border: 1px solid white;";
						$text_style="color:white;";
						if ($is_expired==false) {
							if ($is_idle==true) {
								$img_border_style="border: 1px solid rgba(128,128,128,.5);";
								$img_style.="opacity: 0.4; filter: alpha(opacity=40);";  //filter is for IE8 and below
								$text_style="color:white; opacity: 0.4; filter: alpha(opacity=40);";   //filter is for IE8 and below
							}
							echo_hold( "<div style=\"position:absolute; z-index:999; left:$rel_x; top:$rel_z; width: $zoomed_head_w; height: $zoomed_head_h; $img_border_style\"><img src=\"$chunkymapdata_thisworld_path/players/singleplayer.png\" style=\"$img_style\"/><span style=\"$text_style\">$text</span></div>" );
						}
						//$position_offset_x+=$character_icon_w;
					}
				}
				else echo "<!--CHUNK $chunk_luid: no player count-->";

				if (isset($chunk_assoc[$chunk_luid]["markers_count"])) {
					echo "<!--CHUNK $chunk_luid: markers_count=".$chunk_assoc[$chunk_luid]["markers_count"]."-->";
					$nonprivate_name_beginning_char_count = 20;

					for ($marker_count=0; $marker_count<$chunk_assoc[$chunk_luid]["markers_count"]; $marker_count++) {
						$rel_x = $chunk_assoc[$chunk_luid][ "markers" ][ $marker_count ]["rel_x"];
						$rel_z = $chunk_assoc[$chunk_luid][ "markers" ][ $marker_count ]["rel_z"];
						$is_expired=false;
						$is_idle=false;
						// if (isset($chunk_assoc[$chunk_luid][ "markers" ][ $marker_count ]["file_path"])) {
							// $last_marker_update_time=filemtime($chunk_assoc[$chunk_luid][ "markers" ][ $marker_count ]["file_path"]);
							// if (time()-$last_marker_update_time > $marker_file_age_expired_max_seconds) {
								// $is_expired=true;
							// }
							// elseif (time()-$last_marker_update_time > $marker_file_age_idle_max_seconds) {
								// $is_idle=true;
							// }
						// }
						
						$text = $chunk_assoc[$chunk_luid]["markers"][$marker_count]["text"];
						$image_path = "";
						if (isset($chunk_assoc[$chunk_luid]["markers"][$marker_count]["image"])) {
							$image_path = $chunk_assoc[$chunk_luid]["markers"][$marker_count]["image"];
						}
						if (strlen($chunk_assoc[$chunk_luid]["markers"][$marker_count]["text"])>$nonprivate_name_beginning_char_count) {
							$text = substr($text, 0, $nonprivate_name_beginning_char_count)."*";
						}
						//show head full size (not zoomed):
						//$zoomed_head_w=$character_icon_w;//(int)((float)$character_icon_w*$scale+.5);
						//$zoomed_head_h=$character_icon_h;//(int)((float)$character_icon_h*$scale+.5);
						$zoomed_image_w=16;
						$zoomed_image_h=16;
						$rel_x -= (int)($zoomed_image_w/2);
						$rel_z -= (int)($zoomed_image_h/2);
						//$img_style="position:absolute; ";
						$img_style="";
						$img_border_style="";
						//$img_border_style="border: 1px solid white;";
						$text_style="color:white;";
						if ($is_expired==false) {
							if ($is_idle==true) {
								$img_border_style="";
								//$img_border_style="border: 1px solid rgba(128,128,128,.5);";
								$img_style.="opacity: 0.4; filter: alpha(opacity=40);";  //filter is for IE8 and below
								$text_style="color:white; opacity: 0.4; filter: alpha(opacity=40);";   //filter is for IE8 and below
							}
							echo_hold( "<div style=\"position:absolute; z-index:999; left:$rel_x; top:$rel_z; width: $zoomed_image_w; height: $zoomed_image_h; $img_border_style\"><img src=\"$image_path\" style=\"$img_style\"/><span style=\"$text_style\">$text</span></div>" );
						}
						//$position_offset_x+=$character_icon_w;
					}
				}
				else echo "<!--CHUNK $chunk_luid: no player count-->";
				
				//echo "        <br/>".$x.",0,".$z;
				echo_hold($alignment_comment);
				echo_hold("</div>");
				echo_hold( "</td>\r\n");
				$x++;
			}
			echo_hold( "    </tr>\r\n");
			echo_release();
			$z--;
		}
		echo "  </table>\r\n";
		echo "</center>\r\n";
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
}
?>

