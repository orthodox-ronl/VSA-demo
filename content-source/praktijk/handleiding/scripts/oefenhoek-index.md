---
title: "oefenhoek-index"
linkTitle: "oefenhoek-index"
weight: 140
---

# NAME

`scripts\oefenhoek-index.cmd` — bladermap-markdown opschonen; optioneel SVG uit `.vsa`

# SYNOPSIS

```cmd
scripts\oefenhoek-index.cmd [--dry-run] [--svg] [--verbose]
```

# DESCRIPTION

Zonder flags haalt dit commando automatische includes en score-shortcodes
uit oefenhoek bladermap-`index.md`. Frontmatter en tekst die jij zelf
schreef blijven staan. Pagina’s met shortcode `bieb` of met
`automatische_inhoud: false` worden niet aangepast. De partituurweergave
komt uit de Hugo-layout of uit `bieb`.

Met `--svg` schrijft het script SVG-plaatjes van lokale `.vsa`-bestanden
(zonder basispartituur-`.mscz` ernaast; een `.print.mscz` mag) naar
`static\vsa\bladermap\`, ook onder `bibliotheek\`. Dat gebeurt normaal
tijdens `check` / `build` / `serve` (niet bij `serve --no-build`).

Standaard zie je alleen een samenvatting; `--verbose` toont elk pad.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--dry-run` | Toon wat de strip zou wijzigen, zonder te schrijven |
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
- Workflow: [VSA schrijven](/praktijk/handleiding/vsa/1-vsa-schrijven/)
