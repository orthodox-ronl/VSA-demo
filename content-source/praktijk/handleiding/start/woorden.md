---
title: "Woorden en bestanden"
linkTitle: "Woorden"
weight: 30
---

# Woorden en bestanden

{{< cue >}}
- **basispartituur** / basispartituur-`.mscz` = canonieke MuseScore-partituur (hier bewerk je; daarna normaliseren). Representatie-id: `partituur` (oude naam in docs/scripts: *hub*)
- **print-`.mscz`** = koormap-vel; bestandsnaam eindigt op `.print.mscz`; pipeline blijft ervan af
- **representatie-id** = welk spoor een afgeleide hoort (`partituur` / `vsa` / `print`); bij botsing `{stam}.{id}.mxl`
- **artefacten_handmatig** = frontmatter op bibliotheek-`index.md`: PDF/MXL niet auto-bijwerken
- `.mxl` / `.vsa.mxl` = MusicXML voor Coria (afgeleide; niet terug importeren om te layouten)
- `.pdf` = A4-afgeleide om te lezen of te printen
- `.vsa` = tekst plus melodie in VSA-notatie (SVG + meestal auto Coria-`.vsa.mxl`); overzicht trajecten: [Publicatietrajecten](/praktijk/handleiding/start/publicatietrajecten/)
- **opkuisen** = inhoud opschonen (stemmen/balken, lettergreep↔noot); Capella-script of handmatig in MuseScore
- **normaliseren** / **layouten** = basispartituur-standaard met `scripts\layout.cmd` (zelfde scriptstap; “layouten” is de gewone naam)
- **bibliotheek-id** = `zangstuk/variant/uitvoeringsvorm` (drie lagen); zichtbaar op bibliotheek-leaves en in het colofon van basispartituur-`.mscz`/PDF
- **`bieb`** = shortcode die knoppen + partituur van een bibliotheek-id toont
- **bieb-accepteer** = script dat een `.mscz` / `.vsa` / `.print.mscz` in de bibliotheek zet (mappen + `index.md`); zie [Opnemen in de bibliotheek](/praktijk/handleiding/publiceren/1-opnemen-in-bibliotheek/)
- **publicatiestatus** = wat koorleden op de pagina zien (sticky header); intern *Stap* in de werkvoorraad is iets anders
{{< /cue >}}

**Wat je nu doet:** dezelfde namen gebruiken als de rest van de keten, zodat
commando’s en mappen kloppen.

## Bestanden

| Extensie | In het kort | Wat jij ermee doet |
| --- | --- | --- |
| basispartituur-`.mscz` | MuseScore 4-bestand volgens de basispartituur-norm (`scripts\mscz-partituur-contract.md` in `VSA-demo`) | Openen, nakijken, opslaan; daarna `scripts\layout.cmd`; bron voor PDF en Coria |
| print-`.mscz` | Zelfde soort MuseScore-bestand, naam eindigt op `.print.mscz` | Alleen in MuseScore bewerken; PDF handmatig; in bibliotheek, niet basispartituur-pijplijn — zie [Print-.mscz](/praktijk/handleiding/partituur/7-print-mscz/) |
| `.mxl` | Samengeperste MusicXML (partituur: `{stam}.mxl`; VSA: `{stam}.vsa.mxl`) | Naar Coria (afgeleide); of (na opkuisen) als start voor een nieuwe basispartituur. Nooit roundtrip: `.mscz` → `.mxl` → weer `.mscz` gooit de layout weg. |
| `.pdf` | A4-blad (afgeleide of handmatige print-export) | Downloaden of printen; basispartituur opnieuw via [afgeleiden](/praktijk/handleiding/partituur/6-afgeleiden/) |
| `.vsa` | VSA-notatie | Schrijven in een editor; sitebuild maakt SVG; `check`/`vsa-products` maakt Coria-`.vsa.mxl` — zie [.vsa schrijven](/praktijk/handleiding/vsa/1-vsa-schrijven/) |
| `.cap` / `.capx` | Capella | Als bron bewaren; eerst naar `.mxl` (CapToMusic) als je nog geen `.mxl` hebt |

**Opkuisen** = inhoudelijke opschoning: stemmen en notenbalken goed zetten,
lettergrepen synchroon met noten. Capella-`.mxl`: `scripts\opkuisen.cmd`.
Bij een `.mscz`: vaak handmatig in MuseScore. Zie
[Opkuisen](/praktijk/handleiding/partituur/2-opkuisen/).

