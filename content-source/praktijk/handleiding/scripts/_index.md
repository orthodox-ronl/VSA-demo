---
title: "Script-referentie"
linkTitle: "Scripts"
weight: 50
hide_page_list: true
---

# Script-referentie (man-pages)

Deze sectie beschrijft elk Windows-commando (`.cmd`) dat je als beheerder
in het opdrachtvenster plakt. De workflowpagina’s (partituur, publiceren,
VSA) leggen uit *wanneer* je een stap doet. Hier staat *wat* elk commando
doet, *van welke bestanden*, *naar welk resultaat*, en *waartoe*.

## Twee hulpbronnen

| Waar | Wat |
| --- | --- |
| Deze pagina’s | Uitgebreide uitleg in gewone taal, met voorbeelden en links naar workflows |
| `scripts\h.cmd` in het opdrachtvenster | Korte catalogus in de console; `h <naam>` voor een snelle man-page |

Zet `.\scripts` op je PATH (dat doet `check` via `_ensure`), of roep altijd
`scripts\<naam>.cmd` aan vanuit de repository-map `VSA-demo`.

## Catalogus

| Commando | Wat het doet | Man-page |
| --- | --- | --- |
| `h` | Toont een lijst van bekende commando’s in het opdrachtvenster, of een korte man-page voor één naam. Handig als je even niet weet welke `.cmd` je nodig hebt. | [h](h/) |
| `check` | Controleert of je repository-map `VSA-demo` klaar is om te committen: zelfde soort controles als op GitHub, plus optioneel een lokale sitebuild. Gebruik dit vóór je wijzigingen deelt. | [check](check/) |
| `build` | Bouwt de hele website naar de map `generated\site` op je pc, zonder een preview-server te starten. | [build](build/) |
| `serve` | Start een lokale preview van de site in je browser op http://127.0.0.1:18731/ (niet poort 1313). | [serve](serve/) |
| `pdf` | Maakt van één Markdownbestand (met eventuele VSA-blokken) een A4-PDF die je kiest. Voor willekeurige bladen; vaste demopaden → `demo-pdf`. | [pdf](pdf/) |
| `demo-pdf` | Vernieuwt het vaste demoblad-PDF `static\demo\voorbeeld-blad.pdf` uit de bron `content-source\praktijk\demo\assets\voorbeeld-blad.md`. Die PDF hoort bij de Tooling Demo «Markdown naar PDF»; `check` faalt als die PDF ouder is dan die bronnen. | [demo-pdf](demo-pdf/) |
| `sync-bron-zondagen` | Kopieert zondag-tropaar/kondak-bestanden (`.vsa` en bijbehorende plaatjes) uit de sibling-map `bron` naar `content-source\praktijk\zondagen\`, zodat de demo synchroon blijft met canonieke bron. | [sync-bron-zondagen](sync-bron-zondagen/) |
| `opkuisen` | Schoon een Capella- of CapToMusic-`.mxl` inhoudelijk op (noten, lettergrepen, titelrommel) en schrijft een schone `.mxl` — meestal naar `oefenhoek\input\_werk\`. Geen A4-layout en geen PDF. | [opkuisen](opkuisen/) |
| `layout` | Past de Oefenhoek-basispartituur-standaard toe op een `.mscz` of opgekuiste `.mxl` (A4, fonts, reciteertoon, copyright). Resultaat: een genormaliseerde basispartituur-`.mscz`. | [layout](layout/) |
| `mscz-products` | Maakt naast een basispartituur-`.mscz` de sibling-PDF en Coria-`.mxl` die koorleden downloaden of afspelen. | [mscz-products](mscz-products/) |
| `vsa-products` | Maakt naast een bibliotheek-`.vsa` het Coria-bestand `{stam}.vsa.mxl` voor de Oefenen-knop. | [vsa-products](vsa-products/) |
| `ensure-bibliotheek-id` | Zet of herstelt de regel «Bibliotheek-id: …» in colofon en metadata van basispartituur-`.mscz` onder `oefenhoek\bibliotheek\`, zodat die id overeenkomt met de map. | [ensure-bibliotheek-id](ensure-bibliotheek-id/) |
| `update-werkvoorraad` | Werkt de tabel in `oefenhoek\input\werkvoorraad.md` bij aan de hand van bestanden die in `input\` liggen (nieuwe rijen; bestaande doel-ids blijven). | [update-werkvoorraad](update-werkvoorraad/) |
| `oefenhoek-index` | Ruimt automatische shortcodes uit bladermap-`index.md` op, of schrijft met `--svg` plaatjes van bibliotheek-`.vsa` naar `static\vsa\bladermap\`. Meestal al onderdeel van `check`. | [oefenhoek-index](oefenhoek-index/) |
| `capella-mxl-to-mscz` | Verwerkt een hele map Capella-`.mxl` (recursief) tot standaard-layout `.mscz` — bulk buiten de één-voor-één oefenhoek-flow. | [capella-mxl-to-mscz](capella-mxl-to-mscz/) |
| `bieb-accepteer` | Neemt een klaar `.mscz`, `.vsa` of `.print.mscz` op in `oefenhoek\bibliotheek\` onder een bibliotheek-id (mappen + `index.md` met shortcode `bieb`). | [bieb-accepteer](bieb-accepteer/) |

Begrippen en pipeline: [Werktrajecten](../werktrajecten/); bestand
`scripts\README.md` in de repository-map `VSA-demo` (niet als pagina op
deze site).

{{< navbuttons "Werktrajecten|/praktijk/handleiding/werktrajecten/" "Opkuisen|/praktijk/handleiding/scripts/opkuisen/" >}}
