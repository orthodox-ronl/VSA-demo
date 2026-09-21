---
title: "Bibliotheek en koormap"
linkTitle: "Bibliotheek en koormap"
weight: 10
---

# Bibliotheek en koormap

{{< cue >}}
Nieuwe partituur in de bibliotheek zetten:
[Opnemen in de bibliotheek](../1-opnemen-in-bibliotheek/)
(`scripts\bieb-accepteer.cmd`).

Slot-pagina in de koormap:
`content-source\praktijk\oefenhoek\liturgiemap-hemelum\…\index.md` met
shortcode `bieb` (parameter `id` = bibliotheek-id) en
`automatische_inhoud: false`. Geen basispartituur-bestanden in de koormap-map.

Een **alias-variant** (andere naam voor dezelfde variant) krijgt geen
uitvoeringsvorm-map. Zet `alias_van` op de variant-`_index.md`; zie
[Bibliotheek en koormappen](../../start/bibliotheek-en-koormappen/).

Koormap-sectie (hoofdstuk): map met `_index.md` — kindlijst of eigen TOC;
zie [Bibliotheek en koormappen](../../start/bibliotheek-en-koormappen/).

Id-lijst: [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/).
{{< /cue >}}

**Wat je nu doet:** na het opnemen van bestanden in de **bibliotheek** de
**koormap** laten verwijzen, zodat koorleden de liturgiemap kunnen volgen.
De partituur blijft in de bibliotheek; de koormap is de route.

**Wanneer:** nadat [opnemen in de bibliotheek](../1-opnemen-in-bibliotheek/)
klaar is (of de leaf al bestaat). Familie met meerdere varianten op één
liturgische plek: zie
[Bibliotheek en koormappen](../../start/bibliotheek-en-koormappen/).

## Bibliotheek: kort

Gebruik **bieb-accepteer** voor mappen, `index.md` en de juiste
bestandsnamen. Handmatig kopiëren van voorbeelden is alleen nog nodig bij
uitzonderingen. Details en voorbeelden van commando’s:
[Opnemen in de bibliotheek](../1-opnemen-in-bibliotheek/).

Pad na acceptatie:
`content-source\praktijk\oefenhoek\bibliotheek\<zangstuk>\<variant>\<uitvoeringsvorm>\`
met `index.md` + oefenbestanden (publicatiestam zonder spaties).

Een **alias-variant** (andere naam voor dezelfde variant) krijgt geen
uitvoeringsvorm-map. Zet `alias_van` op de variant-`_index.md`; zie
[Bibliotheek en koormappen](../../start/bibliotheek-en-koormappen/).

## Stap voor stap (slot-pagina in de koormap)

1. Open of maak de slot-pagina (bijvoorbeeld
   `liturgiemap-hemelum\8-trisagion\8a-trisagion\index.md`).
2. Zorg dat alleen **`index.md`** in die slotmap staat — geen `.mscz` meer
   in de koormap.
3. Frontmatter: `automatische_inhoud: false`, `publicatiestatus` passend
   bij wat koorleden zien.
4. In de body: titel + shortcode `bieb` met jouw id (voorbeeld:
   `8-trisagion/8a-nederlands/hemelum`).

| Situatie | Koormap-voorbeeld |
| --- | --- |
| Basispartituur via bibliotheek | `liturgiemap-hemelum\8-trisagion\8a-trisagion\index.md` |
| VSA via bibliotheek | `liturgiemap-hemelum\2-eerste-antifoon\weekdagen\index.md` |
| Sectie (boom van keuzes) | `liturgiemap-hemelum\15-cherubijnenhymne\_index.md` + kindmappen |
| Compositieblad (meerdere scores) | Eén `index.md` met markdown en meerdere `bieb`-shortcodes — zie [Bibliotheek en koormappen](../../start/bibliotheek-en-koormappen/) |
| Diversen / tropaar / kondak | Bijv. `diversen/uw-heilig-kruis/hemelum`, `tropaar/…`, `kondak/…` — altijd `bieb`, geen `:::include` |

5. Hoort het stuk in het liturgie-overzicht? Controleer
   `liturgiemap-hemelum\_index.md` (handmatige inhoudsopgave).

### Meerdere shortcodes op één slot-pagina

Op een compositieblad mag je **meerdere** `bieb`-shortcodes
zetten (elk met een eigen bibliotheek-id). Elke shortcode zet eerst de
knoppen **Oefenen** / **Downloaden** / **Printen** voor die uitvoeringsvorm,
en daarna de PDF of VSA-SVG. Zo heeft elke score op dezelfde pagina een
eigen knoppenrij.

## Oude migratie (alleen historisch)

De eenmalige verhuizing van basispartituren uit de liturgiemap naar de bibliotheek is
al gedaan. Nieuwe stukken gaan via
[opnemen in de bibliotheek](../1-opnemen-in-bibliotheek/). Het oude script
`migrate_oefenhoek_bibliotheek.py` is geen dagelijkse tool meer.

## Klaar als

Na `check --strict` toont de preview de slot-pagina met PDF/**Oefenen**/VSA
via `bieb`. De bibliotheek heeft de bestanden; de
koormap-map heeft geen basispartituur meer. Je weet wanneer je een sectie (boom)
gebruikt en wanneer een compositieblad.

{{< navbuttons "Vorige: opnemen in de bibliotheek|/praktijk/handleiding/publiceren/1-opnemen-in-bibliotheek/" "Volgende: status en check|/praktijk/handleiding/publiceren/2-status-en-check/" >}}
