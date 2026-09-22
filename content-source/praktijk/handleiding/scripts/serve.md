---
title: "serve"
linkTitle: "serve"
weight: 40
---

# NAME

`scripts\serve.cmd` — lokale website-preview in de browser

# SYNOPSIS

```cmd
scripts\serve.cmd [--no-build]
```

# DESCRIPTION

Start de Hugo-development server. Open daarna in je browser
**http://127.0.0.1:18731/**. Gebruik niet poort **1313**; die poort is lokaal
voor iets anders gereserveerd.

Standaard draait `serve` eerst de build-keten (sync, validatie, generate) en
start daarna de server. Validatie is dan sneller dan bij `check --strict`
(zonder `--strict`).

Met `--no-build` slaat `serve` die keten over en start alleen de server
(plus Coria-fingerprints). Daarvoor moet `generated\content` al bestaan —
bijvoorbeeld na een geslaagde `check.cmd --strict`.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--no-build` | Geen sync/validate/generate; wel Coria-fingerprints + server |

# EXAMPLES

Aanbevolen volgorde vóór een commit-achtige preview:

```cmd
scripts\check.cmd --strict
scripts\serve.cmd --no-build
```

# WHEN

Als je in de browser wilt zien hoe de Oefenhoek en de handleiding eruitzien
tijdens beheerwerk.

# SEE ALSO

- [check](../check/)
- [Wat heb je nodig](/praktijk/handleiding/start/wat-heb-je-nodig/)
