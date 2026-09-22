---
title: "check"
linkTitle: "check"
weight: 20
---

# NAME

`scripts\check.cmd` — controleren of de repository klaar is om te delen

# SYNOPSIS

```cmd
scripts\check.cmd [--strict] [--external] [--skip-hugo]
```

# DESCRIPTION

`check` draait lokaal de controles die ook op GitHub lopen: sync van
zondag-materiaal, oefenhoek-index, VSA-validatie, genereren van markdown/SVG,
Coria-controles, Hugo-build en interne linkcontrole. Het is een wrapper om
`scripts\_pipeline.cmd`.

**Vóór commit** (alles streng, zoals CI): gebruik `--strict`. Dat betekent:
ook VSA-waarschuwingen laten falen, niet alleen harde fouten.

MuseScore-PDF’s en Coria-`.mxl` uit een basispartituur maak je apart met
[mscz-products](../mscz-products/); die stap zit niet in `check`.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--strict` | Faal ook op VSA-waarschuwingen (GitHub Actions doet dit standaard) |
| `--external` | Controleer ook links naar internet (kan soms flaky zijn) |
| `--skip-hugo` | Stop na sync, validatie en generate; geen Hugo en geen linkcheck |

# EXAMPLES

```cmd
scripts\check.cmd --strict
scripts\check.cmd --skip-hugo
```

# WHEN

Altijd vóór je commit of push: `scripts\check.cmd --strict`. Tussendoor
alleen aan VSA-bestanden werken: `--skip-hugo` is sneller.

# SEE ALSO

- [serve](../serve/)
- [Wat heb je nodig](/praktijk/handleiding/start/wat-heb-je-nodig/)
- [Status en check](/praktijk/handleiding/publiceren/2-status-en-check/)
