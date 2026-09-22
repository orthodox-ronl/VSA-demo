@echo off
setlocal EnableExtensions EnableDelayedExpansion
cd /d %~dp0\..

REM Overzicht of man-page per script.
REM   scripts\h.cmd              -> korte catalogus
REM   scripts\h.cmd bootstrap    -> detail (man-page)
REM
REM Onderhoud: bij script toevoegen/wijzigen/verwijderen ook scripts\README.md
REM en deze file bijwerken. Echo-tekst: alleen eenvoudige ASCII (->, -).
REM Unicode-pijlen/em-dashes worden in Windows-cmd onleesbaar.

set "FILTER=%~1"
if /I "%FILTER%"=="-h" goto usage
if /I "%FILTER%"=="--help" goto usage

if not "%FILTER%"=="" (
  set "FILTER=!FILTER:scripts\=!"
  set "FILTER=!FILTER:.cmd=!"
)

if "%FILTER%"=="" goto catalog

if /I "%FILTER%"=="bootstrap" goto man_ensure
if /I "%FILTER%"=="check" goto man_check
if /I "%FILTER%"=="build" goto man_build
if /I "%FILTER%"=="serve" goto man_serve
if /I "%FILTER%"=="pdf" goto man_pdf
if /I "%FILTER%"=="demo-pdf" goto man_demo_pdf
if /I "%FILTER%"=="sync-bron-zondagen" goto man_sync
if /I "%FILTER%"=="mscz-products" goto man_mscz_products
if /I "%FILTER%"=="sync_mscz_products.py" goto man_mscz_products
if /I "%FILTER%"=="ensure_bibliotheek_id" goto man_bibliotheek_id
if /I "%FILTER%"=="ensure_bibliotheek_id.py" goto man_bibliotheek_id
if /I "%FILTER%"=="check_bibliotheek_id" goto man_bibliotheek_id
if /I "%FILTER%"=="check_bibliotheek_id.py" goto man_bibliotheek_id
if /I "%FILTER%"=="vsa-products" goto man_vsa_products
if /I "%FILTER%"=="sync_vsa_products.py" goto man_vsa_products
if /I "%FILTER%"=="capella-mxl-to-mscz" goto man_capella_mxl
if /I "%FILTER%"=="batch_capella_mxl_to_mscz.py" goto man_capella_mxl
if /I "%FILTER%"=="bieb-accepteer" goto man_bieb_accepteer
if /I "%FILTER%"=="bieb_accepteer" goto man_bieb_accepteer
if /I "%FILTER%"=="bieb_accepteer.py" goto man_bieb_accepteer
if /I "%FILTER%"=="opkuisen" goto man_opkuisen
if /I "%FILTER%"=="cleanup_capella_mxl" goto man_opkuisen
if /I "%FILTER%"=="cleanup_capella_mxl.py" goto man_opkuisen
if /I "%FILTER%"=="layout" goto man_layout
if /I "%FILTER%"=="apply_mscz_layout" goto man_layout
if /I "%FILTER%"=="apply_mscz_layout.py" goto man_layout
if /I "%FILTER%"=="ensure-bibliotheek-id" goto man_bibliotheek_id
if /I "%FILTER%"=="ensure_bibliotheek_id" goto man_bibliotheek_id
if /I "%FILTER%"=="ensure_bibliotheek_id.py" goto man_bibliotheek_id
if /I "%FILTER%"=="check_bibliotheek_id" goto man_bibliotheek_id
if /I "%FILTER%"=="check_bibliotheek_id.py" goto man_bibliotheek_id
if /I "%FILTER%"=="update-werkvoorraad" goto man_update_werkvoorraad
if /I "%FILTER%"=="update_werkvoorraad" goto man_update_werkvoorraad
if /I "%FILTER%"=="update_werkvoorraad.py" goto man_update_werkvoorraad
if /I "%FILTER%"=="oefenhoek-index" goto man_oefenhoek_index
if /I "%FILTER%"=="sync_oefenhoek_index" goto man_oefenhoek_index
if /I "%FILTER%"=="sync_oefenhoek_index.py" goto man_oefenhoek_index
if /I "%FILTER%"=="migrate_oefenhoek_bibliotheek" goto man_migrate_bibliotheek
if /I "%FILTER%"=="migrate_oefenhoek_bibliotheek.py" goto man_migrate_bibliotheek
if /I "%FILTER%"=="bibliotheek" goto man_migrate_bibliotheek
if /I "%FILTER%"=="bibliotheek.py" goto man_migrate_bibliotheek
if /I "%FILTER%"=="h" goto man_help
if /I "%FILTER%"=="help" goto man_help

