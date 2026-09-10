# Contract: standaard-layout MuseScore (A4)

Proef in VSA-demo (laag 4). **Niet in `check`.** Bij productierijpheid: verhuizen
naar VSA-tooling, inclusief documentatie en een demo-verhaal in deze repo.

Script: `python scripts/apply_mscz_layout.py <bestand.mscz>`
(idempotent: opnieuw draaien past een nieuwe contractversie toe).

MuseScore 4.x (getest tegen 4.7): stijl staat in `score_style.mss` in de `.mscz`,
niet in de `.mscx`. Roundtrip via MusicXML is verboden (stijl verdwijnt).

## Doel

SATB-partituur netjes op **A4**, PDF-export en papier. Muziek (noten, duren,
lyrics, stemmen) blijft onaangeroerd. Playback-MXL voor Coria: dezelfde
`.mscz` via `scripts/export_mscz_coria_mxl.py` (geen roundtrip).

## Pagina en stijl (waarden = `STYLE_OVERRIDES` in het script)

| Regel | Waarde |
| ----- | ------ |
| Papier | A4 staand (210 x 297 mm) |
| Marges | 15 mm alle kanten, niet tweezijdig |
| Eerste systeem | geen extra inspring |
| Laatste systeem (partituur én na sectiebreuk) | niet uitrekken (`lastSystemFillLimit=1`) |
| Verticaal | pagina niet vullen (`enableVerticalSpread=0`) |
| Partijnamen | uit (een instrument / SATB-akkolade) |
| Maatnummers | eerste maat van elke regel (`measureNumberSystem`), ook maat 1 |
| Lyrics | onder de bovenste balk (tussen de twee balken) |
| Titel → eerste systeem | extra ruimte (`frameSystemDistance=14`), zodat p.1-systemen lager komen |

## Typografie (VSA-defaults)

Zie VSA-tooling `typografie` (lyric 13 pt, word 12 pt, font Source Sans 3).
Punten, niet spatium-afhankelijk. Geen lokale Arial-overrides op staff-tekst.

| Toepassing | Font | Grootte |
| ---------- | ---- | ------- |
| Lyrics | Source Sans 3 | 13 pt |
| Staff-/systemtekst (o.a. `P:`/`D:`/`K:`) | Source Sans 3 | 12 pt |
| Composer | Source Sans 3 | 12 pt |
| Titel | Source Sans 3 | 18 pt |

Als MuseScore Source Sans 3 niet heeft: installeren of hij valt terug op een
systeemfont. Niet vervangen door Edwin in dit contract zonder bewuste keuze.

## Titelvak (VBox)

Alleen:

1. **title** = `workTitle`
2. **composer** = `composer` (rechts), als die bekend is

Niet in het titelvak:

- priester-/diaken-/koor-cues (`P:`, `D:`, `K:`, ook `P;`)
- willekeurige staff-tekst

`boxAutoSize=1` (geen vaste hoogte die tekst van de pagina duwt).

## Leidende rusten (na dubbele streep)

Rusten aan het begin van een maat blijven **ritmisch** staan (noten schuiven
niet naar voren). Alleen de **kolombreedte** gaat naar 0: MuseScore `gap` +
onzichtbaar. Dat geldt voor de eerste maat en voor de maat **direct na een
dubbele maatstreep** (priester/koor-wissel).

Niet: maat inkorten of de rust wissen. Dat verwisselt rust en noot.

Coria-MXL (`export_mscz_coria_mxl.py`) doet het omgekeerde: die leidende
rusten **wissen**, de maat korter maken (`senza-misura`). Daarna:

| In `.mscz` | In Coria-`.mxl` (alle SATB-parts, zelfde duur) |
| ---------- | ----------------------------------------------- |
| Dubbele maatstreep | extra maat: 4 kwarten rust, lyric `[PAUZE]`; `P:`/`D:`/`K:`-cue van de volgende koormaat erboven (niet meer op de inzet) |
| Gebogen cesuur (`caesuraCurved`) | 1 kwart rust na die noot, geen lyric |

Onzichtbare rusten in het midden/einde van een maat blijven als gewone rust
(anders loopt SATB uit de pas). De `.mscz` verandert niet.

## Melisma (niet laag 4)

Hyphen (`Barm-har-tig`) ≠ melisma (één lettergreep over extra noten). In dit
Feofan-bestand: `syllabic` begin/middle/end voor koppeltekens, ~40 keer een
lyric-noot gevolgd door een kale noot, **geen** lyric-extender (`ticks`), wel
veel slurs (vaak Capella-melisma).

