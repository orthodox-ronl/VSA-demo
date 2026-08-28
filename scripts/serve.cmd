@echo off
setlocal EnableExtensions
cd /d %~dp0\..

set "NO_BUILD="

:parse_args
if "%~1"=="" goto args_done
if /I "%~1"=="--no-build" set "NO_BUILD=1" & shift & goto parse_args
if /I "%~1"=="-h" goto usage
if /I "%~1"=="--help" goto usage
echo Onbekende optie: %~1
goto usage

:args_done

echo.
echo === VSA-demo local preview ===
echo.

call scripts\_ensure.cmd --hugo --vsa --catalogus --vsa-tool --import vsa
if errorlevel 1 exit /b 1

if defined NO_BUILD (
  if not exist generated\content (
    echo ERROR: generated\content ontbreekt. Draai eerst check
    echo        of serve zonder --no-build.
    exit /b 1
  )
  echo [1/1] Generate overgeslagen --no-build. Start Hugo server
  echo.
  goto start_server
)

set "PIPELINE_SKIP_HUGO=1"
set "PIPELINE_TITLE=VSA-demo preview (generate)"

call scripts\_pipeline.cmd
if errorlevel 1 exit /b 1

echo [2/2] Start Hugo server
:start_server
hugo server ^
  --source . ^
  --contentDir generated\content ^
  --baseURL / ^
  --disableFastRender ^
  --forceSyncStatic ^
  --noHTTPCache
endlocal
exit /b %ERRORLEVEL%

:usage
echo.
echo Gebruik: serve [--no-build]
echo.
echo   --no-build   geen sync/validate/generate; alleen hugo server
echo                (vereist bestaande generated\content)
echo.
echo Detail: h serve
echo.
endlocal
exit /b 2
