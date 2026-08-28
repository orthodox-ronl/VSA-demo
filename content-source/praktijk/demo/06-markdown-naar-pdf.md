---
title: "Markdown naar PDF"
linkTitle: "Markdown naar PDF"
weight: 60
aliases:
  - /praktijk/demo/05-markdown-naar-pdf/
---

# Markdown naar PDF

**Wat je hier leert:** van een Markdownblad (tekst, VSA, includes,
paginascheidingen) een A4-PDF maken. De site-build maakt de PDF niet
automatisch; wel controleert `check` / `serve` of de demo-PDF up-to-date is.

## Bron

`assets\voorbeeld-blad.md` — niet als Hugo-pagina gepubliceerd; alleen bron
voor de PDF. Gebruikt o.a. `::: vsa-notatie` en `:::include svg` (zie de
SVG-demootjes voor die onderwerpen apart).

{{< include-source src="assets/voorbeeld-blad.md" lang="markdown" >}}

- `:::pagebreak:::` forceert een nieuw A4-blad.
- `:::print-only:::` … `:::end-print-only:::` verschijnt wel in de PDF,
  niet op de website.
- Een Coria-oefenlink in de PDF is een gewone markdown-link met een
  **absoluut** adres op de gepubliceerde site (zie het blad). De directive
  `:::include coria` is voor de website; in PDF-export wordt die
  weggelaten — een relatieve site-knop werkt niet vanuit een PDF-bestand.

## Resultaat

{{< pdf-preview src="demo/voorbeeld-blad.pdf" label="voorbeeld-blad.pdf — download" height="560" >}}

## Commando

Na wijziging van het blad (of `voorbeeld.vsa`):

```cmd
scripts\demo-pdf.cmd
```

Dat schrijft `static\demo\voorbeeld-blad.pdf`. Hard refresh in de browser
als de oude PDF gecached blijft.

Is de PDF ouder dan de bronnen, dan faalt `check` / `serve` met precies dit
commando als herstel.

Generiek (andere bestanden): `scripts\pdf.cmd` — zie `scripts\h.cmd pdf`.

| Probleem | Controle |
| -------- | -------- |
| Include niet gevonden | `--content-root` naar `content-source` (zit in `demo-pdf.cmd`) |
| Geen browser | Edge/Chrome; of `CHROME_PATH` / `--chrome` |
| Validatiefout | Zelfde meldingen als `vsa validate` |

Zie ook: `scripts\h.cmd demo-pdf`.
