---
title: "demo-pdf"
linkTitle: "demo-pdf"
weight: 60
---

# NAME

`scripts\demo-pdf.cmd` — demo-PDF `voorbeeld-blad.pdf` bouwen

# SYNOPSIS

```cmd
scripts\demo-pdf.cmd
```

# DESCRIPTION

Bouwt `static\demo\voorbeeld-blad.pdf` uit het demo-Markdownblad. Wrapper om
`scripts\pdf.cmd` met vaste paden.

`check` / `build` / `serve` (met build) controleren of die PDF niet ouder is
dan `voorbeeld-blad.md` en `voorbeeld.vsa`. Bij veroudering: fout + dit
commando als herstel.

# WHEN

Na wijziging van
`content-source\praktijk\demo\assets\voorbeeld-blad.md` of `voorbeeld.vsa`,
vóór je commit of `serve` opnieuw draait.

# SEE ALSO

- [pdf](../pdf/)
- Demo-pagina op de site: Markdown naar PDF
