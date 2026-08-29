---
title: "VSA naar MusicXML (MXL)"
linkTitle: "VSA naar MusicXML"
weight: 40
aliases:
  - /praktijk/demo/02-vsa-naar-mxl/
---

# VSA naar MusicXML (MXL)

**Wat je hier leert:** een `.vsa`-bestand omzetten naar MusicXML (`.mxl`) —
voor download, MuseScore of handmatig importeren in Coria.

## CLI

Werkmap = deze demo-map:

```cmd
vsa musicxml assets\voorbeeld.vsa assets\voorbeeld.mxl
```

Of vanaf de repo-root:

```cmd
vsa musicxml content-source\praktijk\demo\assets\voorbeeld.vsa content-source\praktijk\demo\assets\voorbeeld.mxl
```

## Op de site (downloadknop)

Zelfde bronbestand, via include (pad relatief t.o.v. deze pagina):

```markdown
:::include mxl "assets/voorbeeld.vsa" label="voorbeeld.mxl — download MusicXML":::
```

:::include mxl "assets/voorbeeld.vsa" label="voorbeeld.mxl — download MusicXML":::

Generate: `scripts\check.cmd --skip-hugo` (zet `.mxl` onder `static\vsa\mxl\…`).

## MusicXML in Coria laden

1. Open Coria (web of lokaal).
2. Nieuw project of bestaande oefening.
3. Importeer het `.mxl`-bestand.
4. Speel af of oefen.

Kant-en-klare oefenknop zonder handmatig importeren:
[Oefenen met Coria](../05-coria-oefenen/).
