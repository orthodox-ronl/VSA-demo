@echo off
setlocal EnableExtensions
cd /d %~dp0\..
set "PIPELINE_STRICT=1"
set "PIPELINE_TITLE=VSA-demo build"
call scripts\_pipeline.cmd
if errorlevel 1 exit /b 1
echo Build complete: generated\site
endlocal
exit /b 0
