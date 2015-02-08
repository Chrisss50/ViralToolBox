@echo off

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

set "installer_path=%CD%"
cd installer

if exist tmp.out del tmp.out
if exist pyversion.out del pyversion.out
if exist modulInstall.txt del modulInstall.txt

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: SEVERAL CHECKS

:: check if powershell is in system path
echo check powershell
where powershell >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
	echo Error: powershell was not found in system path.
	goto error
)
:: check if python is in the system path
echo check python
where python >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
	echo Error: python was not found in system path.
	goto error
)
:: check if python has version 2.7
echo check python version
python --version 2>&1 | findstr /I "Python 2.7" > pyversion.out
if %ERRORLEVEL% NEQ 0 (
	if exist pyversion.out del pyversion.out
	echo Error: python must have the version 2.7
	echo Current python version is: 
	python --version
	goto error
) else (
	if exist pyversion.out del pyversion.out
)
:: check if easy_install is in system path
echo check easy_install
where easy_install >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
	echo Error: easy_install was not found in system path.
	goto error
)
:: check if firefox is installed
echo check firefox
reg query "hklm\software\Mozilla" >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
	echo Error: not able to find mozilla firefox in registry. 
	echo mozilla firefox is not installed.
	goto error
)

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: install modules
call install_modules.bat "%installer_path%"
goto end

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:ERROR
echo Installation failed!
pause

:END
echo Viral Tool Box was successfully installed!
pause

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::