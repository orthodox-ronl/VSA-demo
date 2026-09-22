---
title: "mscz-products"
linkTitle: "mscz-products"
weight: 100
---

# NAME

`scripts\mscz-products.cmd` — PDF en Coria-`.mxl` maken bij een basispartituur-`.mscz`

# SYNOPSIS

```cmd
scripts\mscz-products.cmd [pad] [--force] [--dry-run]
```

# DESCRIPTION

Exporteert naast een **basispartituur-`.mscz`** de sibling-bestanden die
koorleden gebruiken: een A4-**PDF** (downloaden/printen) en een
**Coria-`.mxl`** (afspelen via de Oefenen-knop). Het script schrijft ook
herkomstinformatie (`partituur-sha256`, `generated-at`) in die producten.

Het zoekt basispartituur-`.mscz` onder het opgegeven pad (of, zonder pad,
onder `content-source`). Bestanden in `oefenhoek\input\` en namen die
eindigen op `.print.mscz` worden overgeslagen.

**Volgorde:** eerst [layout](../layout/), daarna eventueel een editslag in
MuseScore 4, daarna dit commando — niet meteen PDF maken als je nog gaat
editen. De pipeline roept `mscz-products` lokaal ook aan.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--force` | Bestaande PDF/MXL overschrijven |
| `--dry-run` | Alleen tonen wat er zou gebeuren |

# EXAMPLES

```cmd
scripts\mscz-products.cmd
scripts\mscz-products.cmd content-source\praktijk\oefenhoek\bibliotheek\8-trisagion --force
```

# WHEN

Als de basispartituur-`.mscz` inhoudelijk en qua layout klaar is voor
publicatie-PDF en Coria.

# SEE ALSO

- [layout](../layout/)
- Workflow: [PDF en Coria](/praktijk/handleiding/partituur/5-pdf-en-coria/)
- Bestand `scripts\oefenhoek-product-contract.md` in `VSA-demo`
