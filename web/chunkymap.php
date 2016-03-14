<?php
#this is the backend--don't call it directly. instead do include_once('chunkymap.php'); for further info, see example.php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);


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
//$chunkymap_view_zoom_multiplier=25;
if (!isset($chunkymap_view_x)) {
    $chunkymap_view_x=0;
}
if (!isset($chunkymap_view_z)) {
    $chunkymap_view_z=0;
}
if (!isset($chunkymap_view_zoom_multiplier)) {
    $chunkymap_view_zoom_multiplier=.25;
}

$chunkymapdata_path = "chunkymapdata";
$chunkymapdata_worlds_path = $chunkymapdata_path."/worlds";
$chunkymapdata_thisworld_path = null;
$showplayers=true;

// NOT OPTIONAL:
$chunkymap_tile_original_w=16;
$chunkymap_tile_original_h=16;

$chunk_dimension_min=$chunkymap_tile_original_w;
if ($chunkymap_tile_original_h<$chunk_dimension_min) $chunk_dimension_min=$chunkymap_tile_original_h;

$chunkymap_view_min_zoom=1.0/$chunk_dimension_min; //should be a number that would get to exactly 100 eventually if multiplied by 2 repeatedly (such as 0.09765625); 0.005 was avoided since tiles used to be 80x80 pixels
$chunkymap_view_max_zoom=13107200.0;

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
function set_chunkymap_view($set_chunkymap_view_x, $set_chunkymap_view_z, $set_chunkymap_view_zoom_multiplier) {
    global $chunkymap_view_x;
    global $chunkymap_view_z;
    global $chunkymap_view_zoom_multiplier;
    $chunkymap_view_x = $set_chunkymap_view_x;
    $chunkymap_view_z = $set_chunkymap_view_z;
    $chunkymap_view_zoom_multiplier = $set_chunkymap_view_zoom_multiplier;
}
function echo_chunkymap_anchor() {
    global $chunkymap_anchor_name;
    echo "<a name=\"$chunkymap_anchor_name\"></a>";
}
function echo_chunkymap_controls() {
    global $chunkymap_view_x;
    global $chunkymap_view_z;
    global $chunkymap_view_zoom_multiplier;
    global $chunkymap_view_max_zoom;
    global $chunkymap_view_min_zoom;
    global $chunkymap_anchor_name;
    $is_in=false;
    $is_out=false;
    $in_img_name = "zoom-in.png";
    $out_img_name = "zoom-out.png";

    $in_zoom = $chunkymap_view_zoom_multiplier;
    if ($in_zoom<$chunkymap_view_max_zoom) {
        $is_in=true;
        $in_zoom = $chunkymap_view_zoom_multiplier*2.0;
        //echo "in:$in_zoom ";
    }
    else $in_img_name = "zoom-in_disabled.png";

    $out_zoom = $chunkymap_view_zoom_multiplier;
    if ($out_zoom>$chunkymap_view_min_zoom) {
        $is_out=true;
        $out_zoom = ($chunkymap_view_zoom_multiplier/2.0);
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

    $in_html="<img src=\"chunkymapdata/images/$in_img_name\" style=\"width:16pt; height:16pt\" />";
    $out_html="<img src=\"chunkymapdata/images/$out_img_name\" style=\"width:16pt; height:16pt\" />";
	global $world_name;
	$append_vars="&";
	if (isset($world_name)) {
		$prefix = "";
		if (strlen($append_vars)>0 && !endsWith($append_vars,"&") ) {
			$prefix = "&";
		}
		$append_vars.="$prefix"."world_name=$world_name";
	}
    if ($is_in) $in_html="<a href=\"?chunkymap_view_zoom_multiplier=$in_zoom"."$append_vars"."#$chunkymap_anchor_name\">$in_html</a>";
    if ($is_out) $out_html="<a href=\"?chunkymap_view_zoom_multiplier=$out_zoom"."$append_vars"."#$chunkymap_anchor_name\">$out_html</a>";
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

function get_chunky_coord_from_location($location_x) {
	$chunk_x = intval($location_x/16);
	return $chunk_x;
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

function get_decachunk_image_name_from_decachunk($x, $z) {
	return "decachunk_x"."$x"."z"."$z".".jpg";
}

function echo_chunkymap_canvas() {
    global $chunkymap_view_x;
    global $chunkymap_view_z;
    global $chunkymap_view_zoom_multiplier;
    global $chunkymap_view_max_zoom;
    global $chunkymap_view_min_zoom;
	global $showplayers;

	check_world();
	global $chunkymapdata_thisworld_path;
	global $world_name;
	global $chunkymapdata_worlds_path;

    $x_opener="decachunk_x";
    $z_opener="z";
    $dot_and_ext = ".jpg";
	
    if ($chunkymap_view_zoom_multiplier<$chunkymap_view_min_zoom) $chunkymap_view_zoom_multiplier = $chunkymap_view_min_zoom;
    if ($chunkymap_view_zoom_multiplier>$chunkymap_view_max_zoom) $chunkymap_view_zoom_multiplier = $chunkymap_view_max_zoom;
	
	$decachunks_per_page = intval(1.0/$chunkymap_view_zoom_multiplier);
	if ($decachunks_per_page<1) {
		$decachunks_per_page = 1;
	}
	$view_w = (($decachunks_per_page*160.0));
	$view_h = (($decachunks_per_page*160.0));
	$view_left = (($chunkymap_view_x)) - (($view_w/2.0));
	$view_right = $view_left + $view_w;
	//z is cartesian still:
	$view_top = (($chunkymap_view_z)) + (($view_h/2.0));
	$view_bottom = $view_top - $view_h;

	echo_chunkymap_anchor();
	echo_chunkymap_controls();
	echo "\r\n";
	echo " ".($chunkymap_view_zoom_multiplier*100.0)."%\r\n";//(string)((int)($chunkymap_view_zoom_multiplier*100+.5));
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
	echo "    <td style=\"width:95%\"><a href=\"?world_name=$world_name&chunkymap_view_zoom_multiplier=$chunkymap_view_zoom_multiplier&chunkymap_view_x=$chunkymap_view_x&chunkymap_view_z=".($chunkymap_view_z+($view_h/2.0))."#chunkymap_top\">".'<img src="chunkymapdata/images/arrow-wide-up.png" style="width:90%"/>'.'</a></td>'."\r\n";
	echo '    <td style="width:5%">'."$td_placeholder_content".'</td>'."\r\n";
	echo '  </tr>'."\r\n";
	$cell_perc=intval(round(100.0/$decachunky_count_x));
	echo '  <tr>'."\r\n";
	echo "    <td style=\"width:5%\"><a href=\"?world_name=$world_name&chunkymap_view_zoom_multiplier=$chunkymap_view_zoom_multiplier&chunkymap_view_x=".($chunkymap_view_x-($view_w/2.0))."&chunkymap_view_z=$chunkymap_view_z#chunkymap_top\">".'<img src="chunkymapdata/images/arrow-wide-left.png" style="width:90%"/>'.'</a></td>'."\r\n";
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
	echo "    <td style=\"width:5%\"><a href=\"?world_name=$world_name&chunkymap_view_zoom_multiplier=$chunkymap_view_zoom_multiplier&chunkymap_view_x=".($chunkymap_view_x+($view_w/2.0))."&chunkymap_view_z=$chunkymap_view_z#chunkymap_top\">".'<img src="chunkymapdata/images/arrow-wide-right.png" style="width:100%"/>'.'</a></td>'."\r\n";
	echo '  </tr>'."\r\n";
	echo '  <tr>'."\r\n";
	echo '    <td style="width:5%">'."$td_placeholder_content".'</td>'."\r\n";
	echo "    <td style=\"width:90%\"><a href=\"?world_name=$world_name&chunkymap_view_zoom_multiplier=$chunkymap_view_zoom_multiplier&chunkymap_view_x=$chunkymap_view_x&chunkymap_view_z=".($chunkymap_view_z-($view_h/2.0))."#chunkymap_top\">".'<img src="chunkymapdata/images/arrow-wide-down.png" style="width:100%"/>'.'</a></td>'."\r\n";
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
    global $chunkymap_view_zoom_multiplier;
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

	echo_chunkymap_anchor();
	echo_chunkymap_controls();
	echo " ".($chunkymap_view_zoom_multiplier*100.0)."%";//(string)((int)($chunkymap_view_zoom_multiplier*100+.5));

    if ($chunkymap_view_zoom_multiplier<$chunkymap_view_min_zoom) $chunkymap_view_zoom_multiplier = $chunkymap_view_min_zoom;
    if ($chunkymap_view_zoom_multiplier>$chunkymap_view_max_zoom) $chunkymap_view_zoom_multiplier = $chunkymap_view_max_zoom;
    //$zoom_divisor = (int)(100/$chunkymap_view_zoom_multiplier);
    $chunk_assoc = array();  // used for storing players; and used for determining which chunks are on the edge, since not all generated map tiles are the same size (edge tile images are smaller and corner ones are smaller yet)
    $chunk_count = 0;
    $x_opener="chunk_x";
    $z_opener="z";
    $dot_and_ext = ".png";
    $min_chunkx = 0;
    $min_chunkz = 0;
    $max_chunkx = 0;
    $max_chunkz = 0;
	$chunks_per_page = (1.0/$chunkymap_view_zoom_multiplier)*10;

	$view_w = (($chunks_per_page*16.0));
	$view_h = (($chunks_per_page*16.0));
	$view_left = (($chunkymap_view_x)) - (($view_w/2.0));
	$view_right = $view_left + $view_w;
	//z is cartesian still:
	$view_top = (($chunkymap_view_z)) + (($view_h/2.0));
	$view_bottom = $view_top - $view_h;
	
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
									if (endsWith($file_lower, $dot_and_ext) and startsWith($file_lower, $x_opener)) {
										$z_opener_index = strpos($file_lower, $z_opener, strlen($x_opener));
										if ($z_opener_index !== false) {
											$x_len = $z_opener_index - strlen($x_opener);
											$remaining_len = strlen($file_lower) - strlen($x_opener) - $x_len - strlen($z_opener) - strlen($dot_and_ext);
											$x = substr($file_lower, strlen($x_opener), $x_len);
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
		$scale=(float)$chunkymap_view_zoom_multiplier; // no longer /100
		$zoomed_w=(int)((float)$chunkymap_tile_original_w*$scale+.5);
		$zoomed_h=(int)((float)$chunkymap_tile_original_h*$scale+.5);
		$genresult_suffix_then_dot_then_ext="_mapper_result.txt";
		$dot_yaml=".yml";
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

				$chunk_yaml_name = $x_opener.$x.$z_opener.$z.$dot_yaml;
				//$chunk_yaml_path = $chunkymapdata_thisworld_path.'/'.$chunk_yaml_name;
				//$chunk_yaml_path = $chunks_16px_path.'/'.
				$chunk_yaml_path = get_chunk_folder_path_from_chunky_coords($x, $z).'/'.$chunk_yaml_name;
				//$chunk_genresult_name = $x_opener.$x.$z_opener.$z.$genresult_suffix_then_dot_then_ext;
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
				$chunk_img_name = $x_opener.$x.$z_opener.$z."$dot_and_ext";
				$chunk_img_path = get_chunk_folder_path_from_chunky_coords($x, $z).'/'.$chunk_img_name;
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
			if (isset($chunkymap_view_zoom_multiplier)) {
				$prefix = "";
				if (strlen($append_vars)>0 and !endsWith($append_vars,"&")) {
					$prefix = "&";
				}
				$append_vars.="$prefix"."&chunkymap_view_zoom_multiplier=$chunkymap_view_zoom_multiplier";
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
