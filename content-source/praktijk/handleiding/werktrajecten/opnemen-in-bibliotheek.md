---
title: "Opnemen in de bibliotheek"
linkTitle: "Opnemen"
weight: 10
---

# Opnemen in de bibliotheek

Dit werktraject is de **poort** naar de catalogus: van ruw aangeleverd
materiaal naar een map onder `oefenhoek\bibliotheek\` met een
**bibliotheek-id** (`zangstuk/variant/uitvoeringsvorm`). Publicatiesporen
([Basispartituur](../basispartituur/), [VSA](../vsa/),
[Print-vel](../print-vel/)) sluiten hierop aan — nádat het bestand klaar
genoeg is om op te nemen.

{{< cue >}}
1. Bewaar het ruwe bestand onder `content-source\praktijk\oefenhoek\input\`.
2. Werk de tabel
   `content-source\praktijk\oefenhoek\input\werkvoorraad.md` bij
   (`update-werkvoorraad` of `check`).
3. Vul het **doel-id** in — niet raden; zie het
   [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/).
4. Als het bestand klaar is (basispartituur-`.mscz`, `.vsa` of `.print.mscz`):
   `scripts\bieb-accepteer.cmd`.
5. Controleer met `scripts\check.cmd --strict`.
{{< /cue >}}

## Waartoe

Koorleden zien alleen wat in de **bibliotheek** staat (of via een
**koormap**-slot ernaar verwijst). Ruwe Capella-, PDF- of VOW-bestanden
horen niet rechtstreeks in die catalogus. Dit traject houdt de input
bij, en zet een **klaar** oefenbestand op de juiste plek met de juiste
naam.

## Eindresultaat en criteria

| Op schijf | Rol |
| --- | --- |
| `content-source\praktijk\oefenhoek\input\<herkomst>\…` | Origineel ruw bestand (originele naam) |
| `input\werkvoorraad.md` | Rij per input, met doel-id / koormap / notitie |
| `bibliotheek\<zangstuk>\<variant>\<uitvoeringsvorm>\` | Map met `index.md` + bestand onder **publicatiestam** |

**Klaar** als: het doel-id klopt (of bewust leeg met een vraag in de
notitie); na `bieb-accepteer` bestaat de bladermap met shortcode `bieb`;
`scripts\check.cmd --strict` is groen voor de bibliotheekstructuur.

`bieb-accepteer` maakt **geen** PDF of Coria-`.mxl`. PDF en Coria-`.mxl`
horen bij [Basispartituur](../basispartituur/) of [VSA](../vsa/).

## Wanneer wel / wanneer niet

| Wel | Niet |
| --- | --- |
| Nieuw Capella-, VOW-, MuseScore-, MusicXML-, PDF- of `.vsa`-bestand | Bestand al in de bibliotheek onder het juiste id |
| Klaar oefenbestand in de catalogus zetten | Ruwe Capella-`.capx` of ongekuiste `.mxl` rechtstreeks “publiceren” |

## Volgorde (bestanden)

### Placeholder: ruw materiaal binnenhalen

> **Let op:** een generieke **opkuiser** (één traject voor Capella, PDF,
> `.mscz`, `.vsa`, …) wordt elders gebouwd. Tot die tijd is “binnenhalen”
> het vaste begin; daarna volg je nog de HOW’s onder
> [Partituur](../../partituur/) of [VSA](../../vsa/). Deze sectie krijgt
> dan haar definitieve vorm.

1. Kopieer het bestand naar
   `content-source\praktijk\oefenhoek\input\<herkomst>\`
   (of eerst `_inbox\` — die map gaat niet naar git). Laat de
   **originele bestandsnaam** staan. Herkomst-mappen:
   [Waar ligt wat](../../start/waar-ligt-wat/).
2. Open het Windows-opdrachtvenster in de repository-map `VSA-demo`.
3. Ververs de werkvoorraad:

```cmd
scripts\update-werkvoorraad.cmd
```

   Of draai `scripts\check.cmd` — die doet dezelfde update plus de rest
   van de site-keten.
4. Open `content-source\praktijk\oefenhoek\input\werkvoorraad.md`. Zoek
   de nieuwe rij. Vul kolom **Doel-id** in als je het bibliotheek-id kent
   (bijvoorbeeld `8-trisagion/8a-nederlands/hemelum`). Ken je het id
   niet? Laat de cel leeg en vraag na — **niet verzinnen**.
5. Pas **Koormap** of **Notitie** aan als dat nodig is. Kolommen *Stap*
   en *Volgende* vult het script; die niet met de hand “rechtzetten”.

### Klaar bestand opnemen

6. Zorg dat het bestand een bruikbare **basispartituur-`.mscz`**,
   **`.vsa`** of **`.print.mscz`** is (niet een ruwe Capella-file).
7. Neem op in de bibliotheek:

```cmd
scripts\bieb-accepteer.cmd
```

   Het script vraagt bibliotheek-id en bestand na (of je geeft die op de
   regel). Het maakt de mappen, zet `index.md` met shortcode `bieb`, en
   kopieert het bestand naar de **publicatiestam**-naam.
8. Daarna: het juiste publicatiespoor (PDF/Coria of print-PDF), daarna
   eventueel een [koormap](../../publiceren/1-bladermap/)-slot, daarna
   [Site-build](../site-build/).

Stapsgewijze HOW voor stap 7:
[Opnemen in de bibliotheek (Publiceren)](../../publiceren/1-opnemen-in-bibliotheek/).

## Automatisch (CI)

GitHub Actions **exporteert geen** MuseScore- of VSA-producten bij
opnemen. Wel controleren `check` / CI of de bibliotheekstructuur klopt
(`bibliotheek.py`, publicatiestatus, enz.). Nieuwe of gewijzigde
productbestanden moet jij lokaal maken en **meecommitten**.

## Handmatig

| Situatie | Commando | Man-page |
| --- | --- | --- |
| Werkvoorraad bijwerken | `scripts\update-werkvoorraad.cmd` | [update-werkvoorraad](../../scripts/update-werkvoorraad/) |
| Bestand in de bibliotheek zetten | `scripts\bieb-accepteer.cmd` | [bieb-accepteer](../../scripts/bieb-accepteer/) |
| Alles controleren vóór commit | `scripts\check.cmd --strict` | [check](../../scripts/check/) |

## Zie ook

- HOW: [Ruw materiaal binnenhalen (Partituur)](../../partituur/1-binnenhalen/)
  (doorverwijzing; canonieke plek is deze werktrajectpagina)
- HOW: [Opnemen (Publiceren)](../../publiceren/1-opnemen-in-bibliotheek/)
- [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/)
- Contract: `scripts\oefenhoek-product-contract.md` in `VSA-demo`

{{< navbuttons "Werktrajecten|/praktijk/handleiding/werktrajecten/" "Basispartituur|/praktijk/handleiding/werktrajecten/basispartituur/" >}}
