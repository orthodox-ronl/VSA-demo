---
title: "tekstblad-products"
linkTitle: "tekstblad-products"
weight: 115
---

# NAME

`scripts\tekstblad-products.cmd` — A4-PDF maken bij een bibliotheek-`.tekstblad.md`

# SYNOPSIS

```cmd
scripts\tekstblad-products.cmd [pad] [--force] [--dry-run]
```

# DESCRIPTION

Zoekt canonieke bronnen `{stam}.tekstblad.md` onder het opgegeven pad
(of, zonder pad, onder `oefenhoek\bibliotheek\`) en schrijft ernaast
`{stam}.tekstblad.pdf` via `vsa pdf` (zelfde renderer als
[pdf](../pdf/)). In de PDF komt een stamp (`vsa-source-sha256`,
`vsa-source-kind=tekstblad`) zodat `check` kan zien of de PDF nog bij de
bron hoort.

Bestanden in `oefenhoek\input\` en mappen met
`artefacten_handmatig: true` worden overgeslagen. Alias-varianten ook.

**Waartoe:** liturgische tekst of dialoog in de bibliotheek als downloadbaar
en printbaar blad tonen via shortcode `bieb` — parallel aan
`mscz-products` / `vsa-products`.

De site-build op GitHub **genereert** deze PDF’s niet opnieuw; jij draait
dit commando lokaal en commit bron + PDF samen. Lokale `check` /
`build` / `serve` vernieuwen stale PDF’s wel (Chrome of Edge nodig).

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--force` | Bestaande PDF overschrijven |
| `--dry-run` | Alleen tonen wat er zou gebeuren |

# EXAMPLES

```cmd
scripts\tekstblad-products.cmd
scripts\tekstblad-products.cmd content-source\praktijk\oefenhoek\bibliotheek\7d-dialoog-met-diaken --force
```

# WHEN

Als de `.tekstblad.md` inhoudelijk klaar is voor publicatie-PDF, of als
`check` klaagt dat de PDF ontbreekt of verouderd is.

# SEE ALSO

- [pdf](../pdf/) — generieke markdown → PDF
- Workflow: [Tekstblad](/praktijk/handleiding/werktrajecten/tekstblad/)
- Bestand `scripts\oefenhoek-product-contract.md` in `VSA-demo`
