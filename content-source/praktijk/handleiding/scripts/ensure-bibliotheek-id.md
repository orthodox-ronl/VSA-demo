---
title: "ensure-bibliotheek-id"
linkTitle: "ensure-bibliotheek-id"
weight: 120
---

# NAME

`scripts\ensure-bibliotheek-id.cmd` — bibliotheek-id in basispartituur colofon/meta

# SYNOPSIS

```cmd
scripts\ensure-bibliotheek-id.cmd [root] [--check-only] [--fail]
```

# DESCRIPTION

Basispartituur-`.mscz` onder `oefenhoek\bibliotheek\` moeten de regel
`Bibliotheek-id:` in het colofon én meta `vsaBibliotheekId` hebben, gelijk aan
het pad `zangstuk/variant/uitvoeringsvorm`.

Lokaal herstelt dit commando ontbrekende of verkeerde id’s (via
`process_mscz`, zonder MuseScore). Met `--check-only` (of in CI) alleen
rapporteren. Op `main` / strict-pipeline: falen als er nog problemen zijn.

Zonder `root`: `content-source\praktijk\oefenhoek\bibliotheek`. Daarna
[mscz-products](../mscz-products/) voor verse PDF’s.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `root` | Zoekroot (default: bibliotheek) |
| `--check-only` | Alleen controleren, niet schrijven |
| `--fail` | Exit 1 bij problemen (ook buiten strict) |

# WHEN

Na [layout](../layout/) of verplaatsing in de bibliotheek, of als `check` een
id-mismatch meldt.

# SEE ALSO

- [layout](../layout/)
- [mscz-products](../mscz-products/)
- `scripts\mscz-partituur-contract.md`
