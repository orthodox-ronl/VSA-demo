---
title: "Id-register Hemelum"
linkTitle: "Id-register"
weight: 9800
publicatiestatus: concept
automatische_inhoud: false
vsa_nav_exclude: true
---

# Id-register — liturgiemap Hemelum → bibliotheek

Dit register is de **bron van waarheid** voor bibliotheek-id's tijdens de
conversie op `feat/oefenhoek-mxl-opkuis`. Een bibliotheek-id heeft altijd drie
lagen: `zangstuk-id` / `variant-id` / `uitvoeringsvorm-id` (elk segment
`[a-z0-9_-]+`). De **publicatiestam** voor basispartituur-bestanden is
`{zangstuk}-{variant}-{uitvoeringsvorm}` (functie `stem()` in
`scripts/bibliotheek.py`).

Het migratiescript `scripts/migrate_oefenhoek_bibliotheek.py` volgt de tabellen
**SCORE**, **PRINT** en **STUB** hieronder. Wijzig id's eerst hier en in dat
script tegelijk.

**Status legenda**

| Status | Betekenis |
| --- | --- |
| score | Basispartituur of VSA-bundle verhuist via `SCORE_MOVES` |
| print | Print-`.mscz` + PDF via `PRINT_MOVES` (geen Coria-basispartituur) |
| stub | Geen partituur; bibliotheek-stub + `bieb` op koormap |
| catalogus | Koormap blijft catalogus-include; **geen** bibliotheek-leaf in fase 2 |
| legacy | Dubbele/oude map; opruimen na migratie |
| open | Id of migratiepad nog afspreken |

---

## SCORE — basispartituur, VSA of gemengd

| Koormap-pad (t.o.v. `liturgiemap-hemelum/`) | Bibliotheek-id | Publicatiestam (basispartituur) | Bestanden nu | Opmerking |
| --- | --- | --- | --- | --- |
| `15-cherubijnenhymne/15c-kastorski/` | `15-cherubijnenhymne/15c-kastorski/hemelum` | `15-cherubijnenhymne-15c-kastorski-hemelum` | mscz, mxl, pdf | reviewable; NL (ongemerkt) |
| *(alleen bibliotheek voorlopig)* | `15-cherubijnenhymne/15c-kastorski/hemelum-ksl-trlat` | `15-cherubijnenhymne-15c-kastorski-hemelum-ksl-trlat` | — | Kerkslavisch getranslitereerd; stub |
| `15-cherubijnenhymne/15b-fatejev/` | `15-cherubijnenhymne/15b-fatejev/hemelum` | — | — | voorzien |
| `15-cherubijnenhymne/15d-kastorski/` | `15-cherubijnenhymne/15d-kastorski/hemelum` | — | — | voorzien (andere Kastorski dan 15c) |
| `15-cherubijnenhymne/15e-bortnjanski/` | `15-cherubijnenhymne/15e-bortnjanski/hemelum` | `15-cherubijnenhymne-15e-bortnjanski-hemelum` | — | voorzien; Capella-input aanwezig |

