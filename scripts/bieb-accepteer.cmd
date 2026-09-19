@echo off
setlocal EnableExtensions
cd /d %~dp0\..

REM Neem .mscz / .vsa / .print.mscz op in oefenhoek\bibliotheek.
REM Zie scripts\h.cmd bieb-accepteer

if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage
if "%~1"=="" goto usage

python scripts\bieb_accepteer.py %*
exit /b %ERRORLEVEL%

:usage
echo.
echo Gebruik: scripts\bieb-accepteer.cmd ^<id^> ^<bestand^> [meer...] [opties]
echo.
echo   id = zangstuk/variant/uitvoeringsvorm
echo   bestand = .mscz, .vsa, .print.mscz (optioneel .pdf / .mxl ernaast)
echo.
echo Opties: --title --status --stub --move --force --dry-run
echo         --skip-vsa-validate --artefacten-handmatig
echo.
echo Detail: scripts\h.cmd bieb-accepteer
echo Handleiding: content-source\praktijk\handleiding\publiceren\1-opnemen-in-bibliotheek.md
echo.
endlocal
exit /b 0
