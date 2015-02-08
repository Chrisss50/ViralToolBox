@ECHO OFF

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

SETLOCAL
REM SET "newpython=C:\Users\n2n\Documents\GitHub\ViralToolBox\installer_windows\additional_modules\clustal-omega-1.2.0-win32\"
SET "newprogrampath=%~1"
SET "keyword=%~2"
SET "newpath="

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

REM make a backup of the system variable 'PATH'
PATH >> path_backup.txt

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:temploop
SET tempfile=%random%%random%%random%
IF EXIST "%temp%\%tempfile%*" GOTO temploop
SET "tempfile=%temp%\%tempfile%"
CALL :showpath >"%tempfile%"

FOR /f "delims=" %%p IN ('type "%tempfile%"') DO (
 CALL :addsegment "%%p"
)

REM add new program path to the sys variable %path%
powershell -Command "& {[Environment]::SetEnvironmentVariable('path', '%newprogrampath%;%newpath%','Machine');exit;}"
DEL "%tempfile%"
GOTO :EOF

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:addsegment
SET "segment=%~1"
REM check if there is a substring (program) which we search:
ECHO.%segment% | findstr /C:"%keyword%" 1>NUL
IF %ERRORLEVEL% NEQ 0 (
  SET "newpath=%newpath%;%segment%"
  GOTO :eof
) ELSE (
  GOTO :eof
)

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

:showpath
ECHO(%path:;=&ECHO(%
GOTO :eof

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::