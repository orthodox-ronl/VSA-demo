---
title: "Partituur"
linkTitle: "Partituur"
weight: 20
nav_sort: weight
---

Hier zet je een ruwe Capella- of VOW-partituur om naar een **hub-`.mscz`**
(MuseScore-bestand volgens het
[hub-contract](https://github.com/orthodox-ronl/VSA-demo/blob/main/scripts/mscz-hub-contract.md)),
daarna naar een PDF en een bestand voor Coria. Volg de stappen in volgorde.

**Opkuisen** = Capella-`.mxl` inhoudelijk opschonen met een script. Dat
doe je vóór de layout. Na elke wijziging in MuseScore: de layout
**opnieuw** toepassen (normaliseren), en pas daarna PDF en Coria-`.mxl`
maken ([afgeleiden](6-afgeleiden/)).

Naast dit hub-spoor bestaat een **print-`.mscz`** (`*.print.mscz`): een
koormap-vel dat de pipeline niet normaliseert en waarvoor geen Coria
wordt gemaakt — zie [Print-.mscz](7-print-mscz/).

Technische afspraken:
[hub-contract](https://github.com/orthodox-ronl/VSA-demo/blob/main/scripts/mscz-hub-contract.md),
[product-transforms](https://github.com/orthodox-ronl/VSA-demo/blob/main/scripts/mscz-product-transforms.md).

{{< cue >}}
Capella: `cleanup_capella_mxl.py` → `apply_mscz_layout.py` → MuseScore → `apply_mscz_layout.py` nogmaals → `scripts\mscz-products.cmd`
VOW: begin bij `apply_mscz_layout.py` (opkuisen overslaan).
Print-vel: `naam.print.mscz` + handmatige PDF — geen layout-script, geen `mscz-products`.
Tussenproducten (hub): `input\_werk\<doel-id>\`. Origineel blijft in `input\capella\` of `input\vow\`.
{{< /cue >}}
