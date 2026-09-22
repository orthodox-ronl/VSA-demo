---
title: "mscz-products"
linkTitle: "mscz-products"
weight: 100
---

# NAME

`scripts\mscz-products.cmd` — PDF + Coria-`.mxl` uit basispartituur-`.mscz`

# SYNOPSIS

```cmd
scripts\mscz-products.cmd [pad] [--force] [--dry-run]
```

# DESCRIPTION

Exporteert sibling-PDF en Coria-`.mxl` bij basispartituur-`.mscz` (niet
`oefenhoek\input`, niet `*.print.mscz`). Schrijft provenance
(`partituur-sha256`, `generated-at`).

Zonder pad: onder `content-source`. Pipeline roept dit lokaal aan. Eerst
[layout](../layout/), eventueel editslag in MuseScore, daarna dit script.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--force` | Bestaande producten overschrijven |
| `--dry-run` | Alleen planning tonen |

# EXAMPLES

```cmd
scripts\mscz-products.cmd
scripts\mscz-products.cmd content-source\praktijk\oefenhoek\bibliotheek\8-trisagion --force
```

# WHEN

Als de basispartituur-`.mscz` klaar is voor publicatie-PDF en Coria — na
layout en MuseScore-review, niet meteen na de eerste layout-run als je nog
gaat editen.

# SEE ALSO

- [layout](../layout/)
- Workflow: [PDF en Coria](../../partituur/5-pdf-en-coria/)
- `scripts\oefenhoek-product-contract.md`
