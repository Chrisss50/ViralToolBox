@echo off

for /f "usebackq tokens=* delims= " %%a in (`reg query "hklm\software\Mozilla"`) do (set "ff_registry_path=%%a")
for /f "usebackq tokens=3* delims= " %%a in (`reg query "%ff_registry_path%\bin" /v PathToExe`) do (set "ff_path=%%a %%b")
if exist ffpath.out del ffpath.out
echo "%ff_path%"> ffpath.out
findstr /I "firefox.exe" ffpath.out
if %ERRORLEVEL% NEQ 0 (
	if exist ffpath.out del ffpath.out
	REM path to firefox.exe was not found in registry
	echo NOT_FOUND
) else (
	echo %ffpath%
	if exist ffpath.out del ffpath.out
)

REM use this piece of code to get the firefox path as result of this script
REM for /f "tokens=1 delims=" %a in ('get_firefox_path_from_registry.bat') do (set "p=%a")
REM !!! tokens=1
