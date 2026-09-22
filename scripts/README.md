# Scripts (VSA-demo)

Org-conventie: https://github.com/orthodox-ronl/bron/blob/main/docs/specs/repo-scripts.md

Foutmeldingen (scripts + Hugo): betekenisvol voor wie het script runt; bij voorkeur
`pad:regel:kolom`, korte uitleg en een `Oplossing:`/`Hint:`-regel; fouten opsparen
zodat je ze in één run ziet. VSA-notatie: zie
https://github.com/orthodox-ronl/VSA-tooling/blob/main/docs/specification/error-handling.md
(helper: `scripts/_diag.py`).

`.\scripts` op PATH; Python 3.14; Hugo Extended 0.160.1; `vsa` op PATH.
Geen bootstrap-stap: `_ensure` checkt PATH en pip't catalogus/`vsa-tool`.

| Commando | Doel | Opties |
| -------- | ---- | ------ |
| `h` | catalogus / man-page | `[naam]` |
| `check` | preflight / CI-spiegel | `--strict --external --skip-hugo` |
| `serve` | Hugo-preview op http://127.0.0.1:18731/ (niet 1313) | `--no-build` |
| `build` | site in `generated\site` + interne links | — |
| `pdf` | Markdown + VSA naar A4-PDF | `-o --content-root` |
| `demo-pdf` | demo-PDF `voorbeeld-blad.pdf` bouwen | — |
| `sync-bron-zondagen` | zondag-VSA uit bron | `[bron-root]` |
| `opkuisen` | Herkomstanalyse + inhoudelijke opkuis (MusicXML/MuseScore; optioneel `--layout`) | `<pad> [--analyze\|--dry-run] [-o] [--layout]` |
| `layout` | basispartituur-standaard op `.mscz`/`.mxl` | `<pad> [-o] [--id]` |
| `mscz-products` | PDF + Coria-`.mxl` uit basispartituur-`.mscz` (niet `*.print.mscz`) | `[pad] --force --dry-run` |
| `vsa-products` | Coria-`.vsa.mxl` uit bibliotheek-`.vsa` | `[pad] --force --dry-run` |
| `ensure-bibliotheek-id` | bibliotheek-id in `.mscz` colofon/meta | `[root]` |
| `update-werkvoorraad` | werkvoorraad-tabel uit `input/` | — |
| `oefenhoek-index` | bladermap-index strippen; optioneel SVG | `[--svg --dry-run --verbose]` |
| `capella-mxl-to-mscz` | Capella-`.mxl` map -> standaard-`.mscz` | `[bron] [doel] --force --dry-run --limit` |
| `bieb-accepteer` | Partituur opnemen in `oefenhoek/bibliotheek/` | `<id> <bestand> [--dry-run --force --stub]` |

Uitgebreide man-pages (Hugo): `content-source/praktijk/handleiding/scripts/`.
Console: `scripts\h.cmd <naam>`.

`opkuisen.cmd` (`opkuisen.py`) analyseert de herkomst (Capella, generiek
MusicXML, MuseScore, VSA) en past de bijbehorende inhoudsfixes toe.
Default = content (geen A4). `--analyze` en `--dry-run` zijn synoniemen
(geen schrijven). `--layout` voegt normaliseren toe. Niet in `check`.
Lange man-page: `content-source/praktijk/handleiding/scripts/opkuisen.md`
en `scripts\h.cmd opkuisen`. Compat: `cleanup_capella_mxl.py` roept
`opkuisen --assume capella` aan. Tests: `scripts\test_opkuisen.py`.

`capella-mxl-to-mscz.cmd` (`batch_capella_mxl_to_mscz.py`) kuist een map
Capella-`.mxl` (recursief) op en schrijft standaard-`.mscz` ernaast in de
doelmap, met dezelfde submappen. Default: `ruwe-invoer\capella-backup-mxl`
-> `ruwe-invoer\capella-backup-mscz`. Bestandsnamen zonder spaties;
bestaande verse `.mscz` worden overgeslagen (hervatten). MuseScore 4
nodig, en niet open tijdens de run. Niet in `check`. Geen PDF/Coria.

`layout.cmd` (`apply_mscz_layout.py`) normaliseert de **basispartituur-`.mscz`** (A4-layout, lettergrepen,
reciteer-collaps `||O||`, tempo, copyright, twee-balks G/F-sleutels via
`staff_clefs.py`). Accepteert ook opgekuiste `.mxl`.
Weigert `*.print.mscz` (print-/koormap-vel buiten de basispartituur-spoor).
Copyright: bronnotice of default CC BY-SA 4.0 + eredienst-zin.
In de bibliotheek: colofonregel `Bibliotheek-id:` + meta `vsaBibliotheekId`
(optioneel `--id=`). Contract: `scripts/mscz-partituur-contract.md`.
Hyphenatie: `scripts/nl_hyphen.py`. Transforms: `scripts/mscz-product-transforms.md`.

