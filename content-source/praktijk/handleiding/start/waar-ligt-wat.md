---
title: "Waar ligt wat"
linkTitle: "Waar ligt wat"
weight: 20
---

# Waar ligt wat

{{< cue >}}
- Dump: `oefenhoek\input\<herkomst>\` (originele bestandsnaam mag spaties hebben)
- Tussenwerk: `oefenhoek\input\_werk\<doel-id>\` (alleen op jouw pc, niet in git)
- Wat koorleden zien: `oefenhoek\<deelrubriek>\<doel-id>\` — **geen spaties** in bestandsnamen
- Register: `oefenhoek\input\werkvoorraad.md`
{{< /cue >}}

**Wat je nu doet:** drie soorten plekken uit elkaar houden. Anders verdwijnt
het origineel, of komt een half af bestand op de publieke site.

Een **bladermap** is de publicatiemap van één zangstuk onder de Oefenhoek
(bijvoorbeeld `…\8a-trisagion\`). Daarin horen alleen bestanden die
koorleden mogen zien.

## Drie plekken

| Plek | Map (vanaf `content-source\praktijk\`) | Op de publieke site? |
| --- | --- | --- |
| Ruw, ongewijzigd | `oefenhoek\input\capella\` (of `vow\`, `musescore\`, `musicxml\`, `pdf\`) | Nee |
| Halverwege (tussenwerk) | `oefenhoek\input\_werk\` | Nee (en niet in git) |
| Klaar voor koorleden (bladermap) | `oefenhoek\liturgiemap-hemelum\<doel-id>\` of `oefenhoek\overig\<doel-id>\` | Ja |

De map `input\_inbox\` is een lokale brievenbus voor bestanden die je nog
niet zeker wilt bewaren. Pas als een bestand dé bron is die je wilt
houden, verplaats je het naar `capella\`, `vow\`, of een andere
herkomst-map.

## Herkomst-mappen

| Map onder `input\` | Wat erin hoort |
| --- | --- |
| `capella\` | Capella / CapToMusic: `.cap`, `.capx`, of een `.mxl` zoals het binnenkwam |
| `vow\` | Ruwe VOW-`.mscz` |
| `musescore\` | Andere ruwe `.mscz` (nog niet de Oefenhoek-layout) |
| `musicxml\` | `.xml` / `.musicxml` / `.mxl` uit een ander programma |
| `pdf\` | Scans of print-PDF die je als bron bewaart |

Laat de **originele bestandsnaam** van de dump staan, ook met spaties.
Hernoemen gebeurt pas bij publicatie.

## Publicatienamen

In een bladermap (en in `_werk`): geen spaties; alleen kleine letters,
cijfers, `-` en `_`. Voorbeeld: `8a - trisagion.mxl` wordt
`8a-trisagion.mscz`. Het script `scripts\score_filenames.py` doet die
omzetting als je bij opkuisen en layout `-o` gebruikt.

## Deelrubrieken

| Deelrubriek | Wanneer |
| --- | --- |
| `liturgiemap-hemelum` | Het stuk hoort in de Hemelum-liturgiemap |
| `overig` | Testmateriaal, of iets dat nergens in die liturgiemap past |

Weet je de deelrubriek niet? Laat het veld in de werkvoorraad leeg en vraag
het na. Raad niet.

## Klaar als

Voor een willekeurig bestand kun je zeggen: dump, tussenwerk, of bladermap.
Je zet nooit een ruwe dump rechtstreeks in een bladermap.

{{< navbuttons "Volgende: woorden|/praktijk/handleiding/start/woorden/" >}}
