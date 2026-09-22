---
title: "build"
linkTitle: "build"
weight: 30
---

# NAME

`scripts\build.cmd` — volledige sitebuild

# SYNOPSIS

```cmd
scripts\build.cmd
```

# DESCRIPTION

Bouwt de volledige site naar `generated\site`. Zelfde keten als
`check.cmd --strict` via `scripts\_pipeline.cmd`, zonder `--external`.

Commit geen `generated\` of `static\vsa\` — die mappen zijn build-output.

# WHEN

Als je het site-artifact in `generated\site` nodig hebt zonder Hugo-server.
Voor preflight vóór commit is `check.cmd --strict` genoeg.

# SEE ALSO

- [check](../check/)
- [serve](../serve/)
