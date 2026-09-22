---
title: "PDF en Coria-.mxl maken"
linkTitle: "PDF en Coria"
weight: 50
---

# PDF en Coria-.mxl maken

{{< cue >}}
Basispartituur-`.mscz` staat in het **bibliotheek** (niet alleen in `_werk`). Daarna:
```cmd
scripts\mscz-products.cmd content-source\praktijk\oefenhoek\bibliotheek\8-trisagion\8a-nederlands\hemelum
```
Of heel `content-source`. `--force` als producten ouder zijn dan de basispartituur of
de bestandsdatum niet klopt. Lokale `check`/`build`/`serve` vernieuwen
stale basispartituur-producten ook automatisch. Weigert / slaat `*.print.mscz` over.
{{< /cue >}}

**Wat je nu doet:** uit de nagekeken, genormaliseerde **basispartituur-`.mscz`** twee
sibling-bestanden maken:

| Bestand | Rol |
| --- | --- |
| `{stam}.pdf` | A4-afdruk om te lezen of te printen |
| `{stam}.mxl` | MusicXML voor **Coria** (online oefenen) |

Beide krijgen een ingebedde `partituur-sha256` zodat `check` kan zien of PDF/MXL
nog bij de huidige basispartituur horen. Technische transforms staan in
`scripts\mscz-product-transforms.md` in `VSA-demo`.

Dit is het **partituur**-spoor (representatie-id `partituur`). Eenstemmige VSA gebruikt
`{stam}.vsa.mxl` via [`.vsa schrijven`](../../vsa/1-vsa-schrijven/). Als in
één map ooit twee Coria-bestanden nodig zijn, gebruik expliciete namen
`{stam}.partituur.mxl` / `{stam}.vsa.mxl` — zie
`scripts\oefenhoek-product-contract.md`.

**Wanneer:** ná [reviewen en opnieuw normaliseren](../4-reviewen/). Niet
meteen na de eerste normalisatie als je nog gaat editen: dan maak je de
producten twee keer. Bij een latere basispartituur-wijziging: opnieuw normaliseren,
daarna opnieuw deze stap (of [Afgeleiden](../6-afgeleiden/)).

## Voorwaarden

1. De basispartituur-`.mscz` ligt in het **bibliotheek**, niet alleen in
   `input\_werk\`. Padvoorbeeld:
   `content-source\praktijk\oefenhoek\bibliotheek\8-trisagion\8a-nederlands\hemelum\8-trisagion-8a-nederlands-hemelum.mscz`.
2. Die `.mscz` is na de laatste inhoudelijke edit opnieuw genormaliseerd
   (`scripts\layout.cmd`).
3. **MuseScore 4** is geïnstalleerd (het product-script roept MuseScore aan).
4. Dit is een **basispartituur**-bestand, geen `*.print.mscz` — printvel: PDF handmatig
   ([Print-.mscz](../7-print-mscz/)).

## Stap voor stap

1. Zet de `.mscz` in de bibliotheek als die daar nog niet staat. Gebruik
   bij voorkeur
   [opnemen in de bibliotheek](../../publiceren/1-opnemen-in-bibliotheek/)
   (`scripts\bieb-accepteer.cmd`), zodat map, `index.md` en bestandsnaam
   kloppen. Handmatig: kopieer uit `_werk` naar de publicatiestam zonder
   spaties:

```text
content-source\praktijk\oefenhoek\bibliotheek\8-trisagion\8a-nederlands\hemelum\
  8-trisagion-8a-nederlands-hemelum.mscz
```

   Koormap-slot en verdere publicatie: zie
   [Bibliotheek en koormap](../../publiceren/1-bladermap/).

2. Open het opdrachtvenster in `VSA-demo` en maak de producten:

```cmd
scripts\mscz-products.cmd content-source\praktijk\oefenhoek\bibliotheek\8-trisagion\8a-nederlands\hemelum
```

   Of alles onder content-source:

```cmd
scripts\mscz-products.cmd content-source
```

3. In die bibliotheek-map horen naast de `.mscz` ook
   `8-trisagion-8a-nederlands-hemelum.pdf` en
   `8-trisagion-8a-nederlands-hemelum.mxl` (zelfde stam).

4. Open de PDF even in een PDF-viewer: pagina A4, titel, colofon, tekst
   leesbaar.
5. Coria test je ná `scripts\check.cmd --strict` op het **koormap-slot**
   (knop **Oefenen** komt uit de Oefenhoek-acties op die pagina — niet uit
   een `.mxl` onder `input\`).

### Vernieuwen of forceren

| Situatie | Actie |
| --- | --- |
| PDF/MXL ouder dan de basispartituur-`.mscz` | Gewoon opnieuw `mscz-products` — of `check` lokaal (pipeline vernieuwt stale) |
| Basispartituur inhoudelijk gewijzigd maar bestandsdatum klopt niet | Zet `--force` achter het commando |
| Preview toont een banner dat basispartituur-afgeleiden niet kloppen | Zie [Afgeleiden](../6-afgeleiden/); opnieuw producten ná laatste normalisatie |

## Wat je niet doet

- Geen Coria-`.mxl` uit Capella of uit “Exporteren als MusicXML” in
  MuseScore gebruiken als publicatiebestand.
- Geen producten maken van een basispartituur die je daarna nog gaat editen zonder
  opnieuw te normaliseren én producten te vernieuwen.
- Geen `mscz-products` verwachten voor `*.print.mscz`.

## Klaar als

In de bibliotheek liggen `.mscz`, `.pdf` en `.mxl` met dezelfde
publicatiestam; de PDF ziet er basispartituur-achtig uit; je kunt door naar
[bibliotheek en koormap](../../publiceren/1-bladermap/).

{{< navbuttons "Volgende: afgeleiden|/praktijk/handleiding/partituur/6-afgeleiden/" >}}
