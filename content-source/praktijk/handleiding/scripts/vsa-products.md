---
title: "vsa-products"
linkTitle: "vsa-products"
weight: 110
---

# NAME

`scripts\vsa-products.cmd` — Coria-`.vsa.mxl` uit bibliotheek-`.vsa`

# SYNOPSIS

```cmd
scripts\vsa-products.cmd [pad] [--force] [--dry-run]
```

# DESCRIPTION

Maakt sibling Coria-`.vsa.mxl` bij bibliotheek-`.vsa` (syllabify in temp,
`vsa musicxml` playback, sanitize, `vsa-source-sha256`). Slaat
`artefacten_handmatig: true` over. Zonder pad: `oefenhoek\bibliotheek`.

Pipeline roept dit lokaal aan. `check_vsa_products.py` is op `main` streng.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--force` | Bestaande `.vsa.mxl` overschrijven |
| `--dry-run` | Alleen planning tonen |

# WHEN

Na een `.vsa`-wijziging, of als de Oefenen-knop / `check` een stale `.vsa.mxl`
meldt.

# SEE ALSO

- [oefenhoek-index](../oefenhoek-index/) (`--svg` voor plaatjes)
- Workflow: [VSA schrijven](../../vsa/1-vsa-schrijven/)
- `scripts\oefenhoek-product-contract.md`
