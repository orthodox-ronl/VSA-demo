---
title: ".vsa schrijven en op de pagina"
linkTitle: ".vsa schrijven"
weight: 10
---

# .vsa schrijven en op de pagina

{{< cue >}}
1. Kopieer een bestaand `.vsa` in de bibliotheek (bijvoorbeeld eerste antifoon weekdagen Hemelum).
2. Zet het bestand in de bibliotheek-map; bestandsnaam zonder spaties (publicatiestam).
3. `vsa validate pad\naar\bestand.vsa`
4. Bibliotheek-`index.md` + koormap-slot: shortcode `bibliotheek-score` met de bibliotheek-id
5. `scripts\check.cmd --strict` — de SVG komt vanzelf.
{{< /cue >}}

**Wat je nu doet:** de gezongen tekst in VSA-notatie zetten en via het
bibliotheek op de site tonen. Nog geen vierstemmig blad — daarvoor is de
[volgende pagina](../2-template-satb/), alleen voor tropaar toon 4.

**Wanneer:** je hebt tekst (en een bekende melodie) in plaats van een
Capella-partituur. Voorbeeld:
`2-eerste-antifoon/weekdagen-hemelum/hemelum`.

## Stap voor stap

1. Maak of kies de bibliotheek-map ([publiceren](../../publiceren/1-bladermap/)).
2. Open een **bestaand** `.vsa` dat op het nieuwe stuk lijkt. Verzin de
   tekens niet vanaf nul. Antifoon-voorbeeld:

`content-source\praktijk\oefenhoek\bibliotheek\2-eerste-antifoon\weekdagen-hemelum\hemelum\2-eerste-antifoon-weekdagen-hemelum-hemelum.vsa`

3. Kopieer dat bestand naar jouw bibliotheek-map, hernoem naar de
   publicatiestam (geen spaties), plak jouw tekst in dezelfde notatie. Een
   `.vsa` is **geen** Markdown-pagina: zet geen `#`-koppen in de notatie
   zelf. Optioneel wel YAML bovenaan tussen `---` (titel, `do`, `mode`, …).
4. In het Windows-opdrachtvenster:

```cmd
vsa validate content-source\praktijk\oefenhoek\bibliotheek\2-eerste-antifoon\weekdagen-hemelum\hemelum\2-eerste-antifoon-weekdagen-hemelum-hemelum.vsa
```

   Foutmelding: de markering zit in de **gezongen tekst**, niet in het
   programma. Verbeter de notatie. “Even stil krijgen” door tekens weg te
   halen is geen oplossing.

5. In bibliotheek-`index.md` (kopieer een bestaand voorbeeld):

```markdown
---
title: "…"
publicatiestatus: reviewable
automatische_inhoud: false
---

# …

{{</* bibliotheek-score id="2-eerste-antifoon/weekdagen-hemelum/hemelum" */>}}
```

6. Hetzelfde id in het **koormap-slot** (bijv.
   `liturgiemap-hemelum\2-eerste-antifoon\weekdagen\hemelum\index.md`).

Catalogus-kondaken blijven `:::include` uit de catalogus — geen
`bibliotheek-score`. Zie [Bibliotheek en koormap](../../publiceren/1-bladermap/).

Uitleg van de VSA-tekens (`{/`, `{_`, `*`, …): de pagina’s onder
[Tooling Demo](../../../demo/), niet deze handleiding. Hier gaat het over
*waar* het `.vsa`-bestand hoort en hoe het op de Oefenhoek komt.

## Klaar als

`vsa validate` is stil, bibliotheek en koormap verwijzen met hetzelfde id,
en na `check` zie je het plaatje op de lokale preview.

{{< navbuttons "Volgende: template SATB|/praktijk/handleiding/vsa/2-template-satb/" >}}
