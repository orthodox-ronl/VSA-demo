# Werkvoorraad

Eén rij **per dumpbestand**, niet per zangstuk (hetzelfde stuk kan Capella én
VOW hebben). Dit is het interne geheugen: waar kwam het vandaan, waar moet het
heen, hoever is de conversie.

De **tabel** hieronder wordt bij `check` / `build` / `serve` opnieuw opgebouwd
uit de bestanden in `capella/`, `vow/`, `musescore/`, `musicxml/` en `pdf/`.
Zet **doel-id** (repertoire: `zangstuk/variant/uitvoeringsvorm`), **koormap**
(Hemelum-slot of leeg) en **notitie** zelf in de rij als de automatische
match ze niet kent; die velden worden bij een update bewaard. Stap en volgende
actie komen van wat er op schijf staat (repertoire-uitvoeringsvorm mét
partituur of nog niet).

Op de Oefenhoek-pagina van de site staat deze pagina uitklapbaar onderaan,
ná de lijst met deelrubrieken.

## Kolommen

| Kolom | Betekenis |
| --- | --- |
| Dump | Pad vanaf `input/` (herkomstmap + originele bestandsnaam) |
| Doel-id | Repertoire-id `zangstuk/variant/uitvoeringsvorm`. Leeg = nog niet gekozen |
| Koormap | Hemelum-slot (`15c-cherubijnenhymne-kastorski`) of leeg als het stuk niet in die map hoort |
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
| `gepubliceerd` | Er staat oefenbare inhoud in de repertoire-uitvoeringsvorm |

`publicatiestatus` (`voorzien` / `concept` / `reviewable` / `productie`) staat
op de `index.md` van de uitvoeringsvorm in `oefenhoek/repertoire/`, voor koorleden. Deze tabel is voor wie
converteert.

<!-- werkvoorraad-tabel:begin -->

| Dump | Doel-id | Koormap | Doelvorm | Stap | Volgende | Notitie |
| --- | --- | --- | --- | --- | --- | --- |
| `capella/15c - cherubijnenhymne - kastorski.mxl` | `cherubijnenhymne/15c-kastorski/hemelum` | `15c-cherubijnenhymne-kastorski` | `.mscz` | gepubliceerd | — | gepubliceerd |
| `capella/15c - cherubijnenhymne - kastorskij - ksl.mxl` |  |  | `.mscz` | ontvangen | doel-id | Ksl-variant; bladermap? |
| `capella/15e Cherubijnenhymne Bortnjanski no.5.mxl` | `cherubijnenhymne/15e-bortnjanski-no5/vokn` |  | `.mscz` | gepubliceerd | — | nog geen bladermap |
| `capella/19a - eucharistische kanon - feofan.mxl` | `eucharistische-kanon/19a-feofan/hemelum` | `19a-eucharistische-kanon` | `.mscz` | gepubliceerd | — | gepubliceerd |
| `capella/2 - 1e antifoon.mxl` | `2-eerste-antifoon/vokn/hemelum` | `2-eerste-antifoon` | `.mscz` | ontvangen | opkuisen | bladermap stub (`voorzien`) |
| `capella/20d - in waarheid - moeder godslied.mxl` | `moeder-godslied/20d-in-waarheid/hemelum` | `20d-in-waarheid-moeder-godslied` | `.mscz` | gepubliceerd | — | gepubliceerd |
| `capella/28a - wij hebben het ware licht aanschouwd.mxl` | `28-wij-hebben-het-ware-licht/vokn/hemelum` | `28-wij-hebben-het-ware-licht` | `.mscz` | gepubliceerd | — | bladermap stub |
| `capella/29 - de naam des heren zij gezegend.mxl` | `29-de-naam-des-heren-zij-gezegend/vokn/groningen` | `29-de-naam-des-heren-zij-gezegend` | `.mscz` | gepubliceerd | — | bladermap stub |
| `capella/4 - 2e antifoon.mxl` | `4-tweede-antifoon/vokn/hemelum` | `4-tweede-antifoon` | `.mscz` | ontvangen | opkuisen | bladermap stub |
| `capella/6b - zaligsprekingen.mxl` | `6-derde-antifoon-zaligsprekingen/vokn/hemelum` | `6-derde-antifoon-zaligsprekingen` | `.mscz` | ontvangen | opkuisen | bladermap stub |
| `capella/7 - kleine intocht - zondag.mxl` | `7-kleine-intocht/vokn/hemelum` | `7-kleine-intocht` | `.mscz` | ontvangen | opkuisen | zelfde bladermap als 7b |
| `capella/7b - kleine intocht - weekdagen.mxl` | `7-kleine-intocht/vokn/hemelum` | `7-kleine-intocht` | `.mscz` | ontvangen | opkuisen | zelfde bladermap als 7 |
| `capella/8a - trisagion (+slav).mxl` | `trisagion/8a-slav/hemelum` | `8a-trisagion-slav` | `.mscz` | gepubliceerd | — | gepubliceerd |
| `capella/8a - trisagion.mxl` | `trisagion/8a/hemelum` | `8a-trisagion` | `.mscz` | gepubliceerd | — | gepubliceerd |
| `vow/vow-Cherubijnenlied-Kastorskij.mscz` | `cherubijnenhymne/15c-kastorski/hemelum` | `15c-cherubijnenhymne-kastorski` | `.mscz` | gepubliceerd | — | tweede bron naast Capella |
| `vow/vow-dankzegging_toon_2_Kyiv.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `vow/vow-eind-liturgie.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `vow/vow-Eucharistische Canon-Rostov.mscz` |  |  | `.mscz` | ontvangen | doel-id | niet Feofan |
| `vow/vow-Kleine_intocht-moedergods.mscz` |  |  | `.mscz` | ontvangen | doel-id |  |
| `vow/vow-Kleine_intocht-weekdagen.mscz` | `7-kleine-intocht/vokn/hemelum` | `7-kleine-intocht` | `.mscz` | ontvangen | layout |  |
| `vow/vow-Kleine_intocht-zondag.mscz` | `7-kleine-intocht/vokn/hemelum` | `7-kleine-intocht` | `.mscz` | ontvangen | layout |  |
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

