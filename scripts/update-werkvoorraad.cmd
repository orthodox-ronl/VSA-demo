@echo off
setlocal EnableExtensions
cd /d %~dp0\..

REM Werkvoorraad-tabel in oefenhoek\input\werkvoorraad.md bijwerken.
REM Zie scripts\h.cmd update-werkvoorraad

if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage

python scripts\update_werkvoorraad.py %*
exit /b %ERRORLEVEL%

:usage
echo.
echo Gebruik: scripts\update-werkvoorraad.cmd
echo.
echo   Vult de tabel in oefenhoek\input\werkvoorraad.md uit bestanden op schijf.
echo   Doel-id en notities in bestaande rijen blijven staan.
echo   Verwijdert generated\...\oefenhoek\input (geen Hugo-pagina's voor inputs).
echo   check / build / serve doen dit ook; handmatig na nieuwe input-bestanden.
echo.
echo Detail: scripts\h.cmd update-werkvoorraad
echo Handleiding: content-source\praktijk\handleiding\scripts\update-werkvoorraad.md
echo.
endlocal
exit /b 0