goto filter_list

:catalog
echo.
echo === VSA-demo scripts ===
echo Detail ^(man-page^): h ^<naam^>   bijv. h check
echo Begrippen + wanneer-wat: scripts\README.md
echo Groen voor commit ^(CI-spiegel^): check --strict
echo.
call :emit_short check "preflight / CI-spiegel" "--strict --external --skip-hugo"
call :emit_short build "volledige sitebuild + interne linkcheck" "-"
call :emit_short serve "lokale Hugo-preview" "--no-build"
call :emit_short pdf "Markdown + VSA naar A4-PDF" "-o --content-root"
call :emit_short demo-pdf "demo-PDF voorbeeld-blad.pdf bouwen" "-"
call :emit_short sync-bron-zondagen "sync zondag-VSA uit bron" "[bron-root]"
call :emit_short opkuisen "Capella-MXL inhoudelijk opkuisen" "<bron.mxl> [-o]"
call :emit_short layout "basispartituur-standaard op .mscz/.mxl" "<pad> [-o] [--id]"
call :emit_short mscz-products "PDF + Coria-MXL uit .mscz" "[pad] --force --dry-run"
call :emit_short vsa-products "Coria-.vsa.mxl uit bibliotheek-.vsa" "[pad] --force --dry-run"
call :emit_short ensure-bibliotheek-id "bibliotheek-id in .mscz colofon/meta" "[root]"
call :emit_short update-werkvoorraad "werkvoorraad-tabel uit input/ bijwerken" "-"
call :emit_short oefenhoek-index "bladermap-index strippen / --svg" "[--svg --dry-run]"
call :emit_short capella-mxl-to-mscz "Capella-MXL map -> standaard-.mscz" "[bron] [doel] --force --dry-run --limit"
call :emit_short bieb-accepteer "partituur opnemen in bibliotheek" "<id> <bestand> [--dry-run]"
call :emit_short h "catalogus of man-page per script" "[naam]"
echo.
echo Uitgebreide man-pages: handleiding scripts\
echo   content-source\praktijk\handleiding\scripts\
echo.
echo Python-helpers ^(pipeline / library, geen eigen .cmd^): validate_content.py,
echo   update-nav-placeholders.py, inject_git_dates.py, copy_content_extras.py,
echo   fingerprint_coria_mxl.py, write_build_stamp.py, check_demo_pdf_fresh.py,
echo   check_hugo_links_and_assets.py, check_external_links.py, check_coria_mxl.py,
echo   check_coria_retrieve.py, check_publicatiestatus.py, check_partituur_products.py,
echo   check_bibliotheek_id.py, check_vsa_products.py, bibliotheek.py,
echo   export_mscz_coria_mxl.py, staff_clefs.py, nl_hyphen.py, score_filenames.py,
echo   migrate_oefenhoek_bibliotheek.py, patch_oefenhoek_trisagion.py, rebar_20d_4kwart.py,
echo   test_*.py
echo.
goto end_ok

