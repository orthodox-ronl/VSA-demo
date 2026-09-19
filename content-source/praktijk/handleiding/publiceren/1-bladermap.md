---
title: "Bibliotheek en koormap"
linkTitle: "Bibliotheek en koormap"
weight: 10
---

# Bibliotheek en koormap

{{< cue >}}
Bibliotheek-map:
`content-source\praktijk\oefenhoek\bibliotheek\<zangstuk>\<variant>\<uitvoeringsvorm>\`
met `index.md` + oefenbestanden (hub/PDF/Coria/VSA of print; publicatiestam
zonder spaties).

Slot-pagina in de koormap:
`content-source\praktijk\oefenhoek\liturgiemap-hemelum\…\index.md` met
shortcode `bieb` (parameter `id` = bibliotheek-id) en
`automatische_inhoud: false`.

Een **alias-variant** (andere naam voor dezelfde variant) krijgt geen
uitvoeringsvorm-map. Zet `alias_van` op de variant-`_index.md`; zie
[Bibliotheek en koormappen](../../start/bibliotheek-en-koormappen/).

Koormap-sectie (hoofdstuk): map met `_index.md` — kindlijst of eigen TOC;
zie [Bibliotheek en koormappen](../../start/bibliotheek-en-koormappen/).

Id-lijst: [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/).
{{< /cue >}}

**Wat je nu doet:** oefenbestanden in het **bibliotheek** zetten en de
**koormap** laten verwijzen. Koorleden openen meestal de liturgiemap; de
partituur komt uit de bibliotheek.

**Wanneer:** na partituur-producten of na een werkende `.vsa`. Familie
(meerdere varianten op één liturgische plek): `_index.md` in bibliotheek en
in de koormap — kopieer een bestaande structuur (antifoon, kleine intocht).

## Stap voor stap (bibliotheek)

1. Kies het **bibliotheek-id** (drie lagen). Onbekend? Zie
   [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/) of vraag na;
   niet verzinnen.
2. Maak de map
   `bibliotheek\<zangstuk>\<variant>\<uitvoeringsvorm>\`.
3. Kopieer de oefenbestanden naar die map. Bestandsnamen = publicatiestam +
   extensie (bijv. `8-trisagion-8a-nederlands-hemelum.mscz`). Bij VSA-Coria
   hoort `{stam}.vsa.mxl` naast de `.vsa`. Als één map **twee** Coria- of
   PDF-bestanden van verschillende sporen nodig heeft: gebruik
   `{stam}.hub.mxl` / `{stam}.vsa.mxl` (zie
   `scripts\oefenhoek-product-contract.md`).
4. Maak `index.md` in de bibliotheek door een **bestaand** voorbeeld te
   kopiëren:

| Wat je hebt | Kopieer bibliotheek-`index.md` van |
| --- | --- |
| Hub + PDF + Coria | `bibliotheek\8-trisagion\8a-nederlands\hemelum\` |
| Alleen VSA (+ auto Coria-`.vsa.mxl`) | `bibliotheek\2-eerste-antifoon\weekdagen-hemelum\hemelum\` |
| Print + handmatige PDF/MXL (+ optioneel `.vsa`) | `bibliotheek\tropaar-nikolaas-van-myra\liturgikon\hemelum\` (`*.print.mscz`, `artefacten_handmatig: true`) |
| Print-vel (alleen PDF) | `bibliotheek\7-kleine-intocht\zo-wk-mg\hemelum\` |

In de bibliotheek-`index.md` horen `publicatiestatus`, `automatische_inhoud:
false`, en meestal de shortcode `bieb` (zelfde id als de map).
Bij print of template-export die jij zelf bijhoudt: ook
`artefacten_handmatig: true`.

## Stap voor stap (slot-pagina in de koormap)

1. Open of maak de slot-pagina (bijv.
   `liturgiemap-hemelum\8-trisagion\8a-trisagion\index.md`).
2. Zorg dat alleen **`index.md`** in die slotmap staat — geen `.mscz` meer
   in de koormap.
3. Frontmatter: `automatische_inhoud: false`, `publicatiestatus` passend
   bij wat koorleden zien.
4. In de body: titel + shortcode `bieb` met jouw id (voorbeeld:
   `8-trisagion/8a-nederlands/hemelum`).

| Situatie | Koormap-voorbeeld |
| --- | --- |
| Hub via bibliotheek | `liturgiemap-hemelum\8-trisagion\8a-trisagion\index.md` |
| VSA via bibliotheek | `liturgiemap-hemelum\2-eerste-antifoon\weekdagen\index.md` |
| Sectie (boom van keuzes) | `liturgiemap-hemelum\15-cherubijnenhymne\_index.md` + kindmappen |
| Compositieblad (meerdere scores) | Eén `index.md` met markdown en meerdere `bieb`-shortcodes — zie [Bibliotheek en koormappen](../../start/bibliotheek-en-koormappen/) |
| Diversen / tropaar / kondak | Bijv. `diversen/uw-heilig-kruis/hemelum`, `tropaar/…`, `kondak/…` — altijd `bieb`, geen `:::include` |

5. Hoort het stuk in het liturgie-overzicht? Controleer
   `liturgiemap-hemelum\_index.md` (handmatige inhoudsopgave).

### Meerdere shortcodes op één slot-pagina

Op een compositieblad mag je **meerdere** `bieb`-shortcodes
zetten (elk met een eigen bibliotheek-id). Elke shortcode zet eerst de
knoppen **Oefenen** / **Downloaden** / **Printen** voor die uitvoeringsvorm,
en daarna de PDF of VSA-SVG. Zo heeft elke score op dezelfde pagina een
eigen knoppenrij.

## Eénmalig migreren (bestaande site)

Als veel slots nog hub-bestanden in de koormap hebben:

```cmd
python scripts\migrate_oefenhoek_bibliotheek.py
```

Niet in `check`. Daarna legacy-dubbelen opruimen (zie ID-REGISTER).

## Klaar als

Na `check --strict` toont de preview de slot-pagina met PDF/**Oefenen**/VSA
via `bieb`. De bibliotheek heeft de bestanden; de
koormap-map heeft geen hub meer. Je weet wanneer je een sectie (boom)
gebruikt en wanneer een compositieblad.

{{< navbuttons "Volgende: status en check|/praktijk/handleiding/publiceren/2-status-en-check/" >}}