**Cherubijnen-varianten (Hemelum):** 15b Fatejev, 15c Kastorski, 15d Kastorski,
15e Bortnjanski. Niet: 15a Staro-Simonovskaja, 15f Lvovsky.
| `8-trisagion/8a-trisagion/` | `8-trisagion/8a-nederlands/hemelum` | `8-trisagion-8a-nederlands-hemelum` | mscz, mxl, pdf | Canoniek; niet de legacy-map `8a-trisagion/` |
| `8-trisagion/8a-trisagion-slav/` | `8-trisagion/8a-slav/hemelum` | `8-trisagion-8a-slav-hemelum` | mscz, mxl, pdf | Idem legacy `8a-trisagion-slav/` |
| `19a-eucharistische-kanon/` | `19-eucharistische-canon/19a-feofan/hemelum` | `19-eucharistische-canon-19a-feofan-hemelum` | mscz, mxl, pdf | |
| *(alleen bibliotheek voorlopig)* | `19-eucharistische-canon/rostov/hemelum` | `19-eucharistische-canon-rostov-hemelum` | — | VOW-input; stub |
| `20-moeder-godslied/20d-in-waarheid-moeder-godslied/` | `20-moeder-godslied/20d-in-waarheid/hemelum` | `20-moeder-godslied-20d-in-waarheid-hemelum` | mscz, mxl, pdf | |
| `20-moeder-godslied/20-moeder-godslied-ontslapen-mgods/` | `20-moeder-godslied/ontslapen-moeder-gods/hemelum` | `20-moeder-godslied-ontslapen-moeder-gods-hemelum` | print.mscz, mxl, pdf, vsa | `artefacten_handmatig`; print-track |
| `25-communievers/25-communievers-onthoofding-johannes-de-doper/` | `25-communievers/onthoofding-johannes-de-doper/hemelum` | `25-communievers-onthoofding-johannes-de-doper-hemelum` | vsa, vsa.mxl, pdf | Geen basispartituur-mscz; Coria via VSA-productgate |
| `troparen-en-kondaken/tropaar-nikolaas-van-myra/` | `110-tropaar/nikolaas-van-myra-toon-4/hemelum` | `110-tropaar-nikolaas-van-myra-toon-4-hemelum` | print.mscz, mxl, pdf, vsa | `artefacten_handmatig`; onder zangstuk `110-tropaar/` |
| `2-eerste-antifoon/weekdagen/` | `2-eerste-antifoon/weekdagen/hemelum` | `2-eerste-antifoon-weekdagen-hemelum-hemelum` | vsa, vsa.mxl | Koormap = Hemelum; geen `liturgikon/`-slot meer |
| *(alleen bibliotheek)* | `2-eerste-antifoon/weekdagen-liturgikon/hemelum` | `2-eerste-antifoon-weekdagen-liturgikon-hemelum` | vsa, vsa.mxl | Niet in Hemelum-koormap |
| `2-eerste-antifoon/zondag/` | `2-eerste-antifoon/zondag/hemelum` | `2-eerste-antifoon-zondag-hemelum` | mscz, mxl, pdf | stub-achtig in koormap |
| `4-tweede-antifoon/weekdagen/` | `4-tweede-antifoon/weekdagen/hemelum` | `4-tweede-antifoon-weekdagen-hemelum-hemelum` | vsa, vsa.mxl | |
| `4-tweede-antifoon/zondag/` | `4-tweede-antifoon/zondag/hemelum` | `4-tweede-antifoon-zondag-hemelum` | mscz, mxl, pdf | |
| `6-derde-antifoon/weekdagen/` | `6-derde-antifoon/weekdagen/hemelum` | `6-derde-antifoon-weekdagen-hemelum-hemelum` | vsa, vsa.mxl | |
| `6-derde-antifoon/zondag/` | `6-derde-antifoon/zondag/hemelum` | `6-derde-antifoon-zondag-hemelum` | mscz, mxl, pdf | Variant-id = koormap-mapnaam |
| `5-eniggeboren-zoon/` | `5-eniggeboren-zoon/default/hemelum` | `5-eniggeboren-zoon-default-hemelum` | mscz, mxl, pdf | `default` = enige variant |
| `7-kleine-intocht/zondag/` | `7-kleine-intocht/zondag/hemelum` | `7-kleine-intocht-zondag-hemelum` | mscz, mxl, pdf | |
| `7-kleine-intocht/weekdagen/` | `7-kleine-intocht/weekdagen/hemelum` | `7-kleine-intocht-weekdagen-hemelum` | mscz, mxl, pdf | |
| `7-kleine-intocht/moeder-gods/` | `7-kleine-intocht/moeder-gods/hemelum` | `7-kleine-intocht-moeder-gods-hemelum` | mscz, mxl, pdf | |
| `28-wij-hebben-het-ware-licht/` | `28-wij-hebben-het-ware-licht/default/hemelum` | `28-wij-hebben-het-ware-licht-default-hemelum` | mscz, mxl, pdf | |
| `29-de-naam-des-heren-zij-gezegend/` | `29-de-naam-des-heren-zij-gezegend/default/hemelum` | `29-de-naam-des-heren-zij-gezegend-default-hemelum` | mscz, mxl, pdf | |

