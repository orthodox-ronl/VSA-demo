---
title: "Standaard-.mscz maken"
linkTitle: "Standaard-.mscz"
weight: 30
---

# Standaard- / hub-`.mscz` maken

{{< cue >}}
Van opgekuiste `.mxl`:
```cmd
python scripts\apply_mscz_layout.py content-source\praktijk\oefenhoek\input\_werk\DOEL-ID\DOEL-ID.mxl -o content-source\praktijk\oefenhoek\input\_werk\DOEL-ID\DOEL-ID.mscz
```
Van ruwe VOW-`.mscz`: hetzelfde script; invoer is die `.mscz`; `-o` naar `_werk` zonder spaties in de bestandsnaam.
{{< /cue >}}

**Wat je nu doet:** de hub-standaard toepassen (A4, lettertypes, SATB,
reciteertoon, tempo, copyright). Norm: [hub-contract](https://github.com/orthodox-ronl/VSA-demo/blob/main/scripts/mscz-hub-contract.md).
Reciteertoon (MCI): bij meer dan drie gelijke lettergrepen op dezelfde toon
worden de **eerste en laatste** gewone noten, met daartussen één feathered
`||O||`. MuseScore 4 moet geïnstalleerd zijn; bij een `.mxl`-invoer start
het script MuseScore zelf voor de import.

**Wanneer:** na opkuisen (Capella), of meteen bij een ruwe `.mscz` (VOW).
Sla deze pagina over als er al een layout-`.mscz` is en je alleen noten
wilt wijzigen → [reviewen](../4-reviewen/).

## Stap voor stap

### Van opgekuiste .mxl

Voorbeeld Trisagion:

```cmd
python scripts\apply_mscz_layout.py content-source\praktijk\oefenhoek\input\_werk\8a-trisagion\8a-trisagion.mxl -o content-source\praktijk\oefenhoek\input\_werk\8a-trisagion\8a-trisagion.mscz
```

### Van een VOW-.mscz

Een VOW-bestand is nog geen Oefenhoek-standaard. Kopieer het niet
rechtstreeks naar de bladermap. Eerst layout, naar een naam zonder
spaties:

```cmd
python scripts\apply_mscz_layout.py content-source\praktijk\oefenhoek\input\vow\Cherubijnenlied-Kastorskij.mscz -o content-source\praktijk\oefenhoek\input\_werk\15c-cherubijnenhymne-kastorski\15c-cherubijnenhymne-kastorski.mscz
```

Doe dit alleen als het doel-id in de werkvoorraad klopt. Anders eerst
vragen.

### Wat je niet doet

- Niet “Exporteren als MusicXML” in MuseScore om daarna opnieuw te
  importeren. Dan is de stijl weg.
- Nog geen PDF of Coria-`.mxl` maken. Eerst [reviewen](../4-reviewen/).

Je mag `apply_mscz_layout.py` later opnieuw op dezelfde `.mscz` zetten:
het script is bedoeld om herhaalbaar te zijn (nieuwe contractversie, of
na je eigen editslag).

## Klaar als

Je hebt een `.mscz` in `_werk\<doel-id>\` die in MuseScore 4 opent op A4,
met tekst tussen de balken. Het ruwe origineel in `input\` is
onaangeroerd.

{{< navbuttons "Volgende: reviewen|/praktijk/handleiding/partituur/4-reviewen/" >}}
