---
title: "ensure-bibliotheek-id"
linkTitle: "ensure-bibliotheek-id"
weight: 120
---

# NAME

`scripts\ensure-bibliotheek-id.cmd` — bibliotheek-id in colofon en metadata zetten

# SYNOPSIS

```cmd
scripts\ensure-bibliotheek-id.cmd [root] [--check-only] [--fail]
```

# DESCRIPTION

Elke basispartituur-`.mscz` onder `oefenhoek\bibliotheek\` moet in het
colofon de regel `Bibliotheek-id:` hebben én in de MuseScore-metadata
`vsaBibliotheekId`. Die waarde moet gelijk zijn aan het pad
`zangstuk/variant/uitvoeringsvorm` van de map.

Lokaal herstelt dit commando ontbrekende of verkeerde id’s (zonder MuseScore
te openen). Met `--check-only` (of in CI) alleen rapporteren, niet schrijven.
Op `main` of met een strenge pipeline faalt de check als er nog problemen
zijn.

Zonder `root` zoekt het script onder
`content-source\praktijk\oefenhoek\bibliotheek`. Na een herstel: opnieuw
[mscz-products](../mscz-products/) voor verse PDF’s met het juiste colofon.

# OPTIONS

| Optie | Betekenis |
| --- | --- |
| `root` | Map waaronder gezocht wordt (default: bibliotheek) |
| `--check-only` | Alleen controleren, niet schrijven |
| `--fail` | Exitcode 1 bij problemen (ook buiten de strenge pipeline) |

# WHEN

Na [layout](../layout/) of na verplaatsing in de bibliotheek, of als `check`
een id-mismatch meldt.

# SEE ALSO

- [layout](../layout/)
- [mscz-products](../mscz-products/)
- Bestand `scripts\mscz-partituur-contract.md` in `VSA-demo`
