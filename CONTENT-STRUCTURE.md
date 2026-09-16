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
      bibliotheek/     (conversie) bibliotheek drie lagen; zie Oefenhoek
      liturgiemap-hemelum/  koormap Hemelum
      overig/         testmateriaal
      input/          ruwe dumps
    demo/             tooling-demo's (svg CLI/inline/include, mxl, coria, pdf) + assets/
    handleiding/      beheerder-handleiding oefenhoek (ruwe input tot publicatie)
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
| Beheerder-handleiding (oefenhoek-straat)   | `handleiding/`             | geen `nav_group`; balk-knop **Handleiding** (weight na Demo) |
| WIP-oefenmateriaal voor koorleden          | `oefenhoek/`               | geen `nav_group`; bibliotheek + koormap-slots |
| Parochie-lokaal manifest + `.vsa`          | `lokaal/<zangstuk-id>/...` | pad conform bron-handboek          |
| Header-nav                                 | `nav_group` op sectie-`_index.md` | `diensten` / `materiaal`; sectie zonder groep (Oefenhoek, Demo, Handleiding) wordt dropdown van haar pagina’s |
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
| Eigen rubriek, geen `nav_group` | Balk-knop **Oefenhoek** (weight lager dan Demo, dus links daarvan); dropdown = deelrubrieken |
| Deelrubrieken | `bibliotheek/` (doel), `liturgiemap-hemelum/`, `overig/`; `input/` blijft op oefenhoek-niveau |
| Bibliotheek | `oefenhoek/bibliotheek/<zangstuk-id>/<variant-id>/<uitvoeringsvorm-id>/` (altijd drie lagen). Hub-`.mscz` + PDF/Coria/VSA + `index.md`. Mag uitvoeringsvormen bevatten **zonder** koormap-verwijzing. Root toont oefenbare zangstukken (niet alle stubs). Id-register: `bibliotheek/ID-REGISTER.md`. Special pages: `bibliotheek/speciaal/` (voorzien, ongerefereerd, oefenbaar). Migratie: `scripts/migrate_oefenhoek_bibliotheek.py` (niet in check). Print-vel: `{stam}.print.mscz` in bibliotheek, geen Coria-hub. |
| Koormap | Geordende view (liturgie, later feest/collectie/parochie). Slots verwijzen via `{{< bibliotheek-score id="zangstuk/variant/uitvoeringsvorm" >}}`. Geen hub-`.mscz` in de slotmap. |
| Publicatiestam | `{zangstuk}-{variant}-{uitvoeringsvorm}` voor bronbestanden; afgeleiden bij voorkeur `{stam}.{representatie-id}.{ext}` (`scripts/oefenhoek-product-contract.md`) |
| Migratie uitgevoerd (Hemelum) | Hub-bestanden in `bibliotheek/`; koormap-slots alleen `index.md` + `bibliotheek-score` (catalogus-slots: `:::include`). |
| Geen spaties in publicatienamen | Stam `[a-z0-9_-]+`. Print-vel: `*.print.mscz` (buiten hub-productgate). Afgeleiden per representatie-id: zie product-contract. Ruwe dumps: `oefenhoek/input/` (niet gekopieerd) |
| Geen dubbele canonieke VSA | Catalogus-include (`id:…` / `lokaal:…` / `bron:…`) mag op een koormap-slot; MuseScore-uitgaven in bibliotheek |
| `check --strict` blijft gelden | Alleen plaatsen wat de pipeline groen houdt; anders eerst in de tool-tak laten |
| Klaar? Verhuizen | Naar Diensten/Materiaal (later: oefenmodus op die pagina’s); oefenhoek-pagina inkorten of verwijzen |
| Input vs publicatie | Ruwe dumps in `oefenhoek/input/<herkomst>/` (capella, vow, musescore, musicxml, pdf). `_inbox/` en `_werk/` alleen lokaal (gitignore). Geen `_index.md` in `input/`. |
| Werkvoorraad | `oefenhoek/input/werkvoorraad.md` (een rij per input; tabel bij sitebuild). Doel-id = bibliotheek-id wanneer bekend. |
| Publicatiestatus | Frontmatter `publicatiestatus` op elke oefenhoek-`_index.md` en `index.md`: `voorzien` (gepland, nog geen uitgave), `concept` (eerste versie), `reviewable` (feedback gevraagd), `productie`. Balk + e-mail/GitHub-issue. Secties: collectie als geheel. |
| Kind-lijst linkbaar | `layouts/partials/oefenhoek-linkbaar.html`: doorlinken als er oefenbestanden zijn, of leaf-status in `concept` \| `reviewable` \| `productie`, of (sectie) een nakomeling linkbaar is, of catalogus-`:::include`. Anders platte tekst + `(voorzien)`. |
| Bibliotheek- / koormap-`index.md` | Met `automatische_inhoud: true`: widgets via Hugo-layout uit bestanden in de map. Met `bibliotheek-score` of catalogus-include: `automatische_inhoud: false`. |
| Sectie-`_index.md` | Eigen tekst (geen `#`-titel; die komt uit de layout) + linklijst van kind-pagina's als `automatische_inhoud: true`. Precies 1 kind: doorverwijzen naar dat kind. Knop terug naar de koormap (liturgiemap). Zet `false` als je zelf een TOC houdt. |
| `automatische_inhoud` | Verplicht op elke oefenhoek-`_index.md` / `index.md`: `true` of `false`. |
| `artefacten_handmatig` | Optioneel op bibliotheek-`index.md`: `true` = PDF/MXL e.d. niet via product-pipeline; beheerdersbanner op de pagina. Zie `scripts/oefenhoek-product-contract.md`. |

Intern register (conversiestap) is niet hetzelfde als publieke `publicatiestatus`.

Nog niet in deze ronde: oefenmodus-schakelaar, audio-player, automatische sync
uit VSA-tooling.

Overig: testhoek. Bibliotheek = catalogus van uitvoeringsvormen; koormappen
zijn views. Handleiding: `praktijk/handleiding/start/bibliotheek-en-koormappen.md`.

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