**Normaliseren** (gangbaar: **layouten**) = de basispartituur-standaard toepassen met
`scripts\layout.cmd` (A4, fonts, reciteertoon, contractregels). Zie
[Standaard-.mscz](/praktijk/handleiding/partituur/3-standaard-mscz/) en
[Reviewen](/praktijk/handleiding/partituur/4-reviewen/).

**Contracten** (technische afspraken in de repo, niet als sitepagina):
`scripts\oefenhoek-product-contract.md` (afgeleiden per representatie-id),
`scripts\mscz-partituur-contract.md`, `scripts\mscz-product-transforms.md`.

## Plaatsen en status

| Woord | Betekenis |
| --- | --- |
| **Bibliotheek** | Catalogus onder `oefenhoek\bibliotheek\`: alle oefenbestanden per uitvoeringsvorm; mag stukken bevatten zonder koormap |
| **Bibliotheek-id** | Drie segmenten `[a-z0-9_-]+`, bijv. `8-trisagion/8a-nederlands/hemelum` |
| **Variant-id `default`** | Middelste laag als er maar één variant is (bijv. `5-eniggeboren-zoon/default/hemelum`) |
| **Taal-suffix** | Op uitvoeringsvorm-id: geen = NL; `-ksl` = Kerkslavisch Cyrillisch; `-ksl-trlat` = getranslitereerd; `-nl-ksl` = mengvorm |
| **Koormap** | Geordende view (navigatieboom) voor een gelegenheid; geen basispartituur-bestanden in de slotmappen |
| **Koormap-sectie** | Map met `_index.md` in de koormap: liturgische plek / hoofdstuk (kindlijst of eigen TOC) |
| **Slot-pagina** | Map met `index.md` in de koormap: markdown plus `bieb` (geen catalogus-include in de oefenhoek) |
| **Compositieblad** | Slot-pagina met proza en **meerdere** `bieb`-shortcodes (bijv. prokimens van de week) |
| **Alias-variant** | Variant zonder eigen uitvoeringsvorm-bestanden; op de variant-`_index.md` staat `alias_van: zangstuk/canonieke-variant` |
| **Diversen** | (verouderd als zangstuk-id) Losse gezangen hebben nu een eigen zangstuk-id, bv. `220-uw-heilig-kruis/default/hemelum` |
| **Tropaar** / **kondak** | Nederlandse termen voor die gezangen (niet “troparion” / “kondakion”) |
| **Special page** | Automatisch overzicht onder `bibliotheek\speciaal\` (voorzien, ongerefereerd, oefenbaar) |
| **Werkvoorraad** | Tabel in `input\werkvoorraad.md`: per *input* hoe ver de conversie is |
| **Stap** (werkvoorraad) | Intern: `ontvangen`, `opkuisen`, `layout`, `gepubliceerd`, … — niet zichtbaar voor koorleden |
| **Publicatiestatus** | Op `index.md` in bibliotheek én koormap: `voorzien`, `reviewable`, `concept`, `productie` (sticky header; niet raden) |
| **artefacten_handmatig** | Frontmatter: afgeleiden in die bibliotheekmap niet auto; gele banner voor beheerders |
| **SATB** | Sopraan, alt, tenor, bas — de vier stemmen op één partituur |
| **Coria** | Online oefenen; knop **Oefenen** bij shortcode `bieb`; heeft een schone `.mxl` nodig |
| **Uitvoeringsvorm** | Een concrete manier om een zangstuk uit te voeren (schrijf het woord uit; gebruik niet de afkorting “uv”) |

Org-brede termen: [glossary in bron](https://github.com/orthodox-ronl/bron/blob/main/docs/specs/terminologie.md).

Id-lijst Hemelum: [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/).
Model: [Bibliotheek en koormappen](/praktijk/handleiding/start/bibliotheek-en-koormappen/).

## Klaar als

Je kunt een mail “hier is de Capella” vertalen naar: input in
`input\capella\`, later een basispartituur-`.mscz` in de bibliotheek, plus `.pdf` en
Coria-`.mxl` — slot-pagina met `bieb`. Voor een printvel:
`*.print.mscz` + handmatige PDF (+ `artefacten_handmatig: true`) in de
bibliotheek, slot-pagina in de koormap. Voor een eenstemmige VSA: `.vsa` +
`.vsa.mxl` via `check` / `vsa-products`. Model van secties en
compositiebladen: [Bibliotheek en koormappen](/praktijk/handleiding/start/bibliotheek-en-koormappen/).

{{< navbuttons "Volgende: binnenhalen|/praktijk/handleiding/partituur/1-binnenhalen/" >}}