:filter_list
set "ANY=0"
echo.
echo === VSA-demo scripts ^(filter: %FILTER%^) ===
echo Voor detail: scripts\h.cmd ^<exacte-naam^>   bijv. scripts\h.cmd bootstrap
echo.
call :try_short check "preflight / CI-spiegel" "--strict --external --skip-hugo"
call :try_short build "volledige sitebuild + interne linkcheck" "-"
call :try_short serve "lokale Hugo-preview" "--no-build"
call :try_short pdf "Markdown + VSA naar A4-PDF" "-o --content-root"
call :try_short demo-pdf "demo-PDF voorbeeld-blad.pdf bouwen" "-"
call :try_short sync-bron-zondagen "sync zondag-VSA uit bron" "[bron-root]"
call :try_short opkuisen "Capella-MXL inhoudelijk opkuisen" "<bron.mxl> [-o]"
call :try_short layout "basispartituur-standaard op .mscz/.mxl" "<pad> [-o] [--id]"
call :try_short mscz-products "PDF + Coria-MXL uit .mscz" "[pad] --force --dry-run"
call :try_short vsa-products "Coria-.vsa.mxl uit bibliotheek-.vsa" "[pad] --force --dry-run"
call :try_short ensure-bibliotheek-id "bibliotheek-id in .mscz colofon/meta" "[root]"
call :try_short update-werkvoorraad "werkvoorraad-tabel uit input/ bijwerken" "-"
call :try_short oefenhoek-index "bladermap-index strippen / --svg" "[--svg --dry-run]"
call :try_short capella-mxl-to-mscz "Capella-MXL map -> standaard-.mscz" "[bron] [doel] --force --dry-run --limit"
call :try_short bieb-accepteer "partituur opnemen in bibliotheek" "<id> <bestand> [--dry-run]"
call :try_short h "catalogus of man-page per script" "[naam]"
if "!ANY!"=="0" goto unknown
echo.
echo Meer uitleg: scripts\README.md
echo Handleiding: content-source\praktijk\handleiding\scripts\
echo.
goto end_ok

:unknown
echo Geen script gevonden voor "%FILTER%".
echo Bekende namen: check, build, serve, pdf, demo-pdf, sync-bron-zondagen,
echo   opkuisen, layout, mscz-products, vsa-products, ensure-bibliotheek-id,
echo   update-werkvoorraad, oefenhoek-index, capella-mxl-to-mscz, bieb-accepteer, h
echo.
goto end_fail

:emit_short
echo scripts\%~1.cmd
echo   %~2
if not "%~3"=="-" echo   opties: %~3
echo   detail: scripts\h.cmd %~1
echo.
goto :eof

:try_short
echo %~1| findstr /I /C:"%FILTER%" >nul
if errorlevel 1 goto :eof
set "ANY=1"
call :emit_short %1 %2 %3
goto :eof

:usage
echo.
echo Gebruik:
echo   scripts\h.cmd              korte catalogus
echo   scripts\h.cmd ^<naam^>       man-page voor dat script
echo   scripts\h.cmd -h           deze uitleg
echo.
echo Voorbeelden:
echo   scripts\h.cmd bootstrap
echo   scripts\h.cmd check
echo.
echo Begrippen ^(preflight, CI-spiegel, ...^): scripts\README.md
echo.
goto end_ok

:man_ensure
echo.
echo NAME
echo   _ensure (called by check/serve/build)
echo.
echo DESCRIPTION
echo   Checks PATH (.\scripts, python 3.14, hugo, vsa) and pip-installs
echo   catalogus + vsa-tool into that Python. No separate bootstrap step.
echo.
goto end_ok

