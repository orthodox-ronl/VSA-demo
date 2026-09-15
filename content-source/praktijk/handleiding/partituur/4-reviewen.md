---
title: "Reviewen en opnieuw layouten"
linkTitle: "Reviewen"
weight: 40
---

# Reviewen en opnieuw layouten

{{< cue >}}
1. Open de `.mscz` in MuseScore 4. Corrigeer noten, tekst, herhalingen — **opslaan**.
2. Exporteer niet naar MusicXML.
3. Layout opnieuw:
```cmd
python scripts\apply_mscz_layout.py pad\naar\bestand.mscz
```
4. Open de `.mscz` opnieuw in MuseScore. Herhaal stappen 1–3 zo nodig.
5. Pas daarna [PDF en Coria](../5-pdf-en-coria/).
{{< /cue >}}

**Wat je nu doet:** controleren of noten, tekst, herhaling en
priester-/koor-cues kloppen. Daarna de standaard-layout opnieuw toepassen
zodat A4 niet scheef trekt.

**Wanneer:** altijd tussen de eerste layout-`.mscz` en het maken van PDF
of Coria-`.mxl`. Ook als het koor over een maand een fout meldt: dezelfde
ronde, niet opnieuw vanaf Capella tenzij de dump zelf fout was.

## Stap voor stap

1. Dubbelklik de `.mscz` in `_werk\` (of, als het bestand al in de
   bladermap staat, die bladermap-`.mscz`). MuseScore 4 opent.
2. Loop het stuk door, liefst met de liturgische tekst ernaast. Let op:
   - verkeerde of plakkerige lettergrepen
   - ontbrekende herhaling
   - cues `P:`, `D:`, `K:` (die horen in de partituur, niet in het titelvak)
   - een extra lege notenbalk (het layout-script haalt die meestal weg;
     zie je er toch een, “repareer” niet via MusicXML)
3. Bestand → Opslaan (Ctrl+S). Sluiten mag.
4. Layout opnieuw op **dezelfde** `.mscz` (geen `-o` nodig als de
   bestandsnaam al goed is):

```cmd
python scripts\apply_mscz_layout.py content-source\praktijk\oefenhoek\input\_werk\8a-trisagion\8a-trisagion.mscz
```

5. Open de `.mscz` opnieuw in MuseScore. Ziet de pagina er rarer uit dan
   vóór de layout? Het script zet de stijl bewust terug naar de standaard.
   Inhoudelijke fouten (verkeerde noot) lost het layout-script niet op —
   die verbeter je zelf in stap 2.

### Wat de layout niet mag overschrijven — en wat wel

Jij bent verantwoordelijk voor **inhoud** (noten, tekst, herhaling).
Het script is verantwoordelijk voor **uiterlijk** (A4, marges, fonts,
maatnummers). Daarom na elke editslag opnieuw layouten: anders loopt de
pagina vol of wijkt het stuk af van de andere Oefenhoek-stukken.

Nooit: MuseScore → Exporteren → MusicXML → weer openen. Dan begin je
van voren af aan, zonder stijl.

## Klaar als

Je hebt de `.mscz` zelf beluisterd of bekeken, opgeslagen, layout opnieuw
gedraaid, en het resultaat in MuseScore is aanvaardbaar voor het koor om
te reviewen.

{{< navbuttons "Volgende: PDF en Coria|/praktijk/handleiding/partituur/5-pdf-en-coria/" >}}
