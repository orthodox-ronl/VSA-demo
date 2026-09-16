---
title: "Print-.mscz (koormap-vel)"
linkTitle: "Print-.mscz"
weight: 70
---

# Print-`.mscz` (koormap-vel)

{{< cue >}}
Bestandsnaam eindigt op **`.print.mscz`**. Geen `apply_mscz_layout.py`, geen
`mscz-products`, geen Coria-eis. PDF maak je zelf in MuseScore 4
(Bestand → Exporteren → PDF) en commit je naast het print-bestand **in het
bibliotheek**.
{{< /cue >}}

**Wat je nu doet:** een MuseScore-bestand in het **bibliotheek** zetten dat de
hub-pijplijn **niet** mag aanpassen — typisch één A4-vel voor de koormap met
layout of tekstregels die de hub-normalisatie zou vernielen. Het koormap-slot
verwijst met `bibliotheek-score` (alleen PDF-knoppen, geen Coria).

**Wanneer:** als je bewust **buiten** de hub-straat werkt. Voor gewoon
oefenmateriaal (één tekst, Coria, standaardlayout) gebruik je een gewone
hub-`.mscz` via [standaard-.mscz](../3-standaard-mscz/) en
[PDF en Coria](../5-pdf-en-coria/).

Voorbeeld: [bibliotheek `7-kleine-intocht/zo-wk-mg/hemelum`](/praktijk/oefenhoek/bibliotheek/7-kleine-intocht/zo-wk-mg/hemelum/)
naast de hubs zondag / weekdagen / moeder-gods.

## Wat het is

| In Verkenner (bibliotheek) | Rol |
| --- | --- |
| `{stam}.print.mscz` | MuseScore-bron voor een printvel; scripts laten dit met rust |
| `{stam}.pdf` | Handmatige A4-export |
| Geen Coria-`.mxl` | Geen knop **Oefenen in Coria** voor dit vel |

Bibliotheek-id voorbeeld: `7-kleine-intocht/zo-wk-mg/hemelum`.

## Wat je niet doet

- Geen `apply_mscz_layout.py` op `.print.mscz`.
- Geen `mscz-products.cmd` voor dit bestand.
- Geen hernoemen naar gewone `.mscz` “even snel” — dan eist `check` hub-producten.

## Stap voor stap

1. Bewerk in MuseScore 4; sla op in de bibliotheek als
   `{stam}.print.mscz` (geen spaties; stam uit bibliotheek-id).
2. Exporteer PDF handmatig naar `{stam}.pdf` in dezelfde bibliotheek-map.
3. Bibliotheek-`index.md` + koormap-slot `7-kleine-intocht/zo-wk-mg` met
   `bibliotheek-score` (zie [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/)).
4. `scripts\check.cmd --strict` — hub-productgate negeert `.print.mscz`.

## Klaar als

Bibliotheek bevat `*.print.mscz` en PDF; koormap-slot verwijst ernaar; check
klaagt niet over ontbrekende Coria voor dit vel.

{{< navbuttons "Terug: afgeleiden|/praktijk/handleiding/partituur/6-afgeleiden/" "Handleiding|/praktijk/handleiding/" >}}
