---
title: "Wat heb je nodig"
linkTitle: "Wat heb je nodig"
weight: 10
---

# Wat heb je nodig

{{< cue >}}
1. Installeer MuseScore **4** (niet MuseScore 3).
2. Zorg dat de mappen `bron`, `VSA-tooling` en `VSA-demo` naast elkaar staan onder `C:\Git\orthodox-ronl\`.
3. Open Verkenner, ga naar `C:\Git\orthodox-ronl\VSA-demo`, typ `cmd` in de adresbalk, druk Enter.
4. Eerste keer: `scripts\check.cmd` (wacht tot het klaar is).
5. Lokale preview: `scripts\serve.cmd --no-build` en open http://127.0.0.1:18731/ in de browser.
{{< /cue >}}

**Wat je nu doet:** je pc zo inrichten dat de rest van deze handleiding
neerkomt op copy-paste, zonder zoeken naar paden.

## Programma’s

| Programma | Waarvoor |
| --- | --- |
| [MuseScore 4](https://musescore.org/) | Partituren openen, nakijken, opslaan als `.mscz` |
| De repository-map `VSA-demo` op je schijf | Bestanden zetten en de commando’s uit deze handleiding draaien |
| Een browser | De Oefenhoek lokaal bekijken (preview) |
| Optioneel: Cursor of Kladblok | Bestanden `.md` en `.vsa` bewerken |

Je schrijft geen Python-programma’s. Je plakt kant-en-klare regels in het
Windows-opdrachtvenster. MuseScore bedien je met de muis, zoals een
tekstverwerker voor noten.

## De drie mappen op schijf

Deze website in de browser toont alleen het resultaat. Het beheerwerk
gebeurt in de **repository-map** `VSA-demo` die je met git op je pc hebt
staan. Die map hoort naast twee sibling-mappen te staan:

```text
C:\Git\orthodox-ronl\
  bron\
  VSA-tooling\
  VSA-demo\          <-- hier werk je bijna altijd
```

Ontbreekt een van die drie mappen: vraag iemand die de git-checkouts al
heeft. Verplaats of hernoem de mappen niet zelf; dan breekt de keten.

## Het Windows-opdrachtvenster (eenmaal openen)

1. Open Verkenner.
2. Ga naar `C:\Git\orthodox-ronl\VSA-demo`.
3. Klik in de adresbalk, typ `cmd`, druk Enter.
4. Er opent een venster met een prompt. Alle commando’s in deze
   handleiding plak je in **dat** venster, tenzij de tekst expliciet zegt
   dat je in `VSA-tooling` moet werken.

Plakken: rechtsklik, of Ctrl+V. Druk Enter om te starten. Wacht tot de
prompt terugkomt. Rode tekst of het woord `FAILED` →
[Als het misgaat](../../publiceren/3-als-het-misgaat/).

## Eerste keer (of na een tool-update)

```cmd
scripts\check.cmd
```

Het programma mag een paar minuten duren. Het zet ontbrekende onderdelen
klaar. Daarna, als je de site wilt zien zonder alles opnieuw te bouwen:

```cmd
scripts\serve.cmd --no-build
```

Open in de browser **http://127.0.0.1:18731/**. Gebruik niet poort 1313;
die poort is lokaal voor iets anders gereserveerd.

Laat het venster van `serve` open zolang je kijkt. Klaar met kijken:
Ctrl+C in dat venster, of sluit het venster.

## Klaar als

- MuseScore 4 start vanaf het Start-menu.
- `scripts\check.cmd` eindigt zonder fout.
- De preview op poort **18731** toont de site, inclusief de knop
  **Handleiding** in de balk.

{{< navbuttons "Volgende: waar ligt wat|/praktijk/handleiding/start/waar-ligt-wat/" >}}
