---
title: "check"
linkTitle: "check"
weight: 20
---

# NAME

`scripts\check.cmd` — preflight / CI-spiegel

# SYNOPSIS

```cmd
scripts\check.cmd [--strict] [--external] [--skip-hugo]
```

# DESCRIPTION

`check` draait lokaal de blocking pipeline die CI ook doet: sync zondag →
oefenhoek-index → validate → generate (markdown/SVG/MXL) → Coria-kuis → Hugo →
interne links. Het is een wrapper om `scripts\_pipeline.cmd`.

**Preflight** betekent: controle vóór je commit. **CI-spiegel** met `--strict`
betekent dezelfde strengheid als GitHub Actions (ook VSA-warnings laten falen).

MuseScore-PDF en Coria-`.mxl` uit basispartituur horen bij
[mscz-products](../mscz-products/), niet bij deze keten.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--strict` | Faal ook op VSA-warnings (CI doet dit standaard) |
| `--external` | Check ook externe http(s)-links (kan flaky zijn) |
| `--skip-hugo` | Stop na sync + validate + generate (geen Hugo/linkcheck) |

# EXAMPLES

```cmd
scripts\check.cmd --strict
scripts\check.cmd --skip-hugo
```

# WHEN

Altijd vóór committen of pushen: `scripts\check.cmd --strict`. Tussendoor op
VSA itereren: `--skip-hugo`.

# SEE ALSO

- [serve](../serve/)
- [Wat heb je nodig](../../start/wat-heb-je-nodig/)
- [Status en check](../../publiceren/2-status-en-check/)
