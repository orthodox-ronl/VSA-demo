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

Past de Oefenhoek-**basispartituur**-standaard toe: A4, fonts, reciteer-collaps
`||O||`, tempo, copyright, bibliotheek-id in colofon. Gangbare naam:
**layouten**; contractterm: **normaliseren**.

- Invoer `.mxl` (na [opkuisen](../opkuisen/)): MuseScore 4 importeert; zet `-o`
  naar `_werk\<stam>\<stam>.mscz` (geen spaties).
- Invoer `.mscz`: zonder `-o` **in-place** (idempotent — opnieuw na elke
  editslag in MuseScore).
- Weigert `*.print.mscz` (printvel: zie [Print-.mscz](../../partituur/7-print-mscz/)).

Python-implementatie: `scripts\apply_mscz_layout.py`. Norm:
`scripts\mscz-partituur-contract.md` in `VSA-demo`.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `-o`, `--output` | Doel-`.mscz` |
| `--id` | Bibliotheek-id `zangstuk/variant/uitvoeringsvorm` (anders uit pad onder `bibliotheek/`) |
| `--no-extenders` | Geen lyric-underlines; zet meta `vsaNoLyricExtenders` |

# EXAMPLES

Van opgekuiste `.mxl`:

```cmd
scripts\layout.cmd content-source\praktijk\oefenhoek\input\_werk\STAM\STAM.mxl -o content-source\praktijk\oefenhoek\input\_werk\STAM\STAM.mscz
```

Opnieuw op bestaande basispartituur:

```cmd
scripts\layout.cmd pad\naar\bestand.mscz
```

# WHEN

Na opkuisen, of meteen als de inhoud van een ruwe `.mscz` al klopt. Opnieuw na
elke inhoudelijke editslag, vóór [mscz-products](../mscz-products/).

# SEE ALSO

- [opkuisen](../opkuisen/)
- [mscz-products](../mscz-products/)
- [ensure-bibliotheek-id](../ensure-bibliotheek-id/)
- Workflow: [Standaard-.mscz](../../partituur/3-standaard-mscz/)
- Console: `scripts\h.cmd layout`
