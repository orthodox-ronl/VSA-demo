---
title: "VSA"
linkTitle: "VSA"
weight: 30
nav_sort: weight
---

**VSA** is de notatie voor tekst-plus-melodie in een gewoon tekstbestand
(extensie `.vsa`). De sitebuild maakt daarvan een plaatje (SVG).

Voor een tropaar op **toon 4** kun je dat `.vsa`-bestand daarna combineren
met een formule-template. Dan komen alt, tenor en bas erbij (SATB).

Oefenbare `.vsa`-bestanden staan in het **bibliotheek**; het **koormap-slot**
in de liturgiemap toont ze via shortcode `bibliotheek-score` (zelfde id
als de bibliotheek-map).

{{< cue >}}
- Antifoon / eenstemmig: `.vsa` in de bibliotheek → [schrijven](1-vsa-schrijven/).
- Tropaar toon 4, meerstemmig blad: `.vsa` met `template: tropaar-toon-4` → [template SATB](2-template-satb/).
- Valideren: `vsa validate pad\naar\bestand.vsa`
{{< /cue >}}
