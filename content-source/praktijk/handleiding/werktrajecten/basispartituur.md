---
title: "Basispartituur → PDF en Coria"
linkTitle: "Basispartituur"
weight: 20
---

# Basispartituur → PDF en Coria

Dit werktraject maakt uit een **basispartituur-`.mscz`** (MuseScore) de
bestanden die koorleden downloaden en in Coria oefenen. Representatie-id:
`partituur`.

{{< cue >}}
Na normaliseren en review in MuseScore 4:
```cmd
scripts\mscz-products.cmd content-source\praktijk\oefenhoek\bibliotheek\<zangstuk>\<variant>\<uitvoeringsvorm>
```
Daarna `scripts\check.cmd --strict`. Geen `*.print.mscz` in deze keten.
{{< /cue >}}

## Waartoe

Een vierstemmig (of meer) blad in de bibliotheek moet op de site als
A4-PDF leesbaar zijn en via de knop **Oefenen** in Coria afspeelbaar. Dit
traject houdt PDF en Coria-`.mxl` synchroon met de canonieke
basispartituur.

## Eindresultaat en criteria

| Bestand (in de bladermap) | Rol |
| --- | --- |
| `{stam}.mscz` | Canonieke basispartituur (niet `.print.`) |
| `{stam}.pdf` of `{stam}.partituur.pdf` | A4-afdruk |
| `{stam}.mxl` of `{stam}.partituur.mxl` | MusicXML voor Coria |

**Klaar** als: de PDF/MXL de stamp `partituur-sha256` van de huidige
`.mscz` dragen; de colofonregel **Bibliotheek-id:** klopt met het pad;
`check_partituur_products` (onderdeel van `check --strict`) is groen.
Meerdere producten van hetzelfde type in één map → expliciete namen met
representatie-id (zie `scripts\oefenhoek-product-contract.md` in `VSA-demo`).

## Wanneer wel / wanneer niet

| Wel | Niet |
| --- | --- |
| Gewoon oefenmateriaal: één tekst, standaardlayout, automatische Coria | Bestandsnaam eindigt op `.print.mscz` → [Print-vel](../print-vel/) |
| Na opkuisen, `layout`, en review | Ruwe Capella-`.mxl` zonder basispartituur |
| | Alleen eenstemmige tekst → [VSA](../vsa/) |

## Volgorde (bestanden)

1. Ruw materiaal via [Opnemen](../opnemen-in-bibliotheek/) (of al in
   `_werk\`). Inhoudelijk opkuisen: [Opkuisen](../../partituur/2-opkuisen/).
2. Normaliseren naar basispartituur-standaard:

```cmd
scripts\layout.cmd pad\naar\bestand.mscz
```

   HOW: [Standaard-.mscz](../../partituur/3-standaard-mscz/).
3. Review in MuseScore 4, daarna opnieuw `layout` indien nodig.
   HOW: [Reviewen](../../partituur/4-reviewen/).
4. Bestand in de bibliotheek (als dat nog niet zo is):
   `scripts\bieb-accepteer.cmd` — zie [Opnemen](../opnemen-in-bibliotheek/).
5. Bibliotheek-id in colofon/meta (lokaal vaak al via `check`):

```cmd
scripts\ensure-bibliotheek-id.cmd
```

6. PDF en Coria-`.mxl` exporteren:

```cmd
scripts\mscz-products.cmd content-source\praktijk\oefenhoek\bibliotheek\8-trisagion\8a-nederlands\hemelum
```

   Of heel `content-source`. `--force` als producten ouder zijn dan de
   `.mscz`. HOW: [PDF en Coria](../../partituur/5-pdf-en-coria/).
7. Site zichtbaar maken: [Site-build](../site-build/).

Voorbeeldbladermap:
`content-source\praktijk\oefenhoek\bibliotheek\8-trisagion\8a-nederlands\hemelum\`.

## Automatisch (CI)

Op GitHub Actions (workflows `validate.yml` / `pages.yml`):

- **Wel:** `check_partituur_products.py` en `check_bibliotheek_id.py`
  controleren of PDF/MXL bij de `.mscz` passen en of het bibliotheek-id
  klopt.
- **Niet:** MuseScore-export (`mscz-products`). CI heeft geen MuseScore 4.
  Verouderde of ontbrekende producten laten de build **falen** — jij
  vernieuwt ze lokaal en commit PDF/MXL mee.

Lokaal vernieuwt `scripts\check.cmd` (via `_pipeline.cmd`) stale
basispartituur-producten wél met `sync_mscz_products.py`, en zet
ontbrekende bibliotheek-ids met `ensure_bibliotheek_id.py`.

## Handmatig

| Situatie | Commando | Man-page |
| --- | --- | --- |
| Layout / normaliseren | `scripts\layout.cmd` `<pad>` | [layout](../../scripts/layout/) |
| PDF + Coria | `scripts\mscz-products.cmd` `[map]` | [mscz-products](../../scripts/mscz-products/) |
| Bibliotheek-id in `.mscz` | `scripts\ensure-bibliotheek-id.cmd` | [ensure-bibliotheek-id](../../scripts/ensure-bibliotheek-id/) |
| Alles vóór commit | `scripts\check.cmd --strict` | [check](../../scripts/check/) |

## Zie ook

- [Afgeleiden](../../partituur/6-afgeleiden/)
- Contracten in `VSA-demo`: `scripts\oefenhoek-product-contract.md`,
  `scripts\mscz-partituur-contract.md`, `scripts\mscz-product-transforms.md`

{{< navbuttons "Opnemen|/praktijk/handleiding/werktrajecten/opnemen-in-bibliotheek/" "VSA|/praktijk/handleiding/werktrajecten/vsa/" >}}
