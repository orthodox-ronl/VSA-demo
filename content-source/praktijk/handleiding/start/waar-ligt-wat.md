---
title: "Waar ligt wat"
linkTitle: "Waar ligt wat"
weight: 20
---

# Waar ligt wat

{{< cue >}}
- Input: `oefenhoek\input\<herkomst>\` (originele bestandsnaam mag spaties hebben)
- Tussenwerk: `oefenhoek\input\_werk\<stam>\` (publicatiestam; alleen op jouw pc, niet in git)
- Bibliotheek: `oefenhoek\bibliotheek\<zangstuk>\<variant>\<uitvoeringsvorm>\` — **geen spaties** in bestandsnamen
- Koormap: `oefenhoek\liturgiemap-hemelum\` — sectie-`_index.md` of slot-`index.md` + verwijzing (geen hub-bestanden)
- Register: `oefenhoek\input\werkvoorraad.md` en [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/)
{{< /cue >}}

**Wat je nu doet:** vier soorten plekken uit elkaar houden. Anders verdwijnt
het origineel, of komt een half af bestand op de publieke site.

Een **bibliotheek-uitvoeringsvorm** is één map in de bibliotheek met
`index.md` en de bestanden die koorleden oefenen (hub, PDF, Coria, VSA of
print). In de Hemelum-**koormap** verwijst een **slot-pagina**
(`index.md`) met `bieb` naar die uitvoeringsvorm. Een
**koormap-sectie** (`_index.md`) groepeert kindpagina’s op één liturgische
plek (bijvoorbeeld antifoon weekdagen / zondag). Zie
[Bibliotheek en koormappen](/praktijk/handleiding/start/bibliotheek-en-koormappen/).

## Vier plekken

| Plek | Map (vanaf `content-source\praktijk\`) | Op de publieke site? |
| --- | --- | --- |
| Ruw, ongewijzigd | `oefenhoek\input\capella\` (of `vow\`, `musescore\`, `musicxml\`, `pdf\`) | Nee |
| Halverwege (tussenwerk) | `oefenhoek\input\_werk\` | Nee (en niet in git) |
| Bibliotheek | `oefenhoek\bibliotheek\<zangstuk>\<variant>\<uitvoeringsvorm>\` | Ja (rubriek Bibliotheek) |
| Koormap (sectie of slot-pagina) | `oefenhoek\liturgiemap-hemelum\…` (pad in de liturgie) | Ja (liturgiemap + shortcode) |

Testmateriaal buiten de liturgiemap: `oefenhoek\overig\` (zelfde idee:
bestanden in bibliotheek, slot in `overig` als dat nodig is).

De map `input\_inbox\` is een lokale brievenbus voor bestanden die je nog
niet zeker wilt bewaren. Pas als een bestand dé bron is die je wilt
houden, verplaats je het naar `capella\`, `vow\`, of een andere
herkomst-map.

## Herkomst-mappen

| Map onder `input\` | Wat erin hoort |
| --- | --- |
| `capella\` | Capella / CapToMusic: `.cap`, `.capx`, of een `.mxl` zoals het binnenkwam |
| `vow\` | Ruwe VOW-`.mscz` |
| `musescore\` | Andere ruwe `.mscz` (nog niet de Oefenhoek-layout) |
| `musicxml\` | `.xml` / `.musicxml` / `.mxl` uit een ander programma |
| `pdf\` | Scans of print-PDF die je als bron bewaart |

Laat de **originele bestandsnaam** van de input staan, ook met spaties.
Hernoemen gebeurt pas bij publicatie in de bibliotheek.

## Publicatienamen

In de bibliotheek (en in `_werk`): geen spaties; alleen kleine letters,
cijfers, `-` en `_`. Hub-bestanden hebben de **publicatiestam** uit het
bibliotheek-id (functie `stem()` in `scripts\bibliotheek.py`). Voorbeeld:
id `8-trisagion/8a-nederlands/hemelum` → `8-trisagion-8a-nederlands-hemelum.mscz`.
VSA-Coria: zelfde stam + `.vsa.mxl`. Bij meerdere Coria-bestanden in één map:
`{stam}.hub.mxl` / `{stam}.vsa.mxl` (`scripts\oefenhoek-product-contract.md`).
Het script `scripts\score_filenames.py` helpt bij opkuisen en layout.

## Koormap vs bibliotheek-id

| Veld | Betekenis |
| --- | --- |
| **Bibliotheek-id** | Drie lagen: `zangstuk/variant/uitvoeringsvorm` — staat in werkvoorraad en in `bieb` |
| **Koormap** | Kolom in werkvoorraad: welk liturgie-pad (bijv. `8-trisagion/8a-trisagion` of `9a-prokimen/weekdagen`) |

Weet je de bibliotheek-id niet? Laat **Doel-id** leeg en vraag na. Raad
niet. Lijst: [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/).

## Klaar als

Voor een willekeurig bestand kun je zeggen: input, tussenwerk, bibliotheek,
of koormap (sectie / slot-pagina). Je zet nooit een ruwe input rechtstreeks
in de bibliotheek.

{{< navbuttons "Volgende: bibliotheek en koormappen|/praktijk/handleiding/start/bibliotheek-en-koormappen/" >}}
