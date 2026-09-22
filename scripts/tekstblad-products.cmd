@echo off
setlocal EnableExtensions
cd /d %~dp0\..
call scripts\_ensure.cmd --vsa --catalogus --vsa-tool --import vsa --import yaml --import markdown
if errorlevel 1 exit /b 1
python scripts\sync_tekstblad_products.py %*
exit /b %ERRORLEVEL%
