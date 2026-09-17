# Input voor de oefenhoek

Hier komen **inputs** binnen die **nog geen** oefenhoek-uitgave zijn: bestanden
uit Capella, VOW, MuseScore, een PDF-scan, MusicXML uit een andere app, enz.
Pas na conversie horen hub-bestanden in het **bibliotheek**
(`oefenhoek/bibliotheek/<zangstuk>/<variant>/<uitvoeringsvorm>/`); het
**koormap-slot** in `liturgiemap-hemelum/` verwijst daarheen.

Deze map staat wél in git (zodat conversie herhaalbaar is), maar **niet** op
de publieke site. Daarom geen `_index.md` hier.

## Mappen

| Map          | Wat erin hoort |
| ------------ | -------------- |
| `capella/`   | Capella / CapToMusic: `.cap`, `.capx`, of een input-`.mxl` (originele naam, spaties mag) |
| `vow/`       | ruwe VOW-`.mscz` |
| `musescore/` | andere ruwe `.mscz` (nog niet de Oefenhoek-layout) |
| `musicxml/`  | `.xml` / `.musicxml` / `.mxl` uit andere programma's |
| `pdf/`       | scans of print-PDF die je als bron bewaart |
| `_inbox/`    | lokaal, niet in git: “gisteren in de mail, nog niet gekozen” |
| `_werk/`     | lokaal, niet in git: tussenproducten (opgekuiste MXL, halve layout) |
| `.archief/`  | oude kopieën; git negeert `.archief/` al globaal |

**Inbox:** eerst hierheen (of `_inbox/`), pas committen naar `capella/` / `vow/` / … als dit dé input is die je wilt bewaren.

**Namen:** inputs mag je laten zoals ze binnenkwamen. Publicatie in de bibliotheek: geen spaties, stam = publicatiestam uit de bibliotheek-id (`scripts/bibliotheek.py`, `scripts/score_filenames.py`).

**Overzicht:** `werkvoorraad.md` in deze map — één rij per input. Kolommen **Doel-id** (bibliotheek-id) en **Koormap** (liturgie-slot). De tabel wordt bij `check` / `build` / `serve` opnieuw gevuld. Handmatige **notitie** en **doel-id** in een bestaande rij blijven staan. Op de Oefenhoek-pagina staat dezelfde tekst uitklapbaar onderaan.

**Id-lijst:** [bibliotheek/ID-REGISTER.md](../bibliotheek/ID-REGISTER.md).

## Workflow (kort)

1. Input in de juiste herkomst-map (of eerst `_inbox/`).
2. Bibliotheek-id kiezen (`zangstuk/variant/uitvoeringsvorm`); onbekend: in de tabel leeg laten of vragen, niet raden.
3. Converteren (Capella-`.mxl` → opkuisen → normaliseren; VOW-`.mscz` → stemmen/lettergrepen checken, daarna normaliseren). Tussenwerk in `_werk/`.
   Copyright: alleen notice uit **deze** input meenemen.
4. Bestanden in `oefenhoek/bibliotheek/…/` + koormap-slot met `bieb` als
   `check --strict` groen is. Geen `:::include` naar catalogus of
   `content-source/lokaal/` vanuit de oefenhoek.
5. `publicatiestatus` op bibliotheek-`index.md` en koormap-`index.md`: `voorzien`, `reviewable`, `concept`, `productie` alleen bewust.

Uitgebreider: onderaan `werkvoorraad.md` en [Handleiding voor beheerders](/praktijk/handleiding/).
