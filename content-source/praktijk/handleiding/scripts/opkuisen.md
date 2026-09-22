---
title: "opkuisen"
linkTitle: "opkuisen"
weight: 80
---

# NAME

`scripts\opkuisen.cmd` — Capella/CapToMusic-`.mxl` inhoudelijk opschonen

# SYNOPSIS

```cmd
scripts\opkuisen.cmd <bron.mxl> [-o doel.mxl|doelmap]
```

# DESCRIPTION

**Opkuisen** betekent: de *muzikale en tekstuele inhoud* van een Capella- of
CapToMusic-`.mxl` opschonen. Het script maakt onder meer verborgen
reciteerkwarten zichtbaar, synchroniseert lettergrepen met noten, ruimt
titelrommel op en verwijdert lege maten. Het doet **geen** A4-pagina-layout,
geen PDF en geen Coria-export — dat is [layout](../layout/) en
[mscz-products](../mscz-products/).

Overschrijf het Capella-origineel in `oefenhoek\input\capella\` **niet**.
Schrijf het resultaat naar een map onder
`oefenhoek\input\_werk\<stam>\` met een bestandsnaam zonder spaties.
De **publicatiestam** is het bibliotheek-id met `-` tussen de drie lagen
(bijvoorbeeld id `8-trisagion/8a-nederlands/hemelum` → stam
`8-trisagion-8a-nederlands-hemelum`).

Python-implementatie: `scripts\cleanup_capella_mxl.py`. Dit commando zit
niet in `check` / `build` / `serve`.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `-o`, `--output` | Doel-`.mxl` of doelmap. Zonder `-o`: in-place alleen als de bestandsnaam al geen spaties heeft |

# EXAMPLES

Voorbeeld voor één Capella-bestand (paden zijn illustratief):

```cmd
scripts\opkuisen.cmd "content-source\praktijk\oefenhoek\input\capella\8a - 8-trisagion.mxl" -o content-source\praktijk\oefenhoek\input\_werk\8-trisagion-8a-nederlands-hemelum\8-trisagion-8a-nederlands-hemelum.mxl
```

# WHEN

Bij elke nieuwe Capella- of CapToMusic-`.mxl`, vóór [layout](../layout/).

Heb je een ruwe `.mscz` (bijvoorbeeld VOW): dit Capella-commando overslaan;
werk de checklist in MuseScore 4 af — zie
[Opkuisen](/praktijk/handleiding/partituur/2-opkuisen/).

# SEE ALSO

- [layout](../layout/)
- Workflow: [Opkuisen](/praktijk/handleiding/partituur/2-opkuisen/)
- Console: `scripts\h.cmd opkuisen`
