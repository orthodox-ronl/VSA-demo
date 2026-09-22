---
title: "build"
linkTitle: "build"
weight: 30
---

# NAME

`scripts\build.cmd` — hele website bouwen naar `generated\site`

# SYNOPSIS

```cmd
scripts\build.cmd
```

# DESCRIPTION

Bouwt de volledige site naar de map `generated\site` op je pc. De keten is
dezelfde als bij `check.cmd --strict` (via `scripts\_pipeline.cmd`), zonder
externe linkcheck.

Commit de mappen `generated\` en `static\vsa\` niet: dat is build-output.
Voor «mag ik committen?» is `check.cmd --strict` genoeg; `build` is vooral
handig als je het site-artifact zelf nodig hebt zonder Hugo-server.

# WHEN

Als je de gebouwde site in `generated\site` nodig hebt zonder
`serve` te starten.

# SEE ALSO

- [check](../check/)
- [serve](../serve/)
