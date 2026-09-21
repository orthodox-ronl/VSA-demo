@echo off
setlocal EnableExtensions
cd /d %~dp0\..
call scripts\_ensure.cmd --import vsa
if errorlevel 1 exit /b 1
python scripts\sync_vsa_products.py %*
exit /b %ERRORLEVEL%
