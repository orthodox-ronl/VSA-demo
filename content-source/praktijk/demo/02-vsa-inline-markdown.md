---
title: "VSA inline in Markdown"
linkTitle: "Inline in Markdown"
weight: 20
---

# VSA inline in Markdown

**Wat je hier leert:** VSA-notatie **in de Markdownpagina zelf** zetten. Bij
generate (`vsa build-markdown` / `scripts\check.cmd`) wordt elk
`::: vsa-notatie`-blok omgezet naar een SVG op de site.

Geen apart `.vsa`-bestand, geen `:::include`.

## Schrijf dit in Markdown

```markdown
::: vsa-notatie
[\\:] Dat {//he}melse en {\aard}{/se} {/&/we}{zens_} *
jubelen en zich ver{\&\&\blij_&~&~}{\den_}, *
want {/de} {/Heer} heeft de kracht van Zijn {\arm} {/ge}{/&/o}pen{baard_}. *
Uit de doden was Hij de eerstge{/bo_}re{\ne_}, *
uit de schoot van de {-&\ha}{/des} {/heeft} {/Hij_} {\ons} ver{\lost_} *
// en aan de wereld grote ge{na_}{\de} {\ge}{/&/&/&\&\&\&/schon.&.&.&.&.&.&~}{\ken__}. [:]
:::
```

Daarna, vanuit de repo-root:

```cmd
scripts\check.cmd --skip-hugo
```

## Resultaat op deze pagina

::: vsa-notatie
[\\:] Dat {//he}melse en {\aard}{/se} {/&/we}{zens_} *
jubelen en zich ver{\&\&\blij_&~&~}{\den_}, *
want {/de} {/Heer} heeft de kracht van Zijn {\arm} {/ge}{/&/o}pen{baard_}. *
Uit de doden was Hij de eerstge{/bo_}re{\ne_}, *
uit de schoot van de {-&\ha}{/des} {/heeft} {/Hij_} {\ons} ver{\lost_} *
// en aan de wereld grote ge{na_}{\de} {\ge}{/&/&/&\&\&\&/schon.&.&.&.&.&.&~}{\ken__}. [:]
:::

## Wanneer inline?

| Situatie | Keuze |
| -------- | ----- |
| Notatie hoort bij **deze** pagina en wordt nergens hergebruikt | **Inline** (deze demo) |
| Zelfde melodie op meerdere pagina’s / in PDF-bladen | [`.vsa` includen](../03-vsa-include-bestand/) |
| Alleen even een plaatje zonder site-build | [`vsa svg`](../01-vsa-svg-cli/) |

Volgende demootje: [VSA-bestand includen](../03-vsa-include-bestand/).
