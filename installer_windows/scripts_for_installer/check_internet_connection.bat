@echo off

ping www.google.de -n 1 -w 1000
if %ERRORLEVEL% NEQ 0 (
	echo Error: no internet connection
) else (
	echo TRUE
)
