@echo off

:: check if easy_install is in system path
where easy_install >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
	echo Error: easy_install was not found in system path.
) else (
	echo TRUE
)
