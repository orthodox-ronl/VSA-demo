# Werkvoorraad

Eén rij **per dumpbestand**, niet per zangstuk (hetzelfde stuk kan Capella én
VOW hebben). Dit is het interne geheugen: waar kwam het vandaan, waar moet het
heen, hoever is de conversie.

De **tabel** hieronder wordt bij `check` / `build` / `serve` opnieuw opgebouwd
uit de bestanden in `capella/`, `vow/`, `musescore/`, `musicxml/` en `pdf/`.
Zet **doel-id** en **notitie** zelf in de rij als de automatische match ze
niet kent; die twee velden worden bij een update bewaard. Stap en volgende
actie komen van wat er op schijf staat (bladermap mét partituur of nog niet).

Op de Oefenhoek-pagina van de site staat deze pagina uitklapbaar onderaan,
ná de lijst met deelrubrieken.

## Kolommen

| Kolom | Betekenis |
| --- | --- |
| Dump | Pad vanaf `input/` (herkomstmap + originele bestandsnaam) |
| Doel-id | Mapnaam van de bladermap (`[a-z0-9_-]+`). Leeg = nog niet gekozen |
| Deelrubriek | `liturgiemap-hemelum` of `overig` |
| Doelvorm | Meestal `.mscz` (oefenhoek-layout); soms `.vsa` |
| Stap | Hoever de dump is (zie hieronder) |
| Volgende | Wat je nu zou doen |
| Notitie | Vrij; overleeft de automatische update |

### Stap (intern, niet hetzelfde als `publicatiestatus` op de site)

| Stap | Betekenis |
| --- | --- |
| `ontvangen` | Dump ligt hier; conversie nog niet klaar of doel-id ontbreekt |
| `doel-id` | (in *Volgende*) eerst een mapnaam kiezen |
| `opkuisen` | Capella-laag: `cleanup_capella_mxl.py` |
| `layout` | `apply_mscz_layout.py` → standaard-`.mscz` |
| `playback` | Coria-`.mxl` uit die `.mscz` |
| `pdf` | A4-PDF naast de `.mscz` |
| `bladermap` | Er staat al oefenbare inhoud in de bladermap |

`publicatiestatus` (`voorzien` / `concept` / `reviewable` / `productie`) staat
op de `index.md` van de bladermap, voor koorleden. Deze tabel is voor wie
converteert.

<!-- werkvoorraad-tabel:begin -->

