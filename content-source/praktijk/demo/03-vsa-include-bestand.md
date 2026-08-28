---
title: "VSA-bestand includen"
linkTitle: "Bestand includen"
weight: 30
---

# VSA-bestand includen

**Wat je hier leert:** vanuit Markdown naar een apart `.vsa`-bestand
verwijzen met `:::include svg …:::`. De build leest dat bestand en toont de
SVG op de pagina.

## Wat mag er in het `.vsa`-bestand?

| Wel | Niet |
| --- | --- |
| VSA-notatie (de body) | Omhullende `::: vsa-notatie` … `:::` (dat is Markdown-syntax) |
| Optioneel YAML-frontmatter bovenaan | Proza, koppen of andere Markdown om de notatie heen |
| UTF-8-tekst | Catalogus-ids of `zoek=` — dat hoort in de **include-regel**, niet in het bestand |

Kort: een `.vsa` is **notatie** (plus optionele metadata), geen Markdownpagina.
Zelfde inhoud als bij `vsa svg` of in een inline-blok — zonder de
`::: vsa-notatie`-hekjes.

Voorbeeld: `assets\voorbeeld.vsa` (alleen body).

## Schrijf dit in Markdown

Pad relatief ten opzichte van **deze** `.md` (niet ten opzichte van de
repo-root):

```markdown
:::include svg "assets/voorbeeld.vsa" alt="Tropaar toon 3" scale="85%":::
```

- `alt="…"` — toegankelijke beschrijving
- `scale="85%"` — vaste weergavegrootte (geen schuifregelaar); weglaten = 100%

Daarna:

```cmd
scripts\check.cmd --skip-hugo
```

## Resultaat

:::include svg "assets/voorbeeld.vsa" alt="Tropaar toon 3" scale="85%":::

## Wanneer includen?

| Situatie | Keuze |
| -------- | ----- |
| Eén melodie, meerdere pagina’s of PDF-bladen | **Include** (deze demo) |
| Melodie alleen op deze pagina | [Inline](../02-vsa-inline-markdown/) |
| Los plaatje zonder Markdown | [`vsa svg`](../01-vsa-svg-cli/) |

**Nog niet in deze demo:** includes via catalogus (`zoek=`, `bron:`,
`lokaal:`). Zie daarvoor [Samenstellingen](../../samenstellingen/).

Vorige: [inline](../02-vsa-inline-markdown/). Andere uitvoer:
[MusicXML](../04-vsa-naar-mxl/).
