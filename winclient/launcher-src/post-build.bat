@echo off
REM http://doc.qt.io/qt-5/windows-deployment.html#the-windows-deployment-tool
REM normally the shell is run via the icon in the Qt folder that links to; C:\Windows\System32\cmd.exe /A /Q /K C:\Qt\5.7\mingw53_32\bin\qtenv2.bat
REM and whose working directory is C:\Windows\System32


REM C:\Qt\5.7\mingw53_32\bin\qtenv2.bat
set PATH=C:\Qt\5.7\mingw53_32\bin;C:/Qt/Tools/mingw530_32\bin;%PATH%
cd /D C:\Qt\5.7\mingw53_32


SET RELEASE_PATH=%USERPROFILE%\Documents\GitHub\build-ENLIVEN-Desktop_Qt_5_7_0_MinGW_32bit-Release\release
IF EXIST "%RELEASE_PATH%" (
cd "%RELEASE_PATH%"
windeployqt.exe .
echo Current directory: %CD%
echo "Found USERPROFILE: %USERPROFILE%"
REM TOO LONG:
REM SET FINALDEPLOY=%USERPROFILE%\Documents\GitHub\EnlivenMinetest\install-windows-client\destination
REM echo "COPYING TO %FINALDEPLOY%..."
REM IF NOT EXIST "%FINALDEPLOY%\iconengines" MD "%FINALDEPLOY%\iconengines"
REM IF NOT EXIST "%FINALDEPLOY%\imageformats" MD "%FINALDEPLOY%\imageformats"
REM IF NOT EXIST "%FINALDEPLOY%\platforms" MD "%FINALDEPLOY%\platforms"
REM IF NOT EXIST "%FINALDEPLOY%\translations" MD "%FINALDEPLOY%\translations"
REM copy *.dll "%FINALDEPLOY%\"
REM copy ".\iconengines\*.dll" "%FINALDEPLOY%\iconengines\"
REM copy ".\imageformats\*.dll" "%FINALDEPLOY%\imageformats\"
REM copy ".\platforms\*.dll" "%FINALDEPLOY%\platforms\"
REM copy ".\translations\*.qm" "%FINALDEPLOY%\translations\"
pause
) ELSE (
@echo off
echo "FAILED: couldn't find %RELEASE_PATH%"
pause
) 
REM C:\Qt\5.7\mingw53_32\bin\windeployqt.exe 
REM C:\Users\Owner\Documents\GitHub\build-ENLIVEN-Desktop_Qt_5_7_0_MinGW_32bit-Release\release
REM C:\Users\Owner\Documents\GitHub\EnlivenMinetest\install-windows-client\destination