`ensure-bibliotheek-id.cmd` (`ensure_bibliotheek_id.py`) zet ontbrekende/verkeerde bibliotheek-id’s in
basispartituur-`.mscz` onder `bibliotheek/` (lokaal; CI alleen check).
`check_bibliotheek_id.py` faalt op `main` / `--strict` als meta of colofon
niet klopt. Daarna `mscz-products` voor verse PDF’s.

`mscz-products.cmd` (`sync_mscz_products.py`) exporteert sibling-PDF en
Coria-`.mxl` voor basispartituur-`.mscz` (sla `*.print.mscz` over) en schrijft provenance
(`partituur-sha256`, `generated-at`). Pipeline roept dit lokaal aan.
`check_partituur_products.py` schrijft `data/partituur-product-status.json` (Hugo-banner);
op `main` falen bij mismatch. Print-velden tellen niet mee in die gate.

`vsa-products.cmd` (`sync_vsa_products.py`) maakt `{stam}.vsa.mxl` uit
bibliotheek-`.vsa` (syllabify in temp-bestand, `vsa musicxml` playback,
Coria-sanitize + `vsa-source-sha256` van de canonieke `.vsa`). Slaat
`*.syl.vsa`-sidecars over. Slaat
`artefacten_handmatig` over. Pipeline lokaal; `check_vsa_products.py` →
`data/vsa-product-status.json` (banner; `main` streng). Zie
`oefenhoek-product-contract.md`.

