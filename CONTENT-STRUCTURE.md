# Content-structuur (VSA-demo)

Bewerkbare bron staat in `content-source/`. Alles doorloopt
`scripts\check.cmd --strict` (validate, generate, hugo, links).

## Mappen

```text
content-source/
  praktijk/
    weekdagen/        per-weekdag liturgie (Liturgikon)
    zondagen/         toon 1-8; tropaar/kondak gesynchroniseerd uit bron
    feesteigen/       kalenderfeesten (maand/_index + dd-mm-*.md)
    hemelum-eigen/    parochie Hemelum: inline VSA-bron, losse .vsa
    samenstellingen/  catalogus-demo's, samengestelde liturgieen
    liturgikon/       liturgikon-teksten
    diversen/         losse zangstukken buiten de andere secties
  lokaal/             parochie-lokaal (manifest + repr per zangstuk)
  _index.md           site-home
```

## Waar hoort wat?

| Soort content                              | Pad                        | Opmerking                          |
| ------------------------------------------ | -------------------------- | ---------------------------------- |
| Catalogus-includes (`id:...`)              | `samenstellingen/`         | publiceert via `lokaal/` + bron    |
| Inline VSA ter referentie/bewerking        | `hemelum-eigen/`           | geen duplicate stub-pagina's       |
| Losse zangstukken buiten de andere secties | `diversen/`                | inline VSA, geen catalogus-include |
| Parochie-lokaal manifest + `.vsa`          | `lokaal/<zangstuk-id>/...` | pad conform bron-handboek          |
| Rubriek-navigatie                          | header (`layouts/partials/site-nav.html`) | alle secties onder `praktijk/`     |
| Weekdag-overzicht                          | `weekdagen/_index.md`      | linkt naar samenstellingen         |
| Feest-varianten (zelfde dag)               | `feesteigen/<mm-mon>/`     | aparte bestanden + onderlinge link |

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
