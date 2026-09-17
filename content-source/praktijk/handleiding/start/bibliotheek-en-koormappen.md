---
title: "Bibliotheek en koormappen"
linkTitle: "Bibliotheek en koormappen"
weight: 25
---

# Bibliotheek en koormappen

{{< cue >}}
- **Bibliotheek** = alles wat jullie *hebben* (uitvoeringsvorm + id + partituur)
- **Koormap** = geordende *view* voor één gelegenheid of thema (navigatie + leesbladen)
- Een uitvoeringsvorm mag in de bibliotheek staan **zonder** koormap
- In een koormap is een liturgische plek vaak een **hoofdstuk** (sectie) met
  kindpagina’s of een **compositieblad** (markdown + shortcodes)
{{< /cue >}}

**Wat je nu doet:** het model kennen waarmee de Oefenhoek werkt, zodat
publicatie, ids en navigatie niet door elkaar lopen.

## Drie invalshoeken

| Wie | Vraag | Ingang |
| --- | --- | --- |
| Beheerder | Wat hebben we? Welk id gebruik ik? | [Bibliotheek](/praktijk/oefenhoek/bibliotheek/), [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/), special pages |
| Koor (in situ) | Wat zingen we in welke volgorde? | Koormap, nu vooral [liturgiemap Hemelum](/praktijk/oefenhoek/liturgiemap-hemelum/) |
| Individueel koorlid | Wat moet / wil ik oefenen? | Koormap *of* bibliotheek (ook stukken die nog in geen map zitten) |

## Kernregel

De bibliotheek is de **bron van waarheid**. Koormappen zijn **views**: ze
bevatten geen tweede kopie van de hub-bestanden, maar verwijzen met
`bieb` naar `zangstuk/variant/uitvoeringsvorm`.

Een uitvoeringsvorm mag publiek in de bibliotheek staan terwijl **geen
enkele** koormap ernaar wijst. Dat is bewust: ontdekking en latere opname in
een map (feest, collectie, parochiekeuze) komen daarna.

## Bouwstenen in een koormap

Een koormap is geen platte lijst “één zangstuk = één pagina”. De
[liturgiemap Hemelum](/praktijk/oefenhoek/liturgiemap-hemelum/) is een
**inhoudsopgave van liturgische plekken**. Een titel in die inhoudsopgave
kan naar één zangstuk wijzen, of naar een **hoofdstuk** met meerdere
keuzes (bijvoorbeeld eerste antifoon: weekdagen, zondag, later feestdagen).

| Bouwsteen | Bestand | Rol |
| --- | --- | --- |
| **Koormap-root** | `liturgiemap-hemelum\_index.md` | Handmatige inhoudsopgave van de hele map |
| **Koormap-sectie** | map met `_index.md` | Liturgische plek / hoofdstuk; tekst plus kindlijst, of eigen TOC |
| **Slot-pagina** | map met `index.md` | Lees- of oefenblad: markdown plus `bieb` (geen catalogus/`lokaal/`-include) |

