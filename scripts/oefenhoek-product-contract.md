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
| `vsa` | `{stam}.vsa` | `scripts\vsa-products.cmd` (syllabify in temp → `vsa musicxml` + sanitize + source-sha) → `{stam}.vsa.mxl`; gate `check_vsa_products.py` |
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

## Bibliotheek-id in eindproducten

**Principe** (geldt voor hub, vsa, print en latere sporen zoals mvsa): elk
**menselijk leesbaar** publicatieblad (PDF, afdruk uit `.mscz`) toont het
**bibliotheek-id** (`zangstuk/variant/uitvoeringsvorm`) in het colofon of
eindmateriaal. Machineleesbare provenance (hashes) blijft; het id is
**identiteit**, de hash is **versheid**.

| Spoor | Waar het id landt | Gate |
| ----- | ----------------- | ---- |
| `hub` | Colofon + meta in hub-`.mscz` → PDF via MuseScore-export | `ensure_bibliotheek_id` / `check_bibliotheek_id` |
| `vsa` | Bij `{stam}.vsa.pdf` (nog te bouwen): eindblok met id uit pad; Coria-`.vsa.mxl` mag misc-field `vsa-bibliotheek-id` | zelfde principe bij eerste PDF-export |
| `print` / handmatig | Beheerder zet id in colofon bij export; pipeline overschrijft niet | warn/check optioneel; geen stille overwrite |

Geen uitzondering voor nieuwe generators: wie een blad produceert, schrijft
het bibliotheek-id mee (afleiden via `bibliotheek.id_from_path` / `--id`).

---

## Handmatige artefacten

Frontmatter op bibliotheek-`index.md`:

```yaml
artefacten_handmatig: true
```

Betekenis: PDF, Coria-`.mxl` en andere afgeleiden in deze map worden **niet**
door de product-pipeline bijgewerkt of afgedwongen. Beheerder houdt ze zelf
bij (typisch samen met print-`.mscz` of een eenmalige template-export).

- Hub-productgate en VSA-productgate **slaan** zulke mappen over.
- De bibliotheekpagina toont een **beheerdersmelding** (layout).
- Default als het veld ontbreekt: `false` (automatische keten geldt).

Voorbeelden: tropaar Nikolaas, Moeder Godslied Ontslapen (print-track +
handmatige PDF/MXL naast `.vsa`).

---

## Alias-varianten

Een **alias-variant** heeft geen uitvoeringsvorm-map en geen partituur.
Frontmatter `alias_van` staat op `bibliotheek/<zangstuk>/<variant>/_index.md`
en wijst naar `zangstuk/canonieke-variant`. Product-tools (`vsa-products`,
hub-producten) slaan die mappen over. `python scripts/bibliotheek.py` (in
`check`) weigert extra bestanden onder een alias-variant.

---

## UI: meerdere producten

Meerdere Coria-`.mxl` → meerdere oefenopties (hover-keuzemenu op **Oefenen**).
Zelfde patroon voor meerdere PDF’s op **Downloaden** / **Printen**.

Menulabels zijn **mensentaal** (geen ruwe representatie-id):

| representatie-id | Label | Detailregel |
| ---------------- | ----- | ----------- |
| `vsa` | Melodie (één stem) | Zoals de notatie op deze pagina |
| `hub` | Koorblad (meerdere stemmen) | Zoals het PDF-blad |
| `print` | Printblad | Koormap-vel om te printen |

Legacy korte namen (`{stam}.mxl` / `{stam}.pdf`) volgen de sibling-bron
(hub-`.mscz` → hub, anders `.vsa` → vsa). Bij meerdere opties: voorkeur
eerst (hub als er een hub-`.mscz` is, anders vsa) en een korte hulpzin in
het menu. Twee bestanden met hetzelfde label: bestandsstam erachter
(noodrem; hoort niet bij een schone bladermap).

---

## VSA → Coria-`.mxl` (productgate)

| | |
| --- | --- |
| Commando | `scripts\vsa-products.cmd` (`sync_vsa_products.py`) |
| Product | `{stam}.vsa.mxl` |
| Syllabify | Alleen tijdens export (temp); canonieke `.vsa` blijft zonder Pyphen-streepjes voor SVG. Sidecar `{stam}.syl.vsa` is geen bron. |
| Stamp | `vsa-source-sha256`, `vsa-source-kind=vsa`, `vsa-generator=vsa-musicxml` |
| Lokaal | pipeline stap 2c vernieuwt stale producten |
| Preview | rode banner via `data/vsa-product-status.json` |
| Productie (`main`) | `check_vsa_products.py` faalt bij missing/stale/unstamped |

Commit `.vsa` + `.vsa.mxl` samen. Geen MuseScore nodig.

---

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
