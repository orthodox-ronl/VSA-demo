---
title: "Status, check en live"
linkTitle: "Status en check"
weight: 20
---

# Status, check en live

{{< cue >}}
1. Zet `publicatiestatus` op bibliotheek-`index.md` **en** koormap-`index.md`.
2. `scripts\check.cmd --strict` moet groen zijn.
3. `scripts\serve.cmd --no-build` → http://127.0.0.1:18731/ — klik zelf als koorlid (koormap-slot).
4. Live: pas na groen, via git naar `main` (of vragen). `productie` niet raden.
{{< /cue >}}

**Wat je nu doet:** zeggen wat koorleden mogen verwachten, de keten laten
controleren, zelf de pagina nalopen, daarna pas publiceren op internet.

## Publicatiestatus

Op **elke** Oefenhoek-pagina die koorleden zien (bibliotheek en koormap),
in de `---` bovenaan:

| Waarde | Wanneer |
| --- | --- |
| `voorzien` | Gepland, nog geen oefenbare uitgave (stub) |
| `concept` | Eerste versie; vooral op sectie-`_index` |
| `reviewable` | Er staat iets in; feedback welkom |
| `productie` | Alleen bewust, nooit gokken |

Bibliotheek mét hub, VSA of print-PDF: meestal `reviewable`. Lege stub:
`voorzien`. Intern *Stap* in de werkvoorraad (`opkuisen`, `layout`, …) is
iets anders — dat zien koorleden niet.

## Check

In de map `VSA-demo`:

```cmd
scripts\check.cmd --strict
```

Dat controleert onder meer VSA, Coria-`.mxl`, of `publicatiestatus` erop
staat, en of links op de site kloppen. Rood = niet naar live; eerst
[als het misgaat](../3-als-het-misgaat/).

## Preview

Als check groen is en je niet opnieuw wilt genereren:

```cmd
scripts\serve.cmd --no-build
```

Browser: **http://127.0.0.1:18731/** — nooit poort 1313. Open jouw
**koormap-slot** in de liturgiemap. Klik **Oefenen in Coria**, **Downloaden**,
blader de PDF. Alsof je koorlid bent.

Alles opnieuw opbouwen (langer): `scripts\serve.cmd` zonder `--no-build`.

## Op internet

De publieke site is
[orthodox-ronl.github.io/VSA-demo](https://orthodox-ronl.github.io/VSA-demo/).
Die site volgt branch `main`. Lokaal groen is de drempel; daarna
committen en pushen (of iemand vragen die git doet). Preview-branches
komen onder `/preview/`.

Je hoeft git niet uit deze handleiding te leren. Wél: nooit pushen met
een rode `check --strict`.

## Klaar als

De publicatiestatus klopt op bibliotheek én koormap, check is groen, jij
hebt de preview als koorlid geklikt, en live is een bewuste volgende stap.

{{< navbuttons "Als het misgaat|/praktijk/handleiding/publiceren/3-als-het-misgaat/" >}}
