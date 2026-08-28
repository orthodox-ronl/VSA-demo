@echo off
setlocal EnableExtensions
cd /d %~dp0\..

REM Bouwt de demo-PDF voor praktijk/demo (voorbeeld-blad).
REM Zie scripts\h.cmd demo-pdf

if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage

call scripts\pdf.cmd ^
  content-source\praktijk\demo\assets\voorbeeld-blad.md ^
  -o static\demo\voorbeeld-blad.pdf ^
  --content-root content-source
exit /b %ERRORLEVEL%

:usage
echo.
echo Gebruik: scripts\demo-pdf.cmd
echo.
echo   Bouwt static\demo\voorbeeld-blad.pdf uit
echo   content-source\praktijk\demo\assets\voorbeeld-blad.md
echo   (+ geinclude voorbeeld.vsa).
echo.
echo   check / serve / build falen als die PDF ouder is dan de bronnen;
echo   dit script is het herstelcommando uit die foutmelding.
echo.
echo Detail: scripts\h.cmd demo-pdf
echo.
endlocal
exit /b 0
