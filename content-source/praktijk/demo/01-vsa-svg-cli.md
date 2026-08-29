---
title: "VSA naar SVG (vsa svg)"
linkTitle: "VSA naar SVG"
weight: 10
aliases:
  - /praktijk/zondagen/export-demo/
  - /praktijk/demo/export-demo/
  - /praktijk/demo/01-vsa-naar-svg/
---

# VSA naar SVG (`vsa svg`)

**Wat je hier leert:** één `.vsa`-bestand omzetten naar een `.svg`-bestand
met de CLI. Geen Markdown, geen site-build — alleen conversie.

## Bron

`assets\voorbeeld.vsa` — alleen VSA-notatie (geen YAML-frontmatter nodig):

```text
[\\:] Dat {//he}melse en {\aard}{/se} {/&/we}{zens_} *
jubelen en zich ver{\&\&\blij_&~&~}{\den_}, *
want {/de} {/Heer} heeft de kracht van Zijn {\arm} {/ge}{/&/o}pen{baard_}. *
Uit de doden was Hij de eerstge{/bo_}re{\ne_}, *
uit de schoot van de {-&\ha}{/des} {/heeft} {/Hij_} {\ons} ver{\lost_} *
// en aan de wereld grote ge{na_}{\de} {\ge}{/&/&/&\&\&\&/schon.&.&.&.&.&.&~}{\ken__}. [:]
```

## Commando

Werkmap = deze demo-map (`content-source\praktijk\demo`):

```cmd
vsa svg assets\voorbeeld.vsa ..\..\..\static\demo\voorbeeld.svg
```

Of vanaf de repo-root:

```cmd
vsa svg content-source\praktijk\demo\assets\voorbeeld.vsa static\demo\voorbeeld.svg
```

Optioneel eerst valideren: `vsa validate assets\voorbeeld.vsa`.

## Resultaat

Het geschreven SVG-bestand (hier geopend vanaf `static\demo\voorbeeld.svg`):

{{< vsa src="demo/voorbeeld.svg" alt="Tropaar toon 3 — resultaat van vsa svg" >}}

Open het bestand ook in een browser of image-viewer als je lokaal werkt.

## Wanneer dit, wanneer iets anders?

| Situatie | Gebruik |
| -------- | ------- |
| Snel een losse melodie als plaatje bekijken | **`vsa svg`** (deze demo) |
| Notatie in een Hugo-/Markdownpagina publiceren | [inline](../02-vsa-inline-markdown/) of [include](../03-vsa-include-bestand/) |

Volgende demootje: [VSA inline in Markdown](../02-vsa-inline-markdown/).
