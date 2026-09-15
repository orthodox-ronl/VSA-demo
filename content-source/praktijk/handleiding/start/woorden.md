---
title: "Woorden en bestanden"
linkTitle: "Woorden"
weight: 30
---

# Woorden en bestanden

{{< cue >}}
- **hub-`.mscz`** = canonieke MuseScore-partituur (hier bewerk je; daarna normaliseren)
- **print-`.mscz`** = koormap-vel; bestandsnaam eindigt op `.print.mscz`; pipeline blijft ervan af
- `.mxl` = MusicXML voor Coria (afgeleide; niet terug importeren om te layouten)
- `.pdf` = A4-afgeleide om te lezen of te printen
- `.vsa` = tekst plus melodie in VSA-notatie
- `doel-id` = mapnaam van de bladermap (bijv. `8a-trisagion`)
- `publicatiestatus` = wat koorleden op de pagina zien; intern *Stap* in de werkvoorraad is iets anders
{{< /cue >}}

**Wat je nu doet:** dezelfde namen gebruiken als de rest van de keten, zodat
commando’s en mappen kloppen.

## Bestanden

| Extensie | In het kort | Wat jij ermee doet |
| --- | --- | --- |
| hub-`.mscz` | MuseScore 4-bestand volgens [hub-contract](https://github.com/orthodox-ronl/VSA-demo/blob/main/scripts/mscz-hub-contract.md) | Openen, nakijken, opslaan; daarna `apply_mscz_layout.py`; bron voor PDF en Coria |
| print-`.mscz` | Zelfde soort MuseScore-bestand, naam eindigt op `.print.mscz` | Alleen in MuseScore bewerken; PDF handmatig; zie [Print-.mscz](/praktijk/handleiding/partituur/7-print-mscz/) |
| `.mxl` | Samengeperste MusicXML | Naar Coria (afgeleide); of (na opkuisen) als start voor een nieuwe hub. Nooit roundtrip: `.mscz` → `.mxl` → weer `.mscz` gooit de layout weg. |
| `.pdf` | A4-blad (afgeleide of handmatige print-export) | Downloaden of printen; hub opnieuw via [afgeleiden](/praktijk/handleiding/partituur/6-afgeleiden/) |
| `.vsa` | VSA-notatie | Schrijven in een editor; de sitebuild maakt er een plaatje (SVG) van |
| `.cap` / `.capx` | Capella | Als bron bewaren; eerst naar `.mxl` (CapToMusic) als je nog geen `.mxl` hebt |

**Opkuisen** = een Capella-`.mxl` met `cleanup_capella_mxl.py` inhoudelijk
opschonen vóór de MuseScore-layout.

**Contracten** (technische afspraken): 
[hub-`.mscz`](https://github.com/orthodox-ronl/VSA-demo/blob/main/scripts/mscz-hub-contract.md),
[product-transforms](https://github.com/orthodox-ronl/VSA-demo/blob/main/scripts/mscz-product-transforms.md).

## Plaatsen en status

| Woord | Betekenis |
| --- | --- |
| **Bladermap** | Eén map per [zangstuk](https://github.com/orthodox-ronl/bron/blob/main/docs/specs/terminologie.md) op de site: `index.md` plus partituur, PDF en/of VSA |
| **Doel-id** | De mapnaam van die bladermap, alleen `[a-z0-9_-]`, bijv. `15c-cherubijnenhymne-kastorski` |
| **Werkvoorraad** | Tabel in `input\werkvoorraad.md`: per *inputbestand* hoe ver de conversie is |
| **Stap** (werkvoorraad) | Intern: `ontvangen`, `opkuisen`, `layout`, … — niet zichtbaar voor koorleden |
| **Publicatiestatus** | Op `index.md`: `voorzien` (nog geen oefenbare uitgave), `reviewable` (er staat iets in), `concept` (sectie), `productie` alleen bewust — **niet raden** |
| **SATB** | Sopraan, alt, tenor, bas — de vier stemmen op één partituur |
| **Coria** | Online oefenen; heeft een schone `.mxl` nodig |
| **Uitvoeringsvorm** | Een concrete manier om een zangstuk uit te voeren (schrijf het woord uit; gebruik niet de afkorting “uv”) |

Org-brede termen: [glossary in bron](https://github.com/orthodox-ronl/bron/blob/main/docs/specs/terminologie.md).

## Klaar als

Je kunt een mail “hier is de Capella” vertalen naar: dump in
`input\capella\`, later een hub-`.mscz` in de bladermap, plus `.pdf` en
Coria-`.mxl` — of, voor een printvel, een `*.print.mscz` met handmatige PDF.

{{< navbuttons "Volgende: binnenhalen|/praktijk/handleiding/partituur/1-binnenhalen/" >}}
