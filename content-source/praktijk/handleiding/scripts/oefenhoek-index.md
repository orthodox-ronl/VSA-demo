---
title: "oefenhoek-index"
linkTitle: "oefenhoek-index"
weight: 140
---

# NAME

`scripts\oefenhoek-index.cmd` — bladermap-index strippen; optioneel SVG uit `.vsa`

# SYNOPSIS

```cmd
scripts\oefenhoek-index.cmd [--dry-run] [--svg] [--verbose]
```

# DESCRIPTION

Zonder flags: haalt auto-includes en score-shortcodes uit oefenhoek
bladermap-`index.md`. Frontmatter en eigen tekst blijven. Pagina’s met
`bieb` of `automatische_inhoud: false` blijven onaangeroerd. Widgets komen
uit de Hugo-layout of shortcode `bieb`.

Met `--svg`: schrijft SVG van lokale `.vsa` (geen basispartituur-`.mscz`;
`*.print.mscz` mag) naar `static\vsa\bladermap\` (na `vsa build-markdown`),
ook onder `bibliotheek\`.

Standaard alleen een samenvatting; `--verbose` toont elk pad.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--dry-run` | Toon wat de strip zou wijzigen |
| `--svg` | Schrijf SVG uit `.vsa` |
| `--verbose` | Detail per bestand |

# EXAMPLES

```cmd
scripts\oefenhoek-index.cmd --dry-run
scripts\oefenhoek-index.cmd --svg
```

# WHEN

Automatisch in `check` / `build` / `serve`. Handmatig: `--svg` na een
`.vsa`-edit zonder volle check, of `--dry-run` om te zien wat de strip doet.

# SEE ALSO

- [check](../check/)
- [vsa-products](../vsa-products/)
- Workflow: [VSA schrijven](../../vsa/1-vsa-schrijven/)
