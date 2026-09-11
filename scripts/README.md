# Scripts (VSA-demo)

Org-conventie: https://github.com/orthodox-ronl/bron/blob/main/docs/specs/repo-scripts.md

`.\scripts` op PATH; Python 3.14; Hugo Extended 0.160.1; `vsa` op PATH.
Geen bootstrap-stap: `_ensure` checkt PATH en pip't catalogus/`vsa-tool`.

| Commando | Doel | Opties |
| -------- | ---- | ------ |
| `h` | catalogus / man-page | `[naam]` |
| `check` | preflight / CI-spiegel | `--strict --external --skip-hugo` |
| `serve` | Hugo-preview | `--no-build` |
| `build` | site in `generated\site` + interne links | — |
| `pdf` | Markdown + VSA naar A4-PDF | `-o --content-root` |
| `demo-pdf` | demo-PDF `voorbeeld-blad.pdf` bouwen | — |
| `sync-bron-zondagen` | zondag-VSA uit bron | `[bron-root]` |

`cleanup_capella_mxl.py` is een proef om Capella/CapToMusic-`.mxl` inhoudelijk
op te kuisen (reciteerkwarten, lettergrepen per noot, titel, lege maten,
lyrics tussen de balken; geen lyric-underline onder Capella-slurs). Geen
MuseScore-stijl tot op de pixel. Niet in `check`.
`-o` schrijft naar een naam zonder spaties; in-place op een naam mét spaties
wordt geweigerd. Ruwe Capella-dumps blijven in `oefenhoek/input/`.

`apply_mscz_layout.py` is de proef voor laag 4: A4-standaard-layout op een
`.mscz` (idempotent). Accepteert ook opgekuiste `.mxl` (MuseScore-import).
Contract: `scripts/mscz-layout-contract.md`. Niet in
`check`. Later verhuizen naar VSA-tooling.

`export_mscz_coria_mxl.py` maakt van zo'n layout-`.mscz` een playback-`.mxl`
voor Coria (MuseScore-CLI-export, SATB naar vier parts, geen DOCTYPE,
sectie-pickups weg, `[PAUZE]` na dubbele streep, kwart-rust na cesuur,
BPM-markers als `sound tempo` op alle parts). Een map mag: recursief,
`input\` overslaan. Niet in `check`. Uitvoernamen zonder spaties.

`patch_oefenhoek_trisagion.py` is een inhoudelijke patch op de twee
trisagion-`.mscz` (herhaling m1-m4, noten 'O Heilige God' uit Slavisch maat 5,
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
naam). `fingerprint_coria_mxl.py` publiceert Coria-MXL
als `/mxl/c/<hash>.mxl` (URL eindigt altijd op `.mxl`, geen spaties of
query-string; Coria weigert anders het bestand).

Groen voor commit: `check --strict`. Daarna `serve --no-build`.

Oude namen `serve-hugo` / `build-hugo` / `bootstrap` zijn aliases (`use: ...`).

Echo in `.cmd`: eenvoudige ASCII.
