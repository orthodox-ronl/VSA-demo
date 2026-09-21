# Contract: basispartituur-`.mscz` (canonieke partituur)

Normatieve representatie per bladermap **in de basispartituur-spoor**: één MuseScore 4-`.mscz`
die je mag editen, daarna **normaliseren** met `apply_mscz_layout.py`, en waaruit
PDF en Coria-`.mxl` worden afgeleid. Proef in VSA-demo; later naar VSA-tooling.

**Drie publicatiesporen** (Oefenhoek) — afgeleiden per **representatie-id**:
zie [oefenhoek-product-contract.md](oefenhoek-product-contract.md).

| Spoor (representatie-id) | Bron in de bladermap | Pipeline |
| ----- | -------------------- | -------- |
| Basispartituur (`partituur`) | `naam.mscz` (geen `.print.`) | layout → `mscz-products` → PDF + Coria; partituur-hash-gate |
| VSA (`vsa`) | `naam.vsa` | `vsa-products` → `{stam}.vsa.mxl`; `check_vsa_products` |
| Print-vel (`print`) | `naam.print.mscz` | **buiten** basispartituur-scripts; PDF handmatig; geen Coria van dit bestand |

Print: handleiding
`content-source/praktijk/handleiding/partituur/7-print-mscz.md`.
Helper: `is_print_mscz` in `scripts/score_filenames.py`.
Handmatige artefacten: frontmatter `artefacten_handmatig: true` (product-contract).

