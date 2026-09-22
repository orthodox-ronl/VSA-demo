@echo off
setlocal EnableExtensions
cd /d %~dp0\..

REM Basispartituur-standaard (A4-layout) op .mscz of opgekuiste .mxl.
REM Zie scripts\h.cmd layout

if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage
if "%~1"=="" goto usage

python scripts\apply_mscz_layout.py %*
exit /b %ERRORLEVEL%

:usage
echo.
echo Gebruik: scripts\layout.cmd ^<bestand.mscz^|.mxl^> [-o doel.mscz] [--id ID] [--no-extenders]
echo.
echo   Past de Oefenhoek-basispartituur-standaard toe (normaliseren / layouten).
echo   .mxl: zet -o naar _werk\STAM\STAM.mscz (geen spaties).
echo   .mscz: zonder -o in-place (idempotent; opnieuw na editslag).
echo   Weigert *.print.mscz. MuseScore 4 nodig bij .mxl-invoer.
echo.
echo Detail: scripts\h.cmd layout
echo Handleiding: content-source\praktijk\handleiding\scripts\layout.md
echo.
endlocal
exit /b 0
