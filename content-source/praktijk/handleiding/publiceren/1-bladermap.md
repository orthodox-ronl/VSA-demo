---
title: "Bibliotheek en koormap"
linkTitle: "Bibliotheek en koormap"
weight: 10
---

# Bibliotheek en koormap

{{< cue >}}
Bibliotheek-map:
`content-source\praktijk\oefenhoek\bibliotheek\<zangstuk>\<variant>\<uitvoeringsvorm>\`
met `index.md` + hub/PDF/Coria/VSA (publicatiestam zonder spaties).

Koormap-slot:
`content-source\praktijk\oefenhoek\liturgiemap-hemelum\…\index.md` met
shortcode `bibliotheek-score` (parameter `id` = bibliotheek-id) en
`automatische_inhoud: false`.

Id-lijst: [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/).
{{< /cue >}}

**Wat je nu doet:** oefenbestanden in het **bibliotheek** zetten en het
**koormap-slot** laten verwijzen. Koorleden openen meestal de liturgiemap;
de partituur komt uit de bibliotheek.

**Wanneer:** na partituur-producten of na een werkende `.vsa`. Familie
(meerdere varianten): `_index.md` in bibliotheek en in de koormap — kopieer
een bestaande structuur (antifoon, kleine intocht).

## Stap voor stap (bibliotheek)

1. Kies het **bibliotheek-id** (drie lagen). Onbekend? Zie
   [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/) of vraag na;
   niet verzinnen.
2. Maak de map
   `bibliotheek\<zangstuk>\<variant>\<uitvoeringsvorm>\`.
3. Kopieer hub-`.mscz`, `.pdf`, `.mxl` en/of `.vsa` naar die map. Bestandsnamen =
   publicatiestam + extensie (bijv. `8-trisagion-8a-nederlands-hemelum.mscz`).
4. Maak `index.md` in de bibliotheek door een **bestaand** voorbeeld te
   kopiëren:

| Wat je hebt | Kopieer bibliotheek-`index.md` van |
| --- | --- |
| Hub + PDF + Coria | `bibliotheek\8-trisagion\8a-nederlands\hemelum\` |
| Alleen VSA | `bibliotheek\2-eerste-antifoon\weekdagen-hemelum\hemelum\` |
| Hub + VSA + PDF + Coria | `bibliotheek\8-trisagion\8a-nederlands\hemelum\` |
| Print + handmatige PDF/MXL + VSA | `bibliotheek\tropaar-nikolaas-van-myra\liturgikon\hemelum\` (`*.print.mscz`, `artefacten_handmatig: true`) |
| Print-vel | `bibliotheek\7-kleine-intocht\zo-wk-mg\hemelum\` |

In de bibliotheek-`index.md` horen `publicatiestatus`, `automatische_inhoud:
false`, en meestal de shortcode `bibliotheek-score` (zelfde id als de map).

## Stap voor stap (koormap-slot)

1. Open het liturgie-slot (bijv.
   `liturgiemap-hemelum\8-trisagion\8a-trisagion\index.md`).
2. Zorg dat alleen **`index.md`** in die slotmap staat — geen `.mscz` meer
   in de koormap.
3. Frontmatter: `automatische_inhoud: false`, `publicatiestatus` passend
   bij wat koorleden zien.
4. In de body: titel + shortcode `bibliotheek-score` met jouw id (voorbeeld:
   `8-trisagion/8a-nederlands/hemelum`).

| Situatie | Koormap-voorbeeld |
| --- | --- |
| Hub via bibliotheek | `liturgiemap-hemelum\8-trisagion\8a-trisagion\index.md` |
| VSA via bibliotheek | `liturgiemap-hemelum\2-eerste-antifoon\weekdagen\hemelum\index.md` |
| Catalogus (geen lokale hub) | `troparen-en-kondaken\kondak-moeder-gods-toon-6\index.md` — **geen** `bibliotheek-score`; `:::include` catalogus blijft |

5. Hoort het stuk in het liturgie-overzicht? Controleer
   `liturgiemap-hemelum\_index.md` (handmatige inhoudsopgave).

## Eénmalig migreren (bestaande site)

Als veel slots nog hub-bestanden in de koormap hebben:

```cmd
python scripts\migrate_oefenhoek_bibliotheek.py
```

Niet in `check`. Daarna legacy-dubbelen opruimen (zie ID-REGISTER).

## Klaar als

Na `check --strict` toont de preview het koormap-slot met PDF/Coria/VSA via
`bibliotheek-score`. De bibliotheek heeft de bestanden; de koormap-slotmap
heeft geen hub meer.

{{< navbuttons "Volgende: status en check|/praktijk/handleiding/publiceren/2-status-en-check/" >}}
