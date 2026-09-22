@echo off
setlocal EnableExtensions
cd /d %~dp0\..

REM Capella/CapToMusic-.mxl inhoudelijk opkuisen (lagen 1-3).
REM Zie scripts\h.cmd opkuisen

if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage
if "%~1"=="" goto usage

python scripts\cleanup_capella_mxl.py %*
exit /b %ERRORLEVEL%

:usage
echo.
echo Gebruik: scripts\opkuisen.cmd ^<bron.mxl^> [-o doel.mxl^|doelmap] ...
echo.
echo   Kuist Capella/CapToMusic-.mxl op (reciteerkwarten, lettergrepen, ...).
echo   Geen A4-layout / PDF / Coria - dat is layout.cmd / mscz-products.
echo.
echo   -o: schrijf naar _werk\STAM\STAM.mxl (geen spaties in de naam).
echo   Zonder -o: in-place alleen als de bestandsnaam al geen spaties heeft.
echo   Overschrijf nooit het Capella-origineel in input\capella\.
echo.
echo Detail: scripts\h.cmd opkuisen
echo Handleiding: content-source\praktijk\handleiding\scripts\opkuisen.md
echo.
endlocal
exit /b 0
