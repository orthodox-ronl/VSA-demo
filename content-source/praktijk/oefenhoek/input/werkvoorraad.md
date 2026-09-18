# Werkvoorraad

Eén rij **per inputbestand**, niet per zangstuk (hetzelfde stuk kan Capella én
VOW hebben). Dit is het interne geheugen: waar kwam het vandaan, waar moet het
heen, hoever is de conversie.

De **tabel** hieronder wordt bij `check` / `build` / `serve` opnieuw opgebouwd
uit de bestanden in `capella/`, `vow/`, `musescore/`, `musicxml/` en `pdf/`.
Zet **doel-id** (bibliotheek-id) en **notitie** zelf in de rij als de
automatische match ze niet kent; die velden worden bij een update bewaard.
Stap en volgende actie komen van wat er op schijf staat (bibliotheek-map mét
partituur of VSA, of nog niet).

Op de Oefenhoek-pagina van de site staat deze pagina uitklapbaar onderaan,
ná de lijst met deelrubrieken.

## Kolommen

| Kolom | Betekenis |
| --- | --- |
| Input | Pad vanaf `input/` (herkomstmap + originele bestandsnaam) |
| Doel-id | Bibliotheek-id `zangstuk/variant/uitvoeringsvorm` (`[a-z0-9_-]+` per laag). Leeg = nog niet gekozen. Oude bladermap-namen worden genormaliseerd. |
| Koormap | Slot in de liturgiemap (of leeg). Los van de bibliotheek-map. |
| Doelvorm | Meestal `.mscz` (oefenhoek-layout); soms `.vsa` |
| Stap | Hoever de input is (zie hieronder) |
| Volgende | Wat je nu zou doen |
| Notitie | Vrij; overleeft de automatische update |

### Stap (intern, niet hetzelfde als `publicatiestatus` op de site)

| Stap | Betekenis |
| --- | --- |
| `ontvangen` | Input ligt hier; conversie nog niet klaar of doel-id ontbreekt |
| `doel-id` | (in *Volgende*) eerst een bibliotheek-id kiezen |
| `opkuisen` | Inhoud opschonen: Capella via `cleanup_capella_mxl.py`; bij `.mscz` ook stemmen/lettergrepen in MuseScore |
| `layout` | Normaliseren / layouten: `apply_mscz_layout.py` → standaard-`.mscz` |
| `playback` | Coria-`.mxl` uit die `.mscz` |
| `pdf` | A4-PDF naast de `.mscz` |
| `gepubliceerd` | Er staat al oefenbare inhoud in de bibliotheek (hub, VSA, print-PDF, …) |

`publicatiestatus` (`voorzien` / `concept` / `reviewable` / `productie`) staat
op bibliotheek-`index.md` en koormap-`index.md`, voor koorleden. Deze tabel is
voor wie converteert.

<!-- werkvoorraad-tabel:begin -->