Consequent: extender op de lettergreep, slurs alleen als frase.

- MXL: `cleanup_capella_mxl.py` zet `<extend/>` op stem 1.
- `.mscz`: `apply_mscz_layout.py` zet MuseScore `<ticks>` / `<ticks_f>` (lengte
  van de kale noten erna). Rusten breken de keten. Slurs blijven.
- Coria-MXL: `export_mscz_coria_mxl.py` explodeert SATB naar vier parts en
  zet opnieuw `<extend/>` (MuseScore-export laat ticks/extend vaak vallen).

## Tekstrollen

| Inhoud | Bestemming |
| ------ | ---------- |
| Cues (`P:` / `D:` / `K:`) | `StaffText` op de eerste maat als ze alleen in titel/`movementTitle` stonden |
| Componist (geen cue) | `metaTag composer` + VBox `composer`; weg als `StaffText` in de muziek |
| `movementTitle` die een cue is | leegmaken |

## Secties (priester / koor)

Dit soort liturgie is één partituur met **blokken** (koor, priester, koor, …),
geen losse zangstukken. Twee verschillende markeringen:

| Wat | Betekenis | MuseScore |
| --- | --------- | --------- |
| Dubbele maatstreep | muzikaal einde van het blok | Barlines-palet → double bar |
| **Sectiebreuk** | nieuw systeem **en** het voorgaande systeem niet over de paginabreedte uitsmeren | Add → Layouts → Section break |

Een gewone **systeembreuk** (Enter) is dat niet: die begint wel een nieuwe regel,
maar rechtvaardigt het vorige systeem wél over de volle breedte. Gebruik die
alleen als je midden in een blok een nieuwe regel wilt (bijv. `P:` links),
zonder het blok af te sluiten.

`lastSystemFillLimit=1` geldt voor het laatste systeem van de partituur én,
samen met een sectiebreuk, voor het laatste systeem van elke sectie: kort blok
blijft kort.

Sectiebreuk-eigenschappen: geen extra eerste-systeem-inspring (contract: 0),
courtesy-sleutel/maatsoort naar smaak. Playback-pauze optioneel.

Handmatige systeembreuk, paginabreuk en **sectiebreuk** blijven staan; het
script wist ze niet.

- Systeembreuk: maat die de regel moet afsluiten → Enter.
- Paginabreuk: Ctrl+Enter.
- Sectiebreuk: laatste maat van het blok → Section break (vaak samen met
  dubbele streep).
- Priestertekst aan het begin van een regel: systeembreuk of sectiebreuk op de
  **vorige** maat, tekst op de **eerste noot** van de nieuwe regel,
  **automatisch plaatsen aan**. Geen breuk als de cue midden in de regel hoort.

Niet: automatisch plaatsen uit + naar links slepen. Offset is t.o.v. de anker-noot,
niet t.o.v. het systeem; bij herflow schuift het scheef.

Stijl (alle Staff/System Text): uitlijning links. Anker = eerste noot van de
regel → linkerkant van de tekst op die noot (na sleutel/voortekening), niet op
de paginamarge.

- Alle vakjes van dat type: Format → Style → Text styles → Staff Text (of het
  layout-script: `staffTextAlign` / `systemTextAlign`).
- Alleen een selectie: rechtsklik → Select → All similar elements (of Similar
  on this staff / in range) → Properties. Alleen doen voor een uitzondering.

## P: / D: / K: “boxjes” in MuseScore

Dat zijn geen titelvakken. Het is **Staff Text**, vastgemaakt aan een noot.

1. Noot selecteren waar de cue bij hoort.
2. Ctrl+T (Add → Text → Staff Text).
3. Typen, bijv. `P: Omhoog de harten!`
4. Optioneel kader: Properties → Frame → Rectangle (anders alleen tekst, geen
   box). Standaardstijl heeft geen kader; dat is per cue jouw keuze.

Niet: Add → Frames → Vertical Frame (dat is het titelvak).

System Text (Ctrl+Shift+T) als de cue bij het hele systeem hoort, niet bij één
balk.

## Wat het script niet doet

- Pitches, duren, lyrics, slur/tie, maatstructuur
- Inhoudelijke Capella-opkuis (dat is `cleanup_capella_mxl.py`, lagen 1–3)

## Itereren

1. Regel of `STYLE_OVERRIDES` aanpassen.
2. Script opnieuw over de corpus.
3. In MuseScore openen, PDF naar A4, visueel checken.
