---
title: "Publicatietrajecten (overzicht)"
linkTitle: "Publicatietrajecten"
weight: 5
---

# Publicatietrajecten (overzicht)

Antwoord eerst: **elk zichtbaar product hoort bij precies één bron** in de
bibliotheek. Welke bron, welk afgeleid bestand en welk script — dat staat
hier per **representatie-id** (`partituur`, `vsa`, `print`). Technische details:
`scripts\oefenhoek-product-contract.md` in de repository `VSA-demo`.

Termen: [Woorden](/praktijk/handleiding/start/woorden/) en
[Bibliotheek en koormappen](/praktijk/handleiding/start/bibliotheek-en-koormappen/).

{{< cue >}}
- **Basispartituur:** `{stam}.mscz` → layout → `mscz-products` → PDF + Coria-`.mxl`
- **VSA:** `{stam}.vsa` → SVG uit canonieke bron; Coria-`.vsa.mxl` via `vsa-products` (syllabify alleen tijdens export)
- **Print:** `{stam}.print.mscz` → handmatige PDF (geen basispartituur-pijplijn)
- Controle: `scripts\check.cmd --strict`
{{< /cue >}}

## Drie sporen naar de bibliotheek

| representatie-id | Canonieke bron in de bladermap | Typische afgeleiden | Automatische keten |
| --- | --- | --- | --- |
| `partituur` | `{stam}.mscz` (niet `.print.`) | `{stam}.pdf`, `{stam}.mxl` (legacy) of `{stam}.partituur.pdf` / `{stam}.partituur.mxl` | `apply_mscz_layout.py` → `mscz-products` |
| `vsa` | `{stam}.vsa` | SVG (site), `{stam}.vsa.mxl` (Coria) | `sync_oefenhoek_index.py --svg`, `vsa-products` |
| `print` | `{stam}.print.mscz` | `{stam}.print.pdf` (handmatig) | geen; vaak `artefacten_handmatig: true` |

Meerdere producten van hetzelfde type in één map → expliciete namen met
representatie-id (contract). Eén product per type mag nog korte namen
(`{stam}.mxl`, `{stam}.pdf`).

## Site-build (na bibliotheek-inhoud)

De pipeline in `scripts\_pipeline.cmd` (via `check` / `build` / `serve`):

```text
content-source
    |
    +-- validate, bibliotheek-checks, bibliotheek-id, basispartituur-producten, vsa-producten
    |
    +-- vsa build-markdown  ->  generated/content + static/vsa (SVG uit .vsa in content)
    |
    +-- sync_oefenhoek_index --svg  ->  static/vsa/bladermap/... (bibliotheek-.vsa zonder basispartituur)
    |
    +-- vsa musicxml content-source static/vsa/mxl  (embed-Coria in pagina's, geen oefenhoek-bibliotheek)
    |
    +-- Hugo  ->  generated/site
```

Bibliotheek-**Oefenen**-knoppen gebruiken sibling `{stam}.vsa.mxl` in de
bladermap (niet per se `static/vsa/mxl`).

---

## Traject: basispartituur → PDF en Coria

**Doel:** vierstemmig (of meer) blad in MuseScore, A4-PDF en Coria-`.mxl`.

| Stap | Wat | Commando / tool |
| --- | --- | --- |
| 1 | Opkuisen (stemmen, lettergrepen↔noten) | Capella-script of MuseScore — [Opkuisen](/praktijk/handleiding/partituur/2-opkuisen/) |
| 2 | Basispartituur normaliseren | `python scripts\apply_mscz_layout.py` op `{stam}.mscz` |
| 3 | Review | MuseScore — [Reviewen](/praktijk/handleiding/partituur/4-reviewen/) |
| 4 | Afgeleiden | `scripts\mscz-products.cmd` (MuseScore-export + Coria-sanitize) |
| 5 | Versheid | Stamp `partituur-sha256` in PDF/MXL; `check_partituur_products.py` |

Handleiding: [PDF en Coria](/praktijk/handleiding/partituur/5-pdf-en-coria/),
[Afgeleiden](/praktijk/handleiding/partituur/6-afgeleiden/).

**Niet van toepassing:** `*.print.mscz` (print-spoor).

