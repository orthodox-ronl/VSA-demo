---
title: "Opnemen in de bibliotheek"
linkTitle: "Opnemen in de bibliotheek"
weight: 5
---

# Opnemen in de bibliotheek

{{< cue >}}
1. Ken het **bibliotheek-id** (drie delen met schuine strepen), of vraag het na.
2. Zorg dat je bestand al een bruikbare **hub-`.mscz`**, **`.vsa`**, of
   **`.print.mscz`** is — niet een ruwe Capella-file.
3. Open het Windows-opdrachtvenster in de map `VSA-demo`.
4. Plak een regel zoals hieronder (pas id en pad aan) en druk Enter.
5. Controleer daarna met `scripts\check.cmd --strict`.
{{< /cue >}}

**Wat je nu doet:** een klaar oefenbestand **opnemen** in de catalogus
(de **bibliotheek**), zodat de Oefenhoek het kan tonen. Het script maakt de
mappen en de pagina-bestanden voor je; jij hoeft die niet met de hand te
typen.

**Wanneer:** als de partituur inhoudelijk klaar genoeg is (na opkuisen en
normaliseren bij MuseScore, of na een werkende `.vsa`). Nog niet klaar?
Laat het bestand in `input\` staan; zie [binnenhalen](../../partituur/1-binnenhalen/).

**Bibliotheek-id** = drie namen, gescheiden door `/`, bijvoorbeeld
`5-eniggeboren-zoon/default/hemelum`. Elke naam mag alleen kleine letters,
cijfers, `-` en `_` bevatten. Lijst:
[Id-register](/praktijk/oefenhoek/bibliotheek/id-register/). Ken je het id
niet? **Niet verzinnen** — vraag na.

## Wat het script voor je doet

Het commando `scripts\bieb-accepteer.cmd` (kort: **bieb-accepteer**):

- maakt de mappen
  `content-source\praktijk\oefenhoek\bibliotheek\<zangstuk>\<variant>\<uitvoeringsvorm>\`
  als die nog ontbreken;
- zet daar een `index.md` met de knoppen via shortcode `bieb`;
- kopieert je bestand en geeft het de **publicatiestam** als naam (zonder
  spaties), afgeleid van het id;
- weigert bestanden die niet in de bibliotheek horen (bijvoorbeeld Capella
  `.capx`, of alleen een ruwe `.mxl` zonder hub of VSA);
- controleert een `.vsa` met `vsa validate` voordat die wordt opgenomen.

Het script doet **niet** de muzikale opkuis in MuseScore en maakt **niet**
automatisch PDF/Coria — dat blijft [PDF en Coria](../../partituur/5-pdf-en-coria/)
of [VSA](../../vsa/).

## Stap voor stap

1. Open het Windows-opdrachtvenster in `VSA-demo`
   ([hoe](../../start/wat-heb-je-nodig/)).
2. Kies eerst een **droge proef** (niets wordt weggeschreven), zodat je ziet
   wat er zou gebeuren. Vervang het voorbeeld-id en het pad door jouw
   gegevens:

```cmd
scripts\bieb-accepteer.cmd 5-eniggeboren-zoon/default/hemelum "C:\pad\naar\mijn-bestand.mscz" --dry-run
```

3. Klopt de uitvoer? Draai dezelfde regel **zonder** `--dry-run`:

```cmd
scripts\bieb-accepteer.cmd 5-eniggeboren-zoon/default/hemelum "C:\pad\naar\mijn-bestand.mscz"
```

4. Voor een **VSA**-bestand hetzelfde patroon, met `.vsa` in plaats van
   `.mscz`. Voor een **print-vel**: bestandsnaam eindigend op `.print.mscz`
   (het script zet dan ook `artefacten_handmatig` aan).
5. Optioneel: geef een leesbare titel mee:

```cmd
scripts\bieb-accepteer.cmd 5-eniggeboren-zoon/default/hemelum "C:\pad\naar\bestand.mscz" --title "5 Eniggeboren Zoon"
```

6. Draai de controle:

```cmd
scripts\check.cmd --strict
```

7. Hoort het stuk in de liturgiemap (koormap)? Zet of controleer daar een
   slot-pagina met `bieb` — zie
   [Bibliotheek en koormap](../1-bladermap/). De partituur blijft in de
   bibliotheek; de koormap is alleen de route voor koorleden.

## Welke bestanden mag je aanleveren?

| Bestand | Mag met bieb-accepteer? | Opmerking |
| --- | --- | --- |
| Hub-`.mscz` (MuseScore, genormaliseerd) | Ja | Daarna vaak nog PDF/Coria maken |
| `.vsa` | Ja | Script runt `vsa validate` |
| `naam.print.mscz` | Ja | Print-vel; PDF meestal handmatig |
| `.pdf` of `.mxl` **naast** hub of VSA | Ja | Meenemen in dezelfde opdracht |
| Alleen een `.mxl` (Capella/ CapToMusic) | Nee | Eerst [opkuisen](../../partituur/2-opkuisen/) |
| `.cap` / `.capx` / `.musicxml` | Nee | Eerst omzetten via de partituurstraat |

## Lege plek reserveren (stub)

Wil je het id en de pagina alvast, maar nog geen partituur?

```cmd
scripts\bieb-accepteer.cmd 1-vredeslitanie/default/hemelum --stub
```

Dan wordt `publicatiestatus` standaard `voorzien`.

## Als het misgaat

| Melding (kort) | Wat je doet |
| --- | --- |
| ongeldig bibliotheek-id | Id nakijken in het [Id-register](/praktijk/oefenhoek/bibliotheek/id-register/); drie lagen, kleine letters |
| doel bestaat al | Bewust overschrijven: zelfde opdracht met `--force`, of ander id |
| vsa validate faalde | `.vsa` eerst herstellen; pas daarna opnieuw accepteren |
| formaat weigert / alleen .mxl | Terug naar [partituur](../../partituur/); niet forceren in de bibliotheek |
| alias-variant | Partituur hoort bij de canonieke variant; zie [Bibliotheek en koormappen](../../start/bibliotheek-en-koormappen/) |

Meer storingen: [Als het misgaat](../3-als-het-misgaat/).

## Klaar als

- Onder `bibliotheek\<zangstuk>\<variant>\<uitvoeringsvorm>\` staat je
  bestand met de publicatiestam-naam.
- Er staat een `index.md` met shortcode `bieb` en hetzelfde id.
- `scripts\check.cmd --strict` eindigt zonder fout.
- (Optioneel) De koormap-slotpagina verwijst naar hetzelfde id.

{{< navbuttons "Volgende: bibliotheek en koormap|/praktijk/handleiding/publiceren/1-bladermap/" >}}
