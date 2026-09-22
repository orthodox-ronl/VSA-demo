---
title: "Ingebedde VSA"
linkTitle: "Ingebedde VSA"
weight: 70
---

# Ingebedde VSA

Dit werktraject betreft **VSA buiten** de oefenhoek-bibliotheek: notatie
in gewone content-pagina’s (demo’s, feesteigen, samenstellingen,
handleidingen). De site-build maakt daar SVG (en optioneel MusicXML)
onder `static\vsa\`.

{{< cue >}}
Zet `::: vsa-notatie` … `:::` of een `.vsa`-include in een markdownpagina
onder `content-source`. Draai daarna `scripts\check.cmd` of
`scripts\build.cmd` — de pipeline doet `vsa build-markdown` en
`vsa musicxml`. Dit is **geen** bibliotheek-`{stam}.vsa.mxl`.
{{< /cue >}}

## Waartoe

Je wilt VSA tonen op een pagina die geen bladermap onder
`oefenhoek\bibliotheek\` is — bijvoorbeeld een samenstelling of de
Tooling Demo — zonder `bieb` en zonder bibliotheek-id.

## Eindresultaat en criteria

| Output | Rol |
| --- | --- |
| SVG onder `static\vsa\` | Plaatje op de Hugo-pagina |
| Optioneel MXL onder `static\vsa\mxl\` | Embed-Coria voor die content-keten |

**Klaar** als: de pagina de SVG toont na build; `vsa validate` /
`validate_content` stil is voor die bronnen.

Dit vervangt **niet** sibling `{stam}.vsa.mxl` in de bibliotheek (dat is
[VSA](../vsa/)).

## Wanneer wel / wanneer niet

| Wel | Niet |
| --- | --- |
| Demo, feesteigen, samenstelling, handleiding | Oefenhoek-bibliotheek-uitvoeringsvorm → [VSA](../vsa/) + `bieb` |
| Inline `::: vsa-notatie` of include van een `.vsa` | Alleen een A4-PDF uit markdown → [Markdown naar PDF](../markdown-naar-pdf/) |

## Volgorde (bestanden)

1. Schrijf markdown onder `content-source` (buiten
   `oefenhoek\bibliotheek\…` als bladermap), met VSA-blokken of includes.
2. Bouw de site (of laat `check` de generate-stap doen):

```cmd
scripts\check.cmd --strict
```

   Intern: `vsa build-markdown` → `generated\content` + `static\vsa`;
   daarna `vsa musicxml content-source static\vsa\mxl` (embed-keten);
   sanitize/check op die MXL-map.
3. Preview: [Site-build](../site-build/).

## Automatisch (CI)

Onderdeel van elke PR-/push-build: `vsa build-markdown`,
`sync_oefenhoek_index.py --svg` (bibliotheek-SVG’s), `vsa musicxml`.
Geen apart “embed-product”-script; geen `vsa-products` voor deze pagina’s.

## Handmatig

| Situatie | Commando | Man-page |
| --- | --- | --- |
| Volledige keten | `scripts\check.cmd` of `scripts\build.cmd` | [check](../../scripts/check/), [build](../../scripts/build/) |
| Alleen bibliotheek-SVG | `scripts\oefenhoek-index.cmd --svg` | [oefenhoek-index](../../scripts/oefenhoek-index/) |

## Zie ook

- [VSA (bibliotheek)](../vsa/)
- [Site-build](../site-build/)
- Voorbeeldpagina’s onder `content-source\praktijk\demo\` en
  `content-source\praktijk\samenstellingen\`

{{< navbuttons "Markdown naar PDF|/praktijk/handleiding/werktrajecten/markdown-naar-pdf/" "mvsa|/praktijk/handleiding/werktrajecten/mvsa/" >}}
