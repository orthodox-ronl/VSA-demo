---
title: "Script-referentie"
linkTitle: "Scripts"
weight: 50
hide_page_list: true
---

# Script-referentie (man-pages)

Deze sectie is de **uitgebreide man-page** voor elk Windows-commando
(`.cmd`) dat je als beheerder in het opdrachtvenster plakt. De
workflowpagina’s (partituur, publiceren, VSA) leggen *wanneer* je iets doet;
hier staat *hoe* elk commando werkt: synopsis, opties, voorbeelden.

## Twee hulpbronnen

| Waar | Wat |
| --- | --- |
| Deze pagina’s | Uitgebreide uitleg, voorbeelden, links naar workflows |
| `scripts\h.cmd` in het opdrachtvenster | Korte catalogus; `h <naam>` voor een snelle man-page in de console |

Zet `.\scripts` op je PATH (dat doet `check` via `_ensure`), of roep altijd
`scripts\<naam>.cmd` aan vanuit de repository-map `VSA-demo`.

## Catalogus

| Commando | Kort | Man-page |
| --- | --- | --- |
| `h` | Catalogus / console-man | [h](h/) |
| `check` | Preflight / CI-spiegel | [check](check/) |
| `build` | Volledige sitebuild | [build](build/) |
| `serve` | Lokale Hugo-preview | [serve](serve/) |
| `pdf` | Markdown + VSA → A4-PDF | [pdf](pdf/) |
| `demo-pdf` | Demo-PDF bouwen | [demo-pdf](demo-pdf/) |
| `sync-bron-zondagen` | Zondag-VSA uit bron | [sync-bron-zondagen](sync-bron-zondagen/) |
| `opkuisen` | Capella-`.mxl` opkuisen | [opkuisen](opkuisen/) |
| `layout` | Basispartituur normaliseren | [layout](layout/) |
| `mscz-products` | PDF + Coria uit `.mscz` | [mscz-products](mscz-products/) |
| `vsa-products` | Coria uit bibliotheek-`.vsa` | [vsa-products](vsa-products/) |
| `ensure-bibliotheek-id` | Id in colofon/meta | [ensure-bibliotheek-id](ensure-bibliotheek-id/) |
| `update-werkvoorraad` | Werkvoorraad-tabel | [update-werkvoorraad](update-werkvoorraad/) |
| `oefenhoek-index` | Index strippen / SVG | [oefenhoek-index](oefenhoek-index/) |
| `capella-mxl-to-mscz` | Bulk Capella → `.mscz` | [capella-mxl-to-mscz](capella-mxl-to-mscz/) |
| `bieb-accepteer` | Opnemen in bibliotheek | [bieb-accepteer](bieb-accepteer/) |

Begrippen en pipeline: bestand `scripts\README.md` in de repository-map
`VSA-demo` (niet als pagina op deze site).

{{< navbuttons "Opkuisen|/praktijk/handleiding/scripts/opkuisen/" >}}
