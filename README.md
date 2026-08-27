# VSA-demo

Hugo-demo site voor [VSA-tooling](https://github.com/orthodox-ronl/VSA-tooling):
Markdown + VSA-notatie → SVG → statische site (GitHub Pages).

Gerelateerde documentatie: [bron](https://orthodox-ronl.github.io/bron/) ·
[VSA-tooling](https://orthodox-ronl.github.io/VSA-tooling/)

## Scripts vinden

```cmd
scripts\h.cmd
scripts\h.cmd check
```

Detail, begrippen en testladder: [scripts/README.md](scripts/README.md).  
Bijdragen: [CONTRIBUTING.md](CONTRIBUTING.md).

## Vóór commit

**Groen vóór commit = CI-blocking checks** (`validate.yml` / `pages.yml`).

```cmd
cd /d C:\Git\orthodox-ronl\VSA-demo
check --strict
```

Optioneel — externe `http(s)`-links (in CI non-blocking; lokaal hard fail):

```cmd
check --strict --external
```

| Optie         | Effect                                      |
| ------------- | ------------------------------------------- |
| `--strict`    | Faal ook op VSA-warnings                    |
| `--external`  | Check externe links (kan flaky zijn)        |
| `--skip-hugo` | Alleen sync + validate + generate (sneller) |

## Lokaal

Vereist sibling-checkouts (of `vendor/`) van **bron** en **VSA-tooling**:

```text
C:\Git\orthodox-ronl\
  bron\
  VSA-tooling\
  VSA-demo\
```

Eerste keer / na tool-update: `check` of `serve` (installeert packages zelf).

Na een geslaagde `check --strict` — preview zonder opnieuw te genereren:

```cmd
serve --no-build
```

Open http://localhost:1313/

Volledige preview (sync + validate + generate + server):

```cmd
serve
```

Volledige sitebuild + interne linkcheck (artifact in `generated\site`):

```cmd
build
```

## Structuur

| Pad               | Rol                                              |
| ----------------- | ------------------------------------------------ |
| `content-source/` | Broncontent (bewerken), inclusief `lokaal/` — zie [CONTENT-STRUCTURE.md](CONTENT-STRUCTURE.md) |
| `layouts/`        | Hugo-templates en shortcodes                     |
| `static/`         | CSS, favicons; gegenereerde SVG in `static/vsa/` |
| `scripts/`        | `check`, `serve`, `build`, `_ensure` |
| `_deferred/`      | Uitgesteld: TEv2                                 |

## Afhankelijkheden

- Python 3.14
- Hugo Extended 0.160.1
- `catalogus` uit [bron](https://github.com/orthodox-ronl/bron) (via `_ensure`)
- `vsa-tool[rendering]` uit [VSA-tooling](https://github.com/orthodox-ronl/VSA-tooling)

## CI-checks

| Workflow        | Wanneer          | Blocking                                                         | Niet-blocking        |
| --------------- | ---------------- | ---------------------------------------------------------------- | -------------------- |
| `validate.yml`  | pull request     | sync, validate (+warnings), generate, hugo, interne links/assets | externe links        |
| `pages.yml`     | push / handmatig | hetzelfde + deploy naar `gh-pages`                               | externe links        |

Lokaal equivalent: `check --strict` (zie [CONTRIBUTING.md](CONTRIBUTING.md)).

## GitHub Pages

| Branch | Doel       | URL                                                      |
| ------ | ---------- | -------------------------------------------------------- |
| `main` | Productie  | https://orthodox-ronl.github.io/VSA-demo/           |
| andere | Preview    | https://orthodox-ronl.github.io/VSA-demo/preview/   |

Elke push triggert de workflow. Productie en preview delen branch `gh-pages` (map `preview/` blijft naast de root staan).

**Eenmalig in GitHub:** Settings → Pages → Source: **Deploy from a branch** → Branch: `gh-pages` → Folder: `/`.
