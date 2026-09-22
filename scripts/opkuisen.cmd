@echo off
setlocal EnableExtensions
cd /d %~dp0\..

REM Generieke opkuiser (herkomstanalyse + inhoud; optioneel layout).
REM Zie scripts\h.cmd opkuisen

if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage
if "%~1"=="" goto usage

python scripts\opkuisen.py %*
exit /b %ERRORLEVEL%

:usage
echo.
echo Gebruik: scripts\opkuisen.cmd ^<pad^> [pad...] [opties]
echo.
echo   Herkomstanalyse + inhoudelijke opkuis voor .mxl / .musicxml / .xml /
echo   .mscz / .mscx. Optioneel .vsa/.mvsa (alleen --analyze/--dry-run).
echo.
echo   Default-diepte: content (inhoudsfixes). Geen schrijven: --analyze
echo   of --dry-run (synoniemen). Layout erbij: --layout.
echo.
echo   -o doelbestand^|doelmap   --in-place   --ext .mxl
echo   --assume capella^|musicxml-generic^|musescore^|vsa^|mvsa
echo   --force   --id BIBLIOTHEEK-ID
echo.
echo   Geen A4/PDF/Coria zonder --layout; PDF/Coria is mscz-products.
echo   Overschrijf nooit stil ruwe input\capella\ (gebruik -o of --in-place).
echo.
echo Detail: scripts\h.cmd opkuisen
echo Handleiding: content-source\praktijk\handleiding\scripts\opkuisen.md
echo.
endlocal
exit /b 0
