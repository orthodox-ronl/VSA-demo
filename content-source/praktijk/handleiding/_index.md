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

Een **bladermap** is de map op de site per zangstuk: daarin staan
`index.md` en de bestanden die koorleden zien (partituur, PDF, VSA).

{{< cue >}}
1. Nieuw ruw bestand → [Start](start/), daarna [binnenhalen](partituur/1-binnenhalen/).
2. Capella-`.mxl` → opkuisen → standaard-`.mscz` → review in MuseScore → layout opnieuw → `scripts\mscz-products.cmd`.
3. VOW-`.mscz` → sla opkuisen over; begin bij [standaard-.mscz](partituur/3-standaard-mscz/).
4. Tropaar-tekst → [.vsa schrijven](vsa/1-vsa-schrijven/), daarna eventueel [template SATB](vsa/2-template-satb/).
5. Koormap-vel buiten de hub-straat → [Print-.mscz](partituur/7-print-mscz/) (`*.print.mscz` + handmatige PDF).
6. Klaar voor koorleden → [bladermap](publiceren/1-bladermap/) + in `index.md`: `publicatiestatus: reviewable` + `scripts\check.cmd --strict`.
{{< /cue >}}

## Kies je pad

| Situatie | Begin hier |
| --- | --- |
| Je bent nieuw als beheerder, of je hebt lang geen conversiewerk gedaan | [Start](start/) — programma’s, mappen, woorden |
| Je hebt een Capella- of CapToMusic-bestand (`.mxl`, `.cap`, `.capx`) | [Partituur](partituur/) — vanaf opkuisen |
| Je hebt een VOW-bestand of een andere ruwe `.mscz` | [Standaard-.mscz](partituur/3-standaard-mscz/) |
| Je hebt alleen tekst op een bekende tropaar-melodie | [VSA](vsa/) |
| Je wilt één printvel (bijv. meerdere tekstregels) zonder Coria-pijplijn | [Print-.mscz](partituur/7-print-mscz/) |
| De publicatiebestanden liggen al klaar en moeten op de Oefenhoek | [Publiceren](publiceren/) |

## De route (van ruw tot Oefenhoek)

Er zijn **drie** sporen naar de bladermap. Meng ze niet in één ronde voor
hetzelfde zangstuk, tenzij je bewust een printvel *naast* hubs zet.

```text
ruwe input  (blijft in oefenhoek/input/, niet op de publieke site)
    |
    v
werkvoorraad  (doel-id kiezen; niet raden)
    |
    +-- partituur (hub):  opkuisen? -> standaard .mscz -> review -> PDF + Coria-.mxl
    |
    +-- VSA:              .vsa schrijven -> (optioneel) template SATB -> PDF + Coria-.mxl
    |
    +-- print-vel:        naam.print.mscz in MuseScore -> handmatige PDF (geen Coria)
    |
    v
bladermap  (index.md + bestanden, namen zonder spaties)
    |
    v
check --strict  ->  lokale preview  ->  Oefenhoek op de site
```

**Opkuisen** betekent: een Capella-`.mxl` met een script inhoudelijk
opschonen (lettergrepen, recitatief, titel) vóór MuseScore. Een
Capella-partituur, een tropaar-`.vsa` en een print-`.mscz` zijn drie
verschillende straten.

## Onderdelen

1. [Start](start/) — programma’s, mappen, woorden
2. [Partituur](partituur/) — van Capella/VOW naar hub-`.mscz`, PDF en Coria; plus [print-`.mscz`](partituur/7-print-mscz/)
3. [VSA](vsa/) — notatie schrijven en (voor tropaar toon 4) meerstemmig maken
4. [Publiceren](publiceren/) — bladermap, status, controle, als het misgaat

{{< navbuttons "Start|/praktijk/handleiding/start/" >}}
