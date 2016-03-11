@echo off
SET TRY_PYTHON_EXE=C:\Python27\pythonw.exe
SET MT_CM_INSTALLER_PY=install-chunkymap-on-windows.py
IF EXIST "%TRY_PYTHON_EXE%" THEN "%TRY_PYTHON_EXE%" "%MT_CM_INSTALLER_PY%"
IF NOT EXIST "%TRY_PYTHON_EXE%" THEN echo You are missing %TRY_PYTHON_EXE% so this batch file cannot use it--try running %MT_CM_INSTALLER_PY% in your favorite Python 2.
