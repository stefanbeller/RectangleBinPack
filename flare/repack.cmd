@echo off

REM only enemies are supported in WIndows version of script

IF NOT DEFINED mods (
	echo Please define the variable mods before running this script
	SET abortScript=yes
)

if NOT DEFINED game_dir (
	echo Please define the variable game_dir before running this script
	SET abortScript=yes
)

if "%abortScript%"=="yes" exit /b 1

echo %mods%
echo %game_dir%

FOR %%M IN (%mods%) DO (
	if EXIST %game_dir%\mods\%%M\animations\enemies (
		call :process %%M
	) else (
		echo %%M has no animations folder
	)
)

exit /b 0

:process
FOR /R %game_dir%\mods\%1\animations\enemies %%A IN (*.txt) DO (
	call :pack %1 %%A
	pushd %game_dir%
	git commit -a -m "repack %%~nA.png"
	popd
)
GOTO :eof

:pack
SET mod=%1
SET animationFile=%2
SET basename=%~n2

spritesheetpacker.py --definition %animationFile% --image %game_dir%\mods\%mod%\images\enemies\%basename%.png %spritesheetpacker_args%
GOTO :eof
