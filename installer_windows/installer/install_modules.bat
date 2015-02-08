@echo off

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: check if computer has internet connection
echo check internet connection
echo ----------------------------------------------
ping www.google.de -n 1 -w 1000
if %ERRORLEVEL% NEQ 0 (
	echo Error: no internet connection
	goto error
)
echo ----------------------------------------------

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: Install modules from txt file:
:: read file 'INSTALL_requirements.txt' line by line
:: and install/update modules
set "modulesPath=INSTALL_requirements.txt"
if not exist "%modulesPath%" (
	echo file 'INSTALL_requirements.txt' does not exist!
	goto error
)
echo installing python modules
for /f "tokens=*" %%a in (%modulesPath%) do ( 
	if exist moduleInstall.out del moduleInstall.out
	echo ----------------------------------------------
	easy_install %%a >> modulInstall.txt
	if %ERRORLEVEL% NEQ 0 (
		echo Error. Installation of module '%%a' failed!
		echo You can find full error log in the file 'modulInstall.txt'
		goto error
	) else (
		echo Installed module '%%a'
	)
	echo ----------------------------------------------
)

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:: intall other modules - add folders to system variable PATH

:: path to clustal omega folder with executables:
set "path2clustalo=%~1\additional_modules\clustal-omega-1.2.0-win32"
:: path to vienna rna folder with executables:
set "path2viennarna=%~1\additional_modules\ViennaRNA_32bit"
:: path to phylip folder with executables:
set "path2phylip=%~1\additional_modules\phylip-3.695\exe"

:: add directory to sys variable PATH
:: check if they already in PATH
echo adding paths to executables. Software: 
echo - clustal omega (version 1.2.0, 32 bit)
call add_program_to_sys_path.bat "%path2clustalo%" "clustal"
echo - vienna rna (version 2.1.8, 32 bit)
call add_program_to_sys_path.bat "%path2viennarna%" "phylip"
echo - phylip (version 3.695)
call add_program_to_sys_path.bat "%path2phylip%" "ViennaRNA"

goto end

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:ERROR
echo Installation failed!
pause

:END
echo All modules were successfully installed!
goto :eof

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::