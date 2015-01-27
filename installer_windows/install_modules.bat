@echo off

:: check if python, easy_install and firefox are installed:
:: batch script 'programs_installed.bat' should return "ok",
:: if everything is installed
for /f %%a in ('programs_installed.bat') do (set "programs_installed=%%a")
if "%programs_installed%" == "ok"(
	:: check internet connection
	ping www.google.de -n 1 -w 1000
	if %ERRORLEVEL% NEQ 0 (
		echo Error: no internet connection
		goto error
	) else (
		::
		:: install python modules
		goto todo
		:: TODO	
		:: easy_install Biopython
		:: ...
		:: --> store all module names in txt file modules.txt
		:: --> iterate over each line and install each module
	)
) else (
	echo an error in script programs_installed.bat has occured.
	goto error
)

:ERROR
pause

:TODO
echo todo
pause

REM C:\Users\n2n\Desktop>easy_install Biopython
REM Searching for Biopython
REM Best match: biopython 1.64
REM Processing biopython-1.64-py2.7-win32.egg
REM biopython 1.64 is already the active version in easy-install.pth

REM Using d:\01. programme\anaconda-python\anaconda\lib\site-packages\biopython-1.64
REM -py2.7-win32.egg
REM Processing dependencies for Biopython
REM Finished processing dependencies for Biopython
