---
title: "update-werkvoorraad"
linkTitle: "update-werkvoorraad"
weight: 130
---

# NAME

`scripts\update-werkvoorraad.cmd` — tabel «werkvoorraad» laten aansluiten op `input\`

# SYNOPSIS

```cmd
scripts\update-werkvoorraad.cmd
```

# DESCRIPTION

Werkvoorraad is het register van ruwe bestanden onder
`content-source\praktijk\oefenhoek\input\` (nog niet gepubliceerd). Dit
commando vult de tabel in het bestand `werkvoorraad.md` in die map aan de
hand van wat er op schijf ligt. Doel-id, koormap en notitie in **bestaande**
rijen blijven staan; nieuwe bestanden krijgen een nieuwe rij.

Het verwijdert ook `generated\content\...\oefenhoek\input`, zodat die
inputs geen Hugo-pagina’s op de site worden.

# WHEN

Automatisch in `check` / `build` / `serve`. Handmatig nadat je nieuwe
bestanden in `input\` hebt gezet en niet meteen een volle `check` wilt
draaien.

# SEE ALSO

- [check](../check/)
- Workflow: [Binnenhalen](/praktijk/handleiding/partituur/1-binnenhalen/)
