---
title: "Publiceren"
linkTitle: "Publiceren"
weight: 40
nav_sort: weight
---

De **bladermap** is wat koorleden openen: één `index.md` plus de
publicatiebestanden. Daarna zet je de publicatiestatus, draai je `check`,
en bekijk je de lokale preview. Live op internet is een extra stap (git),
pas als lokaal alles groen is.

{{< cue >}}
- `index.md` + bestanden zonder spaties in `oefenhoek\<deelrubriek>\<doel-id>\`
- `publicatiestatus: reviewable` zodra er iets te oefenen is, anders `voorzien`
- `scripts\check.cmd --strict` → `scripts\serve.cmd --no-build` → http://127.0.0.1:18731/
- `productie` nooit raden
{{< /cue >}}
