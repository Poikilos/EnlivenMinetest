SET SOURCE_DIR=C:\Users\Owner\Documents\GitHub\minetest-chunkymap\web
SET DEST_DIR=C:\wamp\www
COPY /Y "%SOURCE_DIR%\browser.php" "%DEST_DIR%\"
if NOT ["%errorlevel%"]==["0"] pause
COPY /Y "%SOURCE_DIR%\chunkymap.php" "%DEST_DIR%\"
if NOT ["%errorlevel%"]==["0"] pause
COPY /Y "%SOURCE_DIR%\viewchunkymap.php" "%DEST_DIR%\"
if NOT ["%errorlevel%"]==["0"] pause