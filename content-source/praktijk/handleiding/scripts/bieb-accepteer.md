---
title: "bieb-accepteer"
linkTitle: "bieb-accepteer"
weight: 160
---

# NAME

`scripts\bieb-accepteer.cmd` — partituur opnemen in de Oefenhoek-bibliotheek

# SYNOPSIS

```cmd
scripts\bieb-accepteer.cmd [id] [bestand...] [opties]
```

# DESCRIPTION

Neemt een klaar bestand op in de **bibliotheek** (de catalogus onder
`oefenhoek\bibliotheek\`), onder een bibliotheek-id van drie lagen:
`zangstuk/variant/uitvoeringsvorm`. Toegestaan: basispartituur-`.mscz`,
`.vsa`, `.print.mscz`, of `.tekstblad.md` (optioneel sibling-`.pdf` / `.mxl`).
Bij `.tekstblad.md` zet het script indien nodig frontmatter
`build: render: never` zodat de bron geen Hugo-pagina wordt.

Het script maakt ontbrekende `_index.md` / `index.md` met shortcode `bieb`
en hernoemt naar de publicatiestam. Capella-bronformats en een kale
Capella-`.mxl` worden geweigerd — eerst [opkuisen](../opkuisen/) /
[layout](../layout/). Bij `.vsa` draait `vsa validate` (tenzij
`--skip-vsa-validate`). Default `publicatiestatus: reviewable` (`voorzien`
bij `--stub`). Status `productie` alleen met `--force`.

Ontbreken id of bestand, dan vraagt het script die interactief. Typ `?`
voor uitleg, daarna opnieuw invullen. Zonder argumenten: beide vragen.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--title` | Titel override |
| `--status` | Publicatiestatus |
| `--stub` | Lege leaf (`voorzien`) |
| `--move` | Bronbestand verplaatsen in plaats van kopiëren |
| `--force` | Overschrijven / `productie` toestaan |
| `--dry-run` | Alleen tonen |
| `--skip-vsa-validate` | Geen `vsa validate` |
| `--artefacten-handmatig` | Zet `artefacten_handmatig: true` |

# EXAMPLES

```cmd
scripts\bieb-accepteer.cmd
scripts\bieb-accepteer.cmd 8-trisagion/8a-nederlands/hemelum pad\naar\bestand.mscz --dry-run
```

# WHEN

Als de partituur klaar is om in de catalogus te staan (na opkuisen /
normaliseren, of na een werkende `.vsa`). Daarna koormap +
`check --strict`.

# SEE ALSO

- Workflow: [Opnemen in de bibliotheek](/praktijk/handleiding/publiceren/1-opnemen-in-bibliotheek/)
- [check](../check/)
- Console: `scripts\h.cmd bieb-accepteer`
