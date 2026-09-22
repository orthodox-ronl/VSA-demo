---
title: "opkuisen"
linkTitle: "opkuisen"
weight: 80
---

# NAME

`scripts\opkuisen.cmd` — herkomstanalyse en inhoudelijke opkuis van
MusicXML- en MuseScore-bestanden (optioneel daarna layout)

# SYNOPSIS

```cmd
scripts\opkuisen.cmd <pad> [pad...] [opties]
scripts\h.cmd opkuisen
```

Python-entrypoint: `scripts\opkuisen.py`. Compat-shim voor alleen Capella:
`python scripts\cleanup_capella_mxl.py …` (voegt `--assume capella` toe).

# DESCRIPTION

**Opkuisen** betekent: de *muzikale en tekstuele inhoud* van een partituur
opschonen vóór (of naast) de basispartituur-standaard. Het script
`opkuisen.cmd` doet eerst een **herkomstanalyse** (welke “hoek” het
invoerbestand lijkt te komen) en past daarna alleen de **opkuis-manieren**
toe die bij die hoek horen.

De **default-diepte** is **content**: alleen inhoudsfixes, geen
A4-pagina-layout. Met `--layout` volgt daarna normaliseren via
`apply_mscz_layout` (zelfde werk als [layout](../layout/)). PDF en
Coria-`.mxl` blijven bij [mscz-products](../mscz-products/).

Dit commando zit **niet** in `check` / `build` / `serve`. Workflow-checklist
(menselijk werk, stemmen controleren): 
[Opkuisen (partituur)](/praktijk/handleiding/partituur/2-opkuisen/).

## Wat opkuisen wél is / niet is

| Wel | Niet |
| --- | --- |
| Herkomst bepalen (Capella, generiek MusicXML, MuseScore, VSA) | Stil Capella-heuristieken op elk willekeurig bestand toepassen |
| Inhoudsfixes die bij die hoek horen (zie manieren hieronder) | PDF of Coria-export (`mscz-products` / `vsa-products`) |
| Optioneel `--layout` naar basispartituur-`.mscz` | Print-vel `*.print.mscz` bewerken |
| Rapport zonder schrijven (`--analyze` / `--dry-run`) | Stemmen SAT/B voor jou herschikken als die structureel verkeerd staan |
| | SVG uit `.vsa` bouwen of `{stam}.vsa.mxl` maken |

**Normaliseren / layouten** (A4, copyright/colofon, reciteer-collaps
`||O||`, tempo) is een **andere verantwoordelijkheid**, ook als je die
stap met `--layout` in dezelfde run start. Zie [layout](../layout/) en
`scripts\mscz-partituur-contract.md`.

## Invoerformats

| Extensie | In v1 |
| --- | --- |
| `.mxl`, `.musicxml`, `.xml` | Ja (MusicXML) |
| `.mscz`, `.mscx` | Ja (MuseScore) |
| `.vsa` | Alleen `--analyze` / `--dry-run` (`vsa validate`); geen automatische inhoudsfix |
| `.mvsa` | Herkend als voorzien; geen automatische opkuis |
| `.cap`, `.capx` | Geweigerd — eerst CapToMusic naar `.mxl` |
| `*.print.mscz` | Geweigerd — zie [Print-.mscz](/praktijk/handleiding/partituur/7-print-mscz/) |
| Caput / ongeldige zip / geen MusicXML in `.mxl` | Foutmelding, exit 1 |

## Directory-gedrag

Je mag één bestand **of** een map opgeven (zoals bij `vsa validate` op een
boom). Een map wordt **recursief** doorzocht op ondersteunde extensies.

