<?php
include_once('browser.php');
foreach($_REQUEST as $key => $value) {
//in case auto_globals is not enabled
$GLOBALS[$key]=$value;
}
date_default_timezone_set('EST'); //required by PHP >=5.1.0

$chunkymapdata_path = "chunkymapdata";
$showplayers=true;

function get_dict_from_conf($path, $assignment_operator) {
	$handle = fopen($path, "r");
	$result = null;
	if ($handle) {
		while (($line = fgets($handle)) !== false) {
			$line_strip = trim($line);
			if (strlen($line_strip)>0) {
				if (substr($line_strip)!="#") {
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

$map_dict = get_dict_from_conf($chunkymapdata_path."/generated.yml";

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

function is_int($val) {
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

function echo_chunkymap_table($center_x, $center_z, $zoom_min_1_max_100) {
	global $chunkymapdata_path;
	global $map_dict;
	if ($zoom_min_1_max_100<1) $zoom_min_1_max_100 = 1;
	if ($zoom_min_1_max_100>100) $zoom_min_1_max_100 = 100;
	$zoom_divisor = int(100/$zoom_min_1_max_100);
	$chunk_assoc = array();
	$chunk_count = 0;
	$x_opener="chunk_x";
	$z_opener="z";
	$dot_and_ext = ".png";
	$chunkx_min = 0;
	$chunkz_min = 0;
	$chunkx_max = 0;
	$chunkz_max = 0;
	if ($map_dict != null) {
		$chunkx_min = $map_dict["chunkx_min"];
		$chunkz_min = $map_dict["chunkz_min"];
		$chunkx_max = $map_dict["chunkx_max"];
		$chunkz_max = $map_dict["chunkz_max"];
	}
	else {
		//NOTE: no need to detect range if using $map_dict
		$chunkz_max = 0;
		$x_min = 0;
		$z_min = 0;
		$z_max = 0;
		if ($handle = opendir($chunkymapdata_path)) {
			while (false !== ($file = readdir($handle))) {
				if (substr($file, 0, 1) != ".") {
					$file_lower = strtolower($file);
					if (endsWith($file_lower, $dot_and_ext) and startsWith($file_lower, $x_opener)) {
						$z_opener_index = strpos($file_lower, $z_opener, strlen($x_opener));
						if ($z_opener_index !== false) {
							$x_len = $z_opener_index - strlen($x_opener);
							$z_len = strlen($file_lower) - strlen($x_opener) - $x_len - strlen($z_opener) - $dot_and_ext;
							$x = substr($file_lower, strlen($x_opener), $x_len);
							$z = substr($file_lower, $z_opener_index + strlen($z_opener), $z_len);
							if (is_int($x) and is_int($z)) {
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
		}
	}
	$x = $chunkx_min;
	$z = $chunkz_min;
	$x_count = $chunkx_max - $chunkx_min;
	$z_count = $chunkz_max - $chunkz_min;
	echo "<table border=\"0\">";
	while ($z <= $chunkz_max) {
		echo "  <tr>";
		while ($x <= $chunkx_max) {
			echo "    <td>";
			$chunk_luid = "x".$x."z".$z;
			$chunk_img_name = $x_opener.$x.$z_opener.$z."$dot_and_ext";
			$chunk_img_path = $chunkymapdata_path.'/'.$chunk_img_name;
			if (is_file($chunk_img_path)) {
				echo "<img src=\"$chunk_img_path\"/ style=\"width:$zoom_min_1_max_100%\">";
			}
			echo "        <br/>".$x.",0,".$z
			echo "    </td>";
			$x++;
		}
		echo "  </tr>";
		$z++;
	}
	echo "</table>";
}
?>