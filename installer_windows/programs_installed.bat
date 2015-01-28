@echo off

:: check if python is in the system path
where python >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
	echo Error: python was not found in path.
	goto error
)

:: check if python has version 2.7
if exist pyversion.out del pyversion.out
python --version 2>&1 | findstr /I "Python 2.7" > pyversion.out
if %ERRORLEVEL% NEQ 0 (
	echo Error: python must have the version 2.7
	echo Current python version is: 
	python --version
	goto error
)

:: check if easy_install is in path
where easy_install >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
	echo Error: easy_install was not found in path.
	goto error
)

:: check if firefox is installed
reg query "hklm\software\Mozilla" >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
	echo Error: not able to find mozilla firefox in registry. 
	echo mozilla firefox is not installed.
	goto error
)
:: get path to firefox.exe
:: for /f "usebackq tokens=3* delims= " %a in (`reg query "hklm\software\Mozilla\Mozilla Firefox" /ve`) do (set "firefox_version=%a")
for /f "usebackq tokens=* delims= " %%a in (`reg query "hklm\software\Mozilla"`) do (set "ff_registry_path=%%a")
for /f "usebackq tokens=3* delims= " %%a in (`reg query "%ff_registry_path%\bin" /v PathToExe`) do (set "ff_path=%%a %%b")
:: check if path is correct
if exist ffpath.out del ffpath.out
echo %ff_path% > ffpath.out
findstr /I "firefox.exe" ffpath.out
if %ERRORLEVEL% NEQ 0 (
	echo Error: path to firefox.exe was not found
	goto error
) else (
	goto end
)

:ERROR
	if exist pyversion.out del pyversion.out
	if exist ffpath.out del ffpath.out
	echo execution failed
	
:END
	if exist pyversion.out del pyversion.out
	if exist ffpath.out del ffpath.out
	REM echo No errors occured. python, easy_install and firefox are installed
	echo TRUE