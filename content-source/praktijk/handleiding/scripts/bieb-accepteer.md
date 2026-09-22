---
title: "bieb-accepteer"
linkTitle: "bieb-accepteer"
weight: 160
---

# NAME

`scripts\bieb-accepteer.cmd` — partituur opnemen in de bibliotheek

# SYNOPSIS

```cmd
scripts\bieb-accepteer.cmd [id] [bestand...] [opties]
```

# DESCRIPTION

Neemt een basispartituur-`.mscz`, `.vsa` of `.print.mscz` op onder
`oefenhoek\bibliotheek\<zangstuk>\<variant>\<uitvoeringsvorm>\`. Maakt
ontbrekende `_index.md` / `index.md` met shortcode `bieb`, hernoemt naar de
publicatiestam.

Weigert Capella-bronformats en een kale Capella-`.mxl` (eerst
[opkuisen](../opkuisen/) / [layout](../layout/)). Bij `.vsa`: `vsa validate`
(tenzij `--skip-vsa-validate`). Default `publicatiestatus: reviewable`
(`voorzien` bij `--stub`). Geen `productie` zonder `--force`.

Ontbrekende id of bestand: interactief gevraagd. Typ `?` voor uitleg, daarna
opnieuw invullen. Zonder argumenten: beide vragen.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--title` | Titel override |
| `--status` | Publicatiestatus |
| `--stub` | Lege leaf (`voorzien`) |
| `--move` | Bronbestand verplaatsen i.p.v. kopiëren |
| `--force` | Overschrijven / productie toestaan |
| `--dry-run` | Alleen tonen |
| `--skip-vsa-validate` | Geen `vsa validate` |
| `--artefacten-handmatig` | Zet `artefacten_handmatig: true` |

# EXAMPLES

```cmd
scripts\bieb-accepteer.cmd
scripts\bieb-accepteer.cmd 8-trisagion/8a-nederlands/hemelum pad\naar\bestand.mscz --dry-run
```

# WHEN

Als de partituur klaar is om in de bibliotheek te staan (na opkuisen /
normaliseren of na een werkende `.vsa`). Daarna koormap + `check --strict`.

# SEE ALSO

- Workflow: [Opnemen in de bibliotheek](../../publiceren/1-opnemen-in-bibliotheek/)
- [check](../check/)
- Console: `scripts\h.cmd bieb-accepteer`
