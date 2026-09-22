---
title: "vsa-products"
linkTitle: "vsa-products"
weight: 110
---

# NAME

`scripts\vsa-products.cmd` — Coria-`.vsa.mxl` maken bij een bibliotheek-`.vsa`

# SYNOPSIS

```cmd
scripts\vsa-products.cmd [pad] [--force] [--dry-run]
```

# DESCRIPTION

Maakt naast een bibliotheek-`.vsa` het siblingbestand `{stam}.vsa.mxl` voor
Coria-afspelen (Oefenen-knop). Het script syllabificeert in een tijdelijk
bestand, exporteert via `vsa musicxml`, saniteert voor Coria en zet een
`vsa-source-sha256`-stempel.

Mappen met `artefacten_handmatig: true` in de frontmatter worden
overgeslagen. Zonder pad werkt het onder `oefenhoek\bibliotheek`.

De pipeline roept dit lokaal aan. Op branch `main` is de bijbehorende check
streng.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--force` | Bestaande `.vsa.mxl` overschrijven |
| `--dry-run` | Alleen tonen wat er zou gebeuren |

# WHEN

Na een wijziging aan een `.vsa` in de bibliotheek, of als `check` / de
Oefenen-knop meldt dat de `.vsa.mxl` verouderd is.

# SEE ALSO

- [oefenhoek-index](../oefenhoek-index/) (`--svg` voor het plaatje op de pagina)
- Workflow: [VSA schrijven](/praktijk/handleiding/vsa/1-vsa-schrijven/)
- Bestand `scripts\oefenhoek-product-contract.md` in `VSA-demo`
