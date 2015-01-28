@echo off

:: check if python is in the system path
where python >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
	echo Error: python was not found in system path.
) else (
	echo TRUE
)