---

## PRINT — koormap-vel (geen basispartituur-pijplijn)

| Koormap-pad | Bibliotheek-id | Bestanden nu | Opmerking |
| --- | --- | --- | --- |
| `7-kleine-intocht/zo-wk-mg/` | `7-kleine-intocht/zo-wk-mg/hemelum` | `*.print.mscz`, pdf | Print-vel; bij voorkeur `artefacten_handmatig: true` |
| `troparen-en-kondaken/tropaar-nikolaas-van-myra/` | `110-tropaar/nikolaas-van-myra-toon-4/hemelum` | print.mscz, mxl, pdf, vsa | Handmatige artefacten |
| `20-moeder-godslied/…` | `20-moeder-godslied/ontslapen-moeder-gods/hemelum` | print.mscz, mxl, pdf, vsa | Handmatige artefacten |

---

## STUB — alleen koormap + lege bibliotheek-leaf

| Koormap-pad | Bibliotheek-id | Opmerking |
| --- | --- | --- |
| `1-vredeslitanie/` | `1-vredeslitanie/default/hemelum` | voorzien |
| `3-eerste-kleine-litanie/` | `3-eerste-kleine-litanie/default/hemelum` | |
| `10-evangelielezing/` | `10-evangelielezing/default/hemelum` | |
| `11-dringende-litanie/` | `11-dringende-litanie/default/hemelum` | |
| `12-ontslapenen-litanie/` | `12-ontslapenen-litanie/default/hemelum` | |
| `13-catechumenen-litanie/` | `13-catechumenen-litanie/default/hemelum` | |
| `14-gelovigen-litanie/` | `14-gelovigen-litanie/default/hemelum` | |
| `16-vragende-litanie/` | `16-vragende-litanie/default/hemelum` | |
| `17-vredeswens/` | `17-vredeswens/default/hemelum` | |
| `18-geloofsbelijdenis/` | `18-geloofsbelijdenis/default/hemelum` | |
| `21-en-allen/` | `21-en-allen/default/hemelum` | |
| `22-vragende-litanie/` | `22-vragende-litanie/default/hemelum` | |
| `23-onze-vader/` | `23-onze-vader/default/hemelum` | |
| `24-een-is-heilig/` | `24-een-is-heilig/default/hemelum` | |
| `26-gezegend-hij-die-komt/` | `26-gezegend-hij-die-komt/default/hemelum` | |
| `27-communiezang/` | `27-communiezang/default/hemelum` | |
| `7d-dialoog-met-diaken/` | `7d-dialoog-met-diaken/default/hemelum` | tekstblad.md, tekstblad.pdf |

### Prokimen / alleluia (Kiev + znameni-reservering)

**Koormap-slots:** `9a-prokimen/` (prokimens eerder in de liturgie) en
`9b-alleluia/`. In de **bibliotheek** is `9a-` / `9b-` op de *variant*-laag
de melodieklasse (Kiev / znameni), niet het liturgienummer.

| Koormap-pad | Bibliotheek-id (voorbeeld) | Status |
| --- | --- | --- |
| `9a-prokimen/weekdagen/` | `9-prokimen/9a-maandag/groningen` … `9a-zaterdag` | score (VSA); compositieblad |
| `9a-prokimen/zondag-toon-N/` | `9-prokimen/9a-zondag-toon-N/groningen` + `9-alleluia/9a-toon-N/groningen` | voorzien (nog geen `.vsa`) |
| `9b-alleluia/` | `9-alleluia/9a-toon-1/groningen` … `9a-toon-8` | voorzien; compositieblad |

**Znameni (alleen register):** `9-prokimen/9b-{naam}/{uv}`,
`9-alleluia/9b-toon-{1..8}/{uv}` — nog geen leafs.

### Tropaar / kondak

Zangstuk-ids `110-tropaar/` en `120-kondak/`. Variant bv. `zondag-toon-3`,
`maandag-toon-4`, `nikolaas-van-myra-toon-4`. Alias-varianten: veld
`alias_van` op de variant-`_index.md` (geen tweede `.vsa`, geen
uitvoeringsvorm-map).

