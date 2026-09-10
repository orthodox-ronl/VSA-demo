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
op te kuisen (reciteerkwarten, lettergrepen, titel, lege maten, lyrics tussen
de balken). Geen MuseScore-stijl tot op de pixel. Niet in `check`.

Generate kopieert extra page-bundle bestanden (`.mxl`) via
`copy_content_extras.py`. `fingerprint_coria_mxl.py` zet dezelfde MXL onder
`/mxl/c/<hash>/…` (URL eindigt op `.mxl`), zodat Coria verse tekst laadt
zonder query-string.

Groen voor commit: `check --strict`. Daarna `serve --no-build`.

Oude namen `serve-hugo` / `build-hugo` / `bootstrap` zijn aliases (`use: ...`).

Echo in `.cmd`: eenvoudige ASCII.
