@echo off

set filename=%1

call:countString
set /a n = %%number
echo %n%
exit /b

call:generate_random 100 
rem echo "Generated random numbers = %rnd%"
exit /b

:countString
setlocal EnableDelayedExpansion
set "cmd=findstr /R /N "^^" %filename% | find /C ":""
for /f %%a in ('!cmd!') do set number=%%a
echo "Count of strings in %filename% is %number%"
exit /b %number%"
