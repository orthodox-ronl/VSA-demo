---
title: "opkuisen"
linkTitle: "opkuisen"
weight: 80
---

# NAME

`scripts\opkuisen.cmd` — Capella/CapToMusic-`.mxl` inhoudelijk opkuisen

# SYNOPSIS

```cmd
scripts\opkuisen.cmd <bron.mxl> [-o doel.mxl|doelmap]
```

# DESCRIPTION

**Opkuisen** betekent hier: de *inhoud* van een Capella- of CapToMusic-`.mxl`
opschonen (lagen 1–3): reciteerkwarten zichtbaar maken, lettergreep↔noot,
titelrommel weg, lege maten, sleutels bij twee balken. Geen A4-layout, geen
PDF, geen Coria — dat is [layout](../layout/) en [mscz-products](../mscz-products/).

Het Capella-origineel in `oefenhoek\input\capella\` overschrijf je **niet**.
Schrijf naar `input\_werk\<stam>\<stam>.mxl` (publicatiestam zonder spaties).

Python-implementatie: `scripts\cleanup_capella_mxl.py`. Niet in
`check` / `build` / `serve`.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `-o`, `--output` | Doel-`.mxl` of doelmap. Zonder `-o`: in-place alleen als de bestandsnaam al geen spaties heeft |

# EXAMPLES

```cmd
scripts\opkuisen.cmd "content-source\praktijk\oefenhoek\input\capella\8a - 8-trisagion.mxl" -o content-source\praktijk\oefenhoek\input\_werk\8-trisagion-8a-nederlands-hemelum\8-trisagion-8a-nederlands-hemelum.mxl
```

`STAM` = de drie lagen van het bibliotheek-id met `-` ertussen, bijvoorbeeld
`8-trisagion/8a-nederlands/hemelum` → `8-trisagion-8a-nederlands-hemelum`.

# WHEN

Bij elke nieuwe Capella-/CapToMusic-`.mxl`, vóór [layout](../layout/).

Ruwe `.mscz` (VOW e.d.): dit commando overslaan; checklist in MuseScore 4 —
zie workflow [Opkuisen](../../partituur/2-opkuisen/).

# SEE ALSO

- [layout](../layout/)
- Workflow: [Opkuisen](../../partituur/2-opkuisen/)
- Console: `scripts\h.cmd opkuisen`
