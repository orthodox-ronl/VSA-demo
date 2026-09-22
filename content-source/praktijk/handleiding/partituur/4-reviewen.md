---
title: "Reviewen en opnieuw normaliseren"
linkTitle: "Reviewen"
weight: 40
---

# Reviewen en opnieuw normaliseren

{{< cue >}}
1. Open de basispartituur-`.mscz` in MuseScore 4. Corrigeer noten, tekst, herhalingen,
   stemmen, cues — **opslaan** (Ctrl+S). Exporteer niet naar MusicXML.
2. Opnieuw normaliseren (layouten):
```cmd
scripts\layout.cmd pad\naar\bestand.mscz
```
3. Open de `.mscz` opnieuw in MuseScore 4. Herhaal 1–2 zo nodig.
4. Daarna pas [PDF en Coria](../5-pdf-en-coria/).
{{< /cue >}}

**Wat je nu doet:** de basispartituur-`.mscz` inhoudelijk controleren en corrigeren, en
daarna de basispartituur-standaard **opnieuw** toepassen met
`scripts\layout.cmd` (normaliseren / layouten). Zonder die tweede slag
blijven A4, fonts, reciteertoon-encoding of copyright uit de pas lopen met
de rest van de Oefenhoek.

**Wanneer:** altijd tussen de eerste genormaliseerde basispartituur-`.mscz` en het maken
van PDF of Coria-`.mxl`. Ook als het koor later een fout meldt: dezelfde
ronde. Alleen opnieuw vanaf Capella als de **input** zelf fout was.

## Twee rollen in deze ronde

| Rol | Wie / wat | Voorbeelden |
| --- | --- | --- |
| **Inhoud** (opkuisen tijdens review) | Jij in MuseScore 4 | Verkeerde noot, plakkerige lettergreep, SAT op de verkeerde balk, ontbrekende herhaling, cue in het titelvak |
| **Basispartituur-vorm** (normaliseren / layouten) | `scripts\layout.cmd` | A4, marges, Source Sans 3, maatnummers, reciteertoon-collaps, zichtbare eindmaatstrepen, tempo-default, copyright-footer/colofon |

Uitgebreide inhoudschecklist: [Opkuisen](../2-opkuisen/).
Uitgebreide scriptlijst: [Standaard-.mscz](../3-standaard-mscz/).

## Review-checklist (inhoud)

Open de `.mscz` in `_werk\<stam>\` of, als het bestand al in het
**bibliotheek** staat, die basispartituur-`.mscz`. Loop het stuk door, liefst met de
liturgische tekst ernaast. Vink af:

### Noten en vorm

- [ ] Juiste toonhoogtes en lengtes (cadensen niet per ongeluk tot recitatief
      gemaakt of omgekeerd).
- [ ] Herhalingen en herhalingstekens kloppen met de liturgische praktijk.
- [ ] Geen maten die alleen rommelrusten zijn waar muziek hoort.

### Stemmen en notenbalken

- [ ] SATB-verdeling klopt (typisch: bovenstemmen op balk 1, bas op balk 2).
- [ ] Geen gevulde extra balk die niet hoort; een **lege** extra balk ruimt
      normalisatie vaak op — zie je er na normalisatie toch een, niet
      “repareren” via MusicXML.
- [ ] Gezongen tekst staat tussen de balken (niet onder de bas herhaald op
      alle stemmen).

### Lettergrepen

- [ ] Elke lettergreep hoort bij de juiste noot (geen vastgeplakte
      multi-klinker op één noot terwijl er meerdere nodig zijn).
- [ ] Homofoon: waar de sopraan een lettergreep heeft, hebben de andere
      stemmen daar ook een noot.
- [ ] Melisma (één lettergreep over meerdere noten + slur) bewust laten;
      koppelteken `Va-der` is geen melisma.

### Cues, titel, tempo

- [ ] Cues `P:`, `D:`, `K:` als Staff Text in de partituur, niet in het
      titelvak.
- [ ] Titel en componist kloppen; geen boekpagina-cijfer als titel.
- [ ] Er is een tempo (onzichtbare metronoom mag); ontbreekt die, zet
      normalisatie 120 BPM.

### Wat je tijdens review níet doet

- Geen Bestand → Exporteren → MusicXML → weer openen (stijl weg).
- Geen PDF/Coria vóór de her-normalisatie na je laatste edit.
- Geen `scripts\layout.cmd` op `*.print.mscz`.

## Stap voor stap

1. Dubbelklik de basispartituur-`.mscz`. MuseScore 4 opent.
2. Werk de checklist hierboven af. Corrigeer in MuseScore.
3. Bestand → Opslaan (Ctrl+S). Sluiten mag.
4. Normaliseer **dezelfde** `.mscz` opnieuw. Geen `-o` nodig als de
   bestandsnaam al goed is (zonder spaties):

```cmd
scripts\layout.cmd content-source\praktijk\oefenhoek\input\_werk\8-trisagion-8a-nederlands-hemelum\8-trisagion-8a-nederlands-hemelum.mscz
```

   Ligt de basispartituur al in de bibliotheek:

```cmd
scripts\layout.cmd content-source\praktijk\oefenhoek\bibliotheek\8-trisagion\8a-nederlands\hemelum\8-trisagion-8a-nederlands-hemelum.mscz
```

5. Open de `.mscz` opnieuw in MuseScore 4.
   - Ziet de **pagina** er anders uit dan net na je edit? Dat hoort: het
     script zet de stijl terug naar de basispartituur-standaard.
   - Zit er nog een **inhoudelijke** fout? Terug naar stap 2 — het script
     lost een verkeerde noot niet op.
6. Herhaal tot inhoud én basispartituur-vorm aanvaardbaar zijn.

## Wat normaliseren wel en niet overschrijft

| Jij (blijft leidend) | Script (zet opnieuw) |
| --- | --- |
| Toonhoogte, ritme, herhaling | A4, marges, fonts, maatnummers |
| Welke stem op welke balk (gevulde balken) | Lege maat-balken weg; style overlays |
| Welke lettergreep jij aan welke noot hing | Splits/knip volgens contract; reciteertoon-collaps |
| Bewuste melisma-slurs | Lyric-underlines (ticks) standaard weg |
| Bron-copyright die al in de basispartituur zat | Footer + colofon-velden opnieuw opgebouwd |

Daarom na **elke** editslag opnieuw normaliseren, ook als je “maar één noot”
wijzigde.

## Klaar als

Je hebt de basispartituur-`.mscz` beluisterd of doorgelopen, opgeslagen, opnieuw
genormaliseerd, en in MuseScore 4 gecontroleerd dat inhoud én A4-basispartituurvorm
aanvaardbaar zijn voor het koor om te reviewen.

Volgende stap: [PDF en Coria-.mxl maken](../5-pdf-en-coria/).

{{< navbuttons "Volgende: PDF en Coria|/praktijk/handleiding/partituur/5-pdf-en-coria/" >}}
