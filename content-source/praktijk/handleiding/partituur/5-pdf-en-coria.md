---
title: "PDF en Coria-.mxl maken"
linkTitle: "PDF en Coria"
weight: 50
---

# PDF en Coria-.mxl maken

{{< cue >}}
De `.mscz` ligt in de **bladermap** (niet meer alleen in `_werk`). Daarna:
```cmd
scripts\mscz-products.cmd content-source\praktijk\oefenhoek\liturgiemap-hemelum\DOEL-ID
```
`--force` als PDF of Coria-`.mxl` al bestaan maar de `.mscz` inhoudelijk nieuwer is.
`mscz-products` zit **niet** in `check` / `serve`.
{{< /cue >}}

**Wat je nu doet:** uit de nagekeken `.mscz` twee sibling-bestanden maken:
een A4-PDF en een `.mxl` die Coria aankan.

**Wanneer:** ná review en her-layout. Niet meteen na de eerste layout als
je nog gaat editen: dan maak je de producten twee keer.

Zie ook [Afgeleiden bijwerken](../6-afgeleiden/) (banner op preview,
productie-gate, hub-hash).

## Stap voor stap

1. Zet de `.mscz` in de bladermap als het bestand daar nog niet staat
   (kopiëren uit `_werk`). Gebruik namen zonder spaties, met dezelfde
   stam als de latere PDF:

```text
content-source\praktijk\oefenhoek\liturgiemap-hemelum\8a-trisagion\
  8a-trisagion.mscz
```

   `index.md` mag nog ontbreken; die volgt bij
   [publiceren](../../publiceren/1-bladermap/). Zonder `index.md` is er
   nog geen Hugo-pagina, maar `mscz-products` kijkt naar de `.mscz`.

2. Maak de producten:

```cmd
scripts\mscz-products.cmd content-source\praktijk\oefenhoek\liturgiemap-hemelum\8a-trisagion
```

   Zonder pad: alle publicatie-`.mscz` onder `content-source` (handig,
   kan langer duren). MuseScore 4 is nodig.

3. In die bladermap horen nu naast de `.mscz` ook `8a-trisagion.pdf` en
   `8a-trisagion.mxl`.

4. Open de PDF even (niet alleen in MuseScore). Coria test je ná `check`
   op de preview-pagina met de knop **Oefenen in Coria**.

Zijn bestaande PDF of Coria-`.mxl` ouder dan de `.mscz`? Het script
vernieuwt ze. Is de `.mscz` inhoudelijk gewijzigd maar klopt de
bestandsdatum niet? Zet `--force` achter het commando.

Dit commando zit bewust **niet** in `check` of `serve`: eerst nadenken,
dan exporteren.

## Klaar als

In de bladermap liggen `.mscz`, `.pdf` en `.mxl` met dezelfde stam, zonder
spaties. Bestanden die op `.print.mscz` eindigen horen niet in deze
stap — zie [Print-.mscz](../7-print-mscz/). Daarna:
[bladermap afronden](../../publiceren/1-bladermap/).

{{< navbuttons "Volgende: bladermap|/praktijk/handleiding/publiceren/1-bladermap/" >}}
