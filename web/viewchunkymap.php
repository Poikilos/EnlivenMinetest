<html style="width:100%; height:100%">
<head>
<title>Chunkymap</title>
<meta http-equiv="refresh" content="30">
</head>
<body style="font-family:calibri,sans; width:100%; height:100%; margin:0; padding:0" topmargin="0" leftmargin="0" rightmargin="0" bottommargin="0">
<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
//echo "php started...";
if (is_file('chunkymap.php')) {
	//echo "including...";
	include_once('chunkymap.php');
	//echo "about to call echo_chunkymap_as_chunk_table...";

	//The following is not needed, since chunkymap.php should be included above and puts all $_REQUEST array variables into $GLOBALS array
	//if (!isset($_REQUEST['chunkymap_view_x'])) {//if (!isset($chunkymap_view_x)) {
	//	$chunkymap_view_x=0;
	//}
	//else $chunkymap_view_x=$_REQUEST['chunkymap_view_x'];
	//echo "<center>";
	//echo "<h1>";
	//echo_map_heading_text();
	//echo "</h1>";
	//echo "</center>";
	set_chunkymap_view($chunkymap_view_x,$chunkymap_view_z,$chunkymap_view_zoom);
	//echo "<table><tr><td style=\"text-align:left\">";
	$chunk_mode_enable=true; //(this should normally be false) if true, uses 16x16 png files instead of the 160x160 decachunks; it is slower but may have more of the map during times when new chunks are explored but before the render queue is done and the decachunk images are created from the chunk images.);
	$debug_mode_enable=false; //if true, this renders colors based on yml files instead of drawing images (and does not echo images at all)
	$html4_mode_enable=false; //if true, does not echo canvas nor client-side scripting
	echo_chunkymap_canvas($chunk_mode_enable,$debug_mode_enable,$html4_mode_enable);
	//echo_chunkymap_as_chunk_table(false);
	//echo_decachunk_table();
	//echo "</td></tr></table>";
	//echo "returned from echo_chunkymap_as_chunk_table.";
}
else {
	echo "missing chunkymap.php";
}
?>
<center><small>Powered by <a href="https://github.com/expertmm/minetest-chunkymap">Chunkymap</a></small></center>
</body>
</html>

