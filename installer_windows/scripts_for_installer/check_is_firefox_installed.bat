@echo off

:: check if firefox is installed
reg query "hklm\software\Mozilla" >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
	echo Error: not able to find mozilla firefox in registry. 
	echo mozilla firefox is not installed.
) else (
	echo ok
)
