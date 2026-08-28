---
title: "Tropaar voor het voorbeeldblad"
build:
  render: never
  list: never
---

# Tropaar voor het Voorbeeldblad

Dit blad is bedoeld om te laten zien hoe Markdown met VSA tot een printbare
PDF wordt. Onderstaande melodie staat eerst inline, daarna via een include
van `voorbeeld.vsa` (zie de SVG-demootjes voor die vormen apart).

::: vsa-notatie
[\\:] Dat {//he}melse en {\aard}{/se} {/&/we}{zens_} *
jubelen en zich ver{\&\&\blij_&~&~}{\den_}, *
want {/de} {/Heer} heeft de kracht van Zijn {\arm} {/ge}{/&/o}pen{baard_}. *
Uit de doden was Hij de eerstge{/bo_}re{\ne_}, *
uit de schoot van de {-&\ha}{/des} {/heeft} {/Hij_} {\ons} ver{\lost_} *
// en aan de wereld grote ge{na_}{\de} {\ge}{/&/&/&\&\&\&/schon.&.&.&.&.&.&~}{\ken__}. [:]
:::

Zelfde melodie via bestand (handig bij hergebruik; in `.vsa` geen
`::: vsa-notatie`-hekjes):

:::include svg "voorbeeld.vsa" alt="Tropaar toon 3 (include)" scale="85%":::

:::pagebreak:::

# Tweede blad: kleinere schaal

Na de paginascheiding volgt dezelfde melodie nog eens, kleiner gezet.

:::include svg "voorbeeld.vsa" alt="Tropaar toon 3 (kleiner)" scale="70%":::

:::print-only:::
[Oefenen in Coria](https://orthodox-ronl.github.io/VSA-demo/coria/praktijk/demo/assets/voorbeeld.html)

*Dit zinnetje en de Coria-link hierboven staan alleen in de PDF
(`print-only`), niet op de website. De link wijst naar de gepubliceerde
site (niet naar localhost).*
:::end-print-only:::
