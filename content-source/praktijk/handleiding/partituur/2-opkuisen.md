---
title: "Opkuisen"
linkTitle: "Opkuisen"
weight: 20
---

# Opkuisen

{{< cue >}}
Snel (Capella-`.mxl` → schone `.mxl` in `_werk`; origineel in `capella\` blijft):
```cmd
scripts\opkuisen.cmd "content-source\praktijk\oefenhoek\input\capella\NAAM.mxl" -o content-source\praktijk\oefenhoek\input\_werk\STAM\STAM.mxl
```
Alleen herkomst + rapport (geen schrijven; `--analyze` en `--dry-run` zijn
hetzelfde):
```cmd
scripts\opkuisen.cmd content-source\praktijk\oefenhoek\input\capella --analyze
```
`STAM` = publicatiestam uit de bibliotheek-id, zonder spaties
(voorbeeld: id `8-trisagion/8a-nederlands/hemelum` →
`8-trisagion-8a-nederlands-hemelum`).
Volledige man-page (hoeken, manieren wel/niet, exitcodes):
[opkuisen](../../scripts/opkuisen/).
Ruwe `.mscz`: `scripts\opkuisen.cmd pad\naar\bestand.mscz` doet
inhoudsfixes; stemmen/checklist hieronder blijf je in MuseScore 4
controleren, daarna [normaliseren](../3-standaard-mscz/) of
`opkuisen … --layout`.
{{< /cue >}}

**Wat je nu doet:** de **inhoud** van de partituur opschonen zodat noten,
stemmen en lettergrepen kloppen — vóór (of, bij een `.mscz`, naast) de
basispartituur-standaard. **Opkuisen** is geen A4-layout en geen PDF/Coria. Die horen bij
[normaliseren / layouten](../3-standaard-mscz/) en
[PDF en Coria](../5-pdf-en-coria/).

**Wanneer:** bij elke nieuwe Capella-/CapToMusic-`.mxl`, en bij elke ruwe
`.mscz` (VOW, MuseScore-input) waarvan de inhoud nog niet basispartituur-klaar is. Heb je
al een genormaliseerde basispartituur-`.mscz` en corrigeer je alleen een noot of een
lettergreep? Dat is nog steeds opkuiswerk in MuseScore, gevolgd door opnieuw
normaliseren — zie [reviewen](../4-reviewen/).

## Wat “opkuisen” precies betekent

Opkuisen = alles wat de **muzikale en tekstuele inhoud** betreft, zodat de
partituur voldoet aan de afspraken over lettergrepen, stemmen en
reciteertoon die hieronder en op
[standaard-.mscz](../3-standaard-mscz/) staan. De technische norm voor
scripts staat in het bestand `scripts\mscz-partituur-contract.md` in je
repository-map `VSA-demo` (niet als pagina op deze site).

| Wel opkuisen | Niet opkuisen (andere stap) |
| --- | --- |
| Stemmen op de juiste notenbalken | A4, marges, lettertypes (`scripts\layout.cmd`) |
| Lettergreep ↔ noot synchroon | Reciteertoon-collaps naar feathered `\|\|O\|\|` (normalisatie) |
| Geen plakkerige multi-klinker op één noot zonder split | PDF en Coria-`.mxl` (`mscz-products`) |
| Capella: verborgen reciteerkwarten, lege maten, titelrommel | Print-vel buiten de basispartituur (`*.print.mscz`) |

**Normaliseren** (gangbaar: **layouten**) is de volgende scriptstap:
`scripts\layout.cmd`. Dat script doet wél enkele inhoudsfixes (lege balk
weg, lettergrepen splitsen, noot per lettergreep knippen, reciteertoon
collapsen). Een verkeerde stemverdeling of structureel verkeerde tekst
corrigeer jij — dat blijft opkuisen.

## Wat er inhoudelijk moet kloppen (checklist)

Werk deze lijst af tot alles groen is. Bij Capella doet
`scripts\opkuisen.cmd` (hoek `capella`) een groot deel automatisch;
controleer het resultaat toch. Bij een `.mscz` kan `opkuisen` inhoudsfixes
doen; de checklist hieronder controleer je in MuseScore 4.

### 1. Stemmen en notenbalken

De Oefenhoek-basispartituur is meestal één SATB-partituur op **twee notenbalken** in het
systeem: bovenstemmen (S/A/T) op de eerste balk, bas (B) op de tweede, met
de gezongen tekst **tussen** die balken (niet onder de bas, niet vier keer
herhaald per stem).

Veel voorkomende bronproblemen:

| Situatie | Wat jij doet |
| --- | --- |
| SAT op balk 1, B op balk 2, maar verkeerde stemmen of ontbrekende stem | In MuseScore 4: controleer per noot welke stem (1–4) actief is; zet S/A/T/B op de juiste stem en balk |
| Verkeerde of ontbrekende sleutel (bijv. G op de onderbalk, C2, G8vb) | Opkuisen en normalisatie zetten bij twee balken G boven / F onder (ook mid-score). Bij één of drie+ gevulde balken: zelf in MuseScore zetten |
| Extra **lege** derde balk na import | Mag blijven tot normalisatie: `scripts\layout.cmd` verwijdert lege maat-balken vaak automatisch |
| Extra balk mét noten die niet horen | Verwijder of verplaats die noten in MuseScore; het layout-script wist geen gevulde balk “voor jou” |
| Partijnamen “Sopraan / Alt / …” op elk systeem | Capella-script verbergt partijnamen; bij `.mscz` zet je instrumentnamen uit of laat normalisatie de stijl zetten |
| Lyrics op alle vier de stemmen herhaald | Alleen op de bovenstem (stem 1) houden; Capella-script stript lagere stemmen |

### 2. Synchronisatie lettergreep ↔ noot

Elke gezongen lettergreep hoort bij de juiste noot(en). Dat is nodig voor
Coria-playback én voor een leesbare PDF.

| Eis | Uitleg |
| --- | --- |
| Eén lettergreep per noot in recitatief | Hele woorden (`altijd`, `eeuwen`) worden in lettergrepen geknipt; per lettergreep een noot met dezelfde duur (geen triolen van één kwart maken) |
| Multi-klinker tokens splitsen | Bijvoorbeeld `melse` → `mel` + `se`; het Capella-script en later normalisatie voegen daar noten voor in (zelfde duur, alle stemmen homofoon) |
| Homofone dekking | Waar de sopraan een lettergreep heeft, hebben de andere stemmen op dat moment ook een noot (niet één lange noot over meerdere lettergrepen heen zonder knip) |
| Melisma | Eén lettergreep over meerdere noten met slur: laten staan. Koppelteken in de tekst (`Va-der`) is **geen** melisma |
| Geen “plakkerige” tekst | Geen woord met meerdere lettergrepen vastgeplakt op één noot terwijl er meerdere noten nodig zijn |

Controle in MuseScore 4: klik een noot, kijk of de lyric-lettergreep klopt;
loop het stuk door met de liturgische tekst ernaast.

### 3. Capella-specifieke rommel (alleen Capella-`.mxl`)

Zie de sectie hieronder: het script ruimt dit op. Jij overschrijft het
origineel in `input\capella\` **niet**.

### 4. Titel, cues en copyright (inhoud, niet styling)

| Onderdeel | Eis |
| --- | --- |
| Titel | Werk-titel van het stuk; geen boekpagina-cijfers in de partituur |
| Cues `P:` / `D:` / `K:` | Als Staff Text in de muziek, **niet** als ondertitel in het titelvak |
| Copyright / `<rights>` | Uit de bron laten staan als die er is; ontbreekt die, zet normalisatie later default CC BY-SA 4.0 |

## Pad A — Capella- of CapToMusic-`.mxl`

### Wat `scripts\opkuisen.cmd` doet bij Capella

Het script herkent Capella/CapToMusic (hoek `capella`) en past de
Capella-MusicXML-manieren toe. Het is **geen** “maak het mooi in MuseScore”.
A4-layout is een aparte diepte (`--layout` of [layout](../layout/)).
Volledige wel/niet-tabellen, andere hoeken en exitcodes:
[opkuisen](../../scripts/opkuisen/).

| Laag | Wat er gebeurt |
| --- | --- |
| Capella-semantiek | Onzichtbare klinkende noten (`print-object=no`) worden zichtbare reciteerkwarten (duur en noottype blijven). Maatlengte mag groeien als er lettergrepen bijkomen. Halve/hele noten op cadensen blijven echte lengte |
| Tekst–noot-binding | Lettergreep ↔ noot; multi-klinker tokens splitsen met extra noten (zelfde duur op alle stemmen); lyrics alleen op stem 1; backups bijwerken zodat A/T/B niet te laat starten; partijnamen weg; titels naar work-title; boekpagina-cijfers weg; lege/rust-only maten weg |
| Partituurhint | Compactere systeem-/balkafstand in de XML als startpunt voor MuseScore |

Het script **stript geen** `<rights>` / copyright uit de MusicXML.

Twijfel over de herkomst? Eerst alleen analyseren (geen schrijven):

```cmd
scripts\opkuisen.cmd "content-source\praktijk\oefenhoek\input\capella\NAAM.mxl" --analyze
```

`--dry-run` doet precies hetzelfde als `--analyze`.

### Stap voor stap

1. Ken het **bibliotheek-id** (drie lagen), bijvoorbeeld
   `8-trisagion/8a-nederlands/hemelum`. Nog geen id? Ga terug naar
   [binnenhalen](../1-binnenhalen/) en het
   [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/).
2. Bepaal de **publicatiestam** (de drie id-lagen met `-` ertussen, zonder
   spaties): `8-trisagion-8a-nederlands-hemelum`.
3. Maak de map
   `content-source\praktijk\oefenhoek\input\_werk\8-trisagion-8a-nederlands-hemelum\`
   (Verkenner of laat het script de map aanmaken bij schrijven). De map
   `_werk\` staat alleen op jouw pc (niet in git).
4. Open het Windows-opdrachtvenster in de repository-map `VSA-demo`
   ([hoe](../../start/wat-heb-je-nodig/)).
5. Draai het opkuis-commando. Zet de **bron**-bestandsnaam tussen
   aanhalingstekens als er spaties in zitten. Voorbeeld:

```cmd
scripts\opkuisen.cmd "content-source\praktijk\oefenhoek\input\capella\8a - 8-trisagion.mxl" -o content-source\praktijk\oefenhoek\input\_werk\8-trisagion-8a-nederlands-hemelum\8-trisagion-8a-nederlands-hemelum.mxl
```

6. Wacht tot de prompt terugkomt. Het script print hoek/confidence en
   tellers (`unhide=…`, `splits=…`, …). Fout over spaties in de
   *uitvoer*naam: kies een `-o`-pad zonder spaties. Overschrijf nooit het
   Capella-origineel in `capella\` (schrijven naar ruwe `input\capella\`
   vereist `--in-place`; gebruik liever `-o` naar `_werk`).
7. Optioneel: open de opgekuiste `.mxl` even in MuseScore 4 om te zien of
   lettergrepen en maten er redelijk uitzien. Styling hoeft nog niet te
   kloppen.

Daarna: [standaard-.mscz / normaliseren](../3-standaard-mscz/).

## Pad B — ruwe `.mscz` (VOW, MuseScore-input, …)

`scripts\opkuisen.cmd` herkent `.mscz` als hoek `musescore` en kan
**inhoudsfixes** doen (lege balk weg, lettergrepen splitsen, noot per
lettergreep). Dat vervangt **niet** jouw checklist hierboven: verkeerde
stemverdeling of liturgische tekst corrigeer je in MuseScore 4.

1. Zet of kopieer het bestand naar
   `content-source\praktijk\oefenhoek\input\_werk\<stam>\` met een
   bestandsnaam **zonder spaties**. Het origineel in `input\vow\` of
   `input\musescore\` blijft onaangeroerd.
2. Optioneel automatisch:

```cmd
scripts\opkuisen.cmd content-source\praktijk\oefenhoek\input\_werk\STAM\STAM.mscz
```

3. Open de `.mscz` in **MuseScore 4** (niet MuseScore 3).
4. Werk de checklist af: stemmen/balken, lettergreep↔noot, cues, titel.
5. Bestand → Opslaan (Ctrl+S).
6. Ga naar [normaliseren](../3-standaard-mscz/)
   (`scripts\layout.cmd`), of combineer met
   `scripts\opkuisen.cmd … --layout`. Normaliseer **niet** in de hoop dat
   een verkeerde SAT+B-indeling vanzelf goed komt: het script haalt lege
   balken weg en kan lettergrepen knippen, maar herschikt geen verkeerde
   stemmen voor jou.

Twijfel over de bibliotheek-id? Niet raden — vraag na en noteer in
`content-source\praktijk\oefenhoek\input\werkvoorraad.md`.

## Wat je niet doet bij opkuisen

- Geen PDF of Coria-`.mxl` maken (dat is `mscz-products`, later).
- Geen MusicXML-roundtrip: basispartituur-`.mscz` exporteren naar `.mxl` en weer
  openen gooit de MuseScore-stijl weg.
- Geen `scripts\layout.cmd` op `*.print.mscz` (printvel staat buiten deze
  straat — [Print-.mscz](../7-print-mscz/)).
- Geen Capella-origineel in `input\capella\` overschrijven.

## Klaar als

| Bron | Klaar-criterium |
| --- | --- |
| Capella | Opgekuiste `.mxl` zonder spaties in `_werk\<stam>\`; origineel in `capella\` ongewijzigd; checklist hierboven aanvaardbaar |
| `.mscz` | Stemmen, balken en lettergreep–noot-koppeling aanvaardbaar; bestand opgeslagen; je kunt normaliseren |

Volgende stap voor beide paden:
[standaard-.mscz maken (normaliseren / layouten)](../3-standaard-mscz/).

{{< navbuttons "Volgende: standaard-.mscz|/praktijk/handleiding/partituur/3-standaard-mscz/" >}}
