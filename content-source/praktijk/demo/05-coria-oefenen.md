---
title: "Oefenen met Coria"
linkTitle: "Oefenen met Coria"
weight: 50
aliases:
  - /praktijk/demo/03-coria-oefenen/
---

# Oefenen met Coria

[Coria](https://coria.nl) is een **online oefenomgeving voor zangers**. Je
opent een melodie in de browser, hoort hoe die klinkt, en kunt passages
herhalen of een partij volgen — zonder app-installatie. Het is bedoeld om
thuis of in de koorzaal een zangstuk in het gehoor te krijgen, naast de
geschreven notatie.

Op deze site hoort daar een **oefenknop** bij: die opent het stuk meteen in
Coria. Bezoekers hoeven geen MusicXML te downloaden of zelf te importeren
(dat kan wél; zie [VSA naar MusicXML](../04-vsa-naar-mxl/)).

**Wat je hier leert:** die knop in Markdown zetten, gevoed door een
`.coria.html` naast het `.vsa`-bestand.

## Benodigd

- `assets\voorbeeld.vsa`
- `assets\voorbeeld.coria.html` (zelfde bestandsnaam-stam,zelfde map)

## In Markdown

```markdown
:::include coria "assets/voorbeeld.vsa" label="Oefenen in Coria":::
```

Generate: `scripts\check.cmd --skip-hugo`.

## Resultaat

:::include coria "assets/voorbeeld.vsa" label="Oefenen in Coria":::

## MXL-download versus Coria-oefenlink

|           | MusicXML-download             | Coria-oefenlink                |
| --------- | ----------------------------- | ------------------------------ |
| Bron      | `.vsa` (build maakt `.mxl`)   | `.vsa` + sibling `.coria.html` |
| Bezoeker  | Downloaden en zelf importeren | Direct oefenen via de knop     |
| Directive | `:::include mxl …:::`         | `:::include coria …:::`        |

Zonder `.coria.html` kan `include coria` terugvallen op een MXL-URL. Voor
deze demo hoort de HTML-sibling erbij.