:man_check
echo.
echo NAME
echo   scripts\check.cmd - preflight / CI-spiegel
echo.
echo SYNOPSIS
echo   scripts\check.cmd [--strict] [--external] [--skip-hugo]
echo.
echo DESCRIPTION
echo   Draait lokaal de blocking pipeline die CI ook doet:
echo   sync zondag -^> oefenhoek-index -^> validate -^> generate ^(md/svg/mxl^)
echo   -^> Coria-kuis vsa-mxl -^> hugo -^> interne links.
echo   Wrapper om scripts\_pipeline.cmd ^(zie scripts\README.md testladder^).
echo   Geen MuseScore-PDF/Coria-MXL: scripts\mscz-products.cmd
echo.
echo   "Preflight" = check voor commit. "CI-spiegel" = met --strict dezelfde
echo   strengheid als GitHub Actions ^(ook VSA-warnings laten falen^).
echo.
echo OPTIONS
echo   --strict      faal ook op VSA-warnings ^(CI doet dit standaard^)
echo   --external    check ook externe http^(s^)-links ^(kan flaky zijn;
echo                 in CI is dit non-blocking, lokaal faalt het hard^)
echo   --skip-hugo   stop na sync + validate + generate ^(geen Hugo/linkcheck^)
echo.
echo WHEN
echo   Altijd voor committen/pushen: scripts\check.cmd --strict
echo   Tussendoor itereren op VSA: scripts\check.cmd --skip-hugo
echo.
echo SEE ALSO
echo   scripts\h.cmd serve
echo   scripts\README.md  ^(testladder + CI-spiegel^)
echo.
goto end_ok

:man_build
echo.
echo NAME
echo   scripts\build.cmd
echo.
echo SYNOPSIS
echo   scripts\build.cmd
echo.
echo DESCRIPTION
echo   Volledige sitebuild naar generated\site. Zelfde keten als check.cmd --strict
echo   ^(via scripts\_pipeline.cmd^). Geen --external.
echo.
echo   Commit geen generated\ of static\vsa\ - die mappen zijn build-output.
echo.
echo WHEN
echo   Site-artifact in generated\site zonder hugo server.
echo   Voor preflight voor commit: check.cmd --strict is genoeg.
echo.
echo SEE ALSO
echo   scripts\h.cmd check
echo   scripts\h.cmd serve
echo.
goto end_ok

