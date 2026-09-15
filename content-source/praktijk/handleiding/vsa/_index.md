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

Een **bladermap** is de publicatiemap van het zangstuk onder de Oefenhoek.

{{< cue >}}
- Antifoon / eenstemmig: `.vsa` in de bladermap + `:::include svg …:::` → [schrijven](1-vsa-schrijven/).
- Tropaar toon 4, meerstemmig blad: `.vsa` met `template: tropaar-toon-4` → [template SATB](2-template-satb/).
- Valideren: `vsa validate pad\naar\bestand.vsa`
{{< /cue >}}
