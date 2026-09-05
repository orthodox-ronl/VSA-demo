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

echo [1/7] Sync zondag bronbestanden
call scripts\sync-bron-zondagen.cmd
if errorlevel 1 exit /b 1
echo OK
echo.

echo [2/7] Validate content-source
if defined PIPELINE_STRICT (
  "%PY%" scripts\validate_content.py --summary --fail-on-warnings content-source
) else (
  "%PY%" scripts\validate_content.py --summary content-source
)
if errorlevel 1 exit /b 1
echo OK
echo.

echo [3/7] Generate Markdown + SVG + MusicXML
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
"%PY%" scripts\copy_content_extras.py
if errorlevel 1 exit /b 1
"%PY%" scripts\write_build_stamp.py
if errorlevel 1 exit /b 1
echo OK
echo.

echo [4/7] Demo-PDF up-to-date
"%PY%" scripts\check_demo_pdf_fresh.py
if errorlevel 1 exit /b 1
echo OK
echo.

if defined PIPELINE_SKIP_HUGO (
  echo [5/7] Hugo overgeslagen ^(--skip-hugo^)
  echo.
  echo Pipeline OK tot en met generate + demo-PDF-check.
  endlocal
  exit /b 0
)

where hugo >nul 2>&1
if errorlevel 1 (
  echo ERROR: hugo not found on PATH.
  exit /b 1
)

echo [5/7] Build Hugo site
if exist generated\site rmdir /s /q generated\site
hugo ^
  --source . ^
  --contentDir generated\content ^
  --destination generated\site ^
  --baseURL /
if errorlevel 1 exit /b 1
echo OK
echo.

echo [6/7] Interne links en assets
"%PY%" scripts\check_hugo_links_and_assets.py --site-dir generated\site
if errorlevel 1 exit /b 1
echo OK
echo.

if defined PIPELINE_EXTERNAL (
  echo [7/7] Externe http^(s^)-links
  "%PY%" scripts\check_external_links.py --site-dir generated\site
  if errorlevel 1 exit /b 1
  echo OK
  echo.
) else (
  echo [7/7] Externe links overgeslagen ^(gebruik check.cmd --external^)
  echo.
)

echo Pipeline OK.
endlocal
exit /b 0
