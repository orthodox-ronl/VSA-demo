@echo off
setlocal
cd /d %~dp0\..
call scripts\_ensure.cmd --import yaml
if errorlevel 1 exit /b 1
if not "%~1"=="" (
  python scripts\sync_bron_zondagen.py --bron-root %~1
  exit /b %ERRORLEVEL%
)
python scripts\sync_bron_zondagen.py
exit /b %ERRORLEVEL%
