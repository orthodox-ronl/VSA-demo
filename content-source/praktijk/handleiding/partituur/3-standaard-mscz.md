---
title: "Standaard-.mscz maken"
linkTitle: "Standaard-.mscz"
weight: 30
---

# Standaard- / basispartituur-`.mscz` maken (normaliseren / layouten)

{{< cue >}}
Van opgekuiste `.mxl`:
```cmd
python scripts\apply_mscz_layout.py content-source\praktijk\oefenhoek\input\_werk\STAM\STAM.mxl -o content-source\praktijk\oefenhoek\input\_werk\STAM\STAM.mscz
```
Van ruwe `.mscz` (VOW e.d.): zelfde script; invoer is die `.mscz`; `-o` naar
`_werk\STAM\STAM.mscz` (geen spaties in de bestandsnaam).
Opnieuw op een bestaande basispartituur (in-place, na editslag):
```cmd
python scripts\apply_mscz_layout.py pad\naar\bestand.mscz
```
Norm: bestand `scripts\mscz-partituur-contract.md` in `VSA-demo`. Weigert `*.print.mscz`.
{{< /cue >}}

**Wat je nu doet:** **normaliseren** — in gewone taal vaak **layouten**
genoemd. Je past de Oefenhoek-basispartituur-standaard toe met
`scripts\apply_mscz_layout.py`. Uitkomst: een **basispartituur-`.mscz`** (canonieke
MuseScore-partituur) op A4, klaar om na te kijken en later PDF + Coria van te
maken.

**Wanneer:** na [opkuisen](../2-opkuisen/) (Capella-script of handmatige
`.mscz`-check), of meteen als de inhoud van een ruwe `.mscz` al klopt. Sla
deze pagina over als er al een genormaliseerde basispartituur ligt en je alleen noten of
tekst wilt wijzigen → [reviewen en opnieuw normaliseren](../4-reviewen/).

## Normaliseren en layouten — dezelfde scriptstap

| Term | Gebruik |
| --- | --- |
| **Normaliseren** | Contractterm: de basispartituur-regels toepassen op de `.mscz` |
| **Layouten** | Gangbare naam voor dezelfde stap (“de layout opnieuw zetten”) |
| **Script** | Altijd `python scripts\apply_mscz_layout.py …` |
| **Niet** | Handmatig in MuseScore “A4 kiezen” en hopen dat fonts/recitatief/copyright kloppen — dat is niet de basispartituur-standaard |

Opkuisen ≠ normaliseren. Opkuisen maakt de **inhoud** kloppend (stemmen,
lettergrepen). Normaliseren zet die inhoud in de **basispartituur-vorm** (pagina, stijl,
reciteertoon-encoding, tempo, copyright-velden). Details over inhoud:
[Opkuisen](../2-opkuisen/).

## Voorwaarden

1. **MuseScore 4** geïnstalleerd (niet versie 3). Bij een `.mxl`-invoer start
   het script MuseScore zelf voor de import. Typisch pad:
   `C:\Program Files\MuseScore 4\bin\MuseScore4.exe`.
2. Bestandsnamen voor publicatie / `_werk`-uitvoer: **geen spaties**, alleen
   `a-z`, `0-9`, `-`, `_`. Helper: `scripts\score_filenames.py`.
3. Geen `*.print.mscz` — die horen buiten deze pijplijn
   ([Print-.mscz](../7-print-mscz/)).
4. Opdrachtvenster geopend in de repository-map `VSA-demo`
   ([hoe](../../start/wat-heb-je-nodig/)).

## Wat `apply_mscz_layout.py` wél doet

Alles hieronder komt uit die basispartituur-norm (`scripts\mscz-partituur-contract.md`).
Het script is **idempotent**: opnieuw draaien mag en hoort na elke
inhoudelijke editslag.

### Pagina en typografie

| Regel | Waarde |
| --- | --- |
| Papier | A4 staand, marges 15 mm |
| Eerste systeem | Geen extra inspring |
| Laatste systeem | Uitrekken over de paginabreedte (recitatief-tekst niet links opeengedrongen) |
| Verticaal | Pagina niet “volspuiten” |
| Partijnamen | Uit |
| Maatnummers | Eerste maat van elke regel |
| Lyrics | Onder de bovenste balk |
| Fonts | Source Sans 3 (lyrics 13 pt, staff-/systemtekst 12 pt, titel 18 pt, footer 8 pt) |

### Titelvak en cues

- Titelvak (VBox): alleen **title** (= workTitle) en **composer**.
- Cues `P:` / `D:` / `K:` die per ongeluk in ondertitel of movementTitle
  stonden, worden Staff Text op de eerste maat.
- Arial op staff-tekst wordt opgeschoond richting de standaardfont.

### Lettergrepen en stemdekking (contract-fixes)

- Multi-klinker tokens splitsen (`nl_hyphen.py`).
- Waar nodig: extra noten invoegen of langere noten knippen zodat **elke
  partij minstens één noot per lettergreep** heeft (SATB homofoon).
- Lege maat-balken (vaak een derde lege balk na Capella SAT+B-import)
  verwijderen.

### Reciteertoon (MCI, één basispartituur-encoding)

