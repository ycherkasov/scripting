:: ===========================================================================
:: NAME:	reset-settings.bat
:: AUTHOR:	Manuel Gil.
:: DATE:	01/05/2019.
:: VERSION:	0.0.0.6
:: ===========================================================================

echo off
cls

for /f "tokens=4 delims=[] " %%a in ('ver') do set version=%%a

if %version% EQU 6.0.6000 (
	set name=Microsoft Windows Vista
	set family=6
	set compatible=false
) else if %version% EQU 6.0.6001 (
	set name=Microsoft Windows Vista SP1
	set family=6
	set compatible=false
) else if %version% EQU 6.0.6002 (
	set name=Microsoft Windows Vista SP2
	set family=6
	set compatible=false
) else if %version% EQU 6.1.7600 (
	set name=Microsoft Windows 7
	set family=7
	set compatible=true
) else if %version% EQU 6.1.7601 (
	set name=Microsoft Windows 7 SP1
	set family=7
	set compatible=true
) else if %version% EQU 6.2.9200 (
	set name=Microsoft Windows 8
	set family=8
	set compatible=true
) else if %version% EQU 6.3.9200 (
	set name=Microsoft Windows 8.1
	set family=8
	set compatible=true
) else if %version% EQU 6.3.9600 (
	set name=Microsoft Windows 8.1 Update 1
	set family=8
	set compatible=true
) else (
	set family=0
	set compatible=false
)

ver | find "10.0." > nul
if %errorlevel% EQU 0 (
	set name=Microsoft Windows 10
	set family=10
	set compatible=true
)

for /f "tokens=2 delims==" %%a in ('wmic os get BuildNumber /value') do set /a build=%%a

if not defined ProgramFiles(x86) (
	set architecture=32
) else (
	set architecture=64
)

mkdir "%LOCALAPPDATA%\wureset\"

cd \
cd /d "%LOCALAPPDATA%\wureset\"

echo.# .\wureset\ Reset Windows Update Tool>"settings.ini"
echo.# settings.ini>>"settings.ini"
echo.>>"settings.ini"
echo.[system]>>"settings.ini"
echo.name=%name% >>"settings.ini"
echo.version=^%version%>>"settings.ini"
echo.build=^%build%>>"settings.ini"
echo.architecture=^%architecture%>>"settings.ini"
echo.family=^%family%>>"settings.ini"
echo.>>"settings.ini"
echo.# Font color:>>"settings.ini"
echo.#    2 = Green       9 = Light Blue>>"settings.ini"
echo.#    3 = Aqua       10 = Light Green>>"settings.ini"
echo.#    4 = Red        11 = Light Aqua>>"settings.ini"
echo.#    5 = Purple     12 = Light Red>>"settings.ini"
echo.#    6 = Yellow     13 = Light Purple>>"settings.ini"
echo.#    7 = White      14 = Light Yellow>>"settings.ini"
echo.#    8 = Gray       15 = Bright White>>"settings.ini"
echo.[program]>>"settings.ini"
echo.language=>>"settings.ini"
echo.font=^7>>"settings.ini"
echo.>>"settings.ini"
echo.[pass]>>"settings.ini"
echo.compatible=%compatible%>>"settings.ini"
echo.terms=false>>"settings.ini"

goto :eof
