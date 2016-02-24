<?php


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
$chunkymap_tile_original_w=16;
$chunkymap_tile_original_h=16;

$chunk_dimension_min=$chunkymap_tile_original_w;
if ($chunkymap_tile_original_h<$chunk_dimension_min) $chunk_dimension_min=$chunkymap_tile_original_h;

$chunkymap_view_zoom_min=1.0/$chunk_dimension_min; //should be a number that would get to exactly 100 eventually if multiplied by 2 repeatedly (such as 0.09765625); 0.005 was avoided since tiles used to be 80x80 pixels
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
	ini_set('display_errors', 1);
	ini_set('display_startup_errors', 1);
	error_reporting(E_ALL);
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
	global $showplayers;
	$players = array();
	$player_count = 0;
	$character_icon_w=8;
	$character_icon_h=8;
	if ($showplayers==true) {
		$chunkymap_players_path = $chunkymapdata_path."/players";
		if ($handle = opendir($chunkymap_players_path)) {
			while (false !== ($file = readdir($handle))) {
				if (substr($file, 0, 1) != ".") {
					$file_lower = strtolower($file);
					if (endsWith($file_lower, ".yml")) {
						$player_id=substr($file,0,strlen($file)-4); //-4 for .yml
						$file_path = $chunkymap_players_path."/".$file;
						$player_dict = get_dict_from_conf($file_path,":");
						$player_dict["id"]=$player_id;
						//$players[$player_count]=get_dict_from_conf($file_path);
						//$players[$player_count]["id"]=$player_id;
						//if (isset($player_dict["position"])) {
						if (isset($player_dict["x"]) and isset($player_dict["z"])) {
							//$tuple_string=trim($player_dict["position"]);
							//if ( startsWith($tuple_string, "(") and endsWith($tuple_string, ")") ) {
							//	$tuple_string=substr($tuple_string,1,strlen($tuple_string)-2);
							//}
							//$coordinates = explode(",", $tuple_string);
							//if (count($coordinates)==3) {
							//$smallx=(int)$coordinates[0];
							//$smallz=(int)$coordinates[2];
							$smallx=(int)$player_dict["x"];
							$smallz=(int)$player_dict["z"];
							$x = (int)( $smallx/$chunkymap_tile_original_w );
							$z = (int)( $smallz/$chunkymap_tile_original_h );
							$chunk_luid = "x".$x."z".$z;
							$rel_x = $smallx - ($x*$chunkymap_tile_original_w);
							$rel_z = $smallz - ($z*$chunkymap_tile_original_h);
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
								$chunk_assoc[$chunk_luid][ "players" ][ $chunk_assoc[$chunk_luid]["players_count"] ][ "name" ] = $player_dict["name"];
							}
							else {
								$chunk_assoc[$chunk_luid][ "players" ][ $chunk_assoc[$chunk_luid]["players_count"] ][ "name" ] = $player_dict["id"];
							}
							$chunk_assoc[$chunk_luid]["players_count"] += 1;
							//}
							//else {
							//	echo_error("Bad coordinates $tuple_string for player.");
							//}
						}

						//$player_count++;
					}
				}
			}
		}
	}
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
								if (!isset($chunk_assoc[$chunk_luid])) {
									$chunk_assoc[$chunk_luid] = array();
								}
								$chunk_assoc[$chunk_luid]["is_rendered"] = true;
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
	echo_hold( "  <table style=\"border-spacing: 0px; border-style:solid; border-color:gray; border-width:0px\">\r\n");
	$z = (int)$chunkz_max;
	$scale=(float)$chunkymap_view_zoom_multiplier; // no longer /100
	$zoomed_w=(int)((float)$chunkymap_tile_original_w*$scale+.5);
	$zoomed_h=(int)((float)$chunkymap_tile_original_h*$scale+.5);
	$genresult_suffix_then_dot_then_ext="_mapper_result.txt";
	$dot_yaml=".yml";
	$player_file_age_expired_max_seconds=10*60-1;
	$player_file_age_idle_max_seconds=2*60-1;
	while ($z >= $chunkz_min) {
		echo_hold( "    <tr>\r\n");
		$x = (int)$chunkx_min;
		while ($x <= $chunkx_max) {
			$this_zoomed_w = $zoomed_w;
			$this_zoomed_h = $zoomed_h;

			$chunk_yaml_name = $x_opener.$x.$z_opener.$z.$dot_yaml;
			$chunk_yaml_path = $chunkymapdata_path.'/'.$chunk_yaml_name;
			//$chunk_genresult_name = $x_opener.$x.$z_opener.$z.$genresult_suffix_then_dot_then_ext;
			//$chunk_genresult_path = $chunkymapdata_path.'/'.$chunk_img_name;
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
						//	$td_style_suffix.="text-align:left;";
						//}
						else {
							$td_style_suffix.="text-align:left;";
							//$alignment_comment.="<!-- image_left:".$chunk_dict["image_left"]." was the expected $expected_left-->";
						}
					}
				}

				//if (isset($chunk_dict["image_right"])) {
				//	if ( (int)$chunk_dict["image_right"] != $expected_right ) {
				//		$td_style_suffix.="text-align:left;";
				//	}
				//	//else {
				//	//	$td_style_suffix.="text-align:left;";
				//	//}
				//}
				
				if (isset($chunk_dict["image_top"])) {
					if (isset($chunk_dict["image_bottom"])) {
						if ( (int)$chunk_dict["image_top"] > $expected_top) {
							$element_align_style_suffix.="vertical-align:bottom;";
							//$alignment_comment.="<!-- image_top:".$chunk_dict["image_top"]." is greater than expected $expected_top-->";
						}
						//elseif ( (int)$chunk_dict["image_bottom"] < $expected_bottom) {
						//	$element_align_style_suffix.="vertical-align:top;";
						//}
						else {
							$element_align_style_suffix.="vertical-align:top;";
							//$alignment_comment.="<!-- image_top:".$chunk_dict["image_top"]." was the expected $expected_top-->";
						}
					}
				}
				//if (isset($chunk_dict["image_bottom"])) {
				//	if ( (int)$chunk_dict["image_bottom"] != $expected_bottom) {
				//		$element_align_style_suffix.="vertical-align:top;";
				//	}
				//	//else {
				//	//	$element_align_style_suffix.="vertical-align:bottom;";
				//	//}
				//}
				
				//$element_align_style_suffix.="vertical-align:left;";
			}

			echo_hold( "      <td width=\"1\" style=\"padding:0px; background-color:lightgray; $td_style_suffix $element_align_style_suffix\">");
			echo_hold("<div style=\"position: relative\">"); //causes absolute child position to be relative to this div's location, as per http://www.w3schools.com/css/tryit.asp?filename=trycss_position_absolute
			$chunk_luid = "x".$x."z".$z;
			$chunk_img_name = $x_opener.$x.$z_opener.$z."$dot_and_ext";
			$chunk_img_path = $chunkymapdata_path.'/'.$chunk_img_name;

			
			
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
					$player_name = $chunk_assoc[$chunk_luid]["players"][$player_count]["name"];
					if (strlen($chunk_assoc[$chunk_luid]["players"][$player_count]["name"])>$nonprivate_name_beginning_char_count) {
						$player_name = substr($player_name, 0, $nonprivate_name_beginning_char_count)."*";
					}
					//show head full size (not zoomed):
					$zoomed_head_w=$character_icon_w;//(int)((float)$character_icon_w*$scale+.5);
					$zoomed_head_h=$character_icon_h;//(int)((float)$character_icon_h*$scale+.5);
					$rel_x -= (int)($zoomed_head_w/2);
					$rel_z -= (int)($zoomed_head_h/2);
					//$img_style="position:absolute; ";
					$img_style=""
					if (!$is_expired) {
						if ($is_idle) {
							$img_style.="opacity: 0.4; filter: alpha(opacity=40);";  //filter is for IE8 and below
						}
						echo_hold( "<div style=\"position:absolute; z-index:999; left:$rel_x; top:$rel_z; width: $zoomed_head_w; height: $zoomed_head_h; border: 1px solid white\"><img src=\"images/chunkymap_character-face.png\" style=\"$img_style\"/>$player_name</div>" );
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
?>