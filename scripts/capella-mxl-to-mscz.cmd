@echo off
setlocal EnableExtensions
cd /d %~dp0\..

REM Capella-.mxl map -> standaard-layout .mscz (niet via check/build/serve).
REM Zie scripts\h.cmd capella-mxl-to-mscz

if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage

python scripts\batch_capella_mxl_to_mscz.py %*
exit /b %ERRORLEVEL%

:usage
echo.
echo Gebruik: scripts\capella-mxl-to-mscz.cmd [bronmap] [doelmap] [--force] [--dry-run] [--limit N]
echo.
echo   Kuist Capella-.mxl op en zet ze om naar standaard-.mscz.
echo   Zonder paden:
echo     C:\Git\orthodox-ronl\ruwe-invoer\capella-backup-mxl
echo     C:\Git\orthodox-ronl\ruwe-invoer\capella-backup-mscz
echo   MuseScore 4 moet geinstalleerd zijn en niet openstaan.
echo   Hervatbaar: bestaande verse .mscz worden overgeslagen.
echo.
echo Detail: scripts\h.cmd capella-mxl-to-mscz
echo.
endlocal
exit /b 0
