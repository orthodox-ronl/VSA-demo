---
title: "demo-pdf"
linkTitle: "demo-pdf"
weight: 60
---

# NAME

`scripts\demo-pdf.cmd` — demoblad-PDF voor de Tooling Demo vernieuwen

# SYNOPSIS

```cmd
scripts\demo-pdf.cmd
```

# DESCRIPTION

Dit commando hoort bij de **Tooling Demo** op de site (sectie «Markdown naar
PDF»). Het maakt opnieuw het A4-PDF-bestand
`static\demo\voorbeeld-blad.pdf` uit de bron
`content-source\praktijk\demo\assets\voorbeeld-blad.md` (Markdown met
VSA-blokken; die bron wordt zelf niet als Hugo-pagina gepubliceerd). Het
script roept intern `scripts\pdf.cmd` aan met die vaste paden.

**Waartoe:** de demopagina toont die PDF in de browser. Daarnaast controleren
`check`, `build` en `serve` (met build) of `voorbeeld-blad.pdf` niet ouder is
dan `voorbeeld-blad.md` en het meegeleverde `voorbeeld.vsa`. Is de PDF
verouderd, dan faalt die controle en is `demo-pdf` het herstelcommando uit
de foutmelding.

# EXAMPLES

Na een wijziging aan de bron (voorbeeldpaden hierboven):

```cmd
scripts\demo-pdf.cmd
```

# WHEN

Nadat je
`content-source\praktijk\demo\assets\voorbeeld-blad.md` of het bijbehorende
`voorbeeld.vsa` hebt aangepast, en vóór je opnieuw `check` of `serve` draait
of commit.

# SEE ALSO

- [pdf](../pdf/) — generiek PDF-commando met zelf gekozen paden
- Site: [Markdown naar PDF](/praktijk/demo/06-markdown-naar-pdf/)
