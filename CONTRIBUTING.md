# Bijdragen

## Wat bewerken

Alleen handmatige bron — niet gegenereerde output:

| Pad | Opmerking |
| --- | --------- |
| `content-source/` | Markdown, VSA, page-assets — zie [CONTENT-STRUCTURE.md](CONTENT-STRUCTURE.md) |
| `layouts/` | Hugo-templates en shortcodes |
| `static/` | CSS, favicons — **niet** `static/vsa/` (generate) |
| `scripts/` | Build/check/serve — bij wijziging ook [scripts/README.md](scripts/README.md) en `scripts\h.cmd` |

Niet committen: `generated/`, `public/`, `static/vsa/`, `data/build.yaml`.

## Scripts vinden

```cmd
scripts\h.cmd
scripts\h.cmd check
```

Uitleg, begrippen en testladder: [scripts/README.md](scripts/README.md).

## Eerste keer / na tool-update

Vereist sibling-checkouts (of `vendor/`) van **bron** en **VSA-tooling**:

```cmd
cd /d C:\Git\orthodox-ronl\VSA-demo
check
```

## Vóór commit

**Groen vóór commit = CI-blocking checks.** Dit is hetzelfde ritueel als in
[README.md](README.md) en wat `validate.yml` / `pages.yml` draaien.

```cmd
cd /d C:\Git\orthodox-ronl\VSA-demo
check --strict
```

Optioneel (externe links; in CI non-blocking, lokaal wél hard fail):

```cmd
check --strict --external
```

Daarna mag je committen. Push naar `main` triggert Pages-deploy.

## Lokaal bekijken

Na een geslaagde `check.cmd --strict`:

```cmd
serve --no-build
```

Open http://localhost:1313/

Volledige preview inclusief opnieuw genereren:

```cmd
serve
```

Alleen artifact in `generated\site` (zonder server):

```cmd
build
```

## Commits

[Conventional Commits](https://www.conventionalcommits.org/). Voorbeeld:

```text
content(praktijk): verplaats weekdag-antifonen naar samenstellingen
fix(scripts): inject git_date vóór hugo-build
docs: align CONTRIBUTING met check --strict
```

## Meer uitleg

- [README.md](README.md) — overzicht, CI, GitHub Pages
- [AGENTS.md](AGENTS.md) — richtlijnen voor AI-assistenten
- [scripts/README.md](scripts/README.md) — pipeline, testladder, CI-spiegel
