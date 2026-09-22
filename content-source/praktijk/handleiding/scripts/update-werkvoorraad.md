---
title: "update-werkvoorraad"
linkTitle: "update-werkvoorraad"
weight: 130
---

# NAME

`scripts\update-werkvoorraad.cmd` — werkvoorraad-tabel bijwerken

# SYNOPSIS

```cmd
scripts\update-werkvoorraad.cmd
```

# DESCRIPTION

Vult de tabel in
`content-source\praktijk\oefenhoek\input\werkvoorraad.md` uit bestanden die
op schijf in `input\` liggen. Doel-id, koormap en notitie in **bestaande**
rijen blijven staan; nieuwe bestanden krijgen een rij.

Verwijdert ook `generated\content\...\oefenhoek\input`, zodat inputs geen
Hugo-pagina’s worden.

# WHEN

Automatisch in `check` / `build` / `serve`. Handmatig na nieuwe bestanden in
`input\` (Capella, VOW, …), zonder een volle check te willen draaien.

# SEE ALSO

- [check](../check/)
- Workflow: [Binnenhalen](../../partituur/1-binnenhalen/)