Drie Oefenhoek-sporen: basispartituur; VSA; print-`.mscz` (handleiding
`partituur/7-print-mscz`). Afgeleiden per representatie-id en handmatige
artefacten: `oefenhoek-product-contract.md` (`{stam}.partituur.mxl` /
`{stam}.vsa.mxl` / …; frontmatter `artefacten_handmatig`).
Pagina-UI (sticky header, bibliotheek-id op leaves, shortcode `bieb`,
actieknoppen): `oefenhoek-ui-contract.md`.
Bibliotheek-id in eindproducten (colofon): `oefenhoek-product-contract.md`.
`export_mscz_coria_mxl.py` maakt van zo'n layout-`.mscz` een playback-`.mxl`
voor Coria (MuseScore-CLI-export vanaf een temp-kopie zodat de canonieke
`.mscz` niet wordt herschreven; SATB naar vier parts, geen DOCTYPE,
MusicXML 3.1, geen `movement-title`, sectie-pickups weg, `[PAUZE]` na
dubbele streep, kwart-rust na cesuur, BPM-markers als `sound tempo` op
alle parts, daarna Coria-veilige markup, daarna `<accidental>` waar de
klinkende toon afwijkt van de voortekening). Coria speelt via NWC-voortekening
plus toonvoorteken, niet via MusicXML `alter`. Een map mag: recursief, `input\`
overslaan. Uitvoernamen zonder spaties. `--sanitize-mxl` kuist bestaande
publicatie-`.mxl` in-place (geen MuseScore), en na `vsa musicxml` ook
`static\vsa\mxl`. Standaard alleen een samenvatting; `--verbose` toont
detail per bestand. `check_coria_mxl.py` (in `check`) weigert publicatie-`.mxl`
met markup waar Coria `translation failed` op geeft.

`patch_oefenhoek_8-trisagion.py` is een inhoudelijke patch op de twee
8-trisagion-`.mscz` (herhaling m1-m4, noten 'O Heilige God' uit Slavisch maat 5,
transliteratie als 2e couplet). Daarna `apply_mscz_layout.py`. Niet in `check`.

`rebar_20d_4kwart.py` maakt een *apart* `.mscz` van 20d-in-waarheid
(opmaat 1 tel, daarna 4/4, geen zichtbare maatsoort, geen lyric-underlines).
Het origineel blijft staan. Roept `apply_mscz_layout.py --no-extenders` aan.
Niet in `check`.

`apply_mscz_layout.py --no-extenders` slaat lyric-`ticks` (underlines) over en
zet meta `vsaNoLyricExtenders`, zodat een volgende layout-run ze niet
terugzet.
Generate kopieert extra page-bundle bestanden (`.mxl`) via
`copy_content_extras.py` (niet `oefenhoek/input/`; fout bij spaties in de
naam). `fingerprint_coria_mxl.py` leest page-bundle-`.mxl` uit
`content-source` (niet `oefenhoek/input/`) plus `static/vsa/mxl`, en
publiceert uncompressed MusicXML als `/mxl/c/<hash>.musicxml` (URL eindigt
op `.musicxml`, geen spaties of query-string; compressed `.mxl` laat Coria
op sommige stukken falen). Oefenen-knoppen gebruiken die fingerprint via
een **absolute** `raw.githubusercontent.com`-URL op branch `gh-pages`
(`https://raw.githubusercontent.com/orthodox-ronl/VSA-demo/gh-pages/…/mxl/c/<hash>.musicxml`),
niet `github.io` (Coria `failed to retrieve file`), niet `absURL` met lokale
`baseURL=/` en niet een Hugo-`RelPermalink` (pad-only of verdubbelde prefix).
`fingerprint_coria_mxl.py` schrijft die fetch-root in
`data/coria-public-base.json` (zelfde mappen als `pages.yml`: root / `preview` / slug).
`check_hugo_links_and_assets.py` eist die URL en weigert `github.io`.
`check_coria_retrieve.py` (na Pages-deploy, niet in lokale `check`) opent een
steekproef `play_from_url` en faalt op `failed to retrieve file`.
Unit-tests: `test_check_hugo_links_and_assets.py`,
`test_fingerprint_coria_mxl.py`, `test_check_coria_retrieve.py`,
`test_opkuisen.py`
(in `check` / `build` / `serve`).
`check_publicatiestatus.py` (in `check`) eist `publicatiestatus` en
`automatische_inhoud` (`true` / `false`) op elke oefenhoek-`_index.md` /
`index.md` (niet `input/`). Status: `voorzien`, `concept`, `reviewable` of
`productie`.
`update-werkvoorraad.cmd` (`update_werkvoorraad.py`) (in `check` / `build` / `serve`) vult de tabel in
`oefenhoek/input/werkvoorraad.md` en verwijdert `generated/.../oefenhoek/input`
zodat inputs geen Hugo-pagina's worden. Doel-id: bibliotheek-id
(`zangstuk/variant/uitvoeringsvorm`) wanneer bekend; oude bladermap-namen
worden genormaliseerd.
`bibliotheek.py` — pad/id-hulp voor `oefenhoek/bibliotheek/` (drie lagen) en
check van alias-varianten (`alias_van` op de variant-`_index`; geen
uitvoeringsvorm-bestanden). Draait in `check` / `build` / `serve`.
`bieb-accepteer.cmd` (`bieb_accepteer.py`) neemt een basispartituur-`.mscz`, `.vsa` of
`.print.mscz` (optioneel sibling-`.pdf`/`.mxl`) op onder een bibliotheek-id:
maakt sectie-`_index.md` en leaf-`index.md` met `bieb`, hernoemt naar de
publicatiestam. Ontbrekende id/bestand worden interactief gevraagd; typ `?`
voor uitleg. Weigert Capella-bronformats en een kale `.mxl` zonder score.
Bij `.vsa`: `vsa validate`. Default `publicatiestatus: reviewable`
(`voorzien` bij `--stub`). Niet in `check`. Handleiding:
`publiceren/1-opnemen-in-bibliotheek`. Tests: `test_bieb_accepteer.py`,
`test_sync_vsa_products.py`.
`migrate_oefenhoek_bibliotheek.py` — eenmalig liturgiemap -> bibliotheek
(historisch; nieuwe stukken via `bieb-accepteer`; niet in check).
`oefenhoek-index.cmd` (`sync_oefenhoek_index.py`) (in `check` / `build` / `serve`): haalt auto-includes
en score-shortcodes uit bladermap-`index.md` (eigen tekst blijft). Pagina's met
`bieb` of `automatische_inhoud: false` blijven onaangeroerd. De
partituur komt uit de Hugo-layout (`layouts/partials/bladermap-score.html`) of
uit `{{< bieb >}}`. Sectie-pagina's krijgen een linklijst van
kinderen (`oefenhoek-kinderen.html`) als `automatische_inhoud: true`; bij 1
kind volgt een doorverwijzing. Catalogus-includes
(`id:` / `lokaal:` / `bron:`) blijven. `--svg` (na `build-markdown`) zet
lokale `.vsa` zonder basispartituur-`.mscz` om naar `static/vsa/bladermap/` (ook onder
`bibliotheek/`; `*.print.mscz` blokkeert SVG niet). Standaard alleen een
samenvatting; `--verbose` toont elk SVG- of strip-pad. `--dry-run` toont wat de
strip zou wijzigen.
In `check` / `build` / `serve` blijft de console bij stapvoortgang +
samenvattingen (geen bestandslijsten); detail via `--verbose` op die scripts.
Groen voor commit: `check --strict`. Daarna `serve --no-build`.

Oude namen `serve-hugo` / `build-hugo` / `bootstrap` zijn aliases (`use: ...`).

Echo in `.cmd`: eenvoudige ASCII.