---

## Traject: `.vsa` → SVG (publicatie) en Coria-`.vsa.mxl`

**Doel:** eenstemmige VSA-notatie op de pagina (plaatje) en oefenen in Coria.

| Stap | Input | Output | Opmerking |
| --- | --- | --- | --- |
| Schrijven | — | `{stam}.vsa` | YAML: `do`, `mode`, `tempo`; scopes voor cadens — [.vsa schrijven](/praktijk/handleiding/vsa/1-vsa-schrijven/) |
| SVG | canonieke `{stam}.vsa` | `static/vsa/bladermap/.../*.svg` | Geen lettergreepstreepjes tenzij jij ze in de bron zet |
| Coria-MXL | zelfde `{stam}.vsa` | `{stam}.vsa.mxl` | `vsa-products`: syllabify (Pyphen) in **temp-bestand**, dan `vsa musicxml playback`, sanitize, stamp |

**Waarom geen streepjes in de canonieke `.vsa`?** Orthografische `-` (Pyphen)
is handig voor Coria (één kwartnoot per lettergreep), maar hoeft niet op het
gepubliceerde SVG-plaatje. Daarom schrijft `scripts\sync_vsa_products.py` de
syllabified tekst niet terug naar `{stam}.vsa`.

**Handmatig syllabify (experiment):** `vsa syllabify pad\naar\bestand.vsa --extension .syl.vsa`
maakt een sibling `{stam}.syl.vsa`. Die sidecar is **geen** bron voor SVG of
`vsa-products`; leg geen `.syl.vsa` naast canonieke `.vsa` in de bibliotheek.

**Versheid:** stamp `vsa-source-sha256` op de **canonieke** `.vsa`;
`check_vsa_products.py` op `main` / `--strict`.

---

## Traject: print-vel

**Doel:** één PDF voor koormap (meerdere tekstregels, geen basispartituur-Coria-keten).

| Bron | Afgeleide | Pipeline |
| --- | --- | --- |
| `{stam}.print.mscz` | `{stam}.print.pdf` (of korte `{stam}.pdf` als enige PDF) | handmatig in MuseScore |

Geen `apply_mscz_layout`, geen `mscz-products`, geen automatische Coria-`.mxl`.
Zie [Print-.mscz](/praktijk/handleiding/partituur/7-print-mscz/).

---

## Traject: ingebedde VSA op andere pagina's

Pagina's buiten de oefenhoek-bibliotheek kunnen `.vsa` in `content-source`
embedden. De build maakt daar SVG onder `static/vsa/` en optioneel MXL onder
`static/vsa/mxl/` (`vsa build-markdown` + `vsa musicxml` in de pipeline).
Dat is **geen** vervanging van bibliotheek-`{stam}.vsa.mxl`; het is een
aparte embed-keten voor demos en handleidingen.

---

## Later: `.mvsa` (placeholder)

**mvsa** (meerstemmige VSA) is nog geen actief publicatiespoor in VSA-demo.
Als het er komt, hoort het hier als extra rij:

- eigen representatie-id (bijv. `mvsa` of een contract-naam uit `bron`);
- canonieke bron (verwacht: `.mvsa`-bestand);
- afgeleiden (PDF, Coria, SVG — nog te bepalen);
- scripts en stamps analoog aan `vsa-products` / `partituur`-gate.

Tot die tijd: alleen `.vsa` (eenstemmig) en basispartituur-`.mscz` volgens bovenstaande
tabellen. Syntax-plannen staan in VSA-tooling (`docs/plans/mvsa-v0-syntax.md`).

---

## Snelle commando's

| Situatie | Commando |
| --- | --- |
| Basispartituur-PDF/Coria vernieuwen | `scripts\mscz-products.cmd` `[bibliotheek-map]` |
| VSA-Coria vernieuwen | `scripts\vsa-products.cmd` `[bibliotheek-map]` |
| Alleen SVG bibliotheek | `python scripts\sync_oefenhoek_index.py --svg` |
| Alles vóór commit | `scripts\check.cmd --strict` |

Contract en stamps: `scripts\oefenhoek-product-contract.md`,
`scripts\mscz-partituur-contract.md`.
