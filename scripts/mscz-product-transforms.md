# Hub-producten: transforms PDF en Coria-`.mxl`

Bron: genormaliseerde **hub-`.mscz`** ([mscz-hub-contract.md](mscz-hub-contract.md)).
Commando: `scripts\mscz-products.cmd [bladermap]`.

Alleen bestanden die **niet** op `.print.mscz` eindigen. Print-velden horen
in het derde publicatiespoor; zie hub-contract en handleiding print-`.mscz`.

## Provenance (in het productbestand)

Bij elke generatie:

| Veld | MXL | PDF |
| ---- | --- | --- |
| Hub-hash | `miscellaneous-field` `vsa-hub-sha256` | Info `/VSAHubSHA256` |
| Generatietijd (UTC) | `vsa-generated-at` + `encoding-date` | `/VSAGeneratedAt` |
| Generator | `vsa-generator` = `mscz-products` | `/VSAGenerator` |

**Fresh** = product bestaat en `hub-sha256` == SHA-256 van de huidige hub.
Check: `python scripts\check_hub_products.py` → `data/hub-product-status.json`.
Preview: rode banner; productie (`main`): build faalt.

---

## Hub → PDF

| Hub | PDF |
| --- | --- |
| Hele genormaliseerde partituur | MuseScore A4-export, daarna provenance-stamp |
| Reciteernoten `\|\|O\|\|` | blijven compact (geen expansie) |
| Titel / composer / footer / colofon | zoals in hub |
| SATB-akkolade | ongewijzigd |

Geen lettergreep-explosie, geen vier aparte Coria-parts.

## Hub → Coria-`.mxl`

| Hub | Coria |
| --- | --- |
| Feathered reciteernoot + lyrictekst | **Explosie:** één kwart per lettergreep (split op spatie en `-`; anders `nl_hyphen.py`). MuseScore-export als `type=long` telt ook. |
| Melisma (slur + ticks) | lyric op eerste noot + `<extend/>` |
| Dubbele maatstreep | extra maat 4 kwarten rust, lyric `[PAUZE]`; cue `P:`/`D:`/`K:` erboven |
| Gebogen cesuur | 1 kwart rust erna |
| Leidende gap-rusten | wissen; maat korter (`senza-misura`) |
| Onzichtbaar tempo | zichtbaar metronoom + `sound tempo` op alle parts |
| SATB één part / 4 stemmen | explodeer naar S/A/T/B score-parts |
| Layout-only markup | strippen (Coria `translation failed`) |
| Voortekens | `<accidental>` voor playback |
| Copyright | `<rights>` / identification waar mogelijk + provenance-fields |

Script: `export_mscz_coria_mxl.py` (aanroep via `sync_mscz_products.py`).

### Wanneer worden woorden in lettergrepen gesplitst?

1. **Bij hub-normalisatie** (`apply_mscz_layout`): tokens met meerdere
   klinkergroepen (`melse` → `mel` + `se`) krijgen extra noten; reciteerreeksen
   van meer dan drie gelijke lettergrepen collapsen tot **eerste gewone noot +
   één `||O||` (midden) + laatste gewone noot** (MCI).
2. **Bij Coria-export**: tekst onder de feathered middennoot wordt opnieuw
   gesplitst tot één kwart per lettergreep (hyphens in de hub-tekst winnen;
   anders `nl_hyphen`). Eerste en laatste noot blijven al gewone noten.

## Lokaal vs CI

| Omgeving | Genereren | Controleren |
| -------- | --------- | ----------- |
| Lokaal (MuseScore) | `mscz-products` in pipeline | `check_hub_products` (streng) |
| GitHub preview | geen MuseScore; skip export | waarschuwing + banner |
| GitHub `main` | geen MuseScore | fail bij missing/stale/unstamped |

Beheer: [Afgeleiden bijwerken](/praktijk/handleiding/partituur/6-afgeleiden/).
