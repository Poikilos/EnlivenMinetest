<?php
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

// OPTIONAL:
$chunkymapdata_path = "chunkymapdata";
$showplayers=true;

// NOT OPTIONAL:
$chunkymap_tile_original_w=80;
$chunkymap_tile_original_h=80;

$chunk_dimension_min=$chunkymap_tile_original_w;
if ($chunkymap_tile_original_h<$chunk_dimension_min) $chunk_dimension_min=$chunkymap_tile_original_h;

$chunkymap_view_zoom_min=1.0/$chunk_dimension_min; //should be a number that would get to exactly 100 eventually if multiplied by 2 repeatedly (such as 0.09765625); 0.005 doesn't work since tiles are 80x80 pixels
$chunkymap_view_zoom_max=13107200.0;

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

$map_dict = get_dict_from_conf($chunkymapdata_path."/generated.yml",":");

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
function echo_chunkymap_controls($callback_php_path) {
	global $chunkymap_view_x;
	global $chunkymap_view_z;
	global $chunkymap_view_zoom_multiplier;
	global $chunkymap_view_zoom_max;
	global $chunkymap_view_zoom_min;
	global $chunkymap_anchor_name;
	$is_in=false;
	$is_out=false;
	$in_img_name = "chunkymap_zoom-in.png";
	$out_img_name = "chunkymap_zoom-out.png";
	
	$in_zoom = $chunkymap_view_zoom_multiplier;
	if ($in_zoom<$chunkymap_view_zoom_max) {
		$is_in=true;
		$in_zoom = $chunkymap_view_zoom_multiplier*2.0;
		//echo "in:$in_zoom ";
	}
	else $in_img_name = "chunkymap_zoom-in_disabled.png";

	$out_zoom = $chunkymap_view_zoom_multiplier;
	if ($out_zoom>$chunkymap_view_zoom_min) {
		$is_out=true;
		$out_zoom = ($chunkymap_view_zoom_multiplier/2.0);
	}
	else $out_img_name = "chunkymap_zoom-out_disabled.png";
	
	$zoom_clip = $chunkymap_view_zoom_max;
	$found=false;
	while ($zoom_clip>=$chunkymap_view_zoom_min) {
		if ($out_zoom>$zoom_clip) {
			$out_zoom=$zoom_clip*2;
			$found=true;
			break;
		}
		$zoom_clip = $zoom_clip/2;
	}
	if (!$found) {
		$out_zoom=$chunkymap_view_zoom_min;
	}
	//if ($in_zoom>$chunkymap_view_zoom_max) {
	//	$in_zoom=$chunkymap_view_zoom_max;
	//	echo "<!--clipping to max $chunkymap_view_zoom_max-->";
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
	//else $in_zoom=$chunkymap_view_zoom_min;  // if ($in_zoom>1) $in_zoom=5;
	//echo "in:$in_zoom ";
	// if ($out_zoom<$chunkymap_view_zoom_min) $out_zoom=$chunkymap_view_zoom_min;
	// elseif ($out_zoom<2) $out_zoom=1;
	// elseif ($out_zoom<4) $out_zoom=2;
	// elseif ($out_zoom<12) $out_zoom=4;
	// elseif ($out_zoom<25) $out_zoom=12;
	// elseif ($out_zoom<50) $out_zoom=25;
	// elseif ($out_zoom<75) $out_zoom=50;
	// elseif ($out_zoom<100) $out_zoom=75;
	//elseif ($out_zoom<200) $out_zoom=100;
	//elseif ($out_zoom<$chunkymap_view_zoom_max) $out_zoom=(int)($chunkymap_view_zoom_max/2);
	//else $out_zoom=$chunkymap_view_zoom_max; //if ($out_zoom>76) $out_zoom=100;
	$zoom_clip=$chunkymap_view_zoom_min;
	$found=false;
	while ($zoom_clip<=$chunkymap_view_zoom_max) {
		if ($in_zoom<($zoom_clip*2)) {
			$in_zoom=$zoom_clip;
			$found=true;
			break;
		}
		$zoom_clip = $zoom_clip * 2;
	}
	if (!$found) $in_zoom=$chunkymap_view_zoom_max;
	
	$in_html="<img src=\"images/$in_img_name\" style=\"width:16pt; height:16pt\" />";
	$out_html="<img src=\"images/$out_img_name\" style=\"width:16pt; height:16pt\" />";
	if ($is_in) $in_html="<a href=\"?chunkymap_view_zoom_multiplier=$in_zoom#$chunkymap_anchor_name\">$in_html</a>";
	if ($is_out) $out_html="<a href=\"?chunkymap_view_zoom_multiplier=$out_zoom#$chunkymap_anchor_name\">$out_html</a>";
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
function echo_worldname() {
	global $map_dict;
	if (isset($map_dict["world_name"])) {
		echo $map_dict["world_name"];
	}
	else echo "<span style=\"color:red\">(missing world name)</span>";
}
function echo_chunkymap_table() {
	global $is_echo_never_held;
	$is_echo_never_held=true;
	global $chunkymap_view_x;
	global $chunkymap_view_z;
	global $chunkymap_view_zoom_multiplier;
	global $chunkymap_view_zoom_max;
	global $chunkymap_view_zoom_min;
	global $chunkymapdata_path;
	global $map_dict;
	global $is_verbose;
	global $chunkymap_tile_original_w;
	global $chunkymap_tile_original_h;
	global $chunkymap_view_zoom_max;
	if ($chunkymap_view_zoom_multiplier<$chunkymap_view_zoom_min) $chunkymap_view_zoom_multiplier = $chunkymap_view_zoom_min;
	if ($chunkymap_view_zoom_multiplier>$chunkymap_view_zoom_max) $chunkymap_view_zoom_multiplier = $chunkymap_view_zoom_max;
	//$zoom_divisor = (int)(100/$chunkymap_view_zoom_multiplier);
	$chunk_assoc = array();  // used for determining which chunks are on the edge, since not all generated map tiles are the same size (edge tile images are smaller and corner ones are smaller yet)
	$chunk_count = 0;
	$x_opener="chunk_x";
	$z_opener="z";
	$dot_and_ext = ".png";
	$chunkx_min = 0;
	$chunkz_min = 0;
	$chunkx_max = 0;
	$chunkz_max = 0;
	//if ($map_dict != null) {
	//	$chunkx_min = $map_dict["chunkx_min"];
	//	$chunkz_min = $map_dict["chunkz_min"];
	//	$chunkx_max = $map_dict["chunkx_max"];
	//	$chunkz_max = $map_dict["chunkz_max"];
	//}
	//else {
		//echo "calculating range...";
		//NOTE: even though *min and *max could be known from $map_dict, build a dict of chunks in order to align images properly since they are not all the same size:
		if ($handle = opendir($chunkymapdata_path)) {
			while (false !== ($file = readdir($handle))) {
				if (substr($file, 0, 1) != ".") {
					$file_lower = strtolower($file);
					if (endsWith($file_lower, $dot_and_ext) and startsWith($file_lower, $x_opener)) {
						$z_opener_index = strpos($file_lower, $z_opener, strlen($x_opener));
						if ($z_opener_index !== false) {
							$x_len = $z_opener_index - strlen($x_opener);
							$z_len = strlen($file_lower) - strlen($x_opener) - $x_len - strlen($z_opener) - strlen($dot_and_ext);
							$x = substr($file_lower, strlen($x_opener), $x_len);
							$z = substr($file_lower, $z_opener_index + strlen($z_opener), $z_len);
							if (is_int_string($x) and is_int_string($z)) {
								$chunk_luid = "x".$x."z".$z;
								$chunk_assoc[$chunk_luid] = true;
								if ($is_verbose) echo "$chunk_luid,";
								if ($x<$chunkx_min) {
									$chunkx_min=(int)$x;
								}
								if ($x>$chunkx_max) {
									$chunkx_max=(int)$x;
								}
								if ($z<$chunkz_min) {
									$chunkz_min=(int)$z;
								}
								if ($z>$chunkz_max) {
									$chunkz_max=(int)$z;
								}
							}
							else {
								echo "misnamed chunk tile image '$file' had coordinates ".$x.",".$z." for x,z.";
							}
						}
					}
				}
			}
			if ($is_verbose) echo "checked all chunks.";
			echo "<!--found chunks in x $chunkx_min to $chunkx_max and z $chunkz_min to $chunkz_max.-->";
		}
		else {
			echo_error("could not open $chunkymapdata_path");
		}
	//}
	
	$x_count = $chunkx_max - $chunkx_min;
	$z_count = $chunkz_max - $chunkz_min;
	echo "\r\n";
	echo "<center>\r\n";
	echo_hold( "  <table style=\"border-spacing: 0px; border-style:solid; border-color:gray;border-width:0px\">\r\n");
	$z = (int)$chunkz_max;
	$scale=(float)$chunkymap_view_zoom_multiplier; // no longer /100
	$zoomed_w=(int)((float)$chunkymap_tile_original_w*$scale+.5);
	$zoomed_h=(int)((float)$chunkymap_tile_original_h*$scale+.5);
	while ($z >= $chunkz_min) {
		echo_hold( "    <tr>\r\n");
		$x = (int)$chunkx_min;
		while ($x <= $chunkx_max) {
			echo_hold( "      <td width=\"1\" style=\"padding:0px; background-color:lightgray\">");
			$chunk_luid = "x".$x."z".$z;
			$chunk_img_name = $x_opener.$x.$z_opener.$z."$dot_and_ext";
			$chunk_img_path = $chunkymapdata_path.'/'.$chunk_img_name;
			
			if (is_file($chunk_img_path)) {
				echo_hold( "<img style=\"width:$zoomed_w; height:$zoomed_h\" class=\"maptileimg\" src=\"$chunk_img_path\"");
			}
			else {
				//echo_hold( "<span style=\"font-size:1px\">&nbsp;</span>");
			}
			//echo "        <br/>".$x.",0,".$z;
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
?>