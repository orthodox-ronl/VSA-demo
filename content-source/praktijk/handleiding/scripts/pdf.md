---
title: "pdf"
linkTitle: "pdf"
weight: 50
---

# NAME

`scripts\pdf.cmd` — één Markdownbestand (met VSA) omzetten naar A4-PDF

# SYNOPSIS

```cmd
scripts\pdf.cmd <bestand.md> [-o uit.pdf] [--content-root DIR]
```

# DESCRIPTION

Maakt een A4-PDF van een Markdownbestand dat je opgeeft. Dat bestand mag
VSA-blokken, includes en paginascheidingen bevatten. Includes en SVG-rendering
lopen via `vsa pdf` (zelfde soort keten als bij build-markdown voor dat ene
bestand).

Gebruik `pdf` voor **willekeurige** bronbestanden. Voor het vaste demoblad van
de Tooling Demo bestaat een apart commando met vaste paden:
[demo-pdf](../demo-pdf/).

Validatiefouten tonen bestand, regel, kolom en code in hetzelfde formaat als
`check` / `vsa validate`.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `-o`, `--output FILE` | Pad van de uitvoer-PDF (default: `<stem>.pdf` in de huidige map) |
| `--content-root DIR` | Root voor catalogus-includes (`lokaal/`) |
| `--chrome PATH` | Edge/Chrome als auto-detectie faalt |

# EXAMPLES

Voorbeeld: een blad onder `content-source` naar een PDF in je huidige map:

```cmd
scripts\pdf.cmd content-source\praktijk\demo\assets\voorbeeld-blad.md -o mijn-blad.pdf --content-root content-source
```

# WHEN

Je wilt een koormap- of liturgieblad als PDF printen of delen, zonder Hugo.

# SEE ALSO

- [demo-pdf](../demo-pdf/)
- [check](../check/)
