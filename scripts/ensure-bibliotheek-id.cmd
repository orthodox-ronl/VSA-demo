@echo off
setlocal EnableExtensions
cd /d %~dp0\..

REM Bibliotheek-id in basispartituur-.mscz colofon/meta zetten of controleren.
REM Zie scripts\h.cmd ensure-bibliotheek-id

if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage

python scripts\ensure_bibliotheek_id.py %*
exit /b %ERRORLEVEL%

:usage
echo.
echo Gebruik: scripts\ensure-bibliotheek-id.cmd [root] [--check-only] [--fail]
echo.
echo   Zet of herstelt Bibliotheek-id in basispartituur-.mscz onder bibliotheek/.
echo   Zonder root: content-source\praktijk\oefenhoek\bibliotheek.
echo   Daarna mscz-products voor verse PDF's.
echo.
echo Detail: scripts\h.cmd ensure-bibliotheek-id
echo Handleiding: content-source\praktijk\handleiding\scripts\ensure-bibliotheek-id.md
echo.
endlocal
exit /b 0