Bij een rij opeenvolgende noten met **zelfde toon** én **zelfde duur**, elk
met een lettergreep, en **meer dan vijf** lettergrepen in die rij:

| Positie | Resultaat |
| --- | --- |
| Eerste lettergreep | Gewone noot |
| Middelste lettergrepen | Eén stokloze feathered noot `\|\|O\|\|` met de middelste tekst |
| Laatste lettergreep | Gewone noot |

Reeksen van vijf of minder blijven gewone noten. Melisma, cadens met
bewuste lengte en toonwissels worden niet gecollapsed. Coria exploseert de
feathered noot later tot één kwart per lettergreep.

### Maatstrepen, rusten, tempo, copyright

| Onderdeel | Gedrag |
| --- | --- |
| Eindmaatstrepen per systeem | Verborgen eindstrepen weer zichtbaar |
| Opvulrusten aan het eind van een maat | Weg; maatlengte = som van de noten |
| Leidende rusten | Ritmisch behouden; na start/dubbele streep met gap |
| Lyric-underlines (melisma-ticks) | Standaard weg (Capella-slurs zijn frasen); opt-in via meta `vsaLyricExtenders` |
| Tempo | Verplicht voor Coria; default **120 BPM** als er geen metronoom in de basispartituur staat |
| Copyright | Notice uit de bron → korte footer + colofon; ontbreekt notice → CC BY-SA 4.0 (deze uitgave) + eredienst-kopieertoestemming; in de bibliotheek: regel `Bibliotheek-id:` + meta `vsaBibliotheekId` |
| Contractmeta | `vsaPartituurContract` = `partituur-1` |

## Wat het script níet doet

| Niet | Waar dan wel |
| --- | --- |
| Capella-lagen 1–3 (verborgen reciteerkwarten zichtbaar maken, Capella-titelrommel, …) | [Opkuisen](../2-opkuisen/) / `cleanup_capella_mxl.py` |
| Verkeerde stem op de verkeerde balk herschikken | Jij in MuseScore (opkuisen) |
| PDF of Coria-`.mxl` maken | [PDF en Coria](../5-pdf-en-coria/) / `scripts\mscz-products.cmd` |
| Print-vel normaliseren | Bewust geweigerd — [Print-.mscz](../7-print-mscz/) |
| MusicXML-roundtrip “repareren” | Nooit doen; blijf op de `.mscz` |

## Stap voor stap

### Van opgekuiste Capella-`.mxl`

Voorbeeld voor bibliotheek-id `8-trisagion/8a-nederlands/hemelum`:

```cmd
python scripts\apply_mscz_layout.py content-source\praktijk\oefenhoek\input\_werk\8-trisagion-8a-nederlands-hemelum\8-trisagion-8a-nederlands-hemelum.mxl -o content-source\praktijk\oefenhoek\input\_werk\8-trisagion-8a-nederlands-hemelum\8-trisagion-8a-nederlands-hemelum.mscz
```

Het script converteert via MuseScore 4 naar `.mscz` en past daarna de
basispartituur-standaard toe. Wacht tot de regel `ok …` verschijnt; daaronder staan
korte notities (bijvoorbeeld reciteer-collaps, copyright).

### Van een VOW- of andere ruwe `.mscz`

Kopieer de ruwe `.mscz` **niet** rechtstreeks naar de bibliotheek. Eerst
normaliseren naar `_werk` met een naam zonder spaties:

```cmd
python scripts\apply_mscz_layout.py content-source\praktijk\oefenhoek\input\vow\Cherubijnenlied-Kastorskij.mscz -o content-source\praktijk\oefenhoek\input\_werk\15-cherubijnenhymne-15c-kastorski-hemelum\15-cherubijnenhymne-15c-kastorski-hemelum.mscz
```

Controleer vóór of na deze stap of stemmen en lettergrepen kloppen — dat is
[opkuisen](../2-opkuisen/). Doe de normalisatie alleen als de bibliotheek-id
in de werkvoorraad klopt; anders eerst vragen.

### Na de eerste normalisatie

1. Open de nieuwe `.mscz` in MuseScore 4.
2. Controleer: A4, tekst tussen de balken, titel/componist, geen rare lege
   balk, reciteertoon ziet er uit als eerste + `\|\|O\|\|` + laatste waar dat
   hoort.
3. Inhoudelijke fouten (verkeerde noot, plakkerige lettergreep, verkeerde
   stem): corrigeren in MuseScore, opslaan, **opnieuw** hetzelfde script op
   dezelfde `.mscz` — zie [reviewen](../4-reviewen/).
4. Nog geen PDF of Coria maken tot de inhoud akkoord is.

## Klaar als

Je hebt een `.mscz` in `_werk\<stam>\` (of al in de bibliotheek) die:

- in MuseScore 4 opent op A4 met de basispartituur-typografie;
- tekst tussen de balken toont;
- door `apply_mscz_layout.py` is gehaald (meta `vsaPartituurContract`);
- het ruwe origineel in `input\` onaangeroerd laat.

Volgende stap: [reviewen en opnieuw normaliseren](../4-reviewen/).

{{< navbuttons "Volgende: reviewen|/praktijk/handleiding/partituur/4-reviewen/" >}}
