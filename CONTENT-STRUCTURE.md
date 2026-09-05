# Content-structuur (VSA-demo)

Bewerkbare bron staat in `content-source/`. Alles doorloopt
`scripts\check.cmd --strict` (validate, generate, hugo, links).

## Mappen

```text
content-source/
  praktijk/
    weekdagen/        per-weekdag liturgie (Liturgikon)
    zondagen/         toon 1-8; tropaar/kondak gesynchroniseerd uit bron
    feesteigen/       kalenderfeesten (maand/_index + mm-dd-*.md)
    hemelum-eigen/    parochie Hemelum: inline VSA-bron, losse .vsa
    samenstellingen/  catalogus-demo's, samengestelde liturgieen
    liturgikon/       liturgikon-teksten
    diversen/         losse zangstukken buiten de andere secties
    oefenhoek/        WIP-oefenmateriaal voor koorleden (geen catalogus)
    demo/             tooling-demo's (svg CLI/inline/include, mxl, coria, pdf) + assets/
  lokaal/             parochie-lokaal (manifest + repr per zangstuk)
  _index.md           site-home
```

## Waar hoort wat?

| Soort content                              | Pad                        | Opmerking                          |
| ------------------------------------------ | -------------------------- | ---------------------------------- |
| Catalogus-includes (`id:...`)              | `samenstellingen/`         | publiceert via `lokaal/` + bron    |
| Inline VSA ter referentie/bewerking        | `hemelum-eigen/`           | geen duplicate stub-pagina's       |
| Losse zangstukken buiten de andere secties | `diversen/`                | inline VSA, geen catalogus-include |
| Tooling-demo (svg CLI → inline → include; mxl; coria; pdf) | `demo/` (+ `demo/assets/`) | één topic per pagina |
| WIP-oefenmateriaal voor koorleden          | `oefenhoek/`               | geen `nav_group`; bladermap per zangstuk-id |
| Parochie-lokaal manifest + `.vsa`          | `lokaal/<zangstuk-id>/...` | pad conform bron-handboek          |
| Header-nav                                 | `nav_group` op sectie-`_index.md` | `diensten` / `materiaal`; sectie zonder groep (Oefenhoek, Demo) wordt dropdown van haar pagina’s |
| Weekdag-subnav                             | balk onder de header       | ma–za via `weight` 1–6             |
| Feesteigen-subnav                          | balk onder de header       | maanden via `weight` 1–12          |
| Paginalijst op `_index`                    | Hugo `page-list.html`      | default bestandsnaam (`mm-dd-…`); `nav_sort: weight` op weekdagen |
| Feest-varianten (zelfde dag)               | `feesteigen/<mm-mon>/`     | aparte bestanden + onderlinge link |

Zet `hide_page_list: true` als de `_index` zelf al een overzicht heeft (zondagen-tabel, demo-leerpad).

## Oefenhoek

Publieke plek om koorleden naar WIP-oefenmateriaal te sturen (exports uit
VSA-tooling die bruikbaar zijn, maar nog geen afgeronde uitgave). Geen tweede
catalogus en geen tooling-demo.

| Afspraak | Toelichting |
| -------- | ----------- |
| Eigen rubriek, geen `nav_group` | Balk-knop **Oefenhoek** (weight lager dan Demo, dus links daarvan) |
| Eén bladermap per zangstuk | `oefenhoek/<zangstuk-id>/index.md` (Hugo leaf bundle); oefenbestanden ernaast |
| Geen dubbele canonieke VSA | Notatie via catalogus-include (`id:…` / `lokaal:…` / `bron:…`); experimentele exports mogen wél in de bladermap |
| `check --strict` blijft gelden | Alleen plaatsen wat de pipeline groen houdt; anders eerst in de tool-tak laten |
| Klaar? Verhuizen | Naar Diensten/Materiaal (later: oefenmodus op die pagina’s); oefenhoek-pagina inkorten of verwijzen |

Nog niet in deze ronde: oefenmodus-schakelaar, audio-player, automatische sync
uit VSA-tooling.

Eerste bladermap: `troparion-nikolaas-van-myra` (catalogus-id; spelling Nikolaas).

## Antifonen weekdagen (voorbeeld)

| Rol | Bestand |
| --- | ------- |
| Catalogus-demo (1e/2e/3e, Liturgikon + Hemelum) | `samenstellingen/antifonen-weekdagen-catalogus.md` |
| Liturgikon-uitvoeringsvorm | `samenstellingen/antifonen-liturgikon.md` |
| Hemelum via catalogus | `samenstellingen/antifonen-hemelum.md` |
| Hemelum inline bron (per antifoon) | `hemelum-eigen/eerste-…`, `tweede-…`, `derde-…` |
| Lokaal manifest Hemelum | `lokaal/antifoon-*-weekdagen/.../hemelum/` |

## Niet committen

Build-output: `generated/`, `static/vsa/` (SVG/MXL uit generate).

## Zie ook

- [scripts/README.md](scripts/README.md) - testladder, CI-spiegel
- [bron: parochie-lokaal](https://github.com/orthodox-ronl/bron/blob/main/docs/manuals/parochie-lokaal-zangstukken.md)
