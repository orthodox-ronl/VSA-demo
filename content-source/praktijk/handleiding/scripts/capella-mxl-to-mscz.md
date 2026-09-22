---
title: "capella-mxl-to-mscz"
linkTitle: "capella-mxl-to-mscz"
weight: 150
---

# NAME

`scripts\capella-mxl-to-mscz.cmd` — hele map Capella-`.mxl` omzetten naar standaard-`.mscz`

# SYNOPSIS

```cmd
scripts\capella-mxl-to-mscz.cmd [bronmap] [doelmap] [--force] [--dry-run] [--limit N]
```

# DESCRIPTION

Kuist Capella- of CapToMusic-`.mxl`-bestanden **recursief** op en zet ze om
naar standaard-layout `.mscz` (opkuisen + layout in één batch). Submappen
blijven behouden.

Zonder paden gebruikt het script deze defaults buiten de oefenhoek:

- bron: `C:\Git\orthodox-ronl\ruwe-invoer\capella-backup-mxl`
- doel: `C:\Git\orthodox-ronl\ruwe-invoer\capella-backup-mscz`

Het is hervatbaar: bestaande `.mscz` die niet ouder zijn dan de bron worden
overgeslagen, tenzij `--force`. Logbestand: `doel\_batch-log.txt`. MuseScore
4 moet geïnstalleerd zijn en **niet open** staan tijdens de run. Geen PDF
en geen Coria-`.mxl`. Niet in `check` / `build` / `serve`.

Voor **één** stuk in de oefenhoek-publicatiestroom: liever
[opkuisen](../opkuisen/) en daarna [layout](../layout/).

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `--force` | Bestaande `.mscz` overschrijven |
| `--dry-run` | Alleen planning tonen |
| `--limit N` | Stop na N conversies |
| `--batch-size` | MuseScore-jobgrootte (default 10) |

# WHEN

Je hebt een hele Capella-MXL-backup die je in bulk naar standaard-`.mscz`
wilt, buiten de stukken die je één voor één publiceert.

# SEE ALSO

- [opkuisen](../opkuisen/)
- [layout](../layout/)
