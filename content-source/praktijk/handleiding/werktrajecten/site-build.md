---
title: "Site-build"
linkTitle: "Site-build"
weight: 50
---

# Site-build

Dit werktraject zet `content-source` om naar een browsbare site:
lokaal onder `generated\site`, of op GitHub Pages na een push.

{{< cue >}}
Vóór commit:
```cmd
scripts\check.cmd --strict
```
Lokale preview (als check al groen was):
```cmd
scripts\serve.cmd --no-build
```
Open http://127.0.0.1:18731/ — **niet** poort 1313.
{{< /cue >}}

## Waartoe

Koorleden en jij zien markdown, SVG’s, PDF’s en knoppen pas nadat de
site is gebouwd. Dit traject is de gemeenschappelijke keten achter
`check`, `build`, `serve` en de GitHub-workflows.

## Eindresultaat en criteria

| Output | Rol |
| --- | --- |
| `generated\content` | Markdown na `vsa build-markdown` |
| `static\vsa\` (o.a. `bladermap\`) | SVG-plaatjes |
| `static\vsa\mxl\` | Embed-Coria (niet bibliotheek-`{stam}.vsa.mxl`) |
| `generated\site` | Hugo-site |
| GitHub Pages | Productie / preview / branch-URL |

**Klaar** als: `scripts\check.cmd --strict` groen is; lokaal opent de
preview zonder kapotte links; na push is de juiste Pages-URL bijgewerkt.

| Branch | URL |
| --- | --- |
| `main` | https://orthodox-ronl.github.io/VSA-demo/ |
| `development` | https://orthodox-ronl.github.io/VSA-demo/preview/ |
| andere | https://orthodox-ronl.github.io/VSA-demo/{slug}/ |

## Wanneer wel / wanneer niet

| Wel | Niet |
| --- | --- |
| Na wijzigingen in content of producten, vóór commit | Alleen een Capella-bestand opkuisen zonder de site te willen zien |
| Lokale preview of PR-controle | Poort 1313 gebruiken (die is lokaal gereserveerd) |

## Volgorde (bestanden)

De gedeelde keten zit in `scripts\_pipeline.cmd` (wrappers:
`check.cmd`, `build.cmd`, `serve.cmd`):

```text
content-source
    |
    +-- sync bron-zondagen, validate, bibliotheek-checks
    +-- ensure bibliotheek-id; sync basispartituur-producten; sync VSA-producten
    |
    +-- vsa build-markdown  ->  generated/content + static/vsa
    +-- oefenhoek-index --svg  ->  static/vsa/bladermap/...
    +-- vsa musicxml  ->  static/vsa/mxl
    +-- copy extras, fingerprint Coria, build stamp
    +-- gates: partituur-producten, bibliotheek-id, VSA-producten, demo-PDF
    |
    +-- Hugo  ->  generated/site
    +-- interne linkcheck (+ optioneel externe links)
```

Bibliotheek-**Oefenen** voor `.vsa` gebruikt sibling `{stam}.vsa.mxl` in
de bladermap. Embed-MXL onder `static\vsa\mxl\` is een apart spoor — zie
[Ingebedde VSA](../ingebedde-vsa/).

## Automatisch (CI)

| Workflow | Wanneer | Wat |
| --- | --- | --- |
| `validate.yml` | pull request | Zelfde soort validatie + Hugo-build **zonder** deploy |
| `pages.yml` | push (niet `gh-pages`) | Build + deploy naar branch `gh-pages` |

CI doet **geen** MuseScore-`mscz-products`. Wel gates op partituur- en
VSA-producten en versheid van de demo-PDF. Producten die lokaal moeten
worden vernieuwd, commit je mee — anders faalt CI.

## Handmatig

| Situatie | Commando | Man-page |
| --- | --- | --- |
| Preflight / CI-spiegel vóór commit | `scripts\check.cmd --strict` | [check](../../scripts/check/) |
| Alleen site naar `generated\site` | `scripts\build.cmd` | [build](../../scripts/build/) |
| Preview-server | `scripts\serve.cmd` of `serve --no-build` | [serve](../../scripts/serve/) |

Detailflags: `scripts\h.cmd check` (en `build` / `serve`) in het
opdrachtvenster.

## Zie ook

- [Status en check](../../publiceren/2-status-en-check/)
- [Als het misgaat](../../publiceren/3-als-het-misgaat/)
- AGENTS.md / CONTRIBUTING: groen vóór commit = `check --strict`

{{< navbuttons "Print-vel|/praktijk/handleiding/werktrajecten/print-vel/" "Markdown naar PDF|/praktijk/handleiding/werktrajecten/markdown-naar-pdf/" >}}
