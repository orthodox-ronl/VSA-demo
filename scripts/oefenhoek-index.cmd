@echo off
setlocal EnableExtensions
cd /d %~dp0\..

REM Oefenhoek bladermap-index strippen; optioneel SVG uit .vsa.
REM Zie scripts\h.cmd oefenhoek-index

if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage

python scripts\sync_oefenhoek_index.py %*
exit /b %ERRORLEVEL%

:usage
echo.
echo Gebruik: scripts\oefenhoek-index.cmd [--dry-run] [--svg] [--verbose]
echo.
echo   Zonder flags: haalt auto-includes/score-shortcodes uit bladermap-index.md.
echo   --svg: schrijf SVG van lokale .vsa (geen basispartituur-.mscz) naar
echo          static\vsa\bladermap\ (na vsa build-markdown / check).
echo   Standaard alleen samenvatting; --verbose toont elk pad.
echo   check / build / serve roepen dit al aan.
echo.
echo Detail: scripts\h.cmd oefenhoek-index
echo Handleiding: content-source\praktijk\handleiding\scripts\oefenhoek-index.md
echo.
endlocal
exit /b 0
