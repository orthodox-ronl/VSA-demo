---
title: "Afgeleiden bijwerken"
linkTitle: "Afgeleiden"
weight: 60
---

# Afgeleiden bijwerken

{{< cue >}}
Na basispartituur-edit in de bibliotheek:
```cmd
scripts\layout.cmd content-source\praktijk\oefenhoek\bibliotheek\DOEL\STAM.mscz
scripts\mscz-products.cmd content-source\praktijk\oefenhoek\bibliotheek\DOEL
scripts\check.cmd --strict
```
Of producten voor alles: `scripts\mscz-products.cmd content-source`.
`--force` op `mscz-products` als de basispartituur nieuwer is maar dat niet in de
bestandsdatum zichtbaar is.

Na `.vsa`-edit: `scripts\vsa-products.cmd` (of alleen `check` lokaal) en
commit `.vsa` + `.vsa.mxl` samen.
{{< /cue >}}

**Wat je nu doet:** afgeleiden opnieuw laten maken nadat de **bron** is
gewijzigd, en controleren of preview en `check` geen verouderde-afgeleiden-
banner of -fout tonen.

**Afgeleiden** = bestanden die uit een bron komen en niet zelf die bron zijn.
Basispartituur: `{stam}.pdf` en `{stam}.mxl`. VSA: `{stam}.vsa.mxl`. De bron blijft de
plek waar je editet (basispartituur-`.mscz` of `.vsa`).

**Wanneer:** na elke inhoudelijke wijziging aan een basispartituur-`.mscz` of
bibliotheek-`.vsa` die al gepubliceerd wordt, vóór je opnieuw
`publicatiestatus: reviewable` (of hoger) zet. Eerste keer basispartituur-producten:
[PDF en Coria](../5-pdf-en-coria/). Eerste keer VSA-Coria:
[.vsa schrijven](../../vsa/1-vsa-schrijven/).

## Basispartituur: volgorde (niet omdraaien)

1. Basispartituur in MuseScore 4 bewerken → Opslaan.
2. **Opnieuw normaliseren** (`scripts\layout.cmd` op diezelfde basispartituur).
3. **Producten** (`mscz-products.cmd` op de bibliotheek-map).
4. **`check --strict`**.
5. Preview: koormap-slot openen; PDF-download en **Oefenen** testen.

Sla je stap 2 over, dan kunnen PDF/Coria een basispartituur met verouderde layout of
reciteertoon-encoding weergeven. Sla je stap 3 over, klaagt `check` of toont
de preview een rode banner dat de basispartituur-afgeleiden niet bij de partituur-hash horen.

## Basispartituur: stap voor stap

1. Sla de basispartituur-`.mscz` op in het **bibliotheek** (niet alleen in `_werk`).
2. Normaliseer opnieuw:

```cmd
scripts\layout.cmd content-source\praktijk\oefenhoek\bibliotheek\8-trisagion\8a-nederlands\hemelum\8-trisagion-8a-nederlands-hemelum.mscz
```

3. Maak PDF en Coria-`.mxl` opnieuw:

```cmd
scripts\mscz-products.cmd content-source\praktijk\oefenhoek\bibliotheek\8-trisagion\8a-nederlands\hemelum
```

4. Controleer:

```cmd
scripts\check.cmd --strict
```

5. Lokale preview (poort **18731**): open het koormap-slot; test de
   PDF-knoppen en **Oefenen**.

## VSA: Coria-`.vsa.mxl`

`vsa-products` syllabificeert ongescoopte tekst **alleen tijdens export**
(Pyphen, temp-bestand). De canonieke `.vsa` blijft geschikt voor SVG op de
site. Zie [Werktrajecten](/praktijk/handleiding/werktrajecten/)
(basispartituur: [Basispartituur](/praktijk/handleiding/werktrajecten/basispartituur/)).

Na een wijziging in de bibliotheek-`.vsa`:

```cmd
scripts\vsa-products.cmd
scripts\check.cmd --strict
```

Lokale `check` vernieuwt stale `.vsa.mxl` ook zelf. Commit bron en product
samen. Banner “VSA-afgeleiden niet in orde”: zelfde commando’s. Mappen met
`artefacten_handmatig: true` doen **niet** mee — daar houd jij PDF/MXL zelf bij.

## Print-`.mscz`

Een bestand dat op `.print.mscz` eindigt, wordt door `mscz-products`
overslagen. PDF (en eventuele Coria-`.mxl`) maak je handmatig — zie
[Print-.mscz](../7-print-mscz/).

### Banner of check-fout

| Symptoom | Meest waarschijnlijke oorzaak | Actie |
| --- | --- | --- |
| Preview-banner: basispartituur-afgeleiden niet in orde | PDF/MXL niet vernieuwd na basispartituur-edit | Basispartituur-stappen 2–4 opnieuw |
| Preview-banner: VSA-afgeleiden niet in orde | `.vsa.mxl` ontbreekt of ouder dan `.vsa` | `vsa-products` + commit |
| `check` weigert Coria-`.mxl` | Verkeerde `.mxl` (bijv. uit `input\`) of verouderd product | Alleen bibliotheek-producten uit `mscz-products` / `vsa-products` |
| Producten lijken niet te vernieuwen | Tijdstempels kloppen niet | `mscz-products … --force` of `vsa-products … --force` |

Meer storingen: [Als het misgaat](../../publiceren/3-als-het-misgaat/).

## Klaar als

`check --strict` is groen; basispartituur-PDF/MXL horen bij de huidige basispartituur; VSA-`.vsa.mxl`
hoort bij de huidige `.vsa` (tenzij handmatig); preview toont geen
verouderde-afgeleiden-banner.

{{< navbuttons "Print-.mscz|/praktijk/handleiding/partituur/7-print-mscz/" "Bibliotheek en koormap|/praktijk/handleiding/publiceren/1-bladermap/" >}}