- `*.print.mscz` in een mapscan worden overgeslagen.
- Als de scan-root zelf geen mapsegment `input` heeft, worden paden onder
  `input\` overgeslagen (ruwe dumps niet per ongeluk meenemen vanuit
  `content-source`). Een pad dat wél onder `oefenhoek\input\capella\`
  begint, wordt wél gescand.
- Ongeldige of geweigerde bestanden tellen in de samenvatting; de run gaat
  door met de rest.

## Dieptes

| Diepte | Flags | Schrijft bestanden? |
| --- | --- | --- |
| **content** (default) | (geen extra flag) | Ja — alleen inhoudsfixes |
| **analyze** | `--analyze` **of** `--dry-run` | Nee — alleen rapport |
| **layout** | `--layout` (na content) | Ja — content + daarna `apply_mscz_layout` |

`--analyze` en `--dry-run` zijn **synoniemen**: beide zetten dezelfde
optie. Wie “analyse” zoekt gebruikt `--analyze`; wie `--dry-run` kent van
andere scripts (bijvoorbeeld `mscz-products`) gebruikt die vorm. Het
effect is identiek: herkomst, voorgestelde manieren, eventueel
`vsa validate` bij `.vsa`, **geen** schrijfactie. Combineer je
`--analyze`/`--dry-run` met `--layout`, dan rapporteert het script alleen
dat layout *zou* volgen — er wordt nog steeds niets geschreven.

## Herkomstanalyse (“hoek”)

Vóór elke schrijfactie leest het script fingerprints. Resultaat per
bestand: `hoek`, `confidence` (0–1), signalen, voorgestelde passes.

| Signaal | Hoek |
| --- | --- |
| Comment of `<software>` met CapToMusic / Capella | `capella` (hoge confidence) |
| Voldoende verborgen klinkende noten (`print-object=no`) | `capella` |
| Extensie `.mscz` / `.mscx` (+ museScore-root) | `musescore` |
| MusicXML zonder Capella-signalen | `musicxml-generic` |
| Extensie `.vsa` / `.mvsa` | `vsa` / `mvsa` |
| Pad bevat `capella` zonder sterke XML-signalen | `unknown`, lage confidence |

**Lage confidence** (onder 0,5) bij een content-run **zonder** `--assume`
wordt geweigerd (exit 2), zodat Capella-heuristieken niet stilletjes op
het verkeerde bestand lopen. Oplossing: `--assume <hoek>` of (spaarzaam)
`--force`.

`--assume` accepteert: `capella`, `musicxml-generic`, `musescore`, `vsa`,
`mvsa`.

## Opkuis-manieren (wat wél / niet per hoek)

### A. Capella-MusicXML (`hoek=capella`)

Gebaseerd op `cleanup_capella_mxl.cleanup` (lagen 1–3).

| Wel | Niet |
| --- | --- |
| Verborgen klinkende noten zichtbaar als reciteerkwarten | A4-layout, PDF, Coria |
| Lettergreep ↔ noot; multi-klinker tokens splitsen met extra noten | Stemmen structureel herschikken |
| Lyrics alleen op stem 1; backups bijwerken | Originelen in `input\capella\` stil overschrijven |
| Titel/pagina-rommel; lege/rust-only maten weg | Print-`.mscz` |
| Bij twee balken: sleutels G boven / F onder | Lyric-underline onder Capella-frase-slurs forceren als melisma |

### B. Generiek MusicXML (`hoek=musicxml-generic`)

| Wel | Niet |
| --- | --- |
| Twee-balks G/F-sleutels (zelfde helper als Capella) | Capella-unhide, Capella-titel/pagina-rommel, Capella-slur-logica |
| | Belofte dat het resultaat “net zo schoon” is als Capella-pad |

### C. MuseScore-inhoud (`hoek=musescore`, default content)

MSCX-fixes uit `apply_mscz_layout.content_cleanup_mscx`, **zonder**
volle layout.

| Wel | Niet |
| --- | --- |
| Lege notenbalken verwijderen | A4, fonts, copyright/colofon |
| Undersplit lettergrepen splitsen | Reciteer-collaps `\|\|O\|\|` |
| Noot per lettergreep knippen (homofoon waar van toepassing) | Die stappen: gebruik `--layout` of `layout.cmd` |

### D. Layout (`--layout`)

Roept dezelfde keten aan als [layout](../layout/) (MuseScore-convert bij
MusicXML-invoer, daarna `process_mscz`). Weigert `*.print.mscz`. Losse
`.mscx` + `--layout` wordt geweigerd (eerst als `.mscz` opslaan in
MuseScore 4).

### E. VSA / mvsa (v1)

| Situatie | Gedrag |
| --- | --- |
| `.vsa` + `--analyze` / `--dry-run` | `vsa validate` + rapport |
| `.vsa` + content / `--layout` | Weigering met verwijzing naar de VSA-handleiding |
| `.mvsa` | Voorzien; geen automatische opkuis |
| `{stam}.vsa.mxl` als “bron” kuisen met Capella-passes | **Nooit** — Coria-afgeleide blijft product-spoor |

## Uitvoeropties

| Optie | Betekenis |
| --- | --- |
| `-o`, `--output` | Doelbestand (één invoer) of doelmap (één of meer invoeren) |
| `--in-place` | Overschrijf de bron; **vereist** om naar ruwe `oefenhoek\input\<herkomst>\` te schrijven (niet `_werk`) |
| `--ext` | Doel-extensie (bijvoorbeeld `.mxl`) |
| Zonder `-o` | In-place alleen als de bestandsnaam **geen spaties** heeft; anders weigering met hint naar `_werk\STAM\` |

De **publicatiestam** is het bibliotheek-id met `-` tussen de drie lagen,
zonder spaties (voorbeeld: id `8-trisagion/8a-nederlands/hemelum` → stam
`8-trisagion-8a-nederlands-hemelum`). Schrijf opgekuiste Capella-uitvoer
bij voorkeur naar
`content-source\praktijk\oefenhoek\input\_werk\<stam>\<stam>.mxl`.

## Exitcodes

| Code | Betekenis |
| --- | --- |
| 0 | Alles ok |
| 1 | Minstens één harde fout (corrupt bestand, validate-fail, onverwachte exception) |
| 2 | Minstens één weigering (lage confidence, beschermde input, spaties zonder `-o`, VSA-content, …) |

Aan het eind volgt een regel `samenvatting: ok=… geweigerd=… fout=…`.

## OPTIONS (overzicht)

| Optie | Betekenis |
| --- | --- |
| `--analyze` | Alleen rapport; geen schrijven |
| `--dry-run` | Synoniem van `--analyze` |
| `--layout` | Na content ook basispartituur-layout |
| `--assume HOEK` | Overschrijf detectie |
| `--force` | Ga door bij lage confidence zonder `--assume` |
| `-o`, `--output` | Doelbestand of doelmap |
| `--in-place` | Bron overschrijven / ruwe input toestaan |
| `--ext EXT` | Doel-extensie |
| `--id ID` | Bibliotheek-id voor layout-diepte (optioneel) |
| `-h`, `--help` | Korte usage in `opkuisen.cmd` |

# EXAMPLES

Capella-`.mxl` naar `_werk` (origineel blijft staan):

```cmd
scripts\opkuisen.cmd "content-source\praktijk\oefenhoek\input\capella\8a - 8-trisagion.mxl" -o content-source\praktijk\oefenhoek\input\_werk\8-trisagion-8a-nederlands-hemelum\8-trisagion-8a-nederlands-hemelum.mxl
```

Alleen analyseren (geen schrijven) — beide vormen doen hetzelfde:

```cmd
scripts\opkuisen.cmd content-source\praktijk\oefenhoek\input\capella --analyze
scripts\opkuisen.cmd content-source\praktijk\oefenhoek\input\capella --dry-run
```

Ruwe `.mscz` inhoudsfixes in-place (bestandsnaam zonder spaties), daarna
apart layouten of in één run:

```cmd
scripts\opkuisen.cmd content-source\praktijk\oefenhoek\input\_werk\STAM\STAM.mscz
scripts\opkuisen.cmd content-source\praktijk\oefenhoek\input\_werk\STAM\STAM.mscz --layout
```

Lage confidence forceren naar Capella-manier:

```cmd
scripts\opkuisen.cmd pad\naar\twijfel.musicxml --assume capella -o pad\naar\uit.musicxml
```

`.vsa` alleen valideren via analyse:

```cmd
scripts\opkuisen.cmd pad\naar\stuk.vsa --analyze
```

# WHEN

- Nieuwe Capella-/CapToMusic-`.mxl` of andere MusicXML vóór
  [layout](../layout/).
- Ruwe `.mscz` waarvan lettergrepen/lege balken scriptbaar zijn; stemmen
  blijf je in MuseScore 4 controleren ([partituur-opkuisen](/praktijk/handleiding/partituur/2-opkuisen/)).
- Eerst `--analyze` / `--dry-run` als je twijfelt over de herkomst.

# GRENZEN

- Geen vervanging van menselijke stemverdeling of liturgische tekstcontrole.
- Geen MusicXML-roundtrip “om MuseScore te repareren” als standaardpad.
- Geen stil overschrijven van ruwe `oefenhoek\input\capella\` (en andere
  herkomstmappen) zonder `--in-place`.
- Generiek MusicXML wordt niet beloofd even schoon als Capella-pad.
- VSA-autofix hoort later in VSA-tooling; `opkuisen` is in v1 alleen
  dispatcher/validate-rapport voor `.vsa`.
- Niet in de CI-`check`-keten.

# SEE ALSO

- [layout](../layout/)
- [mscz-products](../mscz-products/)
- Workflow: [Opkuisen](/praktijk/handleiding/partituur/2-opkuisen/)
- VSA: [.vsa schrijven](/praktijk/handleiding/vsa/1-vsa-schrijven/)
- mvsa (voorzien): [werktrajecten/mvsa](/praktijk/handleiding/werktrajecten/mvsa/)
- Console: `scripts\h.cmd opkuisen`
- Implementatie: `scripts\opkuisen.py`, `scripts\opkuis_detect.py`,
  `scripts\cleanup_capella_mxl.py`, `scripts\apply_mscz_layout.py`
