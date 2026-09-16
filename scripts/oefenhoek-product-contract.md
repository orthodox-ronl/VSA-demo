# Contract: Oefenhoek-producten (afgeleiden per representatie)

Norm voor **afgeleide artefacten** in `oefenhoek/bibliotheek/` (PDF, Coria-`.mxl`,
later eventueel andere exports). Proef in VSA-demo.

Org-termen: [terminologie](https://github.com/orthodox-ronl/bron/blob/main/docs/specs/terminologie.md)
— `zangstuk-id` → `variant-id` → `uitvoeringsvorm-id` → **`representatie-id`**.

Een **representatie** is één concrete bron (of één productiespoor) binnen een
uitvoeringsvorm. Meerdere representaties in dezelfde map mogen elk eigen
afgeleiden hebben; die mogen elkaar **niet** overschrijven.

Hub-layout/normalisatie: [mscz-hub-contract.md](mscz-hub-contract.md).
Hub-transforms: [mscz-product-transforms.md](mscz-product-transforms.md).

---

## Publicatiesporen → representatie-id

| representatie-id | Canonieke bron in de bladermap | Pipeline (normaal) |
| ---------------- | ------------------------------ | ------------------ |
| `hub` | `{stam}.mscz` (niet `.print.`) | `apply_mscz_layout` → `mscz-products` → PDF + Coria-`.mxl` + hub-hash-gate |
| `vsa` | `{stam}.vsa` | (deel B) `vsa musicxml` + sanitize → Coria-`.mxl`; later optioneel PDF |
| `print` | `{stam}.print.mscz` | Geen layout/products/Coria uit dit bestand; PDF handmatig |

Ids: `[a-z0-9_-]+`. Geen ad-hoc synoniemen (“route”, “uv”) in bestandsnamen.

---

## Bestandsnamen van afgeleiden

**Doelvorm** (expliciet, botsingsvrij):

```text
{publicatiestam}.{representatie-id}.{ext}
```

Voorbeelden:

| Bron | Afgeleide |
| ---- | --------- |
| `{stam}.mscz` | `{stam}.hub.pdf`, `{stam}.hub.mxl` |
| `{stam}.vsa` | `{stam}.vsa.mxl` (later `{stam}.vsa.pdf`) |
| `{stam}.print.mscz` | `{stam}.print.pdf` |

`{publicatiestam}` = `{zangstuk}-{variant}-{uitvoeringsvorm}` zonder spaties
(`[a-z0-9_-]+`). Helper: `scripts/score_filenames.py`.

### Compatibiliteit (legacy, één product per map)

Zolang er **hoogstens één** Coria-`.mxl` / PDF per map is, blijven korte namen
toegestaan:

| Situatie | Betekenis van `{stam}.mxl` / `{stam}.pdf` |
| -------- | ---------------------------------------- |
| Sibling hub-`.mscz` aanwezig | impliciet representatie `hub` |
| Alleen `.vsa` (geen hub-`.mscz`) | impliciet `vsa` (zodra VSA-productgate er is) |
| Sibling `{stam}.print.mscz`, geen hub | PDF hoort bij `print`; korte `{stam}.pdf` mag |

Zodra **twee** producten van hetzelfde type in één map moeten: **altijd**
expliciet `{stam}.{representatie-id}.{ext}`. Geen stille overwrite.

### Ownership

Elk afgeleid bestand heeft **precies één** bron-representatie. Wijzigt de bron,
dan moet dat product opnieuw (automatisch of handmatig). Een product zonder
bijbehorende bron hoort niet in de map (of de map staat op handmatig, zie
hieronder).

---

## Handmatige artefacten

Frontmatter op bibliotheek-`index.md`:

```yaml
artefacten_handmatig: true
```

Betekenis: PDF, Coria-`.mxl` en andere afgeleiden in deze map worden **niet**
door de product-pipeline bijgewerkt of afgedwongen. Beheerder houdt ze zelf
bij (typisch samen met print-`.mscz` of een eenmalige template-export).

- Hub-productgate en (later) VSA-productgate **slaan** zulke mappen over.
- De bibliotheekpagina toont een **beheerdersmelding** (layout).
- Default als het veld ontbreekt: `false` (automatische keten geldt).

Voorbeelden: tropaar Nikolaas, Moeder Godslied Ontslapen (print-track +
handmatige PDF/MXL naast `.vsa`).

---

## UI: meerdere producten

Meerdere Coria-`.mxl` → meerdere oefenopties (hover-keuzemenu op **Oefenen**).
Zelfde patroon voor meerdere PDF’s op **Downloaden** / **Printen**.
Menulabels = representatie-id waar die in de bestandsnaam staat; anders een
korte legacy-label.

---

## Tempo (hub én VSA)

| Situatie | BPM |
| -------- | --- |
| Expliciet in hub-metronoom of `.vsa`-frontmatter `tempo:` | die waarde |
| Default bij ontbreken | **120** |

In `.vsa` bij voorkeur altijd expliciet: `do`, `mode`, `tempo`.

---

## Zie ook

- Print-vel: handleiding `partituur/7-print-mscz`
- Hub-afgeleiden: handleiding `partituur/5-pdf-en-coria`, `6-afgeleiden`
- VSA schrijven: handleiding `vsa/1-vsa-schrijven` (Coria uit VSA: deel B)