| Dump | Doel-id | Deelrubriek | Doelvorm | Stap | Volgende | Notitie |
| --- | --- | --- | --- | --- | --- | --- |
| `capella/15c - cherubijnenhymne - kastorski.mxl` | `15c-cherubijnenhymne-kastorski` | liturgiemap-hemelum | `.mscz` | bladermap | — | gepubliceerd |
| `capella/15c - cherubijnenhymne - kastorskij - ksl.mxl` |  | liturgiemap-hemelum | `.mscz` | ontvangen | doel-id | Ksl-variant; bladermap? |
| `capella/15e Cherubijnenhymne Bortnjanski no.5.mxl` |  | liturgiemap-hemelum | `.mscz` | ontvangen | doel-id | nog geen bladermap |
| `capella/19a - eucharistische kanon - feofan.mxl` | `19a-eucharistische-kanon` | liturgiemap-hemelum | `.mscz` | bladermap | — | gepubliceerd |
| `capella/2 - 1e antifoon.mxl` | `2-eerste-antifoon` | liturgiemap-hemelum | `.mscz` | ontvangen | opkuisen | bladermap stub (`voorzien`) |
| `capella/20d - in waarheid - moeder godslied.mxl` | `20d-in-waarheid-moeder-godslied` | liturgiemap-hemelum | `.mscz` | bladermap | — | gepubliceerd |
| `capella/28a - wij hebben het ware licht aanschouwd.mxl` | `28-wij-hebben-het-ware-licht` | liturgiemap-hemelum | `.mscz` | ontvangen | opkuisen | bladermap stub |
| `capella/29 - de naam des heren zij gezegend.mxl` | `29-de-naam-des-heren-zij-gezegend` | liturgiemap-hemelum | `.mscz` | ontvangen | opkuisen | bladermap stub |
| `capella/4 - 2e antifoon.mxl` | `4-tweede-antifoon` | liturgiemap-hemelum | `.mscz` | ontvangen | opkuisen | bladermap stub |
| `capella/6b - zaligsprekingen.mxl` | `6-derde-antifoon-zaligsprekingen` | liturgiemap-hemelum | `.mscz` | ontvangen | opkuisen | bladermap stub |
| `capella/7 - kleine intocht - zondag.mxl` | `7-kleine-intocht` | liturgiemap-hemelum | `.mscz` | ontvangen | opkuisen | zelfde bladermap als 7b |
| `capella/7b - kleine intocht - weekdagen.mxl` | `7-kleine-intocht` | liturgiemap-hemelum | `.mscz` | ontvangen | opkuisen | zelfde bladermap als 7 |
| `capella/8a - trisagion (+slav).mxl` | `8a-trisagion-slav` | liturgiemap-hemelum | `.mscz` | bladermap | — | gepubliceerd |
| `capella/8a - trisagion.mxl` | `8a-trisagion` | liturgiemap-hemelum | `.mscz` | bladermap | — | gepubliceerd |
| `vow/vow-Cherubijnenlied-Kastorskij.mscz` | `15c-cherubijnenhymne-kastorski` | liturgiemap-hemelum | `.mscz` | bladermap | — | tweede bron naast Capella |
| `vow/vow-dankzegging_toon_2_Kyiv.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `vow/vow-eind-liturgie.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `vow/vow-Eucharistische Canon-Rostov.mscz` |  | liturgiemap-hemelum | `.mscz` | ontvangen | doel-id | niet Feofan |
| `vow/vow-Kleine_intocht-moedergods.mscz` |  | liturgiemap-hemelum | `.mscz` | ontvangen | doel-id |  |
| `vow/vow-Kleine_intocht-weekdagen.mscz` | `7-kleine-intocht` | liturgiemap-hemelum | `.mscz` | ontvangen | layout |  |
| `vow/vow-Kleine_intocht-zondag.mscz` | `7-kleine-intocht` | liturgiemap-hemelum | `.mscz` | ontvangen | layout |  |
| `vow/vow-Tropaar-opstanding-toon1.mscz` |  |  | `.mscz` | ontvangen | doel-id | toon 1-8 (acht bestanden) |
| `vow/vow-Tropaar-opstanding-toon2.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `vow/vow-Tropaar-opstanding-toon3.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `vow/vow-Tropaar-opstanding-toon4.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `vow/vow-Tropaar-opstanding-toon5.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `vow/vow-Tropaar-opstanding-toon6.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `vow/vow-Tropaar-opstanding-toon7.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `vow/vow-Tropaar-opstanding-toon8.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |

<!-- werkvoorraad-tabel:einde -->

## Workflows (achtergrond)

### Nieuwe dump

1. Niet in de bladermap zetten. Eerst `input/<herkomst>/` (of lokaal `_inbox/` tot je zeker weet dat je hem bewaart).
2. Originele bestandsnaam laten staan.
3. Sitebuild draaien of `python scripts/update_werkvoorraad.py`: er komt een rij. Doel-id leeg? Invullen of vragen; niet gokken.
4. Notitie gebruiken voor “tweede bron”, “zelfde bladermap als …”, open vragen.

### Capella / CapToMusic (`.mxl` of `.capx`)

Tussenproducten in `_werk/`, origineel blijft in `capella/`.

1. `cleanup_capella_mxl.py` → opgekuiste `.mxl` zonder spaties in de naam.
2. MuseScore-import + `apply_mscz_layout.py` → standaard-`.mscz`.
3. `export_mscz_coria_mxl.py` → playback-`.mxl`; PDF uit dezelfde `.mscz`.
4. Bestanden in `oefenhoek/<deelrubriek>/<doel-id>/` plus `index.md`.
5. `publicatiestatus: reviewable` als er oefenbare inhoud in staat, anders `voorzien`.
6. `check --strict`.

### VOW of andere ruwe `.mscz`

Zelfde als vanaf stap 2 hierboven (layout is verplicht; een VOW-bestand is nog geen oefenhoek-standaard).

### PDF / scan

Alleen als bron bewaren tot er een `.mscz` of `.vsa` is. Doelvorm in de tabel aanpassen als het VSA wordt.

### Hervatten na een maand

1. Deze tabel: rijen waar *Stap* niet `bladermap` is, *Volgende* en *Notitie* lezen.
2. README in deze map als de mappenstructuur wegzakt.
3. Bladermap op de site: balk `voorzien` / `reviewable` / … is wat koorleden zien, niet deze interne stap.
