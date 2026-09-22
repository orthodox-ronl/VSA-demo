---
title: "h"
linkTitle: "h"
weight: 10
---

# NAME

`scripts\h.cmd` — catalogus of korte man-page per script

# SYNOPSIS

```cmd
scripts\h.cmd
scripts\h.cmd <naam>
scripts\h.cmd -h
```

Met `.\scripts` op PATH: `h` of `h check`.

# DESCRIPTION

Zonder argument toont `h` een korte catalogus van alle gebruikers-`.cmd`-scripts.
Met een exacte scriptnaam (bijvoorbeeld `check`, `opkuisen`, `layout`) print
het opdrachtvenster een korte man-page: doel, opties, wanneer.

Met een onbekende of gedeeltelijke tekst krijg je een gefilterde lijst, of een
foutmelding met bekende namen.

De **uitgebreide** man-pages staan in deze handleiding-sectie
[Scripts](../). Console-`h` is bewust kort (ASCII, snel te lezen in `cmd`).

# EXAMPLES

```cmd
scripts\h.cmd
scripts\h.cmd bootstrap
scripts\h.cmd opkuisen
scripts\h.cmd layout
```

# WHEN

Als je de naam van een script niet meer weet, of even de opties wilt zien
zonder de browser te openen.

# SEE ALSO

- [Script-referentie](../)
- Bestand `scripts\README.md` in `VSA-demo`
