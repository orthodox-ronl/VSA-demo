---
title: "Print-.mscz (koormap-vel)"
linkTitle: "Print-.mscz"
weight: 70
---

# Print-`.mscz` (koormap-vel)

{{< cue >}}
Bestandsnaam eindigt op **`.print.mscz`**. Geen `apply_mscz_layout.py`, geen
`mscz-products`, geen Coria-eis. PDF maak je zelf in MuseScore 4
(Bestand → Exporteren → PDF) en commit je naast het print-bestand.
{{< /cue >}}

**Wat je nu doet:** een MuseScore-bestand in de bladermap zetten dat de
pipeline **niet** mag aanpassen — typisch één A4-vel voor de koormap met
layout of tekstregels die de hub-normalisatie zou vernielen.

**Wanneer:** als je bewust **buiten** de hub-straat werkt. Voor gewoon
oefenmateriaal (één tekst, Coria, standaardlayout) gebruik je een gewone
hub-`.mscz` via [standaard-.mscz](../3-standaard-mscz/) en
[PDF en Coria](../5-pdf-en-coria/).

Dit is het **derde** publicatiespoor naast partituur-hub en VSA; zie
[Handleiding](../../) (drie paden).

## Wat het is

| In Verkenner | Rol |
| --- | --- |
| `naam.print.mscz` | MuseScore-bron voor een printvel; scripts laten dit met rust |
| `naam.pdf` (optioneel) | Handmatige A4-export; mag dezelfde stam hebben **zonder** `.print` |
| Geen Coria-`.mxl` | Geen knop **Oefenen in Coria** van dit bestand |

Voorbeeld: één vel kleine intocht met drie lyric-regels (zondag /
weekdagen / Moeder Gods) naast de aparte hub-bladermappen 7a / 7b / 7c
waar wél geoefend wordt.

## Wat je niet doet

- Geen `python scripts\apply_mscz_layout.py` op dit bestand (het script
  weigert `.print.mscz`).
- Geen `scripts\mscz-products.cmd` verwachten voor dit bestand (wordt
  overgeslagen).
- Geen hernoemen naar gewone `.mscz` “even snel” — dan denkt `check` dat
  het een hub is en eist PDF + Coria met hub-hash.

## Stap voor stap

1. Bewerk in MuseScore 4; sla op als
   `…\bladermap\jouw-stuk.print.mscz` (geen spaties in de naam).
2. Exporteer PDF handmatig naar bijvoorbeeld `jouw-stuk.pdf` in dezelfde
   map.
3. Zet in `index.md` uitleg voor koorleden (welk vel, wanneer welke
   tekstregel). Oefenen blijft via de hub-varianten als die bestaan.
4. Commit print-`.mscz` en PDF samen. Draai `scripts\check.cmd --strict`
   — de hub-productgate negeert dit bestand.

## Klaar als

De bladermap bevat `*.print.mscz` (en eventueel PDF), `check` klaagt niet
over ontbrekende Coria voor dit vel, en je hebt géén layout-script op
het print-bestand gezet.

{{< navbuttons "Terug: afgeleiden|/praktijk/handleiding/partituur/6-afgeleiden/" "Handleiding|/praktijk/handleiding/" >}}
