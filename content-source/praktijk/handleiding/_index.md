---
title: "Handleiding voor beheerders"
linkTitle: "Handleiding"
weight: 100
hide_page_list: true
hide_section_list: true
---

Deze handleiding is bedoeld voor **beheerders**: mensen die zangmateriaal
klaarzetten voor de Oefenhoek. Het traject loopt van een ruw aangeleverd
bestand tot een pagina waarop koorleden kunnen oefenen (of, bij een
printvel, tot een PDF in de koormap).

Koorleden die alleen willen zingen, gebruiken de
[Oefenhoek](../oefenhoek/), niet deze handleiding.

Je hoeft geen programmeur te zijn. Om het werk uit te voeren heb je drie
dingen nodig:

1. het notatieprogramma **MuseScore 4** (gratis te installeren);
2. de repository-map **`VSA-demo`** op je pc (niet alleen deze website in
   de browser — je bewerkt bestanden lokaal, zie
   [Wat heb je nodig](start/wat-heb-je-nodig/));
3. het **Windows-opdrachtvenster** (`cmd`), waarin je kant-en-klare
   regels plakt die deze handleiding geeft.

**Bibliotheek** is de catalogus met oefenbare bestanden (hub-`.mscz`,
PDF, Coria-`.mxl`, `.vsa`, of print-`.mscz`). **Koormap** is een geordende
route op de site (nu vooral de Hemelum-liturgiemap): inhoudsopgave van
liturgische plekken (secties), met slot-pagina’s die via `bieb`
naar de bibliotheek verwijzen. Partituren horen in de bibliotheek, niet in
de koormap-map. Model (boom versus compositieblad):
[Bibliotheek en koormappen](start/bibliotheek-en-koormappen/).

{{< cue >}}
0. Welk spoor? → [Publicatietrajecten](start/publicatietrajecten/) (hub / VSA / print / site-build)
1. Nieuw ruw bestand → [Start](start/), daarna [binnenhalen](partituur/1-binnenhalen/).
2. Capella-`.mxl` → opkuisen → normaliseren (standaard-`.mscz`) → review in MuseScore → opnieuw normaliseren → `scripts\mscz-products.cmd`.
3. VOW-`.mscz` → Capella-script overslaan; wel stemmen/lettergrepen checken ([opkuisen](partituur/2-opkuisen/)), daarna [standaard-.mscz](partituur/3-standaard-mscz/).
4. Eenstemmige tekst → [.vsa schrijven](vsa/1-vsa-schrijven/) (SVG + Coria-`.vsa.mxl` via `check`); tropaar toon 4 optioneel [template SATB](vsa/2-template-satb/).
5. Print-vel → [Print-.mscz](partituur/7-print-mscz/) in de bibliotheek (`*.print.mscz` + handmatige PDF; vaak `artefacten_handmatig: true`).
6. Klaar voor de bibliotheek → [opnemen in de bibliotheek](publiceren/1-opnemen-in-bibliotheek/) (`bieb-accepteer`), daarna [koormap](publiceren/1-bladermap/) + `scripts\check.cmd --strict`.
{{< /cue >}}

## Kies je pad

| Situatie | Begin hier |
| --- | --- |
| Je bent nieuw als beheerder, of je hebt lang geen conversiewerk gedaan | [Start](start/) — programma’s, mappen, woorden |
| Je hebt een Capella- of CapToMusic-bestand (`.mxl`, `.cap`, `.capx`) | [Partituur](partituur/) — vanaf opkuisen |
| Je hebt een VOW-bestand of een andere ruwe `.mscz` | [Opkuisen](partituur/2-opkuisen/) (stemmen/lettergrepen), daarna [standaard-.mscz](partituur/3-standaard-mscz/) |
| Je hebt alleen tekst op een bekende melodie (antifoon, communievers, …) | [VSA](vsa/) — eenstemmig + Coria |
| Je wilt één printvel (bijv. meerdere tekstregels) of handmatig bijgehouden PDF/MXL | [Print-.mscz](partituur/7-print-mscz/) |
| De publicatiebestanden liggen al klaar en moeten op de Oefenhoek | [Opnemen in de bibliotheek](publiceren/1-opnemen-in-bibliotheek/) |

## De route (van ruw tot Oefenhoek)

Er zijn **drie** sporen naar de bibliotheek. Meng ze niet in één ronde voor
hetzelfde zangstuk, tenzij je bewust een printvel *naast* hubs zet.

```text
ruwe input  (blijft in oefenhoek/input/, niet op de publieke site)
    |
    v
werkvoorraad  (bibliotheek-id kiezen; niet raden — zie ID-REGISTER)
    |
    +-- partituur (hub):  opkuisen -> normaliseren -> review -> PDF + Coria-.mxl
    |
    +-- VSA:              .vsa schrijven -> SVG + Coria-.vsa.mxl (check/vsa-products)
    |                     (optioneel tropaar toon 4: template SATB)
    |
    +-- print-vel:        naam.print.mscz -> handmatige PDF (+ eventueel handmatige .mxl)
    |
    v
bibliotheek  (via bieb-accepteer: index.md + bestanden, publicatiestam)
    |
    v
koormap  (sectie-_index of slot-index.md met bieb; geen catalogus/lokaal-include)
    |
    v
check --strict  ->  lokale preview  ->  Oefenhoek op de site
```

**Opkuisen** is inhoudelijke opschoning (stemmen, lettergrepen↔noten);
**normaliseren** / **layouten** is de hub-standaard met
`apply_mscz_layout.py`. Kort overzicht: [Partituur](partituur/). Een
Capella-partituur, een tropaar-`.vsa` en een print-`.mscz` zijn drie
verschillende straten. Opnemen in de catalogus:
[Opnemen in de bibliotheek](publiceren/1-opnemen-in-bibliotheek/).

Id-lijst: [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/).

## Onderdelen

1. [Start](start/) — programma’s, mappen, woorden
2. [Partituur](partituur/) — van Capella/VOW naar hub-`.mscz`, PDF en Coria; plus [print-`.mscz`](partituur/7-print-mscz/)
3. [VSA](vsa/) — notatie schrijven, Coria-`.vsa.mxl`, en (voor tropaar toon 4) template SATB
4. [Publiceren](publiceren/) — opnemen (`bieb-accepteer`), koormap, status, controle, als het misgaat

{{< navbuttons "Start|/praktijk/handleiding/start/" >}}
