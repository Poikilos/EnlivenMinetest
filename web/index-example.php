<html>
<title>Chunkymap Example Page</title>
<body style="font-family:calibri,sans">
<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);
//echo "php started...";
if (is_file('chunkymap.php')) {
	//echo "including...";
	include_once('chunkymap.php');
	//echo "about to call echo_chunkymap_table...";

	//The following is not needed, since chunkymap.php should be included above and puts all $_REQUEST array variables into $GLOBALS array
	//if (!isset($_REQUEST['chunkymap_view_x'])) {//if (!isset($chunkymap_view_x)) {
	//	$chunkymap_view_x=0;
	//}
	//else $chunkymap_view_x=$_REQUEST['chunkymap_view_x'];
	echo "<center>";
	echo "<h1>Map of ";
	echo_worldname();
	echo "</h1>";
	echo "</center>";
	set_chunkymap_view($chunkymap_view_x,$chunkymap_view_z,$chunkymap_view_zoom_multiplier);
	echo "<table><tr><td style=\"text-align:left\">";
	echo_chunkymap_anchor();
	echo_chunkymap_controls(__FILE__);
	echo " ".($chunkymap_view_zoom_multiplier*100.0)."%";//(string)((int)($chunkymap_view_zoom_multiplier*100+.5));
	echo_chunkymap_table();
	echo "</td></tr></table>";
	//echo "returned from echo_chunkymap_table.";
}
else {
	echo "missing chunkymap.php";
}
?>
<center><small>Powered by <a href="https://github.com/expertmm/minetest-chunkymap">Chunkymap</a></small></center>
</body>
</html>