**Reciteertoon / maatstrepen / melisma:** gebaseerd op
[MCI Musical Notation](https://mci.archpitt.org/music/Notation.html).

Script: `python scripts/apply_mscz_layout.py <bestand.mscz>`
(of opgekuiste `.mxl` + `-o <bestand.mscz>`). Idempotent.
Weigert `*.print.mscz`.

Producten: `scripts\mscz-products.cmd` — zie
[mscz-product-transforms.md](mscz-product-transforms.md).
Freshness: embedded `partituur-sha256` in PDF/MXL; gate via `check_partituur_products.py`
(alleen basispartituur-`.mscz`, niet print).

Contractversie-meta: `vsaPartituurContract` = `partituur-1`.

---

## Rol van elk bestand

| Bestand | Rol |
| ------- | --- |
| basispartituur-`.mscz` | Canonieke bron (edit + normaliseer); **niet** `*.print.mscz` |
| `.print.mscz` | Print-/koormap-vel; scripts laten met rust |
| `.pdf` | Afgeleide A4-afdruk (`partituur` / `print` / later `vsa`); zie product-contract |
| Coria-`.mxl` | Afgeleide oefen-playback (`partituur` / `vsa`); zie product-contract |
| `index.md` | Hugo-bladermap; banner bij stale basispartituur-afgeleiden; `artefacten_handmatig` |

## Bestandsnamen

Publicatie (map, basispartituur-`.mscz`, Coria-`.mxl`, PDF): **geen spaties**; stam
`[a-z0-9_-]+`. Print-vel: zelfde stamregels, bestandsnaam eindigt op
`.print.mscz`. Helper: `scripts/score_filenames.py`.
Ruwe input in `oefenhoek/input/` mag spaties houden.

MuseScore 4.x: stijl in `score_style.mss` in de `.mscz`. **Geen** MusicXML-roundtrip
voor layout (stijl verdwijnt).

---

## Reciteertoon (één basispartituur-encoding, MCI)

**Stap 1 — rij vinden:** opeenvolgende noten met **zelfde toonhoogte** én
**zelfde nootduur**, elk met een lettergreep. Andere toon of andere lengte
breekt de rij (een half na kwarten hoort er niet bij).

**Stap 2 — collaps** alleen als die rij **meer dan vijf** lettergrepen heeft
(patroon **1-n-1**):

| Positie | Glyph | Toon / duur | Tekst |
| ------- | ----- | ----------- | ----- |
| Eerste lettergreep | gewone noot | ankertoon; ankerduur uit de rij | die lettergreep |
| Tussenliggende (≥2) | één stokloze feathered noot `\|\|O\|\|` (`headType` breve) | zelfde toon; **metrische breedte ≈ aantal lettergrepen** (zodat MuseScore de witruimte verdeelt i.p.v. alles links te duwen) | middelste lettergrepen |
| Laatste lettergreep | gewone noot | zelfde toon en duur als de eerste (uit dezelfde rij) | die lettergreep |

Reeksen van ≤5 lettergrepen blijven gewone noten. Noten buiten de rij
(andere toon of lengte) blijven onaangeroerd.

**Maatlengte** = som van de noten (geen opvulrust aan het eind).
`<dots>` staat in MSCX **vóór** `<durationType>` (MuseScore-conventie);
anders negeert MuseScore de punt en vult de maat met rusten.
Normalisatie wist niet-leidende rusten en zet `Measure len` opnieuw.
Coria exploseert de feathered noot later tot één kwart per lettergreep.

**Niet collapsen:** melisma (één lettergreep over meerdere noten + slur);
cadens/intonatie met bewuste lengte; toonwissels.

Na MuseScore-edit: normalisatie collapt opnieuw toegevoegde kwarten volgens
bovenstaande regel; de tekst blijft verdeeld over eerste / midden / laatste.

## Sleutels (twee notenbalken)

Bij precies **twee** niet-lege notenbalken (typische SATB-hub):

| Balk | Sleutel | Nodig voor |
| ---- | ------- | ---------- |
| 1 (boven) | G (vioolsleutel) | leesbare PDF |
| 2 (onder) | F (bassleutel) | leesbare PDF |

Normalisatie (`apply_mscz_layout`) en Capella-opkuis (`cleanup_capella_mxl`)
zetten ontbrekende header-sleutels en herschrijven afwijkende sleutels
(inclusief mid-score, bijv. C2 / G8vb) naar G/F. Scores met één balk of
meer dan twee niet-lege balken blijven onaangeroerd. **Toonsoorten**
(key signatures) vallen buiten dit contract.

## Maatstrepen (MCI)

| MCI | Basispartituur | Nodig voor |
| --- | --- | ---------- |
| Enkele maatstreep | einde frase / adempauze; **zichtbaar** aan het einde van elk systeem | PDF |
| Dubbele maatstreep | einde gezang of wissel `P:`/`D:`/`K:` | PDF; Coria `[PAUZE]` |
| Slotstreep | einde langer blok | PDF |
| Sectiebreuk | nieuw systeem | PDF |

Normalisatie zet verborgen eindmaatstrepen (`BarLine` met `visible=0`) weer
zichtbaar, zodat elk systeem een duidelijke rechter maatstreep heeft.

## Melisma

Hyphen (`Va-der`) ≠ melisma. Default bij normalisatie: **geen** lyric-underlines
(`ticks`); Capella-slurs zijn frasen, geen melisma. Opt-in: meta
`vsaLyricExtenders=1`. Coria zet `<extend/>` zelf waar nodig bij export.

## Tempo

| Regel | Waarde | Nodig voor |
| ----- | ------ | ---------- |
| Verplicht | BPM in de basispartituur (onzichtbare metronoom mag) | Coria-playback |
| Default bij ontbreken | 120 BPM | Coria |

## Copyright

| Situatie | Gedrag | Nodig voor |
| -------- | ------ | ---------- |
| Bron heeft notice | korte footer + colofon afgeleid | PDF elke pagina + einde |
| Bron heeft geen notice | CC BY-SA 4.0, bron = deze uitgave (`orthodoxekerkmuziek.nl`) | idem |
| Altijd | zin: kopiëren voor orthodoxe eredienst is toegestaan | colofon |
| Basispartituur onder `bibliotheek/<zangstuk>/<variant>/<uitvoeringsvorm>/` | colofonregel `Bibliotheek-id: …` + meta `vsaBibliotheekId` | identiteit op papier en in check |

| Veld | Rol |
| ---- | --- |
| `metaTag copyright` | Korte footer (letterlijke tekst op alle pagina's; niet `$C`) |
| `metaTag vsaCopyrightFull` | Volledige colofon (inclusief bibliotheek-id-regel indien van toepassing) |
| `metaTag vsaBibliotheekId` | Canonieke `zangstuk/variant/uitvoeringsvorm` (alleen in bibliotheek-basispartituur) |
| VBox "Colofon" | Direct na de laatste muziekmaat; op **dezelfde pagina** als er ruimte is, anders laat MuseScore een nieuwe pagina beginnen |

Bij normalisatie (`apply_mscz_layout`) en bij PDF-export (`mscz-products`) wordt de
korte notice **letterlijk** in `oddFooterC`/`evenFooterC` gezet. MuseScore’s `$C`
toont alleen pagina 1; daarom geen macro meer voor de korte footer.

Pipeline: `ensure_bibliotheek_id.py` zet ontbrekende/verkeerde id’s in de basispartituur
(lokaal); `check_bibliotheek_id.py` faalt op `main` als meta of colofon
niet klopt. Basispartituur-PDF erft het colofon bij `mscz-products`.

VOW-sibling mag **niet** stilzwijgend op een Capella-publicatie worden geplakt.

## Pagina en stijl (A4)

| Regel | Waarde | Nodig voor |
| ----- | ------ | ---------- |
| Papier | A4 staand | PDF |
| Marges | 15 mm | PDF |
| Eerste systeem | geen extra inspring | PDF |
| Laatste systeem | wél uitrekken over de paginabreedte (`lastSystemFillLimit=0`) zodat recitatief-tekst niet links opeengedrongen blijft | PDF |
| Verticaal | pagina niet vullen | PDF |
| Partijnamen | uit | PDF |
| Maatnummers | eerste maat van elke regel | PDF |
| Lyrics | onder bovenste balk | PDF |
| Titel → eerste systeem | `frameSystemDistance=14` | PDF |

## Typografie

| Toepassing | Font | Grootte | Nodig voor |
| ---------- | ---- | ------- | ---------- |
| Lyrics | Source Sans 3 | 13 pt | PDF |
| Staff-/systemtekst | Source Sans 3 | 12 pt | PDF |
| Composer | Source Sans 3 | 12 pt | PDF |
| Titel | Source Sans 3 | 18 pt | PDF |
| Footer | Source Sans 3 | 8 pt | PDF |

## Titelvak (VBox)

Alleen **title** (= `workTitle`) en **composer**. Nodig voor PDF-kop.
Cues `P:`/`D:`/`K:` horen als Staff Text, niet in het titelvak.

## Leidende rusten

Ritmisch behouden; kolom `gap` + onzichtbaar na start/dubbele streep.
Nodig voor PDF-uitlijning. Coria wist ze (zie transforms).

**Geen opvulrusten** aan het eind van een maat: na recite-collaps is
`Measure len` gelijk aan de som van de noten (1-n-1), zodat MuseScore geen
kwart-rust meer tekent om de maat vol te maken.

## Lettergrepen / SATB-dekking

`nl_hyphen.py` splitst multi-klinker tokens; elke partij minstens één noot per
lettergreep. Nodig voor consistente basispartituur vóór Coria-expansie.

## Tekstrollen

| Inhoud | Bestemming | Nodig voor |
| ------ | ---------- | ---------- |
| Cues `P:`/`D:`/`K:` | Staff Text | PDF; Coria-cue boven `[PAUZE]` |
| Componist | meta + VBox | PDF |

## Normalisatie na edit

1. Open de basispartituur in MuseScore 4, corrigeer, opslaan (geen MusicXML-export).
2. `python scripts\apply_mscz_layout.py pad\naar\basispartituur.mscz`
3. Controleer in MuseScore; herhaal zo nodig.
4. `scripts\mscz-products.cmd <bladermap>` → PDF + MXL met provenance-stamps.
5. Commit **basispartituur + pdf + mxl** samen.

## Wat dit script niet doet

- Capella-opkuis (lagen 1–3): `cleanup_capella_mxl.py`
- PDF/Coria-export: `mscz-products` / transforms-doc
