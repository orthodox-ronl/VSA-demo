---
title: "Coria oefenen"
linkTitle: "Coria oefenen"
weight: 50
aliases:
  - /praktijk/demo/03-coria-oefenen/
---

# Coria oefenen

**Wat je hier leert:** op de website een oefenknop tonen die gevoed wordt door
een `.coria.html` naast het `.vsa`-bestand.

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

Zie ook: [VSA naar MusicXML](../04-vsa-naar-mxl/).
