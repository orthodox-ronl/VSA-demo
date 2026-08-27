# AGENTS.md — VSA-demo

Richtlijnen voor AI-assistenten in deze repository (demo-/publicatiesite voor VSA).

Organisatie-context: [bron/AGENTS.md](https://github.com/orthodox-ronl/bron/blob/main/AGENTS.md).
Toolchain: [VSA-tooling](https://github.com/orthodox-ronl/VSA-tooling).

---

## Rol van deze repo

**VSA-demo** is een Hugo-site die laat zien hoe `vsa-tool` in een publicatiepipeline
wordt gebruikt (model voor toekomstige parochie-sites).

| Onderdeel | Pad |
| --------- | --- |
| Bewerkbare bron | `content-source/` |
| Hugo-templates | `layouts/` |
| Statische assets | `static/` (SVG’s in `static/vsa/` zijn gegenereerd) |
| Build-scripts | `scripts/` |
| Gegenereerd | `generated/` (niet committen) |

Normatieve org-specs staan in **bron** — link, niet dupliceren.

---

## Terminologie

[bron/docs/specs/terminologie.md](https://github.com/orthodox-ronl/bron/blob/main/docs/specs/terminologie.md)

`zangstuk-id` → `variant-id` → `uitvoeringsvorm-id` → `representatie-id`

Vermijd: `uv-id`, afkorting `uv`, **uitvoeringsalternatief**, impliciet `variant-id: standaard`.

---

## Modelkeuze (cost-effective)

Het model van **deze chat** kies jij in de Cursor-UI; de agent kan dat niet
wisselen. Wél:

1. **Snel inschatten** bij een nieuwe taak of duidelijk ander zwaartepunt.
2. **Adviseren** als de huidige chat te “zwaar” of te “licht” is
   (“voor deze docs-fix is Fast genoeg”).
3. Bij **subagents** (Task) een passend model kiezen volgens onderstaande
   vuistregel (tenzij jij een model dwingt).

| Taaksoort | Voorkeur |
| --------- | -------- |
| Docs, README, `h.cmd`, ASCII/links, kleine tekstfixes | Snel/licht (bijv. Composer Fast) |
| Scripts/CI-pipeline, gerichte code-edits, commits | Middel (Sonnet / Grok zonder extra High) |
| Architectuur, lastige multi-file redenering, CI-debug | Sterker / High-thinking |

Escaleer alleen als je vastloopt of kwaliteit duidelijk tekortschiet.
Kleine taken in een High-chat: kort adviseren om te switchen of de taak
toch dun afhandelen zonder onnodige subagents.

**Niet:** VSA-notatie “rechtzetten” om `vsa validate` stil te krijgen — dat
is geen modelkeuze-issue; markeringen signaleren fouten in de gezongen tekst.

---

## Lokaal bouwen

Eerste keer / na tool-update:

```cmd
cd /d C:\Git\orthodox-groningen\VSA-demo
check --strict
```

**Vóór commit** (zelfde als [CONTRIBUTING.md](CONTRIBUTING.md) en CI):

```cmd
check --strict
```

Preview na groene check:

```cmd
serve --no-build
```

Scripts vinden / man-pages: `scripts\h.cmd` (detail: `scripts\h.cmd check`).  
Uitleg: [scripts/README.md](scripts/README.md).

`_ensure` installeert catalogus (bron) + vsa-tool[rendering] in Python 3.14.

### Scripts onderhouden

Wijzig, voeg toe of verwijder je iets onder `scripts/`:

1. Werk [scripts/README.md](scripts/README.md) bij (tabellen, testladder, begrippen).
2. Werk `scripts\h.cmd` bij (catalogus + man-page).
3. Gedeelde keten: `_pipeline.cmd` (wrappers: check, build, serve).
4. Console-tekst in `.cmd` (`echo`): **alleen eenvoudige ASCII** (`->`, `-`, geen
   Unicode-pijlen/em-dashes) — Windows-cmd verknoeit UTF-8 anders.

---

## Pipeline

```text
content-source  --vsa validate-->
                --vsa build-markdown-->  generated/content + static/vsa
                --update-nav-placeholders-->
                --inject_git_dates + write_build_stamp-->
                --hugo-->                generated/site
```

---

## GitHub Pages

| Branch | Doel | URL |
| ------ | ---- | --- |
| `main` | Productie | https://orthodox-ronl.github.io/VSA-demo/ |
| andere | Preview | https://orthodox-ronl.github.io/VSA-demo/preview/ |

Zelfde patroon als `bron` (`docs-pages.yml`). Deploy via reusable workflow in VSA-tooling.

---

## Git / commits

Conventional Commits. Alleen committen als de gebruiker dat vraagt.

Menselijke bijdragers: [CONTRIBUTING.md](CONTRIBUTING.md) — groen vóór commit =
`check --strict`.
