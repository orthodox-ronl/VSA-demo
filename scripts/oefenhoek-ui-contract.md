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

## Shortcode `bieb`

```hugo
{{</* bieb id="zangstuk/variant/uitvoeringsvorm" */>}}
```

Per aanroep, in deze volgorde:

1. Actieknoppen Oefenen / Downloaden / Printen voor die bibliotheek-pagina
   (`layouts/partials/oefenhoek-score-acties.html`)
2. PDF-blad en/of VSA-SVG (`layouts/shortcodes/bieb.html`)

Meerdere `bieb`-shortcodes op één markdown-pagina: elke shortcode heeft
een eigen knoppenrij + content.

Oude naam `bibliotheek-score` is verwijderd (geen alias).

SVG voor `.vsa` (geen hub-`.mscz`): `python scripts\sync_oefenhoek_index.py --svg`
(in `check` / `build` / volle `serve`). Ontbrekende SVG: Hugo-waarschuwing
van `bieb` noemt dit commando. `*.print.mscz` blokkeert SVG niet.

## Gerelateerd

- Productbestanden / representatie-id: `scripts/oefenhoek-product-contract.md`
- Hub-PDF/MXL: `scripts/mscz-hub-contract.md`
- Handleiding: `content-source/praktijk/handleiding/publiceren/1-bladermap.md`