**Sectie** (`_index.md`): zet `automatische_inhoud: true` als de layout de
kindpagina’s mag tonen (voorbeeld:
`liturgiemap-hemelum\2-eerste-antifoon\`). Zet `false` als je zelf de
inhoudsopgave van dat hoofdstuk schrijft (zoals de root van de liturgiemap).
Gebruik in sectie-`_index.md` geen `#`-titel in de body; die titel komt uit
de layout.

**Slot-pagina** (`index.md`): gewone markdown. Daartussen kun je één of
meer shortcodes `bieb` zetten. Elke shortcode zet eerst de knoppen
**Oefenen** / **Downloaden** / **Printen** voor die uitvoeringsvorm, en
daarna de PDF of VSA-SVG. De partituur blijft in de bibliotheek; de
slot-pagina is alleen de view. Navigatie naar Bibliotheek of Koormap loopt
via de sticky broodkruimelregel bovenaan de pagina.

### Boom of compositieblad?

Twee manieren om meerdere uitvoeringsvormen op **één liturgische plek** te
tonen —zelfde mechaniek, andere leeservaring:

| Patroon | Wanneer | Voorbeeld |
| --- | --- | --- |
| **Boom** | De zanger kiest één variant (of bladert per kind) | Cherubijnenhymne: sectie → 15b, 15c, …; antifoon: weekdagen / zondag |
| **Compositieblad** | Eén pagina bundelt een set (proza + scores) | Prokimens voor de hele week op één `index.md`, met shortcode per weekdag |

Voorbeeld compositieblad (schets):

```markdown
# Prokimen weekdagen (Kiev, Groningen)

## Maandag
{{</* bieb id="9-prokimen/9a-maandag/groningen" */>}}

## Dinsdag
{{</* bieb id="9-prokimen/9a-dinsdag/groningen" */>}}
```

**Let op:** elke `bieb` op dezelfde pagina heeft een **eigen** knoppenrij
direct boven de partituur van die uitvoeringsvorm. Je hoeft geen aparte
kindpagina’s te maken alleen om knoppen te scheiden.

### Alias-varianten

Soms is dezelfde uitvoeringsvorm onder meerdere namen bekend (bijvoorbeeld
tropaar `maandag-toon-4` = `heilige-engelen-toon-4`). Dan:

- bestanden (`.vsa`, PDF, …) staan **alleen** bij de canonieke id;
- de alias-leaf heeft frontmatter `alias_van: tropaar/maandag-toon-4/hemelum`
  en een `bieb` naar die canonieke id;
- in de bibliotheek-index van het zangstuk (`tropaar/`, `kondak/`, …) staan
  **beide** varianten apart genoemd.

Dat patroon mag voor elk zangstuk met meerdere namen voor dezelfde
uitvoeringsvorm.

## Soorten koormap (classificatie)

Zelfde mechaniek, andere bedoeling — geen nieuwe id-laag:

| Type | Ordening | Voorbeeld |
| --- | --- | --- |
| Liturgisch | Volgorde in de dienst | Liturgiemap Hemelum |
| Feest / kalender | Orde van die dag of cyclus | Pasen, 15 augustus |
| Collectie | Thematisch | Alle cherubijnen, troparen toon 1–8 |
| Parochiekeuze | Wat *dit* koor deze periode zingt | “Hemelum najaar”, “Zwolle-cherubijn” |

Optioneel later: frontmatter `type:` op de koormap-`_index` (`liturgie`,
`feest`, `collectie`, `parochie`).

## Wat de bibliotheek-root toont

De root van de bibliotheek is **geen** sitemap van alle stubs. Koorleden zien
daar vooral **oefenbare** zangstukken (nette titel, liturgienummer-volgorde).
Voorzien-items en technische registers staan onder
[Speciaal](/praktijk/oefenhoek/bibliotheek/speciaal/) en het
[Id-register](/praktijk/oefenhoek/bibliotheek/id-register/).

## Special pages

Automatisch bijgehouden (bij elke sitebuild):

| Pagina | Inhoud |
| --- | --- |
| [Voorzien](/praktijk/oefenhoek/bibliotheek/speciaal/voorzien/) | Zangstukken zonder oefenbare inhoud |
| [Ongerefereerd](/praktijk/oefenhoek/bibliotheek/speciaal/ongerefereerd/) | In de bibliotheek, nog niet in een koormap |
| [Oefenbaar](/praktijk/oefenhoek/bibliotheek/speciaal/oefenbaar/) | Platte lijst van linkbare uitvoeringsvormen + id |

## Klaar als

Je kunt uitleggen waarom een Zwolle-cherubijn eerst in de bibliotheek hoort;
waarom de Hemelum-liturgiemap géén tweede opslag van PDF’s is; en wanneer je
een **sectie** (boom) kiest versus een **compositieblad** (meerdere
shortcodes op één pagina).

{{< navbuttons "Waar ligt wat|/praktijk/handleiding/start/waar-ligt-wat/" "Woorden|/praktijk/handleiding/start/woorden/" >}}
