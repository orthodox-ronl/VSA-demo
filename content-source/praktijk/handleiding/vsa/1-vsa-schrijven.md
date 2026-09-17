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
5. Bibliotheek-`index.md` + slot-pagina (of compositieblad): shortcode `bieb` met de bibliotheek-id
6. `scripts\check.cmd --strict` — maakt SVG (plaatje) én Coria-`.vsa.mxl`; commit `.vsa` + `.vsa.mxl` samen
{{< /cue >}}

**Wat je nu doet:** de gezongen tekst in VSA-notatie zetten en via het
bibliotheek op de site tonen, inclusief oefenen in Coria. Nog geen
vierstemmig blad — daarvoor is de [volgende pagina](../2-template-satb/),
alleen voor tropaar toon 4.

**Wanneer:** je hebt tekst (en een bekende melodie) in plaats van een
Capella-partituur. Voorbeeld-bibliotheek-id:
`2-eerste-antifoon/weekdagen-hemelum/hemelum`.

## Wat de site van je `.vsa` maakt

Op een gewone eenstemmige bibliotheek-pagina (geen hub-`.mscz` ernaast)
doet de build twee aparte dingen met hetzelfde `.vsa`-bestand:

| Afgeleide | Rol op de pagina | Hoe maak je die |
| --- | --- | --- |
| SVG onder `static\vsa\bladermap\…` | Het **plaatje** dat shortcode `bieb` toont | Pipeline-stap `python scripts\sync_oefenhoek_index.py --svg` (zit in `check` / `build` / `serve` **zonder** `--no-build`) |
| `{stam}.vsa.mxl` naast de `.vsa` | Knop **Oefenen** (Coria) | `scripts\vsa-products.cmd` (of dezelfde `check`-keten) |

`*.print.mscz` in dezelfde map blokkeert de SVG **niet** (dat is een
printvel, geen hub). Een hub-`.mscz` wél: dan toont de pagina de PDF uit
de hub-straat, geen VSA-SVG.

Los alleen SVG vernieuwen (na `vsa build-markdown`, of als `static\vsa`
al bestaat):

```cmd
python scripts\sync_oefenhoek_index.py --svg
```

`serve --no-build` slaat generate + `--svg` over. Zie je Hugo-waarschuwing
“SVG ontbreekt”, draai dan eerst die regel of een volle `check` / `serve`
zonder `--no-build`.

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

{{</* bieb id="2-eerste-antifoon/weekdagen-hemelum/hemelum" */>}}
```

6. Hetzelfde id in de **slot-pagina** van de koormap (bijv.
   `liturgiemap-hemelum\2-eerste-antifoon\weekdagen\index.md`). Meerdere
   VSA’s op één liturgische plek? Sectie met kindpagina’s, of één
   compositieblad — zie
   [Bibliotheek en koormappen](../../start/bibliotheek-en-koormappen/).

7. Draai `scripts\check.cmd --strict`. Die keten:
   - schrijft de SVG voor het plaatje (`sync_oefenhoek_index.py --svg`);
   - maakt of vernieuwt `{stam}.vsa.mxl` naast de `.vsa`
     (`scripts\vsa-products.cmd` doet dat ook los).

   Commit **`.vsa` en `.vsa.mxl` samen**. De SVG onder `static\vsa\` hoort
   bij de build-output (niet handmatig committen). Op de preview verschijnt
   het plaatje én de knop **Oefenen**.

Catalogus-includes horen **niet** in de oefenhoek (geen verwijzing naar
`content-source/lokaal/`). Kondaken en troparen: bibliotheek-leaf + `bieb`.
Zie [Bibliotheek en koormap](../../publiceren/1-bladermap/).

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

Ligt er wél een `.vsa` naast een `{stam}.print.mscz`, dan mag de build
nog steeds de **SVG** van die `.vsa` maken (notatie naast de handmatige
PDF). Alleen hub-`.mscz` onderdrukt die SVG-route.

### Banner of check over `.vsa.mxl`

Rode banner “VSA-afgeleiden niet in orde”, of `check` rood op `main`: de
`.vsa.mxl` ontbreekt, is ouder dan de `.vsa`, of mist de provenance-stamp.
Oplossing: `scripts\vsa-products.cmd`, daarna opnieuw `check`, en beide
bestanden committen. Zie ook [Als het misgaat](../../publiceren/3-als-het-misgaat/).

### Hugo-waarschuwing “SVG ontbreekt”

Shortcode `bieb` zoekt
`static\vsa\bladermap\praktijk\oefenhoek\bibliotheek\<…>\<naam>.svg`.
Ontbreekt dat bestand:

```cmd
python scripts\sync_oefenhoek_index.py --svg
```

of `scripts\check.cmd --strict`. Daarna opnieuw previewen. Met
`serve --no-build` gebeurt die SVG-stap niet.

## Klaar als

`vsa validate` is stil, bibliotheek en koormap verwijzen met hetzelfde id,
na `check` zie je het plaatje op de lokale preview, en er ligt een verse
`{stam}.vsa.mxl` naast de `.vsa` (knop **Oefenen**), tenzij
`artefacten_handmatig: true` op die bibliotheekpagina staat (dan houd jij
de Coria-`.mxl` zelf bij; de SVG mag de pipeline nog steeds schrijven).

{{< navbuttons "Volgende: template SATB|/praktijk/handleiding/vsa/2-template-satb/" >}}
