---
title: "Werktrajecten"
linkTitle: "Werktrajecten"
weight: 15
nav_sort: weight
aliases:
  - /praktijk/handleiding/start/publicatietrajecten/
---

Een **werktraject** is een vaste pijplijn: van bronbestand naar eindproduct
dat koorleden (of jij als beheerder) op de site gebruiken. Elke pagina hier
beschrijft waartoe die pijplijn dient, wat het eindresultaat is, wanneer je
hem wel of niet gebruikt, welke bestanden in welke volgorde ontstaan, wat
GitHub Actions (CI) automatisch doet, en welke `scripts\….cmd`-regels je
lokaal plakt.

**Nog niet klaar met je pc?** Begin bij [Start](../start/) (programma’s,
mappen, woorden). Stapsgewijze MuseScore- of VSA-HOW’s staan onder
[Partituur](../partituur/) en [VSA](../vsa/). Commando-flags: [Scripts](../scripts/).

{{< cue >}}
- **Poort:** [Opnemen in de bibliotheek](opnemen-in-bibliotheek/) — ruw materiaal
  binnenhalen, later opkuisen, daarna `bieb-accepteer`
- **Publicatiesporen:** [Basispartituur](basispartituur/), [VSA](vsa/),
  [Print-vel](print-vel/), [Tekstblad](tekstblad/)
- **Site zichtbaar maken:** [Site-build](site-build/)
- **Apart:** [Markdown naar PDF](markdown-naar-pdf/),
  [Ingebedde VSA](ingebedde-vsa/); voorzien: [mvsa](mvsa/)
{{< /cue >}}

## Hoe de trajecten in elkaar haken

```text
ruw materiaal (oefenhoek/input/)
    |
    v
Opnemen in de bibliotheek  (werkvoorraad + later opkuis + bieb-accepteer)
    |
    +-- Basispartituur  ->  PDF + Coria-.mxl
    +-- VSA             ->  SVG + Coria-.vsa.mxl
    +-- Print-vel       ->  handmatige PDF
    +-- Tekstblad       ->  .tekstblad.md -> .tekstblad.pdf
    |
    v
Site-build  (check / build / serve, of CI)  ->  generated/site + GitHub Pages
```

[Markdown naar PDF](markdown-naar-pdf/) en [Ingebedde VSA](ingebedde-vsa/)
zijn aparte sporen (demo’s, handleidingen, samenstellingen). Die vervangen
geen bibliotheek-producten.

## Catalogus

| Werktraject | Waartoe (kort) | Pagina |
| --- | --- | --- |
| Opnemen in de bibliotheek | Ruw bestand bewaren en later als klaar oefenbestand in de catalogus zetten | [Opnemen](opnemen-in-bibliotheek/) |
| Basispartituur | MuseScore-basispartituur naar A4-PDF en Coria-`.mxl` | [Basispartituur](basispartituur/) |
| VSA | Eenstemmige `.vsa` naar SVG-plaatje en Coria-`.vsa.mxl` | [VSA](vsa/) |
| Print-vel | Print-`.mscz` met handmatige PDF, buiten de basispartituur-keten | [Print-vel](print-vel/) |
| Tekstblad | Liturgische tekst/dialoog: `.tekstblad.md` naar A4-PDF | [Tekstblad](tekstblad/) |
| Site-build | `content-source` naar lokale site of GitHub Pages | [Site-build](site-build/) |
| Markdown naar PDF | Markdownblad met VSA naar A4-PDF (generiek / demo) | [Markdown naar PDF](markdown-naar-pdf/) |
| Ingebedde VSA | VSA buiten de oefenhoek-bibliotheek naar SVG (en optioneel MXL) | [Ingebedde VSA](ingebedde-vsa/) |
| mvsa | Meerstemmige VSA — nog niet actief | [mvsa (voorzien)](mvsa/) |

**Representatie-id** in de bibliotheek (`partituur`, `vsa`, `print`): welk
bronbestand hoort bij welk afgeleid product. Technische namen en stamps:
bestand `scripts\oefenhoek-product-contract.md` in de repository-map
`VSA-demo`. Termen: [Woorden](../start/woorden/).

{{< navbuttons "Start|/praktijk/handleiding/start/" "Opnemen|/praktijk/handleiding/werktrajecten/opnemen-in-bibliotheek/" >}}
