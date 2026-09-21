---
title: "Als het misgaat"
linkTitle: "Als het misgaat"
weight: 30
---

# Als het misgaat

{{< cue >}}
Spaties in de publicatiestam? Hernoemen. Layout kwijt? Niet via MusicXML;
wel `apply_mscz_layout.py` op de basispartituur-`.mscz`. Coria rood bij `check`? Gebruik
de `.mxl` in het **bibliotheek** (partituur-product of `{stam}.vsa.mxl`), niet een
`.mxl` onder `input\`. MuseScore niet gevonden? Versie **4**, pad
`C:\Program Files\MuseScore 4\bin\MuseScore4.exe`.
{{< /cue >}}

**Wat je nu doet:** de veelvoorkomende blokkades herkennen. Blijft het
stuk: bewaar de fouttekst en vraag na; probeer niet drie andere scripts
tegelijk.

## Spaties of rare tekens in de naam

**Symptoom:** een script weigert, Coria doet het niet, of `check` klaagt.

Publicatiebestanden in de bibliotheek: geen spaties, geen `(` of `+`. Stam
alleen `a-z0-9_-`. Ruwe inputs in `input\` mogen hun oude naam houden. Schrijf
uitvoer altijd met `-o` naar een schone naam.

## Doel-id leeg of twijfel

Niet verzinnen. Zet in de werkvoorraad-rij een notitie “welk bibliotheek-id?”
en vraag het na. Twee inputs naar dezelfde uitvoeringsvorm mag (Capella én VOW);
noteer dat in de notitie. Id-lijst:
[Id-register](/praktijk/oefenhoek/bibliotheek/id-register/).

## bieb-accepteer weigert het bestand

**Symptoom:** `scripts\bieb-accepteer.cmd` eindigt met `FAIL:`.

Lees de regel `Oplossing:` in het opdrachtvenster. Veelvoorkomend: verkeerd
id, bestand bestaat al (dan `--force` alleen als je bewust overschrijft),
`.vsa` die `vsa validate` niet haalt, of een Capella-`.mxl` zonder basispartituur.
Stappen: [Opnemen in de bibliotheek](../1-opnemen-in-bibliotheek/).

## Layout of `mscz-products` “herstelt” je speciale partituur

Eindigt de bestandsnaam op `.print.mscz`? Dan hoort die **niet** door
`apply_mscz_layout` of `mscz-products`. Zie
[Print-.mscz](/praktijk/handleiding/partituur/7-print-mscz/). Per ongeluk
als gewone `.mscz` gezet? Hernoem terug naar `.print.mscz` vóór de
volgende `check`. Zet `artefacten_handmatig: true` op de bibliotheek-`index.md`
als PDF/MXL handmatig blijven.

## MuseScore start niet / “niet gevonden”

Layout en `mscz-products` hebben MuseScore **4** nodig. Installeer
MuseScore 4; gebruik niet MuseScore 3. Open het opdrachtvenster opnieuw
na installatie. (Voor alleen `.vsa` → Coria is MuseScore niet nodig:
`vsa-products`.)

## De pagina is lelijk of de stijl is weg

Meestal: geëxporteerd naar MusicXML en weer geopend. Ga terug naar de
basispartituur-`.mscz` (of opnieuw vanaf opgekuiste `.mxl` plus normaliseren). Daarna:

```cmd
python scripts\apply_mscz_layout.py pad\naar\bestand.mscz
```

## Coria: `failed to retrieve file`

Coria haalt het muziekbestand zelf vanaf internet op. De Oefenen-knop
moet daarom naar een **volledig** adres op `raw.githubusercontent.com`
wijzen, bijvoorbeeld
`https://raw.githubusercontent.com/orthodox-ronl/VSA-demo/gh-pages/preview/mxl/c/<hash>.musicxml`
(fingerprint op branch `gh-pages`). De website voor mensen blijft
`https://orthodox-ronl.github.io/VSA-demo/`; Coria's server faalt op
`github.io`-MusicXML regelmatig met `failed to retrieve file`.
Gebruik geen pad zonder host (`/mxl/c/…`), geen `http://127.0.0.1:…`,
geen `github.io`-MusicXML, en geen page-bundle-`.mxl`.

Draai `scripts\check.cmd` of `scripts\build.cmd` opnieuw zodat
`fingerprint_coria_mxl.py` en Hugo meelopen.
`check_hugo_links_and_assets.py` faalt op kapotte Coria-URL's.
Na een push controleert de Pages-workflow met `check_coria_retrieve.py`
of Coria het bestand echt ophaalt.

Een nieuw zangstuk dat nog niet op branch `gh-pages` staat, opent in Coria
pas na een `git push` (Coria kan de lokale Hugo-server niet bereiken).

## Coria: `translation failed` of check weigert de `.mxl`

De `.mxl` in de bibliotheek moet uit `mscz-products` of `vsa-products`
komen (of handmatig bij `artefacten_handmatig`), niet een ruwe Capella-`.mxl`.
Maak basispartituur-producten opnieuw ná de laatste normalisatie, of draai
`scripts\vsa-products.cmd` voor een bibliotheek-`.vsa`. `check` heeft een
aparte Coria-controle; de melding wijst het bestand aan.

## Rode banner: partituur- of VSA-afgeleiden niet in orde

| Banner | Oorzaak | Actie |
| --- | --- | --- |
| Basispartituur-afgeleiden | PDF/MXL passen niet bij de basispartituur-`.mscz` | [Afgeleiden](../../partituur/6-afgeleiden/) — layout + `mscz-products` |
| VSA-afgeleiden | `{stam}.vsa.mxl` ontbreekt of is ouder dan de `.vsa` | `scripts\vsa-products.cmd`, commit beide |

Op `main` faalt de build bij dezelfde situaties.

## Gele banner: handmatige artefacten

Geen fout: `artefacten_handmatig: true` staat op die bibliotheekpagina.
PDF/MXL vernieuwen de scripts niet; doe dat zelf na elke bronwijziging.

## `bieb` faalt bij build

De shortcode verwijst naar een bibliotheek-pagina die nog niet bestaat, of
het id klopt niet (`zangstuk/variant/uitvoeringsvorm`). Maak eerst de
bibliotheek-map + `index.md`, of corrigeer het id in het koormap-slot.

## Hugo-waarschuwing: SVG ontbreekt

Shortcode `bieb` toont het VSA-plaatje uit
`static\vsa\bladermap\…`. Ontbreekt die SVG:

```cmd
python scripts\sync_oefenhoek_index.py --svg
```

of `scripts\check.cmd --strict`. `serve --no-build` slaat die stap over.
Uitleg: [.vsa schrijven](../../vsa/1-vsa-schrijven/).

## `vsa validate` klaagt

De markering zit in de gezongen regel. Vergelijk met een werkend `.vsa`
ernaast. Haal niet “even de rare tekens weg” om groen te worden.

## Template SATB: `TemplateInstanceError`

De sopraan in de VSA volgt de tropaar-toon-4-formule niet (toon of
verplicht slot). Lees de hint in het venster; pas de VSA aan, of (met
iemand die de formule beheert) de template. Werk de `.mscz` niet als
eerste bron van waarheid bij.

## `publicatiestatus` ontbreekt

Elke Oefenhoek-`index.md` en `_index.md` (bibliotheek en koormap) moet de
regel `publicatiestatus` in de `---` hebben. Handleiding-pagina’s niet.

## Preview op de verkeerde poort

http://127.0.0.1:**18731**/ — niet 1313.

## Check rood, lange muur tekst

Scroll naar het **eerste** `FAILED` of `error`. Vaak is één bestand de
oorzaak. Los dat ene bestand op, draai check opnieuw. Pak niet de hele
foutenmuur tegelijk aan.

## Waar vraag je het

Gebruik dezelfde kanalen als op de Oefenhoek-pagina’s (e-mail / GitHub).
Stuur mee: welk bibliotheek-id, welk commando, de foutregel, en of het om
Capella, VOW of VSA gaat.

{{< navbuttons "Terug naar overzicht|/praktijk/handleiding/" >}}
