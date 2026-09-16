---
title: "Bibliotheek en koormappen"
linkTitle: "Bibliotheek en koormappen"
weight: 25
---

# Bibliotheek en koormappen

{{< cue >}}
- **Bibliotheek** = alles wat jullie *hebben* (uitvoeringsvorm + id + partituur)
- **Koormap** = geordende *verwijzingen* voor één gelegenheid of thema
- Een uitvoeringsvorm mag in de bibliotheek staan **zonder** koormap
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
`bibliotheek-score` naar `zangstuk/variant/uitvoeringsvorm`.

Een uitvoeringsvorm mag publiek in de bibliotheek staan terwijl **geen
enkele** koormap ernaar wijst. Dat is bewust: ontdekking en latere opname in
een map (feest, collectie, parochiekeuze) komen daarna.

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

Je kunt uitleggen waarom een Zwolle-cherubijn eerst in de bibliotheek hoort,
en waarom de Hemelum-liturgiemap géén tweede opslag van PDF’s is.

{{< navbuttons "Waar ligt wat|/praktijk/handleiding/start/waar-ligt-wat/" "Woorden|/praktijk/handleiding/start/woorden/" >}}
