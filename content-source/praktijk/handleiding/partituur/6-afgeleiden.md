---
title: "Afgeleiden bijwerken (PDF en Coria)"
linkTitle: "Afgeleiden"
weight: 60
---

# Afgeleiden bijwerken (PDF en Coria)

{{< cue >}}
```cmd
scripts\mscz-products.cmd content-source\praktijk\oefenhoek\liturgiemap-hemelum\DOEL-ID
```
Daarna **drie** bestanden committen: `.mscz`, `.pdf`, `.mxl`.
Zie ook [hub-contract](https://github.com/orthodox-ronl/VSA-demo/blob/main/scripts/mscz-hub-contract.md)
en [transforms](https://github.com/orthodox-ronl/VSA-demo/blob/main/scripts/mscz-product-transforms.md).
Print-`.mscz` (`*.print.mscz`) hoort **niet** in deze keten — zie
[Print-.mscz](../7-print-mscz/).
{{< /cue >}}

**Wat je nu doet:** PDF en Coria-`.mxl` opnieuw maken vanuit de hub-`.mscz`,
zodat hun ingebouwde hub-hash weer klopt. Op de preview-site zie je een
rode banner als dat niet zo is; op `main` faalt de build dan.

**Wanneer:** na elke inhoudelijke wijziging aan de hub (noten, tekst,
layout-normalisatie), of als de banner / `check_hub_products` klaagt.

## Voorwaarden

1. MuseScore 4 geïnstalleerd.
2. Hub-`.mscz` ligt in de **bladermap** (niet alleen in `_werk`).
3. Na een editslag eerst normaliseren:

```cmd
python scripts\apply_mscz_layout.py content-source\praktijk\oefenhoek\liturgiemap-hemelum\DOEL-ID\DOEL-ID.mscz
```

## Stappen

1. Draai `mscz-products` op de bladermap (of op heel `content-source`).
   Gebruik `--force` als de bestandsdatum klopt maar de hash-check toch
   faalt.
2. Controleer lokaal:

```cmd
python scripts\check_hub_products.py
```

3. Commit hub + PDF + MXL **samen**. Alleen de hub pushen houdt de
   preview-banner rood en blokkeert productie.

## Wat de check precies doet

Een afgeleide is goed als die bestaat en de metadata `hub-sha256` gelijk
is aan de SHA-256 van de huidige hub-`.mscz`. Ontbreekt de stamp, of
wijkt de hash af, dan moet je opnieuw genereren.

{{< navbuttons "Terug: PDF en Coria|/praktijk/handleiding/partituur/5-pdf-en-coria/" "Volgende: print-.mscz|/praktijk/handleiding/partituur/7-print-mscz/" >}}
