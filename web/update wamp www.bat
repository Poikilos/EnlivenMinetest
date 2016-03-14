
SET SRC_MT_WEB_PATH=%USERPROFILE%\Documents\GitHub\minetest-chunkymap\web
SET DEST_MT_WEBSITE_PATH=C:\wamp\www
copy /y "%SRC_MT_WEB_PATH%\browser.php" "%DEST_MT_WEBSITE_PATH%\"
copy /y "%SRC_MT_WEB_PATH%\chunkymap.php" "%DEST_MT_WEBSITE_PATH%\"
copy /y "%SRC_MT_WEB_PATH%\viewchunkymap.php" "%DEST_MT_WEBSITE_PATH%\"

SET DEST_MT_WEBSITE_CHUNKYMAP_IMAGES_PATH=%DEST_MT_WEBSITE_PATH%\chunkymapdata\images
copy /y "%SRC_MT_WEB_PATH%\chunkymapdata_default\images\*" "%DEST_MT_WEBSITE_CHUNKYMAP_IMAGES_PATH%"


if NOT ["%errorlevel%"]==["0"] pause