| Input | Doel-id | Koormap | Doelvorm | Stap | Volgende | Notitie |
| --- | --- | --- | --- | --- | --- | --- |
| `capella/15c - cherubijnenhymne - kastorski.mxl` | `15-cherubijnenhymne/15c-kastorski/hemelum` | `15-cherubijnenhymne/15c-kastorski` | `.mscz` | gepubliceerd | — | gepubliceerd |
| `capella/15c - cherubijnenhymne - kastorskij - ksl.mxl` | `15-cherubijnenhymne/15c-kastorski/hemelum-ksl-trlat` |  | `.mscz` | ontvangen | opkuisen | Kerkslavisch getranslitereerd |
| `capella/15e Cherubijnenhymne Bortnjanski no.5.mxl` | `15-cherubijnenhymne/15e-bortnjanski/hemelum` | `15-cherubijnenhymne/15e-bortnjanski` | `.mscz` | ontvangen | opkuisen | Capella 15e |
| `capella/19a - eucharistische kanon - feofan.mxl` | `19-eucharistische-canon/19a-feofan/hemelum` | `19a-eucharistische-kanon` | `.mscz` | gepubliceerd | — | gepubliceerd |
| `capella/2 - 1e antifoon.mxl` | `2-eerste-antifoon/zondag/hemelum` | `2-eerste-antifoon` | `.mscz` | gepubliceerd | — |  |
| `capella/20d - in waarheid - moeder godslied.mxl` | `20-moeder-godslied/20d-in-waarheid/hemelum` | `20d-in-waarheid-moeder-godslied` | `.mscz` | gepubliceerd | — | gepubliceerd |
| `capella/28a - wij hebben het ware licht aanschouwd.mxl` | `28-wij-hebben-het-ware-licht/default/hemelum` | `28-wij-hebben-het-ware-licht` | `.mscz` | gepubliceerd | — |  |
| `capella/29 - de naam des heren zij gezegend.mxl` | `29-de-naam-des-heren-zij-gezegend/default/hemelum` | `29-de-naam-des-heren-zij-gezegend` | `.mscz` | gepubliceerd | — |  |
| `capella/4 - 2e antifoon.mxl` | `4-tweede-antifoon/zondag/hemelum` | `4-tweede-antifoon` | `.mscz` | gepubliceerd | — |  |
| `capella/5a Eniggeboren Zoon.mxl` | `5-eniggeboren-zoon/default/hemelum` | `5-eniggeboren-zoon` | `.mscz` | gepubliceerd | — |  |
| `capella/6b - zaligsprekingen.mxl` | `6-derde-antifoon/zondag/hemelum` | `6-derde-antifoon` | `.mscz` | gepubliceerd | — |  |
| `capella/7 - kleine intocht - zondag.mxl` | `7-kleine-intocht/zondag/hemelum` | `7-kleine-intocht` | `.mscz` | gepubliceerd | — | zelfde koormap-sectie als 7b |
| `capella/7b - kleine intocht - weekdagen.mxl` | `7-kleine-intocht/weekdagen/hemelum` | `7-kleine-intocht` | `.mscz` | gepubliceerd | — | zelfde koormap-sectie als 7 |
| `capella/8a - trisagion (+slav).mxl` | `8-trisagion/8a-slav/hemelum` |  | `.mscz` | gepubliceerd | — |  |
| `capella/8a - trisagion.mxl` | `8-trisagion/8a-nederlands/hemelum` |  | `.mscz` | gepubliceerd | — |  |
| `musescore/alleluja-toon-1.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musescore/allelujas 1-8 - ruw.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/021-prokimen-alleluja-toon-1.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/021-prokimen-alleluja-toon-1.musicxml` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/022-prokimen-alleluja-toon-2.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/022-prokimen-alleluja-toon-2.musicxml` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/023-prokimen-alleluja-toon-3.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/023-prokimen-alleluja-toon-3.musicxml` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/024-prokimen-alleluja-toon-4.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/024-prokimen-alleluja-toon-4.musicxml` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/025-prokimen-alleluja-toon-5.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/025-prokimen-alleluja-toon-5.musicxml` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/026-prokimen-alleluja-toon-6.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/026-prokimen-alleluja-toon-6.musicxml` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/027-prokimen-alleluja-toon-7.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/027-prokimen-alleluja-toon-7.musicxml` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/028-prokimen-alleluja-toon-8.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/028-prokimen-alleluja-toon-8.musicxml` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/tonen (vers, stichier, tropaar).musicxml` |  |  | `.mscz` | ontvangen | doel-id |  |
| `musicxml/tonen-vers-stichier-tropaar.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `vow/Cherubijnenlied-Kastorskij.mscz` | `15-cherubijnenhymne/15c-kastorski/hemelum` | `15-cherubijnenhymne/15c-kastorski` | `.mscz` | gepubliceerd | — | tweede bron (VOW); Capella is canonieke hub |
| `vow/dankzegging_toon_2_Kyiv.mscz` |  |  | `.mscz` | ontvangen | doel-id | zie ID-REGISTER OPEN 7 |
| `vow/eind-liturgie.mscz` |  |  | `.mscz` | ontvangen | doel-id | zie ID-REGISTER OPEN 7 |
| `vow/Eucharistische Canon-Rostov.mscz` | `19-eucharistische-canon/rostov/hemelum` |  | `.mscz` | ontvangen | layout | sibling van 19a-feofan |
| `vow/Kleine_intocht-moedergods.mscz` | `7-kleine-intocht/moeder-gods/hemelum` | `7-kleine-intocht` | `.mscz` | ontvangen | migratie |  |
| `vow/Kleine_intocht-weekdagen.mscz` | `7-kleine-intocht/weekdagen/hemelum` | `7-kleine-intocht` | `.mscz` | gepubliceerd | — | tweede bron (VOW) |
| `vow/Kleine_intocht-zondag.mscz` | `7-kleine-intocht/zondag/hemelum` | `7-kleine-intocht` | `.mscz` | gepubliceerd | — | tweede bron (VOW) |
| `vow/Tropaar-opstanding-toon1.mscz` |  |  | `.mscz` | ontvangen | doel-id | voorlopig laten zitten |
| `vow/Tropaar-opstanding-toon2.mscz` |  |  | `.mscz` | ontvangen | doel-id | voorlopig laten zitten |
| `vow/Tropaar-opstanding-toon3.mscz` |  |  | `.mscz` | ontvangen | doel-id | voorlopig laten zitten |
| `vow/Tropaar-opstanding-toon4.mscz` |  |  | `.mscz` | ontvangen | doel-id | voorlopig laten zitten |
| `vow/Tropaar-opstanding-toon5.mscz` |  |  | `.mscz` | ontvangen | doel-id | voorlopig laten zitten |
| `vow/Tropaar-opstanding-toon6.mscz` |  |  | `.mscz` | ontvangen | doel-id | voorlopig laten zitten |
| `vow/Tropaar-opstanding-toon7.mscz` |  |  | `.mscz` | ontvangen | doel-id | voorlopig laten zitten |
| `vow/Tropaar-opstanding-toon8.mscz` |  |  | `.mscz` | ontvangen | doel-id | voorlopig laten zitten |

<!-- werkvoorraad-tabel:einde -->

## Workflows (achtergrond)

### Nieuwe input

1. Niet in bibliotheek of koormap zetten. Eerst `input/<herkomst>/` (of lokaal `_inbox/` tot je zeker weet dat je hem bewaart).
2. Originele bestandsnaam laten staan.
3. Sitebuild draaien of `python scripts/update_werkvoorraad.py`: er komt een rij. Doel-id leeg? Invullen of vragen; niet gokken.
4. Notitie gebruiken voor “tweede bron”, “zelfde koormap-slot als …”, open vragen.

### Capella / CapToMusic (`.mxl` of `.capx`)

Tussenproducten in `_werk/`, origineel blijft in `capella/`.

1. `cleanup_capella_mxl.py` → opgekuiste `.mxl` zonder spaties in de naam.
2. MuseScore-import + `apply_mscz_layout.py` → standaard-`.mscz`.
3. `export_mscz_coria_mxl.py` → playback-`.mxl`; PDF uit dezelfde `.mscz`.
4. Bestanden in `oefenhoek/bibliotheek/<zangstuk>/<variant>/<uitvoeringsvorm>/` plus bibliotheek-`index.md`; koormap-slot met `bieb`.
5. `publicatiestatus: reviewable` op bibliotheek én koormap als er oefenbare inhoud in staat, anders `voorzien`.
6. `check --strict`.

**Copyright:** alleen wat in *deze* Capella-`.mxl` staat. Geen notice → geen
footer/colofon. Een VOW-bestand met dezelfde titel (bijv. Cherubijnenlied) is
een **andere** inputrij; die notice hoort niet automatisch op de Capella-publicatie.

### VOW of andere ruwe `.mscz`

Zelfde als vanaf stap 2 hierboven (layout is verplicht; een VOW-bestand is nog geen oefenhoek-standaard).
VOW heeft meestal CC BY-SA in `metaTag copyright`; layout maakt daar een korte
footer + colofon van.

### PDF / scan

Alleen als bron bewaren tot er een `.mscz` of `.vsa` is. Doelvorm in de tabel aanpassen als het VSA wordt.

### Hervatten na een maand

1. Deze tabel: rijen waar *Stap* niet `gepubliceerd` is, *Volgende* en *Notitie* lezen.
2. README in deze map als de mappenstructuur wegzakt.
3. Koormap-slot op de site: balk `voorzien` / `reviewable` / … is wat koorleden zien, niet deze interne stap.
