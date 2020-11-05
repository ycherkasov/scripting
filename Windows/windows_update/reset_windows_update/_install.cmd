:: ===========================================================================
:: NAME:	  WURESET.cmd
:: AUTHOR:	Manuel Gil.
::
:: VERSION:   1.0.8.3
:: DATE:	  03/19/2018.
:: ===========================================================================

:: ****************************************************************************
:init

	:: Configure the console.
	:: ----------------------------------------
	echo off
	title Reset Windows Update Tool.
	cls
	:: ----------------------------------------

	:: Load the system values.
	:: ----------------------------------------
	if not defined ProgramFiles(x86) (
		set architecture=32-bit
	) else (
		set architecture=64-bit
	)
	:: ----------------------------------------

	:: Run installer.
	:: ----------------------------------------
	if "%architecture%" EQU "32-bit" (
		copy "%~dp0wureset_x86.exe" "%~dp0wureset.exe"
	) else (
		copy "%~dp0wureset_x64.exe" "%~dp0wureset.exe"
	)

	call "%~dp0wureset\bin\reset-settings.bat"

	echo.Press any key for continue...
	pause>nul
	:: ----------------------------------------
	
goto :eof
:: ****************************************************************************
