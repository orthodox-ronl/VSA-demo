---
title: "sync-bron-zondagen"
linkTitle: "sync-bron-zondagen"
weight: 70
---

# NAME

`scripts\sync-bron-zondagen.cmd` — zondag-VSA uit bron synchroniseren

# SYNOPSIS

```cmd
scripts\sync-bron-zondagen.cmd [bron-root]
```

# DESCRIPTION

Kopieert tropaar/kondak (en gerelateerde) zondag-bestanden uit de
**bron**-repository naar `content-source\praktijk\zondagen\`. Alleen binaire
bronassets (`.vsa`, melodie-`.jpg`, `.coria.html`) — geen markdown.

Zo blijft de demo synchroon met canonieke bron-VSA.

Zonder argument: automatisch sibling `..\bron` of `vendor\bron`. Met argument:
expliciet pad naar een bron-checkout.

# EXAMPLES

```cmd
scripts\sync-bron-zondagen.cmd
scripts\sync-bron-zondagen.cmd C:\Git\orthodox-ronl\bron
```

# WHEN

Handmatig als je bron net hebt bijgewerkt en alleen die sync wilt.
`check` / `build` / `serve` roepen sync zelf al aan.

# SEE ALSO

- [check](../check/)
- Bestand `scripts\README.md` in `VSA-demo`
