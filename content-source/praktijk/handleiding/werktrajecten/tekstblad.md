---
title: "Tekstblad → PDF"
linkTitle: "Tekstblad"
weight: 55
---

# Tekstblad → PDF

Dit werktraject maakt uit een bibliotheek-bron **`{stam}.tekstblad.md`**
(vooral tekst, eventueel HTML en `::: vsa-notatie`) een A4-PDF
**`{stam}.tekstblad.pdf`**. Representatie-id: `tekstblad`.

{{< cue >}}
Na een `{stam}.tekstblad.md` in de bladermap:
```cmd
scripts\tekstblad-products.cmd content-source\praktijk\oefenhoek\bibliotheek\<zangstuk>
scripts\check.cmd --strict
```
Commit de `.tekstblad.md` en de `.tekstblad.pdf` samen.
{{< /cue >}}

## Waartoe

Liturgische tekst of dialoog (bijvoorbeeld ustav met de diaken) hoort in de
**bibliotheek**, net als een basispartituur of een `.vsa`. Koorleden zien
en downloaden/printen de PDF via shortcode `bieb` — niet een tweede kopie
van de tekst in de koormap.

## Eindresultaat en criteria

| Bestand (in de bladermap) | Rol |
| --- | --- |
| `{stam}.tekstblad.md` | Canonieke bron (nooit een Hugo-pagina) |
| `{stam}.tekstblad.pdf` | A4-product; stamp `vsa-source-sha256` |

**Klaar** als: de bron frontmatter `build: render: never` (en `list: never`)
heeft; de PDF bij de bron past (`check_tekstblad_products`); `bieb` toont
de PDF met Downloaden/Printen. Geen Coria uit dit spoor.

Voorbeeld:
`content-source\praktijk\oefenhoek\bibliotheek\7d-dialoog-met-diaken\default\hemelum\`.

## Wanneer wel / wanneer niet

| Wel | Niet |
| --- | --- |
| Ustav, dialoog, liturgische proza met korte VSA-regels | Vierstemmig MuseScore → [Basispartituur](../basispartituur/) |
| Tekst die je als A4-blad wilt downloaden/printen | Alleen schermtekst op een gewone `index.md` (geen product) |
| | Demo/generieke markdown buiten de bibliotheek → [Markdown naar PDF](../markdown-naar-pdf/) / `pdf.cmd` |

## Volgorde (bestanden)

1. Schrijf of herstel `{stam}.tekstblad.md` (HTML en `::: vsa-notatie` mogen).
2. Neem op met [Opnemen](../opnemen-in-bibliotheek/) /
   `scripts\bieb-accepteer.cmd` (zet indien nodig de `build:`-frontmatter).
3. Bouw de PDF:

```cmd
scripts\tekstblad-products.cmd content-source\praktijk\oefenhoek\bibliotheek\7d-dialoog-met-diaken
```

4. Koormap-slot: alleen intro + `bieb` (geen tweede kopie van de tekst).
5. [Site-build](../site-build/) / `scripts\check.cmd --strict`.

## Automatisch (CI)

- **Wel:** `check_tekstblad_products.py` controleert of de PDF bij de
  `.tekstblad.md` past (source-sha).
- **Niet:** PDF opnieuw genereren op GitHub Actions. Maak de PDF **lokaal**
  en commit bron + PDF samen.

Lokaal vernieuwt `_pipeline.cmd` stale tekstblad-PDF’s via
`sync_tekstblad_products.py` (Chrome/Edge nodig, zoals `pdf.cmd`).

## Handmatig

| Situatie | Commando | Man-page |
| --- | --- | --- |
| PDF bij tekstblad | `scripts\tekstblad-products.cmd` `[map]` | [tekstblad-products](../../scripts/tekstblad-products/) |
| Willekeurig markdownblad (niet bibliotheek) | `scripts\pdf.cmd` | [pdf](../../scripts/pdf/) |
| Opnemen | `scripts\bieb-accepteer.cmd` | [bieb-accepteer](../../scripts/bieb-accepteer/) |
| Alles vóór commit | `scripts\check.cmd --strict` | [check](../../scripts/check/) |

## Zie ook

- Contract: `scripts\oefenhoek-product-contract.md` in `VSA-demo`
- [Markdown naar PDF](../markdown-naar-pdf/) (generiek / demo)
- [Opnemen](../opnemen-in-bibliotheek/)

{{< navbuttons "Site-build|/praktijk/handleiding/werktrajecten/site-build/" "Markdown naar PDF|/praktijk/handleiding/werktrajecten/markdown-naar-pdf/" >}}
