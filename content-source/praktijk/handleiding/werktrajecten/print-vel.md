---
title: "Print-vel"
linkTitle: "Print-vel"
weight: 40
---

# Print-vel

Dit werktraject houdt een **print-`.mscz`** en een **handmatige PDF** bij
buiten de basispartituur-keten. Representatie-id: `print`.

{{< cue >}}
Bestandsnaam eindigt op **`.print.mscz`**. Geen `scripts\layout.cmd`, geen
`mscz-products`. Exporteer de PDF zelf in MuseScore 4 en commit die naast
het print-bestand in de bibliotheek. Zet op de bibliotheek-`index.md`
`artefacten_handmatig: true`.
{{< /cue >}}

## Waartoe

Soms heb je één A4-vel voor de koormap met layout of tekstregels die de
basispartituur-normalisatie zou vernielen, of een template-SATB-blad dat
jij zelf bijhoudt. Dat hoort **niet** door `layout` / `mscz-products` te
lopen.

## Eindresultaat en criteria

| Bestand (in de bladermap) | Rol |
| --- | --- |
| `{stam}.print.mscz` | MuseScore-bron; scripts laten dit met rust |
| `{stam}.print.pdf` of korte `{stam}.pdf` | Handmatige A4-export |
| Optioneel: Coria-`.mxl` / `.vsa` | Alleen als jij die zelf neerzet en bijhoudt |

**Klaar** als: `artefacten_handmatig: true` op de bibliotheek-`index.md`;
PDF staat naast het print-bestand; shortcode `bieb` toont de PDF; gele
beheerdersbanner op de bibliotheekpagina.

## Wanneer wel / wanneer niet

| Wel | Niet |
| --- | --- |
| Bewust buiten de basispartituur-spoor | Gewoon oefenmateriaal met automatische Coria → [Basispartituur](../basispartituur/) |
| Gecombineerd printvel, template-SATB | Eenstemmige notatie alleen → [VSA](../vsa/) |

Voorbeelden in de bibliotheek:
`7-kleine-intocht/zo-wk-mg/hemelum`,
`110-tropaar/nikolaas-van-myra-toon-4/hemelum`,
`20-moeder-godslied/ontslapen-moeder-gods/hemelum`.

## Volgorde (bestanden)

1. Maak of bewerk `{stam}.print.mscz` in MuseScore 4 (naam moet op
   `.print.mscz` eindigen).
2. Neem op via [Opnemen](../opnemen-in-bibliotheek/)
   (`bieb-accepteer`), of leg het bestand handmatig in de bladermap.
3. Exporteer PDF in MuseScore (Bestand → Exporteren → PDF) naar dezelfde
   map.
4. Zet frontmatter op `index.md`:

```yaml
artefacten_handmatig: true
```

5. Eventueel koormap-slot met `bieb`. HOW:
   [Print-.mscz](../../partituur/7-print-mscz/).
6. [Site-build](../site-build/).

## Automatisch (CI)

Geen automatische PDF/Coria uit `.print.mscz`. CI en `check` eisen geen
`partituur-sha256`-keten voor dit spoor. Maps met
`artefacten_handmatig: true` worden door `mscz-products` /
`vsa-products` overgeslagen.

## Handmatig

| Situatie | Actie |
| --- | --- |
| Layout / PDF / Coria | MuseScore 4 met de hand — **geen** `layout` / `mscz-products` |
| Opnemen | `scripts\bieb-accepteer.cmd` — [bieb-accepteer](../../scripts/bieb-accepteer/) |
| Controle | `scripts\check.cmd --strict` — [check](../../scripts/check/) |

## Zie ook

- HOW: [Print-.mscz](../../partituur/7-print-mscz/)
- Contract: `scripts\oefenhoek-product-contract.md` in `VSA-demo`

{{< navbuttons "VSA|/praktijk/handleiding/werktrajecten/vsa/" "Site-build|/praktijk/handleiding/werktrajecten/site-build/" >}}
