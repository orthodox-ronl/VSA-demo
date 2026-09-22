---
title: "capella-mxl-to-mscz"
linkTitle: "capella-mxl-to-mscz"
weight: 150
---

# NAME

`scripts\capella-mxl-to-mscz.cmd` — Capella-`.mxl`-map naar standaard-`.mscz`

# SYNOPSIS

```cmd
scripts\capella-mxl-to-mscz.cmd [bronmap] [doelmap] [--force] [--dry-run] [--limit N]
```

# DESCRIPTION

Kuist Capella/CapToMusic-`.mxl` **recursief** op en zet ze om naar
standaard-layout `.mscz`. Submappen blijven behouden. Combineert opkuisen +
layout in batch.

Zonder paden:

- bron: `C:\Git\orthodox-ronl\ruwe-invoer\capella-backup-mxl`
- doel: `C:\Git\orthodox-ronl\ruwe-invoer\capella-backup-mscz`

Hervatbaar: bestaande `.mscz` die niet ouder zijn dan de bron worden
overgeslagen, tenzij `--force`. Log: `doel\_batch-log.txt`. MuseScore 4 moet
geïnstalleerd zijn en **niet open** staan. Niet in `check` / `build` /
`serve`. Geen PDF of Coria-`.mxl`.

Voor één bestand in de oefenhoek-flow: liever [opkuisen](../opkuisen/) +
[layout](../layout/).

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--force` | Bestaande `.mscz` overschrijven |
| `--dry-run` | Alleen planning tonen |
| `--limit N` | Stop na N conversies |
| `--batch-size` | MuseScore-jobgrootte (default 10) |

# WHEN

Een hele Capella-MXL-input naar standaard-`.mscz`, buiten de oefenhoek-stukken
die je één voor één publiceert.

# SEE ALSO

- [opkuisen](../opkuisen/)
- [layout](../layout/)
