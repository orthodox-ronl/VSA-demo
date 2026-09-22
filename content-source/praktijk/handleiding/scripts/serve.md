---
title: "serve"
linkTitle: "serve"
weight: 40
---

# NAME

`scripts\serve.cmd` — lokale Hugo-preview

# SYNOPSIS

```cmd
scripts\serve.cmd [--no-build]
```

# DESCRIPTION

Start de Hugo-development server op **http://127.0.0.1:18731/**. Poort **18731**,
niet 1313 (1313 is lokaal gereserveerd).

Standaard: eerst de pipeline (sync/validate/generate), daarna de server.
Validate zonder `--strict` (snellere preview). Met `--no-build`: alleen
Coria-fingerprints + server; daarvoor moet `generated\content` al bestaan
(bijvoorbeeld na `check.cmd --strict`).

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--no-build` | Sla sync/validate/generate over; wel Coria-fingerprints |

# EXAMPLES

```cmd
scripts\check.cmd --strict
scripts\serve.cmd --no-build
```

Open daarna http://127.0.0.1:18731/ in de browser.

# WHEN

Browser-preview tijdens beheerwerk. CI-gelijk: eerst `check --strict`, dan
`serve --no-build`.

# SEE ALSO

- [check](../check/)
- [Wat heb je nodig](../../start/wat-heb-je-nodig/)
