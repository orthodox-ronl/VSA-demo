---
title: "VSA"
linkTitle: "VSA"
weight: 30
nav_sort: weight
---

**VSA** is de notatie voor tekst-plus-melodie in een gewoon tekstbestand
(extensie `.vsa`). De sitebuild maakt daarvan een **plaatje (SVG)** via
`python scripts\sync_oefenhoek_index.py --svg` (onderdeel van `check` /
`build` / `serve`). Bij een bibliotheek-`.vsa` maakt de lokale `check` ook
een Coria-bestand `{stam}.vsa.mxl`, zodat koorleden de knop **Oefenen**
krijgen. Dat zijn twee aparte stappen — zie
[.vsa schrijven](1-vsa-schrijven/).

Voor een tropaar op **toon 4** kun je dat `.vsa`-bestand daarna combineren
met een formule-template. Dan komen alt, tenor en bas erbij (SATB). Dat
blad zet je vaak als print-vel neer (handmatige artefacten), niet als
automatische basispartituur — zie [template SATB](2-template-satb/).

Oefenbare `.vsa`-bestanden staan in het **bibliotheek**; het **koormap-slot**
in de liturgiemap toont ze via shortcode `bieb` (zelfde id
als de bibliotheek-map).

{{< cue >}}
- Antifoon / eenstemmig: `.vsa` in de bibliotheek → [schrijven](1-vsa-schrijven/) (SVG-plaatje + Coria-`.vsa.mxl`).
- Tropaar toon 4, meerstemmig blad: `.vsa` met `template: tropaar-toon-4` → [template SATB](2-template-satb/).
- Valideren: `vsa validate pad\naar\bestand.vsa`
{{< /cue >}}