| Voorbeeld | Id |
| --- | --- |
| Zondag tropaar toon 1 | `110-tropaar/zondag-toon-1/groningen` |
| Weekdag + alias | canonieke variant `110-tropaar/maandag-toon-4` ← alias `110-tropaar/heilige-engelen-toon-4` |
| Nikolaas tropaar | `110-tropaar/nikolaas-van-myra-toon-4/hemelum` |
| Nikolaas kondak | `120-kondak/nikolaas-van-myra-toon-3/hemelum` |
| Moeder Gods kondak | `120-kondak/moeder-gods-toon-6/hemelum` |
| Losse Hemelum-troparen | `110-tropaar/heilige-martelaren-toon-4/hemelum`, `…/icoon-moeder-gods-vladimir-toon-4/…`, `…/mantel-moeder-gods-toon-4/…` |

`default` als variant-id betekent: één uitvoeringsvorm in Hemelum, geen
geneste varianten in de koormap.

### Taal op de uitvoeringsvorm (nieuw werk)

Standaard in deze repo is **Nederlands**; dat markeer je niet.

| Suffix op uitvoeringsvorm-id | Betekenis |
| --- | --- |
| *(geen)* | Nederlands |
| `-ksl` | Kerkslavisch, Cyrillisch schrift (default voor ksl) |
| `-ksl-trlat` | Kerkslavisch, Latijns schrift (getranslitereerd) |
| `-nl-ksl` | mengvorm Nederlands + Kerkslavisch |

Voorbeelden (publicatiestam):

- `15-cherubijnenhymne-15c-kastorski-hemelum` — NL
- `15-cherubijnenhymne-15c-kastorski-hemelum-ksl` — KSL Cyrillisch
- `15-cherubijnenhymne-15c-kastorski-hemelum-ksl-trlat` — KSL getranslitereerd
- `15-cherubijnenhymne-15c-kastorski-hemelum-nl-ksl` — mengvorm

**Legacy:** `8-trisagion/8a-nederlands/…` en `8-trisagion/8a-slav/…` houden taal
nog in de *variant*-laag; niet hernoemen tot een aparte migratie.

---

## CATALOGUS_KOORMAP — niet meer in oefenhoek

Oefenhoek-pagina’s gebruiken **geen** `:::include` naar catalogus/`lokaal/`.
Kondaken en troparen staan als bibliotheek-leafs onder `120-kondak/` en
`110-tropaar/`; losse gezangen onder eigen zangstuk-ids (bv. `220-uw-heilig-kruis/`),
met `bieb` op de koormap.

| Was (catalogus) | Nu (bibliotheek) |
| --- | --- |
| `kondak-nikolaas-van-myra/liturgikon/Liturgikon` | `120-kondak/nikolaas-van-myra-toon-3/hemelum` |
| `kondak-moeder-gods-toon-6/hemelum/Hemelum` | `120-kondak/moeder-gods-toon-6/hemelum` |

### Diversen

| Koormap-pad | Bibliotheek-id |
| --- | --- |
| `troparen-en-kondaken/uw-heilig-kruis/` | `220-uw-heilig-kruis/default/hemelum` |

---

## LEGACY — opgeruimd (2026-09-16)

| Pad | Actie |
| --- | --- |
| `liturgiemap-hemelum/8a-trisagion/` | Verwijderd (dubbel van `8-trisagion/8a-trisagion/`) |
| `liturgiemap-hemelum/8a-trisagion-slav/` | Verwijderd (dubbel van `8-trisagion/8a-trisagion-slav/`) |

---

## OPEN — reviewpunten

### 1. Tropaar Nikolaas — besloten

Bibliotheek-id: `110-tropaar/nikolaas-van-myra-toon-4/hemelum` (zangstuk
`110-tropaar/`, niet een apart zangstuk-id). Oude map
`tropaar-nikolaas-van-myra/…` verwijderd.

### 2. Variant-id `default` — besloten

