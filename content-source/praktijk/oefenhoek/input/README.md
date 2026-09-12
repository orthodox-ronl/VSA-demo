# Input voor de oefenhoek

Hier komen bestanden binnen die **nog geen** oefenhoek-uitgave zijn: dumps
uit Capella, VOW, MuseScore, een PDF-scan, MusicXML uit een andere app, enz.
Pas na conversie naar het afgesproken formaat (meestal een standaard-`.mscz`,
soms `.vsa`) horen ze in een bladermap onder `liturgiemap-hemelum/` of
`overig/`.

Deze map staat wél in git (zodat conversie herhaalbaar is), maar **niet** op
de publieke site. Daarom geen `_index.md` hier.

## Mappen

| Map | Wat erin hoort |
| --- | --- |
| `capella/` | Capella / CapToMusic: `.cap`, `.capx`, of een dump-`.mxl` (originele naam, spaties mag) |
| `vow/` | ruwe VOW-`.mscz` |
| `musescore/` | andere ruwe `.mscz` (nog niet de oefenhoek-layout) |
| `musicxml/` | `.xml` / `.musicxml` / `.mxl` uit andere programma's |
| `pdf/` | scans of print-PDF die je als bron bewaart |
| `_inbox/` | lokaal, niet in git: “gisteren in de mail, nog niet gekozen” |
| `_werk/` | lokaal, niet in git: tussenproducten (opgekuiste MXL, halve layout) |
| `.archief/` | oude kopieën; git negeert `.archief/` al globaal |

**Inbox:** eerst hierheen (of `_inbox/`), pas committen naar `capella/` / `vow/` / … als dit dé dump is die je wilt bewaren.

**Namen:** dumps mag je laten zoals ze binnenkwamen. Publicatiebestanden in de bladermap: geen spaties, stam `[a-z0-9_-]+` (`scripts/score_filenames.py`).

**Overzicht:** `werkvoorraad.md` in deze map — één rij per dump. De tabel wordt bij een sitebuild (`check` / `build` / `serve`) opnieuw gevuld. Handmatige **notitie** en **doel-id** in een bestaande rij blijven staan. Op de Oefenhoek-pagina staat dezelfde tekst uitklapbaar onderaan.

## Workflow (kort)

1. Dump in de juiste herkomst-map (of eerst `_inbox/`).
2. Doel-id kiezen (`[a-z0-9_-]+`); onbekend: in de tabel leeg laten of vragen, niet raden.
3. Converteren (Capella-`.mxl` → opkuisen → layout-`.mscz`; VOW-`.mscz` → layout). Tussenwerk in `_werk/`.
4. Publiceren in `oefenhoek/<deelrubriek>/<doel-id>/` (`index.md` + `.mscz` / Coria-`.mxl` / PDF) als de pipeline groen is.
5. `publicatiestatus` op die bladermap: `voorzien` (nog geen uitgave), `reviewable` (er staat iets in), `concept` (secties), `productie` alleen bewust.

Uitgebreider: onderaan `werkvoorraad.md`.
