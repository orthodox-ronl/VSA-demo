# Oefenhoek UI-contract

Pagina-chrome en shortcode `bieb` voor bibliotheek- en koormap-pagina's
onder `content-source/praktijk/oefenhoek/`.

## Sticky Oefenhoek-header

Onder de site-nav (`.site-chrome`, al sticky) staat op elke Oefenhoek-pagina
een tweede sticky blok: `.oefenhoek-header`.

Inhoud (van boven naar beneden):

1. **Breadcrumb** — vanaf de deelrubriek (`bibliotheek`, `liturgiemap-hemelum`,
   …) tot en met de huidige pagina. Labels = Hugo `.LinkTitle`
   (frontmatter `linkTitle`, anders `title`). Geen `Praktijk` / `Oefenhoek`
   in het pad. De laatste crumb is de huidige pagina (`aria-current="page"`),
   geen link.
2. **Publicatiestatus** — zelfde status/feedback-blok als voorheen
   (frontmatter `publicatiestatus`), nu in deze header i.p.v. los boven
   de titel in `<main>`.

Implementatie: `layouts/partials/oefenhoek-header.html`, aangeroepen vanuit
`layouts/_default/baseof.html`. CSS/JS: `--site-chrome-height` +
`--oefenhoek-header-height` (`static/css/site.css`, `static/js/site-nav.js`).

## Geen pagina-actieknoppen onder de titel

De oude knoppenrij direct onder `<h1>` (Bibliotheek/Koormap, Oefenen,
Downloaden, Printen) bestaat niet meer. Navigatie naar deelrubriek en
bovenliggende onderdelen loopt via de breadcrumb.

## Bibliotheek-id op leaves

Elke **bibliotheek-leaf** (pagina
`bibliotheek/<zangstuk>/<variant>/<uitvoeringsvorm>/`) toont het
**bibliotheek-id** (`zangstuk/variant/uitvoeringsvorm`) zichtbaar op de
pagina. Het id wordt uit het pad afgeleid (layout), niet handmatig in de
markdown herhaald. Alias-varianten: canonieke id via
`layouts/partials/bibliotheek-canonical-id.html`.

Koormap-slots tonen het id niet verplicht (die verwijzen via `bieb`).
Special pages tonen id’s al in hun cataloguslijst.

Implementatie: `layouts/partials/bibliotheek-id-line.html`, aangeroepen
vanuit `layouts/oefenhoek/single.html`.

## Shortcode `bieb`

```hugo
{{</* bieb id="zangstuk/variant/uitvoeringsvorm" */>}}
```

Per aanroep, in deze volgorde:

1. Actieknoppen Oefenen / Downloaden / Printen voor die bibliotheek-pagina
   (`layouts/partials/oefenhoek-score-acties.html`)
2. PDF-blad en/of VSA-SVG (`layouts/shortcodes/bieb.html`)

**Oefenen** met één Coria-`.mxl`: één knop, geen menu. Met meerdere
`.mxl`: keuzemenu met menselijke labels (`Melodie (één stem)` /
`Koorblad (meerdere stemmen)`), detailregel, en hulpzin
«Kies de versie die past bij het blad waarmee je meezingt.» Zelfde
patroon voor meerdere PDF’s op Downloaden/Printen. Zie
`scripts/oefenhoek-product-contract.md` (UI: meerdere producten).

Meerdere `bieb`-shortcodes op één markdown-pagina: elke shortcode heeft
een eigen knoppenrij + content.

Oude naam `bibliotheek-score` is verwijderd (geen alias).

Alias-variant (`alias_van` op de variant-`_index.md`): `bieb` herschrijft
een id waarvan de variant-laag een alias is naar de canonieke
uitvoeringsvorm. De alias-pagina zelf toont een banner en de partituur van
die canonieke variant (`layouts/partials/oefenhoek-alias.html`).

SVG voor `.vsa` (geen basispartituur-`.mscz`): `python scripts\sync_oefenhoek_index.py --svg`
(in `check` / `build` / volle `serve`). Ontbrekende SVG: Hugo-waarschuwing
van `bieb` noemt dit commando. `*.print.mscz` blokkeert SVG niet.

## Gerelateerd

- Productbestanden / representatie-id: `scripts/oefenhoek-product-contract.md`
- Basispartituur-PDF/MXL: `scripts/mscz-partituur-contract.md`
- Handleiding: `content-source/praktijk/handleiding/publiceren/1-bladermap.md`
