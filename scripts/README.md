# Scripts (VSA-demo)

Org-conventie: https://github.com/orthodox-ronl/bron/blob/main/docs/specs/repo-scripts.md

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
| `mscz-products` | PDF + Coria-`.mxl` uit hub-`.mscz` (niet `*.print.mscz`) | `[pad] --force --dry-run` |
| `capella-mxl-to-mscz` | Capella-`.mxl` map -> standaard-`.mscz` | `[bron] [doel] --force --dry-run --limit` |

`cleanup_capella_mxl.py` is een proef om Capella/CapToMusic-`.mxl` inhoudelijk
op te kuisen (reciteerkwarten, lettergrepen per noot, titel, lege maten,
lyrics tussen de balken; geen lyric-underline onder Capella-slurs). Geen
MuseScore-stijl tot op de pixel. Niet in `check`.
`-o` schrijft naar een naam zonder spaties; in-place op een naam mét spaties
wordt geweigerd. Ruwe Capella-inputs blijven in `oefenhoek/input/`.

`capella-mxl-to-mscz.cmd` (`batch_capella_mxl_to_mscz.py`) kuist een map
Capella-`.mxl` (recursief) op en schrijft standaard-`.mscz` ernaast in de
doelmap, met dezelfde submappen. Default: `ruwe-invoer\capella-backup-mxl`
-> `ruwe-invoer\capella-backup-mscz`. Bestandsnamen zonder spaties;
bestaande verse `.mscz` worden overgeslagen (hervatten). MuseScore 4
nodig, en niet open tijdens de run. Niet in `check`. Geen PDF/Coria.

`apply_mscz_layout.py` normaliseert de **hub-`.mscz`** (A4-layout, lettergrepen,
reciteer-collaps `||O||`, tempo, copyright). Accepteert ook opgekuiste `.mxl`.
Weigert `*.print.mscz` (print-/koormap-vel buiten de hub-straat).
Copyright: bronnotice of default CC BY-SA 4.0 + eredienst-zin.
Contract: `scripts/mscz-hub-contract.md`. Hyphenatie: `scripts/nl_hyphen.py`.
Transforms: `scripts/mscz-product-transforms.md`.

`mscz-products.cmd` (`sync_mscz_products.py`) exporteert sibling-PDF en
Coria-`.mxl` voor hub-`.mscz` (sla `*.print.mscz` over) en schrijft provenance
(`hub-sha256`, `generated-at`). Pipeline roept dit lokaal aan.
`check_hub_products.py` schrijft `data/hub-product-status.json` (Hugo-banner);
op `main` falen bij mismatch. Print-velden tellen niet mee in die gate.

Drie Oefenhoek-sporen: hub-partituur; VSA; print-`.mscz` (handleiding
`partituur/7-print-mscz`).
`export_mscz_coria_mxl.py` maakt van zo'n layout-`.mscz` een playback-`.mxl`
voor Coria (MuseScore-CLI-export, SATB naar vier parts, geen DOCTYPE,
MusicXML 3.1, geen `movement-title`, sectie-pickups weg, `[PAUZE]` na
dubbele streep, kwart-rust na cesuur, BPM-markers als `sound tempo` op
alle parts, daarna Coria-veilige markup, daarna `<accidental>` waar de
klinkende toon afwijkt van de voortekening). Coria speelt via NWC-voortekening
plus toonvoorteken, niet via MusicXML `alter`. Een map mag: recursief, `input\`
overslaan. Uitvoernamen zonder spaties. `--sanitize-mxl` kuist bestaande
publicatie-`.mxl` in-place (geen MuseScore), en na `vsa musicxml` ook
`static\vsa\mxl`. `check_coria_mxl.py` (in `check`) weigert publicatie-`.mxl`
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
op sommige stukken falen). Oefenen-knoppen moeten die fingerprint-sleutel
gebruiken (`mxl/<content-pad>/<bestand>`), niet een Hugo-`RelPermalink`
(die verdubbelt de GitHub Pages-baseURL → Coria `failed to retrieve file`).
`check_publicatiestatus.py` (in `check`) eist `publicatiestatus` en
`automatische_inhoud` (`true` / `false`) op elke oefenhoek-`_index.md` /
`index.md` (niet `input/`). Status: `voorzien`, `concept`, `reviewable` of
`productie`.
`update_werkvoorraad.py` (in `check` / `build` / `serve`) vult de tabel in
`oefenhoek/input/werkvoorraad.md` en verwijdert `generated/.../oefenhoek/input`
zodat inputs geen Hugo-pagina's worden. Doel-id: bibliotheek-id
(`zangstuk/variant/uitvoeringsvorm`) wanneer bekend; oude bladermap-namen
worden genormaliseerd.
`bibliotheek.py` — pad/id-hulp voor `oefenhoek/bibliotheek/` (drie lagen).
`migrate_oefenhoek_bibliotheek.py` — eenmalig liturgiemap -> bibliotheek (niet
in check; zie CONTENT-STRUCTURE.md).
`sync_oefenhoek_index.py` (in `check` / `build` / `serve`): haalt auto-includes
en score-shortcodes uit bladermap-`index.md` (eigen tekst blijft). Pagina's met
`bibliotheek-score` of `automatische_inhoud: false` blijven onaangeroerd. De
partituur komt uit de Hugo-layout (`layouts/partials/bladermap-score.html`) of
uit `{{< bibliotheek-score >}}`. Sectie-pagina's krijgen een linklijst van
kinderen (`oefenhoek-kinderen.html`) als `automatische_inhoud: true`; bij 1
kind volgt een doorverwijzing. Catalogus-includes
(`id:` / `lokaal:` / `bron:`) blijven. `--svg` (na `build-markdown`) zet
lokale `.vsa` zonder `.mscz` om naar `static/vsa/bladermap/` (ook onder
`bibliotheek/`). `--dry-run` toont wat de strip zou wijzigen.

Groen voor commit: `check --strict`. Daarna `serve --no-build`.

Oude namen `serve-hugo` / `build-hugo` / `bootstrap` zijn aliases (`use: ...`).

Echo in `.cmd`: eenvoudige ASCII.
