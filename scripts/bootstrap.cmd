@echo off
echo use: _ensure (no separate bootstrap step)
call "%~dp0_ensure.cmd" --hugo --vsa --catalogus --vsa-tool --import vsa
exit /b %ERRORLEVEL%