1. Niet in de repertoire-map zetten. Eerst `input/<herkomst>/` (of lokaal `_inbox/` tot je zeker weet dat je hem bewaart).
2. Originele bestandsnaam laten staan.
3. Sitebuild draaien of `python scripts/update_werkvoorraad.py`: er komt een rij. Doel-id leeg? Invullen of vragen; niet gokken.
4. Notitie gebruiken voor “tweede bron”, “zelfde uitvoeringsvorm als …”, open vragen.

### Capella / CapToMusic (`.mxl` of `.capx`)

Tussenproducten in `_werk/`, origineel blijft in `capella/`.

1. `cleanup_capella_mxl.py` → opgekuiste `.mxl` zonder spaties in de naam.
2. MuseScore-import + `apply_mscz_layout.py` → standaard-`.mscz`.
3. `export_mscz_coria_mxl.py` → playback-`.mxl`; PDF uit dezelfde `.mscz`.
4. Bestanden in `oefenhoek/repertoire/<zangstuk>/<variant>/<uitvoeringsvorm>/` plus `index.md`.
5. `publicatiestatus: reviewable` als er oefenbare inhoud in staat, anders `voorzien`.
6. `check --strict`.

### VOW of andere ruwe `.mscz`

Zelfde als vanaf stap 2 hierboven (layout is verplicht; een VOW-bestand is nog geen oefenhoek-standaard).

### PDF / scan

Alleen als bron bewaren tot er een `.mscz` of `.vsa` is. Doelvorm in de tabel aanpassen als het VSA wordt.

### Hervatten na een maand

1. Deze tabel: rijen waar *Stap* niet `gepubliceerd` is, *Volgende* en *Notitie* lezen.
2. README in deze map als de mappenstructuur wegzakt.
3. Uitvoeringsvorm op de site: balk `voorzien` / `reviewable` / … is wat koorleden zien, niet deze interne stap.
