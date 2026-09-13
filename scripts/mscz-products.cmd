@echo off
setlocal EnableExtensions
cd /d %~dp0\..

REM PDF + Coria-MXL uit een publicatie-.mscz (niet via check/build/serve).
REM Zie scripts\h.cmd mscz-products

if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage

python scripts\sync_mscz_products.py %*
exit /b %ERRORLEVEL%

:usage
echo.
echo Gebruik: scripts\mscz-products.cmd [pad] [--force] [--dry-run]
echo.
echo   Exporteert sibling-PDF en Coria-.mxl bij publicatie-.mscz.
echo   Zonder pad: content-source. Na de editslag in MuseScore, niet
echo   meteen na apply_mscz_layout.py.
echo.
echo Detail: scripts\h.cmd mscz-products
echo.
endlocal
exit /b 0
