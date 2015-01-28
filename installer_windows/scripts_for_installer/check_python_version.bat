@ echo off

:: check if python has version 2.7
if exist pyversion.out del pyversion.out
python --version 2>&1 | findstr /I "Python 2.7" > pyversion.out
if %ERRORLEVEL% NEQ 0 (
	if exist pyversion.out del pyversion.out
	echo Error: python must have the version 2.7
	echo Current python version is: 
	python --version
) else (
	if exist pyversion.out del pyversion.out
	echo ok
)
