@echo off
setlocal EnableExtensions
cd /d %~dp0\..

REM Markdown + VSA -> A4 PDF. Zie scripts\h.cmd pdf

call scripts\_ensure.cmd --vsa --catalogus --vsa-tool --import vsa --import yaml --import markdown
if errorlevel 1 exit /b 1

if "%~1"=="" goto usage
if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage

python -m vsa.cli pdf %*
exit /b %ERRORLEVEL%

:usage
echo.
echo Gebruik: scripts\pdf.cmd ^<bestand.md^> [-o uit.pdf] [--content-root DIR]
echo.
echo   Rendert het hele Markdownbestand naar PDF: VSA-blokken, includes,
echo   pagebreaks, print-only. Fouten: zelfde formaat als check/validate.
echo.
echo Detail: scripts\h.cmd pdf
echo.
endlocal
exit /b 2
