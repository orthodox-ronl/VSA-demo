---
title: "Capella opkuisen"
linkTitle: "Opkuisen"
weight: 20
---

# Capella opkuisen

{{< cue >}}
```cmd
python scripts\cleanup_capella_mxl.py "content-source\praktijk\oefenhoek\input\capella\NAAM.mxl" -o content-source\praktijk\oefenhoek\input\_werk\DOEL-ID\DOEL-ID.mxl
```
VOW-`.mscz`: sla deze pagina over. Het Capella-origineel blijft in `capella\`; schrijf uitvoer **zonder spaties** via `-o`.
{{< /cue >}}

**Wat je nu doet:** van een Capella-`.mxl` een schone `.mxl` maken die
MuseScore aankan (lettergrepen per noot, recitatief, titel, geen lege
maten). **Opkuisen** is die inhoudelijke opschoning. Het is nog geen
mooie A4-layout.

**Wanneer:** de herkomst is Capella of CapToMusic. Heb je al een
VOW-`.mscz`, ga naar [standaard-.mscz](../3-standaard-mscz/).

## Stap voor stap

1. Ken het doel-id (bijvoorbeeld `8a-trisagion`). Nog geen id? Ga terug
   naar [binnenhalen](../1-binnenhalen/).
2. Maak de tussenwerk-map
   `content-source\praktijk\oefenhoek\input\_werk\<doel-id>\`
   (Verkenner: nieuwe map; het script kan de map ook aanmaken bij
   schrijven).
3. Draai het commando. Zet de **jouw** bestandsnaam tussen
   aanhalingstekens als er spaties in zitten. Voorbeeld met het Trisagion:

```cmd
python scripts\cleanup_capella_mxl.py "content-source\praktijk\oefenhoek\input\capella\8a - trisagion.mxl" -o content-source\praktijk\oefenhoek\input\_werk\8a-trisagion\8a-trisagion.mxl
```

4. Wacht tot de prompt terugkomt. Fout over spaties in de *uitvoer*naam:
   gebruik `-o` naar een schone naam; overschrijf het Capella-origineel
   niet.

Je hoeft de interne lagen van het script niet te kennen. Kort: het script
maakt verborgen reciteernoten zichtbaar, koppelt tekst aan noten, en ruimt
Capella-rommel op. Layout (A4, lettertypes) komt in de **volgende** stap.

## Klaar als

Er ligt een `.mxl` **zonder spaties** in `_werk\<doel-id>\`, en het
bestand in `input\capella\` is ongewijzigd.

{{< navbuttons "Volgende: standaard-.mscz|/praktijk/handleiding/partituur/3-standaard-mscz/" >}}
