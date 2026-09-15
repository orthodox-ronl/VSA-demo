---
title: "Als het misgaat"
linkTitle: "Als het misgaat"
weight: 30
---

# Als het misgaat

{{< cue >}}
Spaties in de bladermap-naam? Hernoemen. Layout kwijt? Niet via MusicXML;
wel `apply_mscz_layout.py` op de `.mscz`. Coria rood bij `check`? Gebruik
de `.mxl` in de bladermap, niet een `.mxl` onder `input\`. MuseScore niet
gevonden? Versie **4**, pad `C:\Program Files\MuseScore 4\bin\MuseScore4.exe`.
{{< /cue >}}

**Wat je nu doet:** de veelvoorkomende blokkades herkennen. Blijft het
stuk: bewaar de fouttekst en vraag na; probeer niet drie andere scripts
tegelijk.

## Spaties of rare tekens in de naam

**Symptoom:** een script weigert, Coria doet het niet, of `check` klaagt.

Publicatiebestanden: geen spaties, geen `(` of `+`. Stam alleen
`a-z0-9_-`. Ruwe dumps in `input\` mogen hun oude naam houden. Schrijf
uitvoer altijd met `-o` naar een schone naam.

## Doel-id leeg of twijfel

Niet verzinnen. Zet in de werkvoorraad-rij een notitie “welke bladermap?”
en vraag het na. Twee dumps naar dezelfde bladermap mag (Capella én VOW);
noteer dat in de notitie.

## Layout of `mscz-products` “herstelt” je speciale partituur

Eindigt de bestandsnaam op `.print.mscz`? Dan hoort die **niet** door
`apply_mscz_layout` of `mscz-products`. Zie
[Print-.mscz](/praktijk/handleiding/partituur/7-print-mscz/). Per ongeluk
als gewone `.mscz` gezet? Hernoem terug naar `.print.mscz` vóór de
volgende `check`.

## MuseScore start niet / “niet gevonden”

Layout en `mscz-products` hebben MuseScore **4** nodig. Installeer
MuseScore 4; gebruik niet MuseScore 3. Open het opdrachtvenster opnieuw
na installatie.

## De pagina is lelijk of de stijl is weg

Meestal: geëxporteerd naar MusicXML en weer geopend. Ga terug naar de
`.mscz` (of opnieuw vanaf opgekuiste `.mxl` plus layout). Daarna:

```cmd
python scripts\apply_mscz_layout.py pad\naar\bestand.mscz
```

## Coria: `translation failed` of check weigert de `.mxl`

De `.mxl` in de bladermap moet uit `mscz-products` (of de
VSA-template-render) komen, niet een ruwe Capella-`.mxl`. Maak de
producten opnieuw ná de laatste layout. `check` heeft een aparte
Coria-controle; de melding wijst het bestand aan.

## `vsa validate` klaagt

De markering zit in de gezongen regel. Vergelijk met een werkend `.vsa`
ernaast. Haal niet “even de rare tekens weg” om groen te worden.

## Template SATB: `TemplateInstanceError`

De sopraan in de VSA volgt de tropaar-toon-4-formule niet (toon of
verplicht slot). Lees de hint in het venster; pas de VSA aan, of (met
iemand die de formule beheert) de template. Werk de `.mscz` niet als
eerste bron van waarheid bij.

## `publicatiestatus` ontbreekt

Elke Oefenhoek-`index.md` en `_index.md` moet de regel `publicatiestatus`
in de `---` hebben. Handleiding-pagina’s niet.

## Preview op de verkeerde poort

http://127.0.0.1:**18731**/ — niet 1313.

## Check rood, lange muur tekst

Scroll naar het **eerste** `FAILED` of `error`. Vaak is één bestand de
oorzaak. Los dat ene bestand op, draai check opnieuw. Pak niet de hele
foutenmuur tegelijk aan.

## Waar vraag je het

Gebruik dezelfde kanalen als op de Oefenhoek-pagina’s (e-mail / GitHub).
Stuur mee: welk doel-id, welk commando, de foutregel, en of het om
Capella, VOW of VSA gaat.

{{< navbuttons "Terug naar overzicht|/praktijk/handleiding/" >}}
