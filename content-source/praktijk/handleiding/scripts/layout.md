---
title: "layout"
linkTitle: "layout"
weight: 90
---

# NAME

`scripts\layout.cmd` — basispartituur-standaard toepassen (normaliseren / layouten)

# SYNOPSIS

```cmd
scripts\layout.cmd <bestand.mscz|.mxl> [-o doel.mscz] [--id ID] [--no-extenders]
```

# DESCRIPTION

Past de Oefenhoek-**basispartituur**-standaard toe: A4-papier, fonts,
reciteertoon-codering (`||O||`), tempo, copyrightvelden en (in de
bibliotheek) de colofonregel met bibliotheek-id. In het dagelijks taalgebruik
heet deze stap vaak **layouten**; de contractterm is **normaliseren**.

- Invoer is een opgekuiste `.mxl` (na [opkuisen](../opkuisen/)): MuseScore 4
  importeert het bestand; zet `-o` naar een `.mscz` zonder spaties in de
  naam (meestal onder `input\_werk\<stam>\`).
- Invoer is al een `.mscz`: zonder `-o` wijzigt het script het bestand
  **in-place**. Opnieuw draaien mag en hoort na elke inhoudelijke editslag
  in MuseScore.
- Bestanden die eindigen op `.print.mscz` worden geweigerd (printvel:
  [Print-.mscz](/praktijk/handleiding/partituur/7-print-mscz/)).

Python-implementatie: `scripts\apply_mscz_layout.py`. Technische norm:
`scripts\mscz-partituur-contract.md` in de repository-map `VSA-demo`.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `-o`, `--output` | Pad van de doel-`.mscz` |
| `--id` | Bibliotheek-id `zangstuk/variant/uitvoeringsvorm` (anders afgeleid uit het pad onder `bibliotheek/`) |
| `--no-extenders` | Geen lyric-underlines; zet meta `vsaNoLyricExtenders` |

# EXAMPLES

Van een opgekuiste `.mxl` naar een basispartituur-`.mscz` (stam is
illustratief):

```cmd
scripts\layout.cmd content-source\praktijk\oefenhoek\input\_werk\STAM\STAM.mxl -o content-source\praktijk\oefenhoek\input\_werk\STAM\STAM.mscz
```

Opnieuw op een bestaande basispartituur na een editslag in MuseScore:

```cmd
scripts\layout.cmd pad\naar\bestand.mscz
```

# WHEN

Na opkuisen, of meteen als de inhoud van een ruwe `.mscz` al klopt. Opnieuw
na elke inhoudelijke editslag, vóór [mscz-products](../mscz-products/).

# SEE ALSO

- [opkuisen](../opkuisen/)
- [mscz-products](../mscz-products/)
- [ensure-bibliotheek-id](../ensure-bibliotheek-id/)
- Workflow: [Standaard-.mscz](/praktijk/handleiding/partituur/3-standaard-mscz/)
- Console: `scripts\h.cmd layout`
