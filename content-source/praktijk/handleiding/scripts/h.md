---
title: "h"
linkTitle: "h"
weight: 10
---

# NAME

`scripts\h.cmd` — hulp in het opdrachtvenster: catalogus of korte man-page

# SYNOPSIS

```cmd
scripts\h.cmd
scripts\h.cmd <naam>
scripts\h.cmd -h
```

Met `.\scripts` op PATH kun je ook `h` of `h check` typen.

# DESCRIPTION

Zonder argument toont `h` een korte lijst van alle gebruikerscommando’s
(`.cmd`) die bij deze repository horen. Met een exacte naam (bijvoorbeeld
`check`, `opkuisen` of `layout`) print het opdrachtvenster een korte
man-page: doel, opties en wanneer je het gebruikt.

Met een onbekende of gedeeltelijke tekst krijg je een gefilterde lijst, of
een foutmelding met bekende namen.

De console-tekst is bewust kort (alleen eenvoudige tekens). De **uitgebreide**
uitleg staat in deze handleiding-sectie [Scripts](../).

# EXAMPLES

Voorbeelden (niet de enige geldige namen):

```cmd
scripts\h.cmd
scripts\h.cmd opkuisen
scripts\h.cmd layout
```

# WHEN

Als je de naam van een script niet meer weet, of even de opties wilt zien
zonder de browser te openen.

# SEE ALSO

- [Script-referentie](../)
- Bestand `scripts\README.md` in de repository-map `VSA-demo`
