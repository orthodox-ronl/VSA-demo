---
title: ".vsa schrijven en op de pagina"
linkTitle: ".vsa schrijven"
weight: 10
---

# .vsa schrijven en op de pagina

{{< cue >}}
1. Kopieer een bestaand `.vsa` in de buurt (bijvoorbeeld een antifoon in de Oefenhoek).
2. Zet het bestand in de bladermap; bestandsnaam zonder spaties.
3. `vsa validate pad\naar\bestand.vsa`
4. In `index.md`: `:::include svg "bestand.vsa" alt="…":::`
5. `scripts\check.cmd --strict` — de SVG komt vanzelf.
{{< /cue >}}

**Wat je nu doet:** de gezongen tekst in VSA-notatie zetten en op de
bladermap tonen. Nog geen vierstemmig blad — daarvoor is de
[volgende pagina](../2-template-satb/), alleen voor tropaar toon 4.

**Wanneer:** je hebt tekst (en een bekende melodie) in plaats van een
Capella-partituur. Voorbeeld in de Oefenhoek: eerste antifoon weekdagen
Hemelum.

## Stap voor stap

1. Maak of kies de bladermap ([publiceren](../../publiceren/1-bladermap/)).
2. Open een **bestaand** `.vsa` dat op het nieuwe stuk lijkt. Verzin de
   tekens niet vanaf nul. Antifoon-voorbeeld:

`content-source\praktijk\oefenhoek\liturgiemap-hemelum\2-eerste-antifoon\weekdagen\hemelum\2-eerste-antifoon-weekdagen-hemelum.vsa`

3. Kopieer dat bestand, hernoem naar het doel-id (geen spaties), plak jouw
   tekst in dezelfde notatie. Een `.vsa` is **geen** Markdown-pagina: zet
   geen `#`-koppen in de notatie zelf. Optioneel wel YAML bovenaan tussen
   `---` (titel, `do`, `mode`, …).
4. In het Windows-opdrachtvenster:

```cmd
vsa validate content-source\praktijk\oefenhoek\liturgiemap-hemelum\2-eerste-antifoon\weekdagen\hemelum\2-eerste-antifoon-weekdagen-hemelum.vsa
```

   Foutmelding: de markering zit in de **gezongen tekst**, niet in het
   programma. Verbeter de notatie. “Even stil krijgen” door tekens weg te
   halen is geen oplossing.

5. In `index.md` van dezelfde bladermap (pad relatief t.o.v. die
   `index.md`):

```markdown
:::include svg "2-eerste-antifoon-weekdagen-hemelum.vsa" alt="Eerste antifoon, weekdagen (Hemelum)":::
```

6. Nog geen Coria of PDF? Laat de Coria- en PDF-regels in `index.md` als
   commentaar staan tot die bestanden er zijn. Zie
   [bladermap](../../publiceren/1-bladermap/).

Uitleg van de VSA-tekens (`{/`, `{_`, `*`, …): de pagina’s onder
[Tooling Demo](../../../demo/), niet deze handleiding. Hier gaat het over
*waar* het `.vsa`-bestand hoort en hoe het op de Oefenhoek komt.

## Klaar als

`vsa validate` is stil, de include staat in `index.md`, en na `check` zie
je het plaatje op de lokale preview.

{{< navbuttons "Volgende: template SATB|/praktijk/handleiding/vsa/2-template-satb/" >}}