Voor slots zonder geneste varianten: middelste laag = `default`
(bijv. `5-eniggeboren-zoon/default/hemelum`).

### 3. Derde antifoon zondag — besloten

Bibliotheek-id: `6-derde-antifoon/zondag/hemelum` (niet `zaligsprekingen-zondag`).

### 4. Familie-`_index.md` zonder `bieb` — besloten

Alleen leaves krijgen `bieb`; familie-pagina’s blijven TOC
(`automatische_inhoud: true`).

### 5. Capella `5a Eniggeboren Zoon.mxl` — afgerond

Doel-id: `5-eniggeboren-zoon/default/hemelum`.

### 6. Inputs met doel-id — deels gezet

| Input | Doel-id | Status |
| --- | --- | --- |
| `capella/…kastorskij - ksl.mxl` | `15-cherubijnenhymne/15c-kastorski/hemelum-ksl-trlat` | stub; nog converteren |
| `capella/15e … Bortnjanski….mxl` | `15-cherubijnenhymne/15e-bortnjanski/hemelum` | stub; Capella zegt **15e** (niet 15c) |
| `vow/Eucharistische Canon-Rostov.mscz` | `19-eucharistische-canon/rostov/hemelum` | stub naast Feofan |
| `vow/Tropaar-opstanding-toon*.mscz` | *(leeg)* | voorlopig laten zitten |

### 7. Dankzegging / eind-liturgie — strategie (voorstel)

Probleem: bestandsnamen mengen liturgische plek (`dankzegging`, `eind-liturgie`)
met variantinfo (`toon_2_Kyiv`). In het **bibliotheek** hoort de liturgische
functie in `zangstuk-id`, de melodische/traditionele uitwerking in
`variant-id`. De **koormap-TOC** mag wél de variantnaam tonen (`linkTitle`).

Voorstel:

1. Eerst inhoudelijk bepalen: is `dankzegging_toon_2_Kyiv` hetzelfde zangstuk
   als slot 28, een ander danklied, of een medley? Idem voor `eind-liturgie`
   (één stuk, of bundel 28+29?).
2. Bibliotheek: `zangstuk-id` = functie (bijv. `dankzegging` of het bestaande
   `28-wij-hebben-het-ware-licht` als het dát is); `variant-id` =
   `kyiv-toon-2` (niet de functienaam).
3. Koormap: map/slot blijft functioneel (`28-…` of `dankzegging/`); kindpagina
   of `linkTitle` mag “Kyiv toon 2” heten.
4. Doel-id leeg houden tot stap 1 klaar is — niet raden.

### 8. Eucharistische kanon + 20-moeder-godslied — al in bibliotheek

Lokaal aanwezig (nog untracked tot commit):

- `19-eucharistische-canon/19a-feofan/hemelum` (+ stub `rostov/hemelum`)
- `20-moeder-godslied/20d-in-waarheid/hemelum`
- `20-moeder-godslied/ontslapen-moeder-gods/hemelum`

Koormap-slots verwijzen via `bieb`; basispartituur-bestanden staan niet meer
in de liturgiemap (dat is de migratie, geen verdwijning).

---

## Review-checklist (na migratie)

- [x] Geen basispartituur-bestanden meer in koormap-leaves (`*.print.mscz` alleen in bibliotheek)
- [x] Legacy-mappen `8a-trisagion*` weg
- [x] Catalogus-kondak-pagina's ongewijzigd qua includes
- [x] `check --strict` groen (2026-09-16)
- [x] Variant-id `default` (was `standaard`)
- [x] Derde antifoon zondag: bibliotheek-variant `zondag`
- [x] Familie-`_index` zonder `bieb`
- [x] Werkvoorraad: gepubliceerde rijen op bibliotheek-id; open inputs nog zonder doel-id
- [x] Uitvoeringsvorm mét partituur → `reviewable` (koormap + bibliotheek)
- [x] Term “input” (niet “dump”) in werkvoorraad/handleiding
- [x] Taal-suffix op uitvoeringsvorm gedocumenteerd (`-ksl`, `-ksl-trlat`, `-nl-ksl`)
