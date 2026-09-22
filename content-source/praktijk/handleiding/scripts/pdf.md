---
title: "pdf"
linkTitle: "pdf"
weight: 50
---

# NAME

`scripts\pdf.cmd` — Markdown + VSA naar A4-PDF

# SYNOPSIS

```cmd
scripts\pdf.cmd <bestand.md> [-o uit.pdf] [--content-root DIR]
```

# DESCRIPTION

Maakt een A4-PDF van een Markdownbestand met VSA-blokken. Includes,
pagebreaks, print-only en SVG-rendering lopen via `vsa pdf` (zelfde keten als
build-markdown voor dat ene bestand).

Validatiefouten tonen bestand, regel, kolom en code in hetzelfde formaat als
`check` / `vsa validate`.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `-o`, `--output FILE` | Uitvoer-PDF (default: `<stem>.pdf` in de huidige map) |
| `--content-root DIR` | Root voor catalogus-includes (`lokaal/`) |
| `--chrome PATH` | Edge/Chrome als auto-detectie faalt |

# WHEN

Een koormap- of liturgieblad uit `content-source` printen, zonder Hugo.

# SEE ALSO

- [demo-pdf](../demo-pdf/)
- [check](../check/)
