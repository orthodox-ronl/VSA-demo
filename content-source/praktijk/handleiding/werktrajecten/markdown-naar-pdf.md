---
title: "Markdown naar PDF"
linkTitle: "Markdown naar PDF"
weight: 60
---

# Markdown naar PDF

Dit werktraject maakt van één Markdownbestand (tekst, VSA-blokken,
includes, paginascheidingen) een **A4-PDF**. Het is geen vervanging van
bibliotheek-PDF’s uit MuseScore.

{{< cue >}}
Willekeurig blad:
```cmd
scripts\pdf.cmd pad\naar\blad.md -o pad\naar\uit.pdf --content-root content-source
```
Vaste demo (Tooling Demo «Markdown naar PDF»):
```cmd
scripts\demo-pdf.cmd
```
{{< /cue >}}

## Waartoe

Je wilt een printbaar blad (bijvoorbeeld een demo of een liturgisch
leesblad) dat markdown en `::: vsa-notatie` combineert, zonder een
basispartituur-`.mscz`.

## Eindresultaat en criteria

| Bron (voorbeeld) | Product |
| --- | --- |
| `content-source\praktijk\demo\assets\voorbeeld-blad.md` | `static\demo\voorbeeld-blad.pdf` |

**Klaar** (demo) als: de PDF niet ouder is dan
`voorbeeld-blad.md` en eventuele includes (zoals `voorbeeld.vsa`);
`check_demo_pdf_fresh` onder `check` is groen. Op de demopagina staat een
PDF-voorbeeldviewer.

Kenmerken van de export: `:::pagebreak:::` start een nieuw A4-blad;
`:::print-only:::` … `:::end-print-only:::` verschijnt in de PDF, niet
op de website; ruwe HTML in het markdownblad mag mee (Chrome/Edge
rendert de tussen-HTML).

## Wanneer wel / wanneer niet

| Wel | Niet |
| --- | --- |
| Demo- of los blad met VSA in markdown | Bibliotheek-basispartituur → [Basispartituur](../basispartituur/) |
| A4-PDF uit markdown nodig | Alleen schermweergave op de site (dan volstaat Hugo) |

## Volgorde (bestanden)

1. Schrijf of bewerk het markdownblad (bij de demo:
   `content-source\praktijk\demo\assets\voorbeeld-blad.md`, met
   `build: render: never` zodat Hugo het blad niet als pagina
   publiceert).
2. Bouw de PDF:

```cmd
scripts\demo-pdf.cmd
```

   of generiek:

```cmd
scripts\pdf.cmd content-source\praktijk\demo\assets\voorbeeld-blad.md -o static\demo\voorbeeld-blad.pdf --content-root content-source
```

3. Hard refresh in de browser als een oude PDF gecached blijft.
4. Commit bron én PDF samen als de demo-gate groen moet blijven.

Site-demo-uitleg: [Markdown naar PDF (Tooling Demo)](/praktijk/demo/06-markdown-naar-pdf/).

## Automatisch (CI)

CI en lokale `check` / `build` / `serve` **genereren geen** willekeurige
markdown-PDF’s. Wel faalt `check_demo_pdf_fresh.py` als
`static\demo\voorbeeld-blad.pdf` ontbreekt of ouder is dan de bronnen.
Herstel: `scripts\demo-pdf.cmd`, daarna opnieuw committen.

## Handmatig

| Situatie | Commando | Man-page |
| --- | --- | --- |
| Willekeurig blad | `scripts\pdf.cmd` `<bestand.md>` `-o` … | [pdf](../../scripts/pdf/) |
| Demo-PDF | `scripts\demo-pdf.cmd` | [demo-pdf](../../scripts/demo-pdf/) |

Vereist: Edge of Chrome (of `CHROME_PATH` / `--chrome`); zelfde
validatiefouten als `vsa validate` bij kapotte VSA-blokken.

## Zie ook

- [Site-build](../site-build/) (waar de demo-PDF-gate in de keten zit)
- [Ingebedde VSA](../ingebedde-vsa/) (SVG op de site, geen A4-PDF)

{{< navbuttons "Site-build|/praktijk/handleiding/werktrajecten/site-build/" "Ingebedde VSA|/praktijk/handleiding/werktrajecten/ingebedde-vsa/" >}}
