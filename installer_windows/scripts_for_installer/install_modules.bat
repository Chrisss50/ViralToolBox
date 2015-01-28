@echo off

REM Install modules from txt file:
REM read file 'INSTALL_requirements.txt' line by line
REM and install/update modules
set "modulesPath=INSTALL_requirements.txt"
if not exist modulesPath (
	echo file 'INSTALL_requirements.txt' does not exist!
	goto :error
)
for /f "tokens=*" %%a in (modulesPath) do ( 
	if exist moduleInstall.out del moduleInstall.out
	echo ----------------------------------------------
	easy_install %%a >> modulInstall.txt
	if %ERRORLEVEL% NEQ 0 (
		echo Error. Installation of module '%%a' failed!
		echo You can find full error log in the file 'modulInstall.txt'
		goto :error
	) else (
		echo Installed module '%%a'
	)
	echo ----------------------------------------------
)

echo Adding paths to executables. Software: 
echo - clustal omega (version 1.2.0, 32 bit)
echo - vienna rna (version 2.1.8, 32 bit)
echo - phylip (version 3.695)

REM other modules:
REM collect all and save all paths to executables in csv table
REM <module_name_1>,<module_path_1>
REM ...
REM <module_name_n>,<module_path_n>

REM path to clustal omega folder with executables:
set "path2clustalo=ViralToolBox\installer_windows\additional_modules\clustal-omega-1.2.0-win32"

REM path to vienna rna folder with executables:
set "path2viennarna=ViralToolBox\installer_windows\additional_modules\ViennaRNA_32bit"

REM path to phylip folder with executables:
set "path2phylip=ViralToolBox\installer_windows\additional_modules\phylip-3.695\exe"











C:\Users\n2n\Documents\GitHub\ViralToolBox\installer_windows\additional_modules\
clustal-omega-1.2.0-win32>

:: RUN CLUSTAL
clustalo.exe --force -i "C:\Users\n2n\Documents\GitHub\ViralToolBox\part_msa\Yersinia_multiple.fasta" -o "C:\Users\n2n\Desktop\clustalo_out.txt" --outfmt phy -v


ViennaRNA: http://www.tbi.univie.ac.at/RNA/index.html#download
ClustalO: http://www.clustal.org/omega/
Phylib: http://evolution.genetics.washington.edu/phylip.html

goto :end

:ERROR
exit

:END
echo All modules were successfully installed!