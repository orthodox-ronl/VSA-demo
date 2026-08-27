@echo off
setlocal EnableExtensions
cd /d %~dp0\..

call scripts\_ensure.cmd --hugo --vsa --catalogus --vsa-tool --import vsa --import yaml
if errorlevel 1 exit /b 1

set "PY=python"


if not defined PIPELINE_TITLE set "PIPELINE_TITLE=VSA-demo pipeline"

echo.
echo === %PIPELINE_TITLE% ===
echo Python: %PY%
echo.

echo [1/6] Sync zondag bronbestanden
call scripts\sync-bron-zondagen.cmd
if errorlevel 1 exit /b 1
echo OK
echo.

echo [2/6] Validate content-source
if defined PIPELINE_STRICT (
  "%PY%" scripts\validate_content.py --summary --fail-on-warnings content-source
) else (
  "%PY%" scripts\validate_content.py --summary content-source
)
if errorlevel 1 exit /b 1
echo OK
echo.

echo [3/6] Generate Markdown + SVG + MusicXML
if exist generated\content rmdir /s /q generated\content
if exist static\vsa rmdir /s /q static\vsa
"%PY%" -m vsa.cli build-markdown ^
  content-source ^
  generated\content ^
  static\vsa ^
  --output-mode shortcode
if errorlevel 1 exit /b 1
"%PY%" -m vsa.cli musicxml ^
  content-source ^
  static\vsa\mxl
if errorlevel 1 exit /b 1
"%PY%" scripts\update-nav-placeholders.py generated\content
if errorlevel 1 exit /b 1
"%PY%" scripts\inject_git_dates.py generated\content content-source
if errorlevel 1 exit /b 1
"%PY%" scripts\write_build_stamp.py
if errorlevel 1 exit /b 1
echo OK
echo.

if defined PIPELINE_SKIP_HUGO (
  echo [4/6] Hugo overgeslagen ^(--skip-hugo^)
  echo.
  echo Pipeline OK tot en met generate.
  endlocal
  exit /b 0
)

where hugo >nul 2>&1
if errorlevel 1 (
  echo ERROR: hugo not found on PATH.
  exit /b 1
)

echo [4/6] Build Hugo site
if exist generated\site rmdir /s /q generated\site
hugo ^
  --source . ^
  --contentDir generated\content ^
  --destination generated\site ^
  --baseURL /
if errorlevel 1 exit /b 1
echo OK
echo.

echo [5/6] Interne links en assets
"%PY%" scripts\check_hugo_links_and_assets.py --site-dir generated\site
if errorlevel 1 exit /b 1
echo OK
echo.

if defined PIPELINE_EXTERNAL (
  echo [6/6] Externe http^(s^)-links
  "%PY%" scripts\check_external_links.py --site-dir generated\site
  if errorlevel 1 exit /b 1
  echo OK
  echo.
) else (
  echo [6/6] Externe links overgeslagen ^(gebruik check.cmd --external^)
  echo.
)

echo Pipeline OK.
endlocal
exit /b 0
