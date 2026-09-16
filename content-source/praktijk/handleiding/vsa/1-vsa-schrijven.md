---
title: ".vsa schrijven en op de pagina"
linkTitle: ".vsa schrijven"
weight: 10
---

# .vsa schrijven en op de pagina

{{< cue >}}
1. Kopieer een bestaand `.vsa` in de bibliotheek (bijvoorbeeld eerste antifoon weekdagen Hemelum).
2. Zet het bestand in de bibliotheek-map; bestandsnaam zonder spaties (publicatiestam).
3. Zet bovenaan YAML met minstens `do`, `mode` en `tempo: 120`.
4. `vsa validate pad\naar\bestand.vsa`
5. Bibliotheek-`index.md` + koormap-slot: shortcode `bibliotheek-score` met de bibliotheek-id
6. `scripts\check.cmd --strict` — SVG én Coria-`.vsa.mxl`; commit `.vsa` + `.vsa.mxl` samen
{{< /cue >}}

**Wat je nu doet:** de gezongen tekst in VSA-notatie zetten en via het
bibliotheek op de site tonen, inclusief oefenen in Coria. Nog geen
vierstemmig blad — daarvoor is de [volgende pagina](../2-template-satb/),
alleen voor tropaar toon 4.

**Wanneer:** je hebt tekst (en een bekende melodie) in plaats van een
Capella-partituur. Voorbeeld-bibliotheek-id:
`2-eerste-antifoon/weekdagen-hemelum/hemelum`.

## Stap voor stap

1. Maak of kies de bibliotheek-map ([publiceren](../../publiceren/1-bladermap/)).
2. Open een **bestaand** `.vsa` dat op het nieuwe stuk lijkt. Verzin de
   tekens niet vanaf nul. Antifoon-voorbeeld:

`content-source\praktijk\oefenhoek\bibliotheek\2-eerste-antifoon\weekdagen-hemelum\hemelum\2-eerste-antifoon-weekdagen-hemelum-hemelum.vsa`

3. Kopieer dat bestand naar jouw bibliotheek-map, hernoem naar de
   publicatiestam (geen spaties), plak jouw tekst in dezelfde notatie. Een
   `.vsa` is **geen** Markdown-pagina: zet geen `#`-koppen in de notatie
   zelf. Zet wél YAML bovenaan tussen `---` met minstens `do`, `mode` en
   `tempo` (default in de toolchain is **120** BPM):

```yaml
---
do: F4
mode: major
tempo: 120
---
```

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

7. Draai `scripts\check.cmd --strict`. De pipeline maakt of vernieuwt
   `{stam}.vsa.mxl` naast de `.vsa` (commando ook los:
   `scripts\vsa-products.cmd`). Commit **`.vsa` en `.vsa.mxl` samen**.
   Op de preview verschijnt de knop **Oefenen**.

Catalogus-kondaken blijven `:::include` uit de catalogus — geen
`bibliotheek-score`. Zie [Bibliotheek en koormap](../../publiceren/1-bladermap/).

Uitleg van de VSA-tekens (`{/`, `{_`, `*`, …): de pagina’s onder
[Tooling Demo](../../../demo/), niet deze handleiding. Hier gaat het over
waar het `.vsa`-bestand hoort en hoe het op de Oefenhoek komt.

### Handmatige artefacten

Zet je op de bibliotheek-`index.md` `artefacten_handmatig: true`, dan
vernieuwt `vsa-products` de Coria-`.mxl` **niet**. Dat hoort bij print-velden
of template-exports die jij zelf bijhoudt — zie
[Print-.mscz](../../partituur/7-print-mscz/) en de gele banner op die
bibliotheekpagina. Afspraak over namen en sporen:
`scripts\oefenhoek-product-contract.md` in `VSA-demo`.

### Banner of check over `.vsa.mxl`

Rode banner “VSA-afgeleiden niet in orde”, of `check` rood op `main`: de
`.vsa.mxl` ontbreekt, is ouder dan de `.vsa`, of mist de provenance-stamp.
Oplossing: `scripts\vsa-products.cmd`, daarna opnieuw `check`, en beide
bestanden committen. Zie ook [Als het misgaat](../../publiceren/3-als-het-misgaat/).

## Klaar als

`vsa validate` is stil, bibliotheek en koormap verwijzen met hetzelfde id,
na `check` zie je het plaatje op de lokale preview, en er ligt een verse
`{stam}.vsa.mxl` naast de `.vsa` (knop **Oefenen**), tenzij
`artefacten_handmatig: true` op die bibliotheekpagina staat.

{{< navbuttons "Volgende: template SATB|/praktijk/handleiding/vsa/2-template-satb/" >}}
