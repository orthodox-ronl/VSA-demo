---
title: "sync-bron-zondagen"
linkTitle: "sync-bron-zondagen"
weight: 70
---

# NAME

`scripts\sync-bron-zondagen.cmd` — zondag-zangstukken uit `bron` naar de demo kopiëren

# SYNOPSIS

```cmd
scripts\sync-bron-zondagen.cmd [bron-root]
```

# DESCRIPTION

Kopieert tropaar- en kondakbestanden voor de zondagstonen (en gerelateerde
assets) uit de canonieke repository **bron** naar
`content-source\praktijk\zondagen\` in `VSA-demo`. Het kopieert alleen
binaire bronbestanden: `.vsa`, melodie-afbeeldingen (`.jpg`) en
`.coria.html`. Er wordt geen markdown geschreven.

**Waartoe:** de demo-site blijft synchroon met de canonieke VSA in `bron`,
zonder die stukken handmatig te kopiëren.

Zonder argument zoekt het script automatisch de sibling-map `..\bron` of
`vendor\bron`. Met argument geef je een expliciet pad naar een
bron-checkout.

# EXAMPLES

```cmd
scripts\sync-bron-zondagen.cmd
scripts\sync-bron-zondagen.cmd C:\Git\orthodox-ronl\bron
```

# WHEN

Handmatig als je `bron` net hebt bijgewerkt en alleen die sync wilt.
`check`, `build` en `serve` roepen dit commando zelf al aan.

# SEE ALSO

- [check](../check/)
- Bestand `scripts\README.md` in de repository-map `VSA-demo`