:man_serve
echo.
echo NAME
echo   scripts\serve.cmd
echo.
echo SYNOPSIS
echo   scripts\serve.cmd [--no-build]
echo.
echo DESCRIPTION
echo   Start de Hugo-development server ^(http://127.0.0.1:18731/^).
echo   Poort 18731, niet 1313 ^(1313 is lokaal gereserveerd^).
echo   Standaard: pipeline ^(sync/validate/generate via _pipeline.cmd^), daarna server.
echo   Validate zonder --strict ^(snellere preview^).
echo   Console: stapvoortgang + samenvattingen, geen bestandslijsten.
echo   Met --no-build: alleen Coria-fingerprints + server; vereist bestaande
echo   generated\content ^(bijv. na check.cmd --strict^).
echo.
echo OPTIONS
echo   --no-build   sla sync/validate/generate over; wel Coria-fingerprints
echo.
echo WHEN
echo   Browser-preview. CI-gelijk: eerst check.cmd --strict, dan --no-build.
echo.
echo SEE ALSO
echo   scripts\h.cmd check
echo.
goto end_ok

:man_pdf
echo.
echo NAME
echo   scripts\pdf.cmd
echo.
echo SYNOPSIS
echo   scripts\pdf.cmd ^<bestand.md^> [-o uit.pdf] [--content-root DIR]
echo.
echo DESCRIPTION
echo   Maakt een A4-PDF van een Markdownbestand met VSA-blokken.
echo   Includes, pagebreaks, print-only en SVG-rendering lopen via vsa pdf
echo   ^(zelfde keten als build-markdown voor dat ene bestand^).
echo.
echo   Validatiefouten: bestand, regel, kolom, code, bronregel - hetzelfde
echo   formaat als check / vsa validate.
echo.
echo OPTIONS
echo   -o, --output FILE     uitvoer-PDF ^(default: ^<stem^>.pdf in de cwd^)
echo   --content-root DIR    root voor catalogus-includes ^(lokaal/^)
echo   --chrome PATH         Edge/Chrome als auto-detectie faalt
echo.
echo WHEN
echo   Koormap / liturgie-blad uit content-source printen, zonder Hugo.
echo.
echo SEE ALSO
echo   scripts\h.cmd demo-pdf
echo   scripts\h.cmd check
echo.
goto end_ok

:man_demo_pdf
echo.
echo NAME
echo   scripts\demo-pdf.cmd
echo.
echo SYNOPSIS
echo   scripts\demo-pdf.cmd
echo.
echo DESCRIPTION
echo   Bouwt static\demo\voorbeeld-blad.pdf uit het demo-Markdownblad.
echo   Wrapper om scripts\pdf.cmd met vaste paden.
echo.
echo   check / build / serve ^(met build^) controleren of die PDF niet ouder
echo   is dan voorbeeld-blad.md en voorbeeld.vsa. Bij veroudering: fout +
echo   dit commando als herstel.
echo.
echo WHEN
echo   Na wijziging van content-source\praktijk\demo\assets\voorbeeld-blad.md
echo   of voorbeeld.vsa, voordat je commit of serve opnieuw draait.
echo.
echo SEE ALSO
echo   scripts\h.cmd pdf
echo   scripts\check_demo_pdf_fresh.py
echo.
goto end_ok

:man_sync
echo.
echo NAME
echo   scripts\sync-bron-zondagen.cmd
echo.
echo SYNOPSIS
echo   scripts\sync-bron-zondagen.cmd [bron-root]
echo.
echo DESCRIPTION
echo   Kopieert tropaar/kondak ^(en gerelateerde^) zondag-bestanden uit de
echo   bron-repository naar content-source\praktijk\zondagen\.
echo   Zo blijft de demo synchroon met canonieke bron-VSA.
echo.
echo   Zonder argument: automatisch sibling ..\bron of vendor\bron.
echo   Met argument: expliciet pad naar een bron-checkout.
echo.
echo WHEN
echo   Handmatig als je bron net hebt bijgewerkt en alleen sync wilt.
echo   check.cmd / build / serve roepen sync zelf al aan.
echo.
echo SEE ALSO
echo   scripts\h.cmd check
echo   scripts\README.md  ^(begrip: Sync zondag^)
echo.
goto end_ok

:man_mscz_products
echo.
echo NAME
echo   scripts\mscz-products.cmd
echo.
echo SYNOPSIS
echo   scripts\mscz-products.cmd [pad] [--force] [--dry-run]
echo.
echo DESCRIPTION
echo   Exporteert sibling-PDF en Coria-.mxl bij basispartituur-.mscz
echo   (niet oefenhoek\input, niet *.print.mscz). Zonder pad:
echo   content-source. Ontbrekend/verkeerde partituur-hash stamp,
echo   tenzij --force.
echo.
echo   Pipeline roept dit lokaal aan. Eerst apply_mscz_layout.py,
echo   eventueel editslag in MuseScore, daarna dit script.
echo   check_partituur_products.py controleert stamps (main: streng).
echo   ensure_bibliotheek_id.py zet Bibliotheek-id in colofon/meta.
echo   Print-velden (*.print.mscz): zie handleiding partituur/7-print-mscz.
echo.
echo WHEN
echo   Als de basispartituur-.mscz klaar is voor publicatie-PDF en Coria.
echo.
echo SEE ALSO
echo   scripts\apply_mscz_layout.py
echo   scripts\ensure_bibliotheek_id.py
echo   scripts\sync_mscz_products.py
echo   scripts\check_partituur_products.py
echo   scripts\score_filenames.py
echo   scripts\oefenhoek-product-contract.md
echo   scripts\mscz-partituur-contract.md
echo   scripts\mscz-product-transforms.md
echo.
goto end_ok

:man_bibliotheek_id
echo.
echo NAME
echo   scripts\ensure-bibliotheek-id.cmd
echo   scripts\ensure_bibliotheek_id.py / check_bibliotheek_id.py
echo.
echo SYNOPSIS
echo   scripts\ensure-bibliotheek-id.cmd [root] [--check-only] [--fail]
echo.
echo DESCRIPTION
echo   Basispartituur-.mscz onder bibliotheek/ moeten Bibliotheek-id in colofon
echo   en meta vsaBibliotheekId hebben. ensure herstelt lokaal
echo   (process_mscz); check-only / CI schrijft niet. main/strict: fail.
echo   Zonder root: oefenhoek\bibliotheek. Daarna mscz-products voor verse PDF.
echo.
echo WHEN
echo   Na layout / verplaatsing in bibliotheek, of als check id-mismatch meldt.
echo.
echo SEE ALSO
echo   scripts\h.cmd layout
echo   scripts\h.cmd mscz-products
echo   handleiding scripts\ensure-bibliotheek-id
echo   scripts\mscz-partituur-contract.md
echo.
goto end_ok

:man_vsa_products
echo.
echo NAME
echo   scripts\vsa-products.cmd
echo.
echo SYNOPSIS
echo   scripts\vsa-products.cmd [pad] [--force] [--dry-run]
echo.
echo DESCRIPTION
echo   Maakt sibling Coria-.vsa.mxl bij bibliotheek-.vsa
echo   (syllabify in temp, vsa musicxml playback, sanitize, source-sha stamp).
echo   Slaat artefacten_handmatig over. Zonder pad: oefenhoek\bibliotheek.
echo   Pipeline roept dit lokaal aan. check_vsa_products.py op main streng.
echo.
echo WHEN
echo   Na .vsa-wijziging, of als Oefenen-knop / check een stale .vsa.mxl meldt.
echo.
echo SEE ALSO
echo   scripts\sync_vsa_products.py
echo   scripts\check_vsa_products.py
echo   scripts\oefenhoek-product-contract.md
echo.
goto end_ok

:man_capella_mxl
echo.
echo NAME
echo   scripts\capella-mxl-to-mscz.cmd
echo.
echo SYNOPSIS
echo   scripts\capella-mxl-to-mscz.cmd [bronmap] [doelmap] [--force] [--dry-run] [--limit N]
echo.
echo DESCRIPTION
echo   Kuist Capella/CapToMusic-.mxl recursief op en zet ze om naar
echo   standaard-layout .mscz. Submappen blijven behouden.
echo   Zonder paden:
echo     C:\Git\orthodox-ronl\ruwe-invoer\capella-backup-mxl
echo     C:\Git\orthodox-ronl\ruwe-invoer\capella-backup-mscz
echo.
echo   Hervatbaar: bestaande .mscz die niet ouder zijn dan de bron
echo   worden overgeslagen, tenzij --force. Log: doel\_batch-log.txt
echo   MuseScore 4 nodig; sluit MuseScore voor je start.
echo   Niet in check/build/serve. Geen PDF of Coria-.mxl.
echo.
echo OPTIONS
echo   --force       bestaande .mscz overschrijven
echo   --dry-run     alleen de planning tonen
echo   --limit N     stop na N conversies
echo   --batch-size  MuseScore-jobgrootte ^(default 10^)
echo.
echo WHEN
echo   Een hele Capella-MXL-input naar standaard-.mscz, buiten de oefenhoek.
echo.
echo SEE ALSO
echo   scripts\cleanup_capella_mxl.py
echo   scripts\apply_mscz_layout.py
echo   scripts\mscz-partituur-contract.md
echo   scripts\mscz-product-transforms.md
echo.
goto end_ok

:man_oefenhoek_index
echo.
echo NAME
echo   scripts\oefenhoek-index.cmd
echo   scripts\sync_oefenhoek_index.py
echo.
echo SYNOPSIS
echo   scripts\oefenhoek-index.cmd [--dry-run] [--svg] [--verbose]
echo.
echo DESCRIPTION
echo   Zonder flags: haalt auto-includes en score-shortcodes uit
echo   oefenhoek bladermap-index.md. Frontmatter en eigen tekst blijven.
echo   Catalogus-includes, bieb en automatische_inhoud: false
echo   blijven. Widgets komen uit de Hugo-layout of bieb.
echo.
echo   --svg schrijft SVG van lokale .vsa (geen basispartituur-.mscz; print-.mscz
echo   mag) naar static\vsa\bladermap\ (na vsa build-markdown), ook onder
echo   bibliotheek\.
echo   Standaard alleen een samenvatting; --verbose toont elk pad.
echo.
echo WHEN
echo   Automatisch in check/build/serve. Handmatig: alleen --svg na .vsa-edit
echo   zonder volle check, of --dry-run om te zien wat de strip zou doen.
echo.
echo SEE ALSO
echo   scripts\h.cmd check
echo   handleiding scripts\oefenhoek-index
echo   scripts\README.md
echo.
goto end_ok

:man_opkuisen
echo.
echo NAME
echo   scripts\opkuisen.cmd
echo   scripts\cleanup_capella_mxl.py
echo.
echo SYNOPSIS
echo   scripts\opkuisen.cmd ^<bron.mxl^> [-o doel.mxl^|doelmap]
echo.
echo DESCRIPTION
echo   Kuist Capella/CapToMusic-.mxl inhoudelijk op (lagen 1-3):
echo   reciteerkwarten, lettergrepen, titelrommel, lege maten, sleutels.
echo   Geen A4-layout (dat is layout.cmd). Niet in check/build/serve.
echo   -o naar _werk\STAM\STAM.mxl zonder spaties. Overschrijf nooit
echo   het Capella-origineel in input\capella\.
echo.
echo OPTIONS
echo   -o, --output   doel-.mxl of doelmap (default: in-place zonder spaties)
echo.
echo WHEN
echo   Elke nieuwe Capella-/CapToMusic-.mxl, voor layout.cmd.
echo.
echo SEE ALSO
echo   scripts\h.cmd layout
echo   handleiding scripts\opkuisen
echo   handleiding partituur\2-opkuisen
echo.
goto end_ok

:man_layout
echo.
echo NAME
echo   scripts\layout.cmd
echo   scripts\apply_mscz_layout.py
echo.
echo SYNOPSIS
echo   scripts\layout.cmd ^<bestand.mscz^|.mxl^> [-o doel.mscz] [--id ID] [--no-extenders]
echo.
echo DESCRIPTION
echo   Past de Oefenhoek-basispartituur-standaard toe (normaliseren / layouten):
echo   A4, fonts, reciteer-collaps, copyright, bibliotheek-id-colofon.
echo   .mxl: MuseScore-import + layout; zet -o. .mscz: default in-place.
echo   Weigert *.print.mscz. Idempotent. Niet in check (handmatig / producten).
echo.
echo OPTIONS
echo   -o, --output      doel-.mscz
echo   --id              bibliotheek-id (anders uit pad onder bibliotheek/)
echo   --no-extenders    geen lyric-underlines; meta vsaNoLyricExtenders
echo.
echo WHEN
echo   Na opkuisen, of opnieuw na editslag in MuseScore, voor mscz-products.
echo.
echo SEE ALSO
echo   scripts\h.cmd opkuisen
echo   scripts\h.cmd mscz-products
echo   handleiding scripts\layout
echo   scripts\mscz-partituur-contract.md
echo.
goto end_ok

:man_update_werkvoorraad
echo.
echo NAME
echo   scripts\update-werkvoorraad.cmd
echo   scripts\update_werkvoorraad.py
echo.
echo SYNOPSIS
echo   scripts\update-werkvoorraad.cmd
echo.
echo DESCRIPTION
echo   Vult de tabel in oefenhoek\input\werkvoorraad.md uit bestanden op schijf.
echo   Doel-id, koormap en notitie in bestaande rijen blijven. Verwijdert
echo   generated\...\oefenhoek\input zodat inputs geen Hugo-pagina's worden.
echo.
echo WHEN
echo   Automatisch in check/build/serve. Handmatig na nieuwe files in input/.
echo.
echo SEE ALSO
echo   scripts\h.cmd check
echo   handleiding scripts\update-werkvoorraad
echo   handleiding partituur\1-binnenhalen
echo.
goto end_ok

:man_bieb_accepteer
echo.
echo NAME
echo   scripts\bieb-accepteer.cmd
echo   scripts\bieb_accepteer.py
echo.
echo SYNOPSIS
echo   scripts\bieb-accepteer.cmd [id] [bestand...] [opties]
echo   python scripts\bieb_accepteer.py [id] [bestand...] ...
echo.
echo DESCRIPTION
echo   Neemt een basispartituur-.mscz, .vsa of .print.mscz op in
echo   oefenhoek\bibliotheek\zangstuk\variant\uitvoeringsvorm\.
echo   Maakt ontbrekende _index.md / index.md met bieb, hernoemt naar
echo   de publicatiestam. Weigert Capella-.capx e.d. en kale Capella-.mxl.
echo   Bij .vsa: vsa validate (tenzij --skip-vsa-validate).
echo   Default status: reviewable (stub: voorzien). Geen productie zonder
echo   --force. Niet in check/build/serve.
echo   Ontbrekende id of bestand: interactief gevraagd. Typ ? voor uitleg,
echo   daarna opnieuw invullen. Zonder argumenten: beide vragen.
echo.
echo OPTIONS
echo   --title --status --stub --move --force --dry-run
echo   --skip-vsa-validate --artefacten-handmatig
echo.
echo WHEN
echo   Als de partituur klaar is om in de bibliotheek te staan (na opkuisen
echo   / normaliseren of na een werkende .vsa). Daarna koormap + check.
echo.
echo SEE ALSO
echo   scripts\h.cmd bibliotheek
echo   handleiding publiceren/1-opnemen-in-bibliotheek
echo   handleiding scripts\bieb-accepteer
echo   layouts\shortcodes\bieb.html
echo.
goto end_ok

:man_migrate_bibliotheek
echo.
echo NAME
echo   scripts\migrate_oefenhoek_bibliotheek.py
echo   scripts\bibliotheek.py
echo.
echo SYNOPSIS
echo   python scripts\migrate_oefenhoek_bibliotheek.py
echo.
echo DESCRIPTION
echo   Eenmalig (historisch): verplaatste basispartituur-partituren van
echo   liturgiemap-hemelum naar oefenhoek\bibliotheek\... en zette
echo   koormap-slots op bieb. Nieuwe stukken: scripts\bieb-accepteer.cmd.
echo   bibliotheek.py: parse_id / folder / stem / leaf_folders / resolve_id.
echo   In check: python scripts\bibliotheek.py weigert alias-varianten met
echo   een uitvoeringsvorm-map; alias_van hoort op de variant-_index
echo   (zangstuk/canonieke-variant).
echo.
echo WHEN
echo   Alleen bij herhaalbare SCORE_MOVES-conversie; dagelijks werk via
echo   bieb-accepteer.
echo.
echo SEE ALSO
echo   scripts\h.cmd bieb-accepteer
echo   CONTENT-STRUCTURE.md
echo   layouts\shortcodes\bieb.html
echo   scripts\oefenhoek-ui-contract.md
echo.
goto end_ok

:man_help
echo.
echo NAME
echo   scripts\h.cmd
echo.
echo SYNOPSIS
echo   scripts\h.cmd
echo   scripts\h.cmd ^<naam^>
echo   scripts\h.cmd -h
echo.
echo DESCRIPTION
echo   Zonder argument: korte catalogus van alle .cmd-scripts.
echo   Met exacte scriptnaam: man-page ^(doel, opties, wanneer^).
echo   Met onbekende/partiele tekst: gefilterde korte lijst, of foutmelding.
echo.
echo EXAMPLES
echo   scripts\h.cmd
echo   scripts\h.cmd bootstrap
echo   scripts\h.cmd check
echo.
echo SEE ALSO
echo   scripts\README.md  ^(begrippen, pipeline, CI-spiegel^)
echo.
goto end_ok

:end_ok
endlocal
exit /b 0

:end_fail
endlocal
exit /b 1
