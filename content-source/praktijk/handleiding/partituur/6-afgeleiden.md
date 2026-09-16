---
title: "Afgeleiden bijwerken"
linkTitle: "Afgeleiden"
weight: 60
---

# Afgeleiden bijwerken

{{< cue >}}
Na hub-edit in de bibliotheek:
```cmd
python scripts\apply_mscz_layout.py content-source\praktijk\oefenhoek\bibliotheek\DOEL\STAM.mscz
scripts\mscz-products.cmd content-source\praktijk\oefenhoek\bibliotheek\DOEL
scripts\check.cmd --strict
```
Of producten voor alles: `scripts\mscz-products.cmd content-source`.
`--force` op `mscz-products` als de hub nieuwer is maar dat niet in de
bestandsdatum zichtbaar is.
{{< /cue >}}

**Wat je nu doet:** PDF en Coria-`.mxl` opnieuw laten maken nadat de
**hub-`.mscz`** is gewijzigd, en controleren of preview en `check` geen
verouderde-afgeleiden-banner of -fout tonen.

**Afgeleiden** = de bestanden die uit de hub komen en niet zelf de bron
zijn: `{stam}.pdf` en `{stam}.mxl` (Coria). De hub blijft de plek waar je
editet.

**Wanneer:** na elke inhoudelijke wijziging in MuseScore aan een
hub-`.mscz` die al in de bibliotheek staat, vóór je opnieuw
`publicatiestatus: reviewable` (of hoger) zet. Eerste keer producten maken:
[PDF en Coria](../5-pdf-en-coria/).

## Volgorde (niet omdraaien)

1. Hub in MuseScore 4 bewerken → Opslaan.
2. **Opnieuw normaliseren** (`apply_mscz_layout.py` op diezelfde hub).
3. **Producten** (`mscz-products.cmd` op de bibliotheek-map).
4. **`check --strict`**.
5. Preview: koormap-slot openen; PDF-download en Coria-knop testen.

Sla je stap 2 over, dan kunnen PDF/Coria een hub met verouderde layout of
reciteertoon-encoding weergeven. Sla je stap 3 over, klaagt `check` of toont
de preview een banner dat de afgeleiden niet bij de hub-hash horen.

## Stap voor stap

1. Sla de hub-`.mscz` op in het **bibliotheek** (niet alleen in `_werk`).
2. Normaliseer opnieuw:

```cmd
python scripts\apply_mscz_layout.py content-source\praktijk\oefenhoek\bibliotheek\8-trisagion\8a-nederlands\hemelum\8-trisagion-8a-nederlands-hemelum.mscz
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
   PDF-knoppen en **Oefenen in Coria**.

### Print-`.mscz`

Een bestand dat op `.print.mscz` eindigt, wordt door `mscz-products`
overslagen. PDF daarvoor maak je handmatig in MuseScore — zie
[Print-.mscz](../7-print-mscz/).

### Banner of check-fout over hub-hash

| Symptoom | Meest waarschijnlijke oorzaak | Actie |
| --- | --- | --- |
| Preview-banner: afgeleiden horen niet bij de hub | PDF/MXL niet vernieuwd na hub-edit | Stap 2–4 opnieuw |
| `check` weigert Coria-`.mxl` | Verkeerde `.mxl` (bijv. uit `input\`) of verouderd product | Alleen bibliotheek-`.mxl` uit `mscz-products` |
| Producten lijken niet te vernieuwen | Tijdstempels kloppen niet | `mscz-products … --force` |

Meer storingen: [Als het misgaat](../../publiceren/3-als-het-misgaat/).

## Klaar als

`check --strict` is groen; PDF en Coria-`.mxl` in de bibliotheek horen bij
de huidige hub; preview toont geen verouderde-afgeleiden-banner.

{{< navbuttons "Print-.mscz|/praktijk/handleiding/partituur/7-print-mscz/" "Bibliotheek en koormap|/praktijk/handleiding/publiceren/1-bladermap/" >}}
