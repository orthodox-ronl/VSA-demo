---
title: "De bladermap"
linkTitle: "Bladermap"
weight: 10
---

# De bladermap

{{< cue >}}
Map: `content-source\praktijk\oefenhoek\liturgiemap-hemelum\DOEL-ID\`
(of `overig\`). Erin: `index.md` + `.mscz`/`.pdf`/`.mxl` en/of `.vsa`.
Kopieer een buurman: `8a-trisagion` (partituur), of
`2-eerste-antifoon\weekdagen\hemelum` (VSA), of tropaar Nikolaas (beide).
{{< /cue >}}

**Wat je nu doet:** de bestanden die je al hebt, tot één pagina maken die
de Oefenhoek kan tonen.

Een **bladermap** is die publicatiemap: één zangstuk, één map, met
`index.md` en de oefenbestanden.

**Wanneer:** na partituur-producten of na een werkende `.vsa`. Familie
(meerdere varianten): een `_index.md` in de oudermap en kind-bladermappen
eronder — kopieer die structuur, verzinnen hoeft niet.

## Stap voor stap

1. De mapnaam is het doel-id: alleen `a-z`, `0-9`, `-`, `_`.
2. Kopieer de publicatiebestanden naar die map (niet de ruwe dump uit
   `input\`).
3. Maak `index.md` door een **bestaand** bestand te kopiëren en namen te
   vervangen. Dat is betrouwbaarder dan overtypen.

| Wat je hebt | Kopieer dit `index.md` |
| --- | --- |
| `.pdf` + Coria-`.mxl` | `oefenhoek\liturgiemap-hemelum\8a-trisagion\index.md` |
| Alleen `.vsa` (plaatje) | `oefenhoek\liturgiemap-hemelum\2-eerste-antifoon\weekdagen\hemelum\index.md` |
| `.vsa` + PDF + Coria | `oefenhoek\liturgiemap-hemelum\troparen-en-kondaken\troparion-nikolaas-van-myra\index.md` |

In dat gekopieerde bestand staan onder meer:

- bovenaan tussen `---`: `title`, `publicatiestatus`
- een regel `:::include svg "….vsa" …:::` als er VSA is
- een blok voor de knoppen **Oefenen in Coria**, **Downloaden**, **Printen**
- een regel die de PDF op de pagina toont

Vervang overal de oude stam (bijvoorbeeld `8a-trisagion`) door de stam
van jouw zangstuk.

4. Pas `weight` alleen aan als de volgorde in een familie-map telt
   (antifonen, troparen).
5. Hoort het stuk in de Hemelum-liturgie? Zet de titel ook in
   `liturgiemap-hemelum\_index.md` (die inhoudsopgave is handmatig).
   Anders vinden koorleden het stuk alleen via de mappen, niet via het
   liturgie-overzicht.

## Klaar als

Na `check` toont de lokale preview de pagina, met plaatje en/of PDF, en
de knoppen als die bestanden er zijn.

{{< navbuttons "Volgende: status en check|/praktijk/handleiding/publiceren/2-status-en-check/" >}}
