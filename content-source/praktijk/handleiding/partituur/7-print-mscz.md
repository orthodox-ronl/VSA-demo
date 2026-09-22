---
title: "Print-.mscz (koormap-vel)"
linkTitle: "Print-.mscz"
weight: 70
---

# Print-`.mscz` (koormap-vel)

{{< cue >}}
Bestandsnaam eindigt op **`.print.mscz`**. Geen `scripts\layout.cmd`, geen
`mscz-products`, geen Coria-eis uit dit MuseScore-bestand. PDF maak je zelf in
MuseScore 4 (Bestand → Exporteren → PDF) en commit je naast het print-bestand
**in het bibliotheek**. Zet op de bibliotheek-`index.md`
`artefacten_handmatig: true` (gele beheerdersbanner).
{{< /cue >}}

**Wat je nu doet:** een MuseScore-bestand in het **bibliotheek** zetten dat de
basispartituur-pijplijn **niet** mag aanpassen — typisch één A4-vel voor de koormap met
layout of tekstregels die de basispartituur-normalisatie zou vernielen, of een
template-SATB-blad dat jij handmatig bijhoudt. Het koormap-slot verwijst met
`bieb`.

**Wanneer:** als je bewust **buiten** de basispartituur-spoor werkt. Voor gewoon
oefenmateriaal (één tekst, automatische Coria, standaardlayout) gebruik je een
gewone basispartituur-`.mscz` via [standaard-.mscz](../3-standaard-mscz/) en
[PDF en Coria](../5-pdf-en-coria/), of een eenstemmige `.vsa` via
[.vsa schrijven](../../vsa/1-vsa-schrijven/).

Voorbeelden in de bibliotheek:

- `7-kleine-intocht/zo-wk-mg/hemelum` — gecombineerd printvel;
- `110-tropaar/nikolaas-van-myra-toon-4/hemelum` — template-SATB + handmatige
  PDF/MXL + `.vsa`;
- `20-moeder-godslied/ontslapen-moeder-gods/hemelum` — idem print + handmatig.

## Wat het is

| In Verkenner (bibliotheek) | Rol |
| --- | --- |
| `{stam}.print.mscz` | MuseScore-bron voor een printvel; scripts laten dit met rust |
| `{stam}.pdf` | Handmatige A4-export |
| Optioneel: Coria-`.mxl` | Alleen als jij die zelf neerzet en bijhoudt (geen `mscz-products`) |
| Optioneel: `.vsa` | Notatie naast het printvel; `vsa-products` slaat de map over bij `artefacten_handmatig: true` |

Bibliotheek-id voorbeeld: `7-kleine-intocht/zo-wk-mg/hemelum`.

Frontmatter op bibliotheek-`index.md`:

```yaml
artefacten_handmatig: true
```

Die regel betekent: PDF, Coria-`.mxl` en andere afgeleiden in **deze** map
worden niet automatisch bijgewerkt. De bibliotheekpagina toont een gele
beheerdersmelding. Afspraak over bestandsnamen per spoor:
`scripts\oefenhoek-product-contract.md`.

## Wat je niet doet

- Geen `scripts\layout.cmd` op `.print.mscz`.
- Geen `mscz-products.cmd` voor dit bestand.
- Geen hernoemen naar gewone `.mscz` “even snel” — dan eist `check` basispartituur-producten.
- Geen verwachting dat `vsa-products` de Coria-`.mxl` vernieuwt zolang
  `artefacten_handmatig: true` staat.

## Stap voor stap

1. Bewerk in MuseScore 4. Neem het bestand op met
   [bieb-accepteer](/praktijk/handleiding/publiceren/1-opnemen-in-bibliotheek/)
   (bestandsnaam eindigend op `.print.mscz`), of sla handmatig op als
   `{stam}.print.mscz` in de bibliotheek (geen spaties; stam uit
   bibliotheek-id).
2. Exporteer PDF handmatig naar `{stam}.pdf` in dezelfde bibliotheek-map.
   Eventuele Coria-`.mxl` eveneens handmatig (of uit de template-render)
   ernaast zetten en bij elke bronwijziging meenemen.
3. Bibliotheek-`index.md` met `artefacten_handmatig: true` (bieb-accepteer
   zet dat automatisch bij `.print.mscz`) + koormap-slot met `bieb` (zie
   [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/)).
4. `scripts\check.cmd --strict` — partituur- en VSA-productgate slaan deze map over.

## Klaar als

Bibliotheek bevat `*.print.mscz` en PDF (plus eventueel handmatige `.mxl` /
`.vsa`); `artefacten_handmatig: true` staat op de `index.md`; koormap-slot
verwijst ernaar; check klaagt niet over ontbrekende automatische Coria voor
dit printvel.

{{< navbuttons "Terug: afgeleiden|/praktijk/handleiding/partituur/6-afgeleiden/" "Handleiding|/praktijk/handleiding/" >}}
