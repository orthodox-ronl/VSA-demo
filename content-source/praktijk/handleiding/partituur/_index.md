---
title: "Partituur"
linkTitle: "Partituur"
weight: 20
nav_sort: weight
---

Hier zet je een ruwe Capella- of VOW-partituur om naar een **basispartituur-`.mscz`**
(MuseScore-bestand volgens de basispartituur-norm in
`scripts\mscz-partituur-contract.md` in de repository-map `VSA-demo`),
daarna naar een PDF en een bestand voor Coria. Volg de stappen in volgorde.
De subpagina’s hieronder zijn de volledige instructie; deze pagina is alleen
het overzicht.

Pijplijn (waartoe, CI, commando’s): werktraject
[Basispartituur](../werktrajecten/basispartituur/). Print buiten die keten:
[Print-vel](../werktrajecten/print-vel/).

Drie begrippen — meng ze niet door elkaar:

| Term | In het kort (typisch) | Volledige pagina |
| --- | --- | --- |
| **Opkuisen** | Inhoud opschonen: stemmen/balken (bijv. SAT op balk 1, B op balk 2), lettergreep↔noot synchroon. Capella: script; `.mscz`: MuseScore. | [Opkuisen](2-opkuisen/) |
| **Normaliseren** | Basispartituur-standaard met `scripts\layout.cmd` (A4, fonts, reciteertoon, copyright, …). Contractterm. | [Standaard-.mscz](3-standaard-mscz/) |
| **Layouten** | Zelfde scriptstap in gewone taal. Na elke MuseScore-edit **opnieuw**, vóór PDF/Coria. | [Standaard-.mscz](3-standaard-mscz/), [reviewen](4-reviewen/) |

Na elke wijziging in MuseScore: opslaan → **normaliseren / layouten** → pas
daarna PDF en Coria-`.mxl` ([PDF en Coria](5-pdf-en-coria/),
[afgeleiden](6-afgeleiden/)).

Naast dit partituur-spoor bestaat een **print-`.mscz`** (`*.print.mscz`): een
koormap-vel dat de pipeline niet normaliseert; PDF (en eventuele Coria)
houd je handmatig bij met `artefacten_handmatig: true` — zie
[Print-.mscz](7-print-mscz/). Eenstemmige VSA hoort onder [VSA](../vsa/),
niet in deze partituurstraat.

Technische afspraken voor wie scripts of CI aanhoudt (bestanden in de repo,
niet op deze site): `scripts\oefenhoek-product-contract.md`,
`scripts\mscz-partituur-contract.md`, `scripts\mscz-product-transforms.md`.

{{< cue >}}
Capella: opkuisen (`scripts\opkuisen.cmd`) → normaliseren (`scripts\layout.cmd`) → MuseScore (inhoud) → opnieuw normaliseren → `scripts\mscz-products.cmd`
VOW / ruwe `.mscz`: Capella-script overslaan; controleer wel stemmen en lettergrepen (opkuisen), daarna normaliseren.
Print-vel: `naam.print.mscz` + handmatige PDF (+ `artefacten_handmatig: true`) — geen layout-script, geen `mscz-products`.
Tussenproducten (basispartituur): `input\_werk\<doel-id>\`. Origineel blijft in `input\capella\` of `input\vow\`.
{{< /cue >}